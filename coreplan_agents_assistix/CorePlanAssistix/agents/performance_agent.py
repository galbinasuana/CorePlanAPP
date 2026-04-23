import openai
import os
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nlp.intent_classifier import classify_intent
from nlp.query_builder import build_performance_query
from nlp.query_executor import execute_query
from dotenv import load_dotenv
from flask import render_template
from prompts.format_performance import format_performance
from prompts.format_performance_full import format_performance_full


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_performance_agent():
    print("✅  Performance Agent is running ...")

def handle_performance_query(question, session_id):
    """
    Processes the performance-related question and returns a professional summary.
    """
    print("🟡 Received question:", question)

    # 1. NLP
    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    # 2. Build query
    department_id = 3  # TEMP: Sales
    sql_query = build_performance_query(intent_data, department_id=department_id)
    print("🔎 Generated SQL query:\n", sql_query)

    # 3. Execute query
    raw_data = execute_query(sql_query)
    print(f"📊 Raw results: {len(raw_data)} rows")

    # 4. Verificare volum date
    if len(raw_data) > 100:
        print("⚠️ Too many records. Switching to summary response...")

        # Ne asigurăm că folosim un sumar agregat
        intent_data["intent"] = "full_performance_overview"
        sql_summary_query = build_performance_query(intent_data, department_id=department_id)
        raw_data = execute_query(sql_summary_query)

        # Adăugăm și un mesaj de avertizare în final_summary
        summary_html = format_performance(
            raw_data,
            f"{question}\n\n⚠️ Note: Due to a large dataset, the response below is an aggregated summary.",
            intent_data
        )
    else:
        summary_html = format_performance(raw_data, question, intent_data)

    return summary_html

def handle_full_performance_report(question, session_id):
    print("📄 Generating Full Performance Report...")

    # 1. Analiză NLP
    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    # 2. Interogare date principale pentru raport
    sql_full = build_performance_query(intent_data)
    raw_data = execute_query(sql_full)

    aggregated = False
    if len(raw_data) > 100:
        print("⚠️ Too many records — switching to aggregated data...")
        intent_data["intent"] = "full_performance_overview"
        sql_full = build_performance_query(intent_data)
        raw_data = execute_query(sql_full)
        aggregated = True

    # 3. Date separate pentru generare grafice (limit 200, neafectat de agregare)
    chart1_path, chart2_path = (None, None)
    chart_data_query = """
        SELECT employee_name AS full_name, department, efficiency_score,
               engagement_score, burnout_probability, idle_time_minutes, task_complexity
        FROM employee_performance
        WHERE record_date >= DATE_SUB(CURDATE(), INTERVAL 60 DAY)
        LIMIT 200;
    """
    chart_data = execute_query(chart_data_query)

    if chart_data:
        chart1_path, chart2_path = generate_performance_charts(chart_data, session_id)
    else:
        print("⚠️ No data available for generating charts.")

    # 4. Formatare finală a raportului
    full_summary = format_performance_full(
        raw_data,
        question,
        intent_data,
        chart1_path,
        chart2_path
    )

    return render_template(
        "dashboard_performance.html",
        summary_html=full_summary,
        date=datetime.date.today(),
        chart1_path=chart1_path,
        chart2_path=chart2_path,
        question=question
    )



def generate_performance_charts(data, session_id):
    os.makedirs("static/temp", exist_ok=True)

    efficiency = [row["efficiency_score"] for row in data if row["efficiency_score"] is not None]
    burnout = [row["burnout_probability"] for row in data if row["burnout_probability"] is not None]

    plt.figure()
    plt.scatter(efficiency, burnout, color='teal')
    plt.xlabel("Efficiency Score")
    plt.ylabel("Burnout Probability")
    plt.title("Efficiency vs Burnout")
    plt.tight_layout()
    chart1_filename = f"static/temp/efficiency_vs_burnout_{session_id}.png"
    plt.savefig(chart1_filename)
    plt.close()

    employees = [row["full_name"] for row in data if row.get("engagement_score") is not None]
    engagement = [row["engagement_score"] for row in data if row.get("engagement_score") is not None]

    plt.figure(figsize=(10, 4))
    plt.bar(employees, engagement, color='steelblue')
    plt.xlabel("Employees")
    plt.ylabel("Engagement Score")
    plt.title("Engagement Score per Employee")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    chart2_filename = f"static/temp/engagement_scores_{session_id}.png"
    plt.savefig(chart2_filename)
    plt.close()

    return chart1_filename, chart2_filename