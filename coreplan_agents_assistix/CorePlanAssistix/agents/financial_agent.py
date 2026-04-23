import os
import openai
import datetime
import matplotlib.pyplot as plt
from flask import render_template
from dotenv import load_dotenv

from nlp.intent_classifier import classify_intent
from nlp.query_executor import execute_query
from nlp.query_builder import build_financial_query
from prompts.format_financial import format_financial
from prompts.format_financial_full import format_financial_full

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def run_financial_agent():
    print("✅  Financial Agent is running...")


def handle_financial_query(question, session_id):
    print("🟡 Received financial question:", question)

    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    sql_query = build_financial_query(intent_data)
    raw_data = execute_query(sql_query)
    print(f"📊 Raw results: {len(raw_data)} rows")

    if len(raw_data) > 100:
        print("⚠️ Too many records. Using aggregated summary.")
        intent_data["intent"] = "full_financial_overview"
        sql_query = build_financial_query(intent_data)
        raw_data = execute_query(sql_query)

        summary_html = format_financial(
            raw_data,
            f"{question}\n\n⚠️ Note: The results below are aggregated for clarity.",
            intent_data
        )
    else:
        summary_html = format_financial(raw_data, question, intent_data)

    return summary_html


def handle_full_financial_report(question, session_id):
    print("📄 Generating Full Financial Report...")

    intent_data = classify_intent(question)
    print("🧠 Intent data:", intent_data)

    # 1. Select principal
    sql_raw = build_financial_query(intent_data)
    raw_data = execute_query(sql_raw)
    print(f"📊 Raw financial records: {len(raw_data)}")

    # 2. Agregare dacă sunt prea multe
    aggregated = False
    if len(raw_data) > 500:
        print("⚠️ Too many records. Switching to aggregated version.")
        intent_data["intent"] = "full_financial_overview"
        sql_raw = build_financial_query(intent_data)
        raw_data = execute_query(sql_raw)
        aggregated = True

    # 3. Query separat pentru grafice (limitat și optimizat)
    chart_query = """
        SELECT record_date, revenue, expenses, (profit / expenses * 100) AS roi
        FROM financial_data
        WHERE department_id = (SELECT department_id FROM departments WHERE department_name = 'Sales')
          AND record_date >= DATE_SUB(CURDATE(), INTERVAL 60 DAY)
        ORDER BY record_date ASC
        LIMIT 200;
    """
    chart_data = execute_query(chart_query)
    chart1_path, chart2_path = generate_financial_charts(chart_data, session_id, aggregated=False)

    # 4. Formatare finală
    full_summary = format_financial_full(raw_data, question, intent_data, chart1_path, chart2_path)

    return render_template(
        "dashboard_financial.html",
        summary_html=full_summary,
        date=datetime.date.today(),
        chart1_path=chart1_path,
        chart2_path=chart2_path,
        question=question
    )


def generate_financial_charts(data, session_id, aggregated=False):
    os.makedirs("static/temp", exist_ok=True)

    dates = [row.get("record_date", f"Day {i+1}") for i, row in enumerate(data)]
    revenue = [row.get("avg_revenue") if aggregated else row.get("revenue", 0) for row in data]
    expenses = [row.get("avg_expenses") if aggregated else row.get("expenses", 0) for row in data]
    roi = [row.get("avg_roi") if aggregated else row.get("roi", 0) for row in data]

    # Chart 1: Revenue vs Expenses over time
    plt.figure(figsize=(10, 5))
    x = range(len(dates))
    plt.bar(x, revenue, width=0.4, label="Revenue", align="center", color="steelblue")
    plt.bar(x, expenses, width=0.4, label="Expenses", align="edge", color="lightcoral")
    plt.xticks(x, dates, rotation=45, ha="right")
    plt.title("Revenue vs Expenses – Last 60 Days")
    plt.legend()
    chart1 = f"static/temp/revenue_expenses_{session_id}.png"
    plt.tight_layout()
    plt.savefig(chart1)
    plt.close()

    # Chart 2: ROI Trend
    plt.figure(figsize=(10, 4))
    plt.plot(dates, roi, marker="o", color="seagreen")
    plt.title("ROI Trend – Last 60 Days")
    plt.ylabel("ROI (%)")
    plt.xticks(rotation=45, ha="right")
    chart2 = f"static/temp/roi_chart_{session_id}.png"
    plt.tight_layout()
    plt.savefig(chart2)
    plt.close()

    return chart1, chart2

