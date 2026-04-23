from prompts.summary_generator import generate_section_summary

def format_planning_full(raw_data, question, intent_data, chart1_path=None, chart2_path=None):
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "the organization")

    section_title = f"Comprehensive Planning Report – {department.title()} ({time_range})"

    example_html = """
<h3>Full Planning Overview – Sales Department (Last 60 Days)</h3>

<p>This report delivers an in-depth analysis of operational planning indicators and time utilization trends observed across the selected timeframe.</p>

<ul>
  <li><b>Task Complexity:</b> Tasks ranged from low (1) to high (5) complexity. Average complexity was 3.2, with spikes observed during campaign launches and month-end reporting periods.</li>

  <li><b>Idle Time Patterns:</b> Daily idle time averaged 25 minutes per employee. Sales and Support teams showed the highest idle time peaks, often linked to meeting congestion or blocked tasks.</li>

  <li><b>Meeting Load & Appointment Density:</b> Sales and client-facing teams averaged 3.9 appointments per day, with some employees exceeding 6–7 meetings daily. Internal teams averaged 1.5 meetings/day.</li>

  <li><b>Time Allocation:</b> 62% of logged hours were spent on high-priority deliverables. However, 18% was consumed by repetitive admin tasks, which could be streamlined through automation.</li>
</ul>

<p><b>Strategic Recommendations:</b></p>
<ul>
  <li><b>Redistribute workload</b> across departments to address bottlenecks and uneven task complexity.</li>
  <li><b>Limit non-essential meetings</b> in overbooked teams using scheduling caps.</li>
  <li><b>Introduce time-blocking practices</b> for teams with high context-switching rates.</li>
  <li><b>Automate low-value activities</b> via digital workflow tools (e.g., status updates, reporting).</li>
</ul>

<h3>Short-Term Actions</h3>
<ul>
  <li>Audit calendar data to identify excessive meeting overlaps and conflicts.</li>
  <li>Enable smart alerts for idle time >45 minutes in any shift.</li>
  <li>Launch pilot on workload rebalance for high-burnout roles.</li>
</ul>

<h3>Long-Term Strategy</h3>
<ul>
  <li>Adopt adaptive planning frameworks to shift resources dynamically across weeks.</li>
  <li>Integrate personal productivity insights in performance evaluations.</li>
  <li>Develop cross-functional task pools for more balanced task allocation.</li>
</ul>
"""

    summary = generate_section_summary(
        question="Generate a full planning report using all aggregated indicators available.",
        intent="full_planning_overview",
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )

    html = f"""
    <h2>Executive Summary</h2>
    <div>{summary}</div>
    """

    if chart1_path and chart2_path:
        html += f"""
        <h3>Visual Insights for the Last 60 Days</h3>
        <div style="display:flex; gap: 40px; margin-bottom: 30px;">
            <div style="flex:1;">
                <img src="/{chart1_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>Appointment Load per Day</i></p>
            </div>
            <div style="flex:1;">
                <img src="/{chart2_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>Idle Time and Task Complexity</i></p>
            </div>
        </div>
        """

    html += """
    <h3>Final Notes</h3>
    <p>This planning report provides strategic visibility over operational efficiency, workload balancing, and time utilization across teams.</p>
    """

    return html
