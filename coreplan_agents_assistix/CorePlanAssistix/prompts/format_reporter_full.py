from prompts.summary_generator import generate_section_summary

def format_reporter_full(raw_data, question, intent_data, chart1_path=None, chart2_path=None):
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "the organization")

    section_title = f"Comprehensive Reporting Analysis – {department.title()} ({time_range})"

    example_html = """
<h3>Full Reporting Overview – Sales Department (Last 60 Days)</h3>

<p>This comprehensive report highlights all relevant insights extracted from internal reporting data.</p>

<ul>
  <li><b>Urgency Patterns:</b> Average <b>urgency index</b> was 61.3, with 6 reports marked above 85 — signaling critical situations that required immediate action.</li>

  <li><b>Employee Morale Trends:</b> The morale index fluctuated between 45–88. A downward trend was observed in the second half of June, especially in the Support and Logistics teams.</li>

  <li><b>Anomalies:</b> A total of 32 anomalies were recorded, most often related to data incompleteness or KPI mismatches.</li>

  <li><b>Schedule Slippage:</b> Median slippage was 2.4 days/report, with 4 reports exceeding 6 days — a potential indicator of planning or execution issues.</li>

  <li><b>Report Quality:</b> Quality scores ranged between 58 and 92. 4 reports scored under 70, often linked with unverified data sources or low scan coverage.</li>

  <li><b>Recommendations Analysis:</b> Most frequent types were <i>Optimize Workflow</i> and <i>Increase QA Checks</i>, suggesting process-level refinements are needed.</li>
</ul>

<h3>Strategic Recommendations</h3>
<ul>
  <li><b>Investigate high urgency reports</b> to ensure timely interventions and avoid cascading risks.</li>
  <li><b>Improve data pipeline health</b> to reduce anomaly rates and support better decision-making.</li>
  <li><b>Enhance review protocols</b> for reports with low quality scores.</li>
  <li><b>Standardize morale tracking</b> to correlate team sentiment with report quality or delivery risk.</li>
</ul>

<h3>Short-Term Actions</h3>
<ul>
  <li>Audit the 5 lowest-scoring reports from the last 30 days.</li>
  <li>Set a minimum scan threshold per report to improve completeness.</li>
  <li>Roll out reviewer training for departments with repeated low-quality submissions.</li>
</ul>

<h3>Long-Term Strategy</h3>
<ul>
  <li>Implement anomaly auto-detection in reporting pipeline.</li>
  <li>Use urgency index and morale scores to forecast operational risks.</li>
  <li>Introduce a quarterly QA dashboard to track reporting quality KPIs across units.</li>
</ul>
"""

    summary = generate_section_summary(
        question="Generate a full professional analysis using all available reporting indicators, highlighting risks, anomalies, and recommended actions.",
        intent="full_reporting_overview",
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )

    html = f"""
    <h2>📌 Executive Summary</h2>
    <div>{summary}</div>
    """

    if chart1_path and chart2_path:
        html += f"""
        <h3>📊 Visual Insights (Past 60 Days)</h3>
        <div style="display:flex; gap: 40px; margin-bottom: 30px;">
            <div style="flex:1;">
                <img src="/{chart1_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>Employee Morale Over Time</i></p>
            </div>
            <div style="flex:1;">
                <img src="/{chart2_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>Urgency Index – Daily Trends</i></p>
            </div>
        </div>
        """

    html += """
    <h3>📝 Final Notes</h3>
    <p>This full reporting report is designed to support strategic decision-making by highlighting risk zones, operational anomalies, and improvement opportunities extracted from the latest internal reports.</p>
    """

    return html
