from prompts.summary_generator import generate_section_summary

def format_performance(raw_data, question, intent_data):
    intent = intent_data.get("intent", "")
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "the selected department")

    section_title = f"Performance Insights – {department.title()} ({time_range})"

    example_html = """
<p><b>Performance Insights – Sales Department (Q2 2025):</b> Here’s a summary of key highlights extracted from your team’s performance data this quarter:</p>
<ul>
  <li><b>Top Performers:</b> Alice Johnson (94.2) and David Smith (92.5) led in efficiency, exceeding expectations across all tasks.</li>
  <li><b>Engagement Overview:</b> While the average engagement score was 78.2, 3 employees fell below the threshold of 60 — a potential sign of disengagement or misalignment.</li>
  <li><b>Burnout Risk:</b> 28% of employees displayed burnout probabilities above 70%, with correlations to longer working hours and low break time usage.</li>
  <li><b>Idle Time Patterns:</b> A few high performers had elevated idle time (>40 min/day), possibly due to system delays or task-switching overhead.</li>
</ul>
<p><b>Actionable Tip:</b> Consider targeted 1-on-1s with those showing signs of disengagement or burnout, and highlight high performers for recognition or mentorship roles.</p>
"""

    return generate_section_summary(
        question=question,
        intent=intent,
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )



# def format_performance(raw_data, question, intent_data):
#     """
#     Generates a clear, professional answer to the user's question about employee performance.
#     This is used in the blue summary card on results.html.
#     """
#
#     intent = intent_data.get("intent", "")
#     time_range = intent_data.get("time_range", "the recent period")
#     department = intent_data.get("department", "the selected department")
#     metric = intent_data.get("metrics", ["efficiency_score"])[0] if intent_data.get("metrics") else "efficiency_score"
#
#     if not raw_data:
#         return f"<i>No performance data was found for {department} during {time_range}.</i>"
#
#     if intent == "top_performers":
#         title = f"<b>Top performers in {department.title()} ({time_range})</b>"
#         rows = ""
#         for i, row in enumerate(raw_data, 1):
#             name = row["full_name"]
#             score = row.get(metric, "–")
#             rows += f"<p><b>{i}. {name}</b> — {metric.replace('_', ' ').title()}: <u>{score}</u></p>"
#         explanation = "<p>The employees listed above demonstrated consistently high performance levels in recent evaluations. Their contributions had measurable impact in key areas such as task completion, collaboration, and engagement.</p>"
#         return f"{title}{rows}{explanation}"
#
#     elif intent == "burnout_risk":
#         title = f"<b>Employees with high burnout risk in {department.title()} ({time_range})</b>"
#         rows = ""
#         for i, row in enumerate(raw_data, 1):
#             name = row["full_name"]
#             risk = row.get("burnout_probability", "–")
#             rows += f"<p><b>{i}. {name}</b> — Burnout Probability: <u>{risk}</u></p>"
#         explanation = "<p>The individuals above are showing signs of elevated stress and reduced engagement. Immediate follow-up and intervention strategies are recommended to prevent productivity decline.</p>"
#         return f"{title}{rows}{explanation}"
#
#     elif intent == "efficiency_comparison":
#         title = f"<b>Efficiency scores across {department.title()} ({time_range})</b>"
#         rows = ""
#         for i, row in enumerate(raw_data, 1):
#             name = row["full_name"]
#             score = row.get("efficiency_score", "–")
#             rows += f"<p><b>{i}. {name}</b> — Efficiency Score: <u>{score}</u></p>"
#         return f"{title}{rows}<p>This breakdown allows management to quickly assess disparities in employee productivity levels and initiate relevant actions where needed.</p>"
#
#     elif intent == "correlation_analysis":
#         title = f"<b>Correlation insights between key performance indicators ({time_range})</b>"
#         explanation = (
#             "<p>Based on recent data, there is a measurable relationship between efficiency, engagement, and burnout scores. "
#             "Higher engagement tends to correlate with increased efficiency, while rising burnout probability is often linked to drops in productivity.</p>"
#         )
#         return f"{title}{explanation}"
#
#     else:
#         title = f"<b>Department-level performance summary ({time_range})</b>"
#         rows = ""
#         for row in raw_data:
#             dept = row["department"]
#             eff = row.get("avg_efficiency", "–")
#             burn = row.get("avg_burnout", "–")
#             eng = row.get("avg_engagement", "–")
#             rows += f"<p><b>{dept}</b>: Efficiency: <u>{eff}</u>, Burnout: <u>{burn}</u>, Engagement: <u>{eng}</u></p>"
#         return f"{title}{rows}<p>Use this snapshot to compare departments and identify where improvements or additional support may be needed.</p>"
