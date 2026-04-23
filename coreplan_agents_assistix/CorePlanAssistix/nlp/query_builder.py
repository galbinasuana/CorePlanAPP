from datetime import datetime, timedelta

def parse_time_range(time_range_str):
    """
    Transforms a string like 'last 3 months' or 'this quarter' into a date string.
    """
    today = datetime.today()
    time_range_str = (time_range_str or "").lower()

    if "last 3 months" in time_range_str:
        start_date = today - timedelta(days=90)
    elif "last quarter" in time_range_str:
        start_date = today - timedelta(days=90)
    elif "last month" in time_range_str:
        start_date = today - timedelta(days=30)
    elif "last year" in time_range_str:
        start_date = today - timedelta(days=365)
    elif "this quarter" in time_range_str:
        start_date = today - timedelta(days=90)
    elif "recent period" in time_range_str:
        start_date = today - timedelta(days=60)
    else:
        # Default fallback: last 30 days
        start_date = today - timedelta(days=30)

    return start_date.strftime("%Y-%m-%d"), (today - start_date).days



def build_performance_query(parsed_intent, department_id=None):
    intent = parsed_intent.get("intent", "general_summary")
    time_range_str = parsed_intent.get("time_range", "last 3 months")
    start_date, num_days = parse_time_range(time_range_str)
    metrics = parsed_intent.get("metrics", [])
    special_focus = parsed_intent.get("special_focus", "")

    # Protecție pentru lipsa metrice
    if not metrics:
        if special_focus == "burnout risk":
            metrics = ["burnout_probability"]
        elif special_focus == "engagement":
            metrics = ["engagement_score"]
        else:
            metrics = ["efficiency_score"]

    metric = metrics[0]

    where_clauses = [f"record_date >= '{start_date}'"]
    if department_id:
        where_clauses.append(
            f"department = (SELECT department_name FROM departments WHERE department_id = {department_id})"
        )

    where = " AND ".join(where_clauses)

    # Construim query-ul în funcție de intent
    if intent == "top_performers":
        return f"""
            SELECT employee_name AS full_name, department, {metric}
            FROM employee_performance
            WHERE {where}
            ORDER BY {metric} DESC
            LIMIT 5;
        """

    elif intent == "burnout_risk":
        return f"""
            SELECT employee_name AS full_name, department, burnout_probability
            FROM employee_performance
            WHERE {where}
            ORDER BY burnout_probability DESC
            LIMIT 5;
        """

    elif intent == "correlation_analysis":
        return f"""
            SELECT efficiency_score, engagement_score, burnout_probability
            FROM employee_performance
            WHERE {where};
        """

    elif intent == "efficiency_comparison":
        return f"""
            SELECT employee_name AS full_name, department, efficiency_score
            FROM employee_performance
            WHERE {where}
            ORDER BY efficiency_score DESC;
        """


    elif intent == "full_performance_overview":
        return f"""
            SELECT
                department,
                COUNT(DISTINCT employee_name) AS num_employees,
                MIN(efficiency_score) AS min_efficiency,
                MAX(efficiency_score) AS max_efficiency,
                AVG(efficiency_score) AS avg_efficiency,
                MIN(engagement_score) AS min_engagement,
                MAX(engagement_score) AS max_engagement,
                AVG(engagement_score) AS avg_engagement,
                MIN(burnout_probability) AS min_burnout,
                MAX(burnout_probability) AS max_burnout,
                AVG(burnout_probability) AS avg_burnout,
                MIN(idle_time_minutes) AS min_idle,
                MAX(idle_time_minutes) AS max_idle,
                AVG(idle_time_minutes) AS avg_idle,
                task_complexity
            FROM employee_performance
            WHERE {where}
            GROUP BY department, task_complexity
            ORDER BY department, task_complexity;
        """

    else:
        # Default summary
        return f"""
            SELECT department,
                   AVG(efficiency_score) AS avg_efficiency,
                   AVG(burnout_probability) AS avg_burnout,
                   AVG(engagement_score) AS avg_engagement
            FROM employee_performance
            WHERE {where}
            GROUP BY department
            ORDER BY avg_efficiency DESC;
        """


def build_financial_query(parsed_intent):
    intent = parsed_intent.get("intent", "general_financial_summary")
    time_range_str = parsed_intent.get("time_range", "last 2 months")
    start_date, _ = parse_time_range(time_range_str)

    where_clause = f"record_date >= '{start_date}' AND department_id = (SELECT department_id FROM departments WHERE department_name = 'Sales')"

    if intent == "financial_detailed":
        return f"""
            SELECT 
                revenue, 
                expenses, 
                profit,
                (budget_used - budget_allocated) AS budget_variance,
                (profit / expenses * 100) AS roi
            FROM financial_data
            WHERE {where_clause};
        """

    elif intent == "financial_overview":
        return f"""
            SELECT
                COUNT(*) AS num_records,
                AVG(revenue) AS avg_revenue,
                AVG(expenses) AS avg_expenses,
                AVG(profit) AS avg_profit,
                AVG(budget_used - budget_allocated) AS avg_budget_variance,
                AVG(profit / expenses * 100) AS avg_roi
            FROM financial_data
            WHERE {where_clause};
        """

    elif intent == "high_roi_focus":
        return f"""
            SELECT record_date, (profit / expenses * 100) AS roi
            FROM financial_data
            WHERE {where_clause}
            ORDER BY roi DESC
            LIMIT 5;
        """

    elif intent == "budget_risk":
        return f"""
            SELECT record_date, (budget_used - budget_allocated) AS budget_variance
            FROM financial_data
            WHERE {where_clause}
            ORDER BY ABS(budget_used - budget_allocated) DESC
            LIMIT 5;
        """

    else:  # fallback summary
        return f"""
            SELECT
                AVG(revenue) AS avg_revenue,
                AVG(expenses) AS avg_expenses,
                AVG(profit) AS avg_profit,
                AVG(budget_used - budget_allocated) AS avg_budget_variance,
                AVG(profit / expenses * 100) AS avg_roi
            FROM financial_data
            WHERE {where_clause};
        """

