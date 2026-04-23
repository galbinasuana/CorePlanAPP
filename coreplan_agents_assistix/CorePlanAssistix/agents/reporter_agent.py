import os
import datetime
import openai
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import render_template

from nlp.intent_classifier import classify_intent
from nlp.query_executor import execute_query
from nlp.query_builder import build_reporting_query
from prompts.format_reporter import format_reporter
from prompts.format_reporter_full import format_reporter_full

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def run_reporter_agent():
    print("✅  Reporter Agent is running ...")


def handle_reporting_query(question, session_id):
    """
    Processes a reporting-related question and returns a summary report.
    """
    print("🟡 Received reporting question:", question)

    # NLP
    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    # Build query
    department_id = 3  # TEMP: Sales
    sql_query = build_reporting_query(intent_data)
    print("🔎 Generated SQL query:\n", sql_query)

    # Execute
    raw_data = execute_query(sql_query)
    print(f"📊 Raw results: {len(raw_data)} rows")

    # Format
    if len(raw_data) > 100:
        print("⚠️ Large dataset, switching to summary view...")
        intent_data["intent"] = "reporter_overview"
        raw_data = execute_query(build_reporting_query(intent_data))

        summary_html = format_reporter(
            raw_data,
            f"{question}\n\n⚠️ Note: This is an aggregated view due to large data.",
            intent_data
        )
    else:
        summary_html = format_reporter(raw_data, question, intent_data)

    return summary_html


def handle_full_reporting_report(question, session_id):
    print("📄 Generating Full Reporting Report...")

    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    sql_query = build_reporting_query(intent_data)
    raw_data = execute_query(sql_query)

    aggregated = False
    if len(raw_data) > 100:
        print("⚠️ Too many records — switching to aggregated data...")
        intent_data["intent"] = "reporter_overview"
        raw_data = execute_query(build_reporting_query(intent_data))
        aggregated = True

    # Charts (latest 10 days only)
    chart_data_query = """
        SELECT report_date, department_focus, employee_morale_index, urgency_index
        FROM reporting_data
        WHERE report_date >= DATE_SUB(CURDATE(), INTERVAL 60 DAY)
        ORDER BY report_date ASC
        LIMIT 200;
    """
    chart_data = execute_query(chart_data_query)

    chart1_path, chart2_path = (None, None)
    if chart_data:
        chart1_path, chart2_path = generate_reporting_charts(chart_data, session_id)
    else:
        print("⚠️ No data available for generating charts.")

    full_summary = format_reporter_full(
        raw_data,
        question,
        intent_data,
        chart1_path,
        chart2_path
    )

    return render_template(
        "dashboard_reporter.html",
        summary_html=full_summary,
        date=datetime.date.today(),
        chart1_path=chart1_path,
        chart2_path=chart2_path,
        question=question
    )


def generate_reporting_charts(data, session_id):
    os.makedirs("static/temp", exist_ok=True)

    # Chart 1 – Urgency Index per Department
    departments = [row["department_focus"] for row in data]
    urgency = [row["urgency_index"] for row in data]

    plt.figure(figsize=(8, 4))
    plt.bar(departments, urgency, color="indianred")
    plt.title("Urgency Index per Department")
    plt.ylabel("Urgency Index")
    plt.xticks(rotation=45, ha="right")
    chart1_path = f"static/temp/urgency_index_{session_id}.png"
    plt.tight_layout()
    plt.savefig(chart1_path)
    plt.close()

    # Chart 2 – Morale Trend
    dates = [row["report_date"].strftime("%m-%d") for row in data]
    morale = [row["employee_morale_index"] for row in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, morale, marker="o", linestyle="-", color="mediumblue")
    plt.title("Employee Morale Trend")
    plt.ylabel("Morale Index")
    plt.xticks(rotation=45)
    chart2_path = f"static/temp/morale_trend_{session_id}.png"
    plt.tight_layout()
    plt.savefig(chart2_path)
    plt.close()

    return chart1_path, chart2_path
