import os
import openai
import datetime
import matplotlib.pyplot as plt
from flask import render_template
from dotenv import load_dotenv

from nlp.intent_classifier import classify_intent
from nlp.query_executor import execute_query
from nlp.query_builder import build_planning_query
from prompts.format_planning import format_planning
from prompts.format_planning_full import format_planning_full

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def run_planner_agent():
    print("✅  Planning Agent is running...")


def handle_planner_query(question, session_id):
    """
    Processes the planning-related question and returns a concise summary.
    """
    print("🟠 Received planning question:", question)

    # 1. NLP
    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    # 2. Build query
    department_id = 3  # TEMP: Sales
    intent_data["department_id"] = department_id

    sql_query = build_planning_query(intent_data, department_id=department_id)
    print("🔎 Generated SQL query:\n", sql_query)

    # 3. Execute query
    raw_data = execute_query(sql_query)
    print(f"📊 Raw results: {len(raw_data)} rows")

    # 4. Verificare volum date
    if len(raw_data) > 100:
        print("⚠️ Too many records. Switching to summary response...")

        intent_data["intent"] = "planning_overview"
        sql_query = build_planning_query(intent_data, department_id=department_id)
        raw_data = execute_query(sql_query)

        summary_html = format_planning(
            raw_data,
            f"{question}\n\n⚠️ Note: Results below are aggregated for clarity.",
            intent_data
        )
    else:
        summary_html = format_planning(raw_data, question, intent_data)

    return summary_html


def handle_full_planning_report(question, session_id):
    """
    Generates a full dashboard-like planning report with updated charts.
    """
    print("📄 Generating Full Planning Report...")

    # 1. NLP
    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    # 2. Build main query
    department_id = 3  # TEMP: Sales
    intent_data["department_id"] = department_id

    sql_query = build_planning_query(intent_data, department_id=department_id)
    raw_data = execute_query(sql_query)

    # 3. Check data size and aggregate if needed
    aggregated = False
    if len(raw_data) > 500:
        print("⚠️ Too many records — switching to aggregated data...")
        intent_data["intent"] = "planning_overview"
        sql_query = build_planning_query(intent_data, department_id=department_id)
        raw_data = execute_query(sql_query)
        aggregated = True

    # 4. New chart 1 – Appointment distribution (60 days)
    appointments_query = """
        SELECT 
            a.appointment_date,
            COUNT(*) AS num_appointments
        FROM appointments a
        GROUP BY a.appointment_date
        ORDER BY a.appointment_date ASC
        LIMIT 60;
    """
    appointments_data = execute_query(appointments_query)

    # 5. New chart 2 – Utilization vs Employees per Department
    utilization_query = """
        SELECT 
            d.department_name,
            COUNT(DISTINCT a.employee_id) AS employee_count,
            ROUND(SUM(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time)) / 
                  (COUNT(DISTINCT a.appointment_date) * 480), 2) AS avg_utilization
        FROM appointments a
        JOIN employees e ON a.employee_id = e.employee_id
        JOIN departments d ON e.department_id = d.department_id
        GROUP BY d.department_name
        ORDER BY avg_utilization DESC;
    """
    utilization_data = execute_query(utilization_query)

    chart1_path, chart2_path = (None, None)
    if appointments_data and utilization_data:
        chart1_path, chart2_path = generate_planning_charts_v2(
            appointments_data, utilization_data, session_id
        )
    else:
        print("⚠️ Missing data for one or both charts.")

    # 6. Format final report
    full_summary = format_planning_full(
        raw_data,
        question,
        intent_data,
        chart1_path,
        chart2_path
    )

    return render_template(
        "dashboard_planner.html",
        summary_html=full_summary,
        date=datetime.date.today(),
        chart1_path=chart1_path,
        chart2_path=chart2_path,
        question=question
    )

def generate_planning_charts_v2(appointments_data, utilization_data, session_id):
    """
    Generates two custom planning charts:
    1. Appointment load over time
    2. Utilization vs employee count per department
    """
    os.makedirs("static/temp", exist_ok=True)

    # Chart 1: Appointment load per day (bar)
    dates = [row["appointment_date"] for row in appointments_data]
    values = [row["num_appointments"] for row in appointments_data]

    plt.figure(figsize=(10, 4))
    plt.bar(dates, values, color="slateblue")
    plt.title("Appointment Load Over Time")
    plt.xlabel("Date")
    plt.ylabel("Appointments")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    chart1 = f"static/temp/appointment_distribution_{session_id}.png"
    plt.savefig(chart1)
    plt.close()

    # Chart 2: Utilization vs Employees per Department
    departments = [row["department_name"] for row in utilization_data]
    employees = [row["employee_count"] for row in utilization_data]
    utilization = [row["avg_utilization"] for row in utilization_data]

    x = range(len(departments))
    width = 0.4

    plt.figure(figsize=(10, 5))
    plt.bar(x, employees, width=width, label="Employees", align='center', alpha=0.6)
    plt.bar([i + width for i in x], utilization, width=width, label="Utilization Ratio", align='center', alpha=0.8)
    plt.xticks([i + width / 2 for i in x], departments, rotation=45, ha="right")
    plt.title("Employees vs Utilization per Department")
    plt.ylabel("Count / Ratio")
    plt.legend()
    plt.tight_layout()
    chart2 = f"static/temp/utilization_vs_employees_{session_id}.png"
    plt.savefig(chart2)
    plt.close()

    return chart1, chart2

