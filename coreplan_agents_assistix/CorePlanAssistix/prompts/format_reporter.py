from prompts.summary_generator import generate_section_summary

def format_reporter(raw_data, question, intent_data):
    intent = intent_data.get("intent", "")
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "the selected department")

    section_title = f"Reporting Insights – {department.title()} ({time_range})"

    example_html = """
<p><b>Reporting Insights – Sales Department (Last 30 Days):</b> Here’s a summary of key signals and patterns extracted from recent operational reports:</p>
<ul>
  <li><b>Urgent Reports:</b> 5 reports were flagged with a high <b>urgency index > 80</b>, mainly related to resource shortages and slippages in delivery timelines.</li>
  <li><b>Anomalies Detected:</b> A spike in anomalies occurred between June 10–14, especially in the Marketing department due to missing data sources and inconsistent KPIs.</li>
  <li><b>Report Quality:</b> The average <b>report_quality_score</b> was 73/100, with notable declines in accuracy and completeness in 4 out of 12 reports.</li>
  <li><b>Recommendations Overview:</b> The most frequent recommendation type was <i>Restructure Workflow</i>, indicating systemic inefficiencies in cross-team processes.</li>
</ul>
<p><b>Actionable Tip:</b> Prioritize follow-up on high urgency reports, and consider improving data integration workflows to reduce anomalies and improve quality.</p>
"""

    result =  generate_section_summary(
        question=question,
        intent=intent,
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )

    print("✅ PLANNER SUMMARY GENERATED:")
    print(result[:500])  # Doar primele 500 caractere

    return result
