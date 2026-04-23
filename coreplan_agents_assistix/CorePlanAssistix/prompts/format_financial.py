from prompts.summary_generator import generate_section_summary

def format_financial(raw_data, question, intent_data):
    intent = intent_data.get("intent", "")
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "Sales Department")

    section_title = f"Financial Overview – {department.title()} ({time_range})"

    example_html = """
<p><b>Financial Overview – Sales Department (Last 60 Days):</b> Below is a high-level snapshot of key financial indicators observed in the selected timeframe:</p>
<ul>
  <li><b>Revenue Trends:</b> Average revenue per department was $84,200, with a positive variance in 3 out of 4 weeks.</li>
  <li><b>Expense Efficiency:</b> Operating expenses remained within budget in most cases, but one unit exceeded the threshold by 18%.</li>
  <li><b>Profitability:</b> The average profit margin was 22.4%, slightly above forecast. However, variance was high across sub-teams.</li>
  <li><b>ROI Insights:</b> Highest ROI (48%) was observed in the West Region Sales, while East Region underperformed with only 12% ROI.</li>
</ul>
<p><b>Actionable Tip:</b> Investigate regions with low ROI and initiate cost-optimization discussions. Consider shifting resources toward consistently high-performing teams.</p>
"""

    return generate_section_summary(
        question=question,
        intent=intent,
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )
