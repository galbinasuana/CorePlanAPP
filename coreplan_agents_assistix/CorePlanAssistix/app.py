import os
import uuid
from flask import Flask, request, render_template
from agents.performance_agent import handle_performance_query, handle_full_performance_report
from agents.financial_agent import handle_financial_query, handle_full_financial_report
from agents.planner_agent import handle_planner_query, handle_full_planning_report
from agents.reporter_agent import handle_reporting_query, handle_full_reporting_report
from nlp.intent_classifier import classify_intent
from datetime import date
from dotenv import load_dotenv
from collections import defaultdict

report_cache = defaultdict(dict)
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_cached_or_generate(agent, question, session_id, generator_func):
    cache_key = f"{agent}_{session_id}_{question}"  # adăugat session_id și în cache_key
    if session_id in report_cache and cache_key in report_cache[session_id]:
        return report_cache[session_id][cache_key]
    html = generator_func(question, session_id)
    report_cache[session_id][cache_key] = html
    return html

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    question = request.form.get("question", "").strip()

    if not question:
        return render_template("index.html", error="Please enter a valid question.")

    session_id = str(uuid.uuid4())

    intent_data = classify_intent(question)
    agents_detected = intent_data.get("agents", [])

    performance_summary = handle_performance_query(question, session_id) if "performance" in agents_detected else ""
    financial_summary = handle_financial_query(question, session_id) if "financial" in agents_detected else ""
    planner_summary = handle_planner_query(question, session_id) if "planning" in agents_detected else ""
    reporter_summary = handle_reporting_query(question, session_id) if "reporting" in agents_detected else ""

    return render_template(
        "results.html",
        question=question,
        intent_data=intent_data,
        performance_summary=performance_summary,
        financial_summary=financial_summary,
        planning_summary=planner_summary,
        reporting_summary=reporter_summary,
        active_agents=agents_detected,
        session_id=session_id
    )


@app.route("/full/performance")
def full_performance():
    question = request.args.get("question", "").strip()
    session_id = request.args.get("session_id", "").strip()

    if not question or not session_id:
        return render_template("error.html", message="Missing question or session ID.")

    return get_cached_or_generate("performance", question, session_id, handle_full_performance_report)


@app.route("/full/financial")
def full_financial():
    question = request.args.get("question", "").strip()
    session_id = request.args.get("session_id", "").strip()

    if not question or not session_id:
        return render_template("error.html", message="Missing question or session ID.")

    return get_cached_or_generate("financial", question, session_id, handle_full_financial_report)


@app.route("/full/planner")
def full_planner():
    question = request.args.get("question", "").strip()
    session_id = request.args.get("session_id", "").strip()

    if not question or not session_id:
        return render_template("error.html", message="Missing question or session ID.")

    return get_cached_or_generate("planner", question, session_id, handle_full_planning_report)


@app.route("/full/reporter")
def full_reporter():
    question = request.args.get("question", "").strip()
    session_id = request.args.get("session_id", "").strip()

    if not question or not session_id:
        return render_template("error.html", message="Missing question or session ID.")

    return get_cached_or_generate("reporter", question, session_id, handle_full_reporting_report)



if __name__ == "__main__":
    print("🚀 Starting CorePlan Agents...")
    app.run(host="0.0.0.0", port=5001)
