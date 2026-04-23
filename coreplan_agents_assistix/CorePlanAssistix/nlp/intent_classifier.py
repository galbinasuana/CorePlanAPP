import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_intent(user_input):
    """
    Detectează intenția și agenții relevanți pentru o întrebare dată, folosind OpenAI GPT-3.5.
    Returnează un dicționar cu cheile: agents, intent, time_range, department, metrics, special_focus.
    """
    system_prompt = """
    You are an intent classification assistant for a multi-agent business analytics system. 
    Your job is to extract intent metadata from natural language questions, and return a structured JSON with the following fields:

    {
      "agents": ["performance", "financial", "planning", "reporting"],
      "intent": "summary / kpi / trend / anomaly / forecasting / comparison / risk_alert / recommendation / other",
      "time_range": "last 30 days / Q2 2024 / this year / etc.",
      "department": "Sales / Marketing / All / None",
      "metrics": ["efficiency_score", "revenue", "burnout_probability", etc],
      "special_focus": "Optional description for focus (e.g. 'compare top vs bottom performers')"
    }

    Agent responsibilities:
    - performance: Handle employee KPIs such as efficiency_score, engagement_score, burnout_probability, top performers.
    - financial: Covers revenue, expenses, profit, ROI, budget allocation and variance.
    - planning: Responsible for schedule optimization, workload balance, calendar gaps, overbooking.
    - reporting: Detects anomalies, flags, report quality issues, alerts, urgent risks, and generates recommendations.

    Common metrics by agent:
    - performance: efficiency_score, burnout_probability, engagement_score
    - financial: revenue, expenses, profit, roi, budget_variance
    - planning: schedule_efficiency, workload_distribution, resource_gap
    - reporting: report_quality_score, alert_flag, urgency_index, anomalies_detected

    Example mappings:
    - "How is employee efficiency trending in Q2?" → agents: ["performance"], intent: "trend", time_range: "Q2", metrics: ["efficiency_score"]
    - "What was the total revenue in the past 60 days?" → agents: ["financial"], intent: "summary", time_range: "last 60 days", metrics: ["revenue"]
    - "Are there any scheduling conflicts in the operations department?" → agents: ["planning"], intent: "anomaly", department: "Operations"
    - "How is workload distributed across teams this month?" → agents: ["planning"], intent: "summary", time_range: "this month", metrics: ["workload_distribution"]
    - "Any anomalies detected in the latest reports?" → agents: ["reporting"], intent: "anomaly", time_range: "latest", metrics: ["anomalies_detected"], special_focus: "report anomalies"
    - "Are there urgent issues we need to address this month?" → agents: ["reporting"], intent: "risk_alert", time_range: "this month", metrics: ["urgency_index", "alert_flag"]
    - "Which departments have the lowest report quality?" → agents: ["reporting"], intent: "comparison", metrics: ["report_quality_score"], special_focus: "compare by department"
    - "What actions were suggested based on last month’s reports?" → agents: ["reporting"], intent: "recommendation", time_range: "last month", metrics: ["intervention_suggested"]

    Only return a valid JSON object. Never explain anything or add comments.
    """

    user_prompt = f"User question: {user_input}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content
        import json
        return json.loads(content)
    except Exception as e:
        print("❌ Error during intent classification:", e)
        return {
            "agents": [],
            "intent": "unknown",
            "time_range": "",
            "department": "",
            "metrics": [],
            "special_focus": ""
        }