def build_planning_query(intent_data, department_id=None, time_range=None):
    """
    Generează interogări SQL pentru agentul de planning, în funcție de intent-ul identificat.
    Acceptă opțional un `department_id` și un `time_range` deja procesat.
    """
    where_clauses = []

    if department_id:
        where_clauses.append(f"d.department_id = {department_id}")

    if time_range:
        where_clauses.append(f"a.appointment_date >= '{time_range}'")

    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

    intent = intent_data.get("intent", "schedule_optimization")

    if intent == "schedule_optimization":
        return f"""
            SELECT 
                e.employee_id, 
                CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                d.department_name,
                COUNT(a.appointment_id) AS total_appointments,
                ROUND(AVG(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)), 1) AS avg_duration_minutes,
                SUM(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)) AS total_minutes,
                ROUND(SUM(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)) / 
                      (COUNT(DISTINCT a.appointment_date) * 480) * 100, 1) AS utilization_percent
            FROM appointments a
            JOIN employees e ON e.employee_id = a.employee_id
            JOIN departments d ON d.department_id = e.department_id
            WHERE {where_clause}
            GROUP BY e.employee_id, d.department_name
            ORDER BY utilization_percent DESC;
        """

    elif intent == "task_distribution":
        return f"""
            SELECT 
                ep.employee_name,
                ep.department,
                COUNT(*) AS records_count,
                ROUND(AVG(ep.task_complexity), 2) AS avg_complexity,
                ROUND(AVG(ep.hours_logged), 1) AS avg_hours_logged,
                ROUND(AVG(ep.tasks_completed), 1) AS avg_tasks_completed
            FROM employee_performance ep
            JOIN employees e ON e.employee_id = ep.employee_id
            JOIN departments d ON d.department_id = e.department_id
            {"WHERE " + " AND ".join(where_clauses) if where_clauses else ""}
            GROUP BY ep.employee_id
            ORDER BY avg_complexity DESC;
        """

    elif intent == "resource_planning":
        return f"""
            SELECT 
                d.department_name,
                COUNT(DISTINCT e.employee_id) AS total_employees,
                COUNT(a.appointment_id) AS total_appointments,
                ROUND(AVG(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)), 1) AS avg_duration,
                ROUND(SUM(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)) / 
                      (COUNT(DISTINCT a.appointment_date) * 480), 2) AS avg_utilization_ratio
            FROM appointments a
            JOIN employees e ON e.employee_id = a.employee_id
            JOIN departments d ON d.department_id = e.department_id
            WHERE {where_clause}
            GROUP BY d.department_name
            ORDER BY avg_utilization_ratio DESC;
        """

    else:
        return f"""
            SELECT 
                ROUND(AVG(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)), 1) AS avg_duration_minutes,
                COUNT(a.appointment_id) AS total_appointments,
                COUNT(DISTINCT a.appointment_date) AS distinct_days,
                COUNT(DISTINCT a.employee_id) AS total_employees
            FROM appointments a
            JOIN employees e ON e.employee_id = a.employee_id
            JOIN departments d ON d.department_id = e.department_id
            WHERE {where_clause};
        """


def build_reporting_query(parsed_intent):
    intent = parsed_intent.get("intent", "reporting_summary")
    time_range_str = parsed_intent.get("time_range", "last 2 months")
    start_date, _ = parse_time_range(time_range_str)

    where_clause = f"report_date >= '{start_date}'"

    if intent == "reporting_overview":
        return f"""
            SELECT 
                COUNT(*) AS total_reports,
                AVG(employee_morale_index) AS avg_morale,
                AVG(planning_accuracy) AS avg_accuracy,
                SUM(anomalies_detected) AS total_anomalies,
                AVG(report_quality_score) AS avg_quality,
                AVG(urgency_index) AS avg_urgency
            FROM reporting_data
            WHERE {where_clause};
        """

    elif intent == "high_alert_reports":
        return f"""
            SELECT 
                report_date,
                department_focus,
                alert_flag,
                urgency_index,
                anomalies_detected,
                budget_variance_alert
            FROM reporting_data
            WHERE {where_clause}
              AND alert_flag = 'Critical'
            ORDER BY urgency_index DESC
            LIMIT 5;
        """

    elif intent == "recommendation_focus":
        return f"""
            SELECT 
                report_date,
                department_focus,
                recommendation_type,
                intervention_suggested,
                reviewed_by,
                report_quality_score
            FROM reporting_data
            WHERE {where_clause}
            ORDER BY report_quality_score DESC
            LIMIT 10;
        """

    else:
        return f"""
            SELECT 
                department_focus,
                COUNT(*) AS num_reports,
                AVG(employee_morale_index) AS avg_morale,
                AVG(planning_accuracy) AS avg_accuracy,
                AVG(urgency_index) AS avg_urgency
            FROM reporting_data
            WHERE {where_clause}
            GROUP BY department_focus
            ORDER BY avg_urgency DESC;
        """
