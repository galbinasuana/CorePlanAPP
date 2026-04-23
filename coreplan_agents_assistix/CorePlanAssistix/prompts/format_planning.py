from prompts.summary_generator import generate_section_summary

def format_planning(raw_data, question, intent_data):
    intent = intent_data.get("intent", "")
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "Planning Department")

    if not raw_data:
        return f"<i>No planning records were found for <b>{department}</b> during <u>{time_range}</u>.</i>"

    section_title = f"Planning Overview – {department.title()} ({time_range})"

    example_html = """
<p><b>Planning Overview – Sales Department (Last 60 Days):</b> Below is a concise snapshot of key planning metrics and workload dynamics:</p>
<ul>
  <li><b>Task Complexity:</b> The average complexity score remained steady around 3.1, indicating moderate task intensity. However, spikes were observed during project delivery weeks.</li>
  <li><b>Idle Time:</b> Idle time averaged 22 minutes per day per employee, with some peaks surpassing 60 minutes—especially in low-engagement departments.</li>
  <li><b>Meeting Load:</b> Teams handled an average of 2.7 meetings per day, with the Sales department reaching a peak of 5.1 daily meetings mid-month.</li>
  <li><b>Time Utilization:</b> Workload distribution was uneven across departments, suggesting potential for rebalancing assignments and schedules.</li>
</ul>
<p><b>Actionable Tip:</b> Reevaluate task delegation in teams with high idle time and optimize recurring meeting frequency to boost productivity.</p>
"""

    result = generate_section_summary(
        question=question,
        intent=intent,
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )

    print("✅ PLANNER SUMMARY GENERATED:")
    print(result[:500])  # Doar primele 500 caractere

    return result


