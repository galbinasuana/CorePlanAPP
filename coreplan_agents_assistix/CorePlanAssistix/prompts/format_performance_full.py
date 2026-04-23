from prompts.summary_generator import generate_section_summary

def format_performance_full(raw_data, question, intent_data, chart1_path=None, chart2_path=None):
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "the organization")

    section_title = f"Comprehensive Performance Report – {department.title()} ({time_range})"

    example_html = """
<h3> Full Performance Overview – Sales Department (Q2 2025)</h3>

<p>This report provides a comprehensive analysis of all available performance indicators across the selected department.</p>

<ul>
  <li><b>Efficiency Scores:</b> Range between <b>54.3</b> and <b>94.2</b>. Top 10% consistently exceeded 90. The bottom quartile scored under 65, signaling possible performance challenges.</li>

  <li><b>Engagement Trends:</b> Median engagement score was <b>73.2</b>. However, 5 employees fell below 60, suggesting the need for morale or alignment interventions.</li>

  <li><b>Burnout Risk:</b> 4 employees exceeded 75% probability. These individuals often had longer work durations with minimal rest periods and above-average task complexity.</li>

  <li><b>Idle Time:</b> The average was 27 minutes/day. However, several employees exceeded 50 minutes, possibly due to unclear responsibilities or task handoffs.</li>

  <li><b>Task Complexity Impact:</b> Employees handling high-complexity tasks (Level 3) generally had lower engagement but higher efficiency, indicating focused expertise but possible fatigue.</li>
</ul>

<p><b>Strategic Recommendations:</b></p>
<ul>
  <li><b>Recognize top performers</b> publicly or through bonuses to reinforce excellence.</li>
  <li><b>Mentor low scorers</b> via pairing with high-efficiency peers.</li>
  <li><b>Address burnout early</b> through workload adjustments or wellness programs.</li>
  <li><b>Investigate outliers</b> with abnormal idle time or mismatch between engagement and efficiency.</li>
</ul>

<h3>Short-Term Actions</h3>
<ul>
  <li>Run 1:1 check-ins with employees in the bottom quartile of engagement or efficiency.</li>
  <li>Prioritize weekly pulse surveys to monitor morale changes post-interventions.</li>
  <li>Activate peer mentoring pilot for 4 weeks across low-performing individuals.</li>
</ul>

<h3>Long-Term Strategy</h3>
<ul>
  <li>Build predictive models to track burnout risk early based on workload and idle time.</li>
  <li>Design role-specific training paths for complex-task teams to sustain performance.</li>
  <li>Standardize idle time KPIs to improve alignment between teams.</li>
</ul>
"""

    summary = generate_section_summary(
        question="Generate a complete professional analysis using all performance indicators and employee data.",
        intent="full_performance_overview",
        data=raw_data,
        section_title=section_title,
        example_html=example_html
    )

    html = f"""
    <h2>Executive Summary</h2>
    <div>{summary}</div>
    """

    # ✅ Grafice doar dacă există
    if chart1_path and chart2_path:
        html += f"""
        <h3>Visual Insights for the Last 60 Days</h3>
        <div style="display:flex; gap: 40px; margin-bottom: 30px;">
            <div style="flex:1;">
                <img src="/{chart1_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>Efficiency vs Burnout</i></p>
            </div>
            <div style="flex:1;">
                <img src="/{chart2_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>Engagement per Employee</i></p>
            </div>
        </div>
        """

    html += """
    <h3>Final Notes</h3>
    <p>This full performance report was generated using all employee data available during the selected period, with the goal of aiding executive decision-making and team optimization.</p>
    """

    return html



# from prompts.summary_generator import generate_section_summary
#
#
# def format_performance_full(raw_data, question, intent_data, chart1_path=None, chart2_path=None):
#     time_range = intent_data.get("time_range", "the recent period")
#     department = intent_data.get("department", "the organization")
#
#     section_title = f"Comprehensive Performance Report – {department.title()} ({time_range})"
#
#     example_html = """
# <h3> Full Performance Overview – Sales Department (Q2 2025)</h3>
#
# <p>This report provides a comprehensive analysis of all available performance indicators across the selected department.</p>
#
# <ul>
#   <li><b>Efficiency Scores:</b> Range between <b>54.3</b> and <b>94.2</b>. Top 10% consistently exceeded 90. The bottom quartile scored under 65, signaling possible performance challenges.</li>
#
#   <li><b>Engagement Trends:</b> Median engagement score was <b>73.2</b>. However, 5 employees fell below 60, suggesting the need for morale or alignment interventions.</li>
#
#   <li><b>Burnout Risk:</b> 4 employees exceeded 75% probability. These individuals often had longer work durations with minimal rest periods and above-average task complexity.</li>
#
#   <li><b>Idle Time:</b> The average was 27 minutes/day. However, several employees exceeded 50 minutes, possibly due to unclear responsibilities or task handoffs.</li>
#
#   <li><b>Task Complexity Impact:</b> Employees handling high-complexity tasks (Level 3) generally had lower engagement but higher efficiency, indicating focused expertise but possible fatigue.</li>
# </ul>
#
# <p><b>Strategic Recommendations:</b></p>
# <ul>
#   <li> <b>Recognize top performers</b> publicly or through bonuses to reinforce excellence.</li>
#   <li> <b>Mentor low scorers</b> via pairing with high-efficiency peers.</li>
#   <li>️ <b>Address burnout early</b> through workload adjustments or wellness programs.</li>
#   <li> <b>Investigate outliers</b> with abnormal idle time or mismatch between engagement and efficiency.</li>
# </ul>
# """
#
#     summary = generate_section_summary(
#         question="Generate a complete professional analysis using all performance indicators and employee data.",
#         intent="full_performance_overview",
#         data=raw_data,
#         section_title=section_title,
#         example_html=example_html
#     )
#
#     html = f"""
#     <h2> Executive Summary</h2>
#     <div>{summary}</div>
#     """
#
#     if chart1_path and chart2_path:
#         html += f"""
#         <h3> Visual Insights</h3>
#         <div style="display:flex; gap: 40px; margin-bottom: 30px;">
#             <div style="flex:1;">
#                 <img src="/{chart1_path}" style="max-width:100%;">
#                 <p style="text-align:center;"><i>Efficiency vs Burnout</i></p>
#             </div>
#             <div style="flex:1;">
#                 <img src="/{chart2_path}" style="max-width:100%;">
#                 <p style="text-align:center;"><i>Engagement per Employee</i></p>
#             </div>
#         </div>
#         """
#
#     html += """
#     <h3> Final Notes</h3>
#     <p>This full performance report was generated using all employee data available during the selected period, with the goal of aiding executive decision-making and team optimization.</p>
#     """
#     return html

# def format_performance_full(raw_data, question, intent_data, chart1_path=None, chart2_path=None):
#     """
#     Generates a comprehensive professional report for /full/performance.
#     Intended for presentation to executive leadership.
#     """
#
#     intent = intent_data.get("intent", "")
#     time_range = intent_data.get("time_range", "the recent period")
#     department = intent_data.get("department", "the selected department")
#     metric = intent_data.get("metrics", ["efficiency_score"])[0] if intent_data.get("metrics") else "efficiency_score"
#
#     if not raw_data:
#         return f"<i>No performance records were found for {department} during {time_range}.</i>"
#
#     html = f"""
#     <h2>📌 Executive Summary</h2>
#     <p>This report provides a detailed analysis of employee performance trends across <b>{department.title()}</b> during <u>{time_range}</u>. The focus is on identifying high-impact contributors, diagnosing performance gaps, and outlining evidence-based recommendations to guide strategic decision-making.</p>
#     """
#
#     if intent == "top_performers":
#         html += """
#         <h3>📊 Key Metrics: Top Performers</h3>
#         <table class="report-table">
#             <tr><th>Rank</th><th>Employee</th><th>Score</th></tr>
#         """
#         for i, row in enumerate(raw_data, 1):
#             html += f"<tr><td>{i}</td><td>{row['full_name']}</td><td>{row.get(metric, '-')}</td></tr>"
#         html += "</table>"
#
#         html += """
#         <p><b>Interpretation:</b> These employees consistently delivered high results, demonstrating strong task ownership, adaptability, and positive peer influence. Retention strategies and growth pathways should be prioritized for this group.</p>
#         """
#
#     elif intent == "burnout_risk":
#         html += """
#         <h3>⚠️ Burnout Risk Monitoring</h3>
#         <table class="report-table">
#             <tr><th>Employee</th><th>Burnout Probability</th></tr>
#         """
#         for row in raw_data:
#             html += f"<tr><td>{row['full_name']}</td><td>{row['burnout_probability']}</td></tr>"
#         html += "</table>"
#
#         html += """
#         <p><b>Executive Insight:</b> These individuals show signs of elevated psychological strain. Intervention plans, workload audits, and engagement restoration strategies are recommended to mitigate risk.</p>
#         """
#
#     elif intent == "correlation_analysis":
#         html += """
#         <h3>📈 KPI Correlation Analysis</h3>
#         <p>This section examines the interplay between three key indicators:</p>
#         <ul>
#             <li><b>Efficiency Score</b></li>
#             <li><b>Engagement Score</b></li>
#             <li><b>Burnout Probability</b></li>
#         </ul>
#         <p>Preliminary results indicate the following patterns:</p>
#         <ul>
#             <li>Employees with higher engagement consistently exhibit elevated efficiency scores.</li>
#             <li>Burnout risk is inversely correlated with engagement and moderately with efficiency.</li>
#         </ul>
#         <p><b>Recommendation:</b> Prioritize engagement initiatives to maintain operational output while reducing burnout exposure.</p>
#         """
#
#     elif intent == "efficiency_comparison":
#         html += """
#         <h3>📊 Efficiency Score Comparison</h3>
#         <table class="report-table">
#             <tr><th>Employee</th><th>Efficiency Score</th></tr>
#         """
#         for row in raw_data:
#             html += f"<tr><td>{row['full_name']}</td><td>{row['efficiency_score']}</td></tr>"
#         html += "</table>"
#
#         html += """
#         <p><b>Insight:</b> Significant performance gaps observed. Follow-up 1:1 sessions are advised with low-scorers to determine blockers (e.g., unclear objectives, overload, skill mismatch).</p>
#         """
#
#     else:
#         html += """
#         <h3>🧭 Department-Level Performance Overview</h3>
#         <table class="report-table">
#             <tr><th>Department</th><th>Avg. Efficiency</th><th>Avg. Burnout</th><th>Avg. Engagement</th></tr>
#         """
#         for row in raw_data:
#             html += f"""
#                 <tr>
#                     <td>{row['department']}</td>
#                     <td>{row['avg_efficiency']}</td>
#                     <td>{row['avg_burnout']}</td>
#                     <td>{row['avg_engagement']}</td>
#                 </tr>
#             """
#         html += "</table>"
#
#         html += """
#         <p><b>Summary:</b> This overview provides a comparative snapshot between teams. Performance disparities suggest the need for department-specific optimization strategies and targeted coaching initiatives.</p>
#         """
#
#     # 🔽🔽 Adăugăm graficele aici
#     if chart1_path and chart2_path:
#         html += f"""
#         <h3>📊 Visual Insights</h3>
#         <div style="display:flex; flex-wrap:wrap; gap: 40px; margin-bottom: 30px;">
#             <div style="flex: 1; min-width: 300px;">
#                 <img src="/{chart1_path}" alt="Efficiency vs Burnout" style="max-width:100%; border:1px solid #ccc; border-radius:8px;">
#                 <p style="text-align:center;"><i>Efficiency vs Burnout Probability</i></p>
#             </div>
#             <div style="flex: 1; min-width: 300px;">
#                 <img src="/{chart2_path}" alt="Engagement Score" style="max-width:100%; border:1px solid #ccc; border-radius:8px;">
#                 <p style="text-align:center;"><i>Engagement Score per Employee</i></p>
#             </div>
#         </div>
#         """
#
#     # 🔽 Recomandările strategice
#     html += """
#     <h3>✅ Strategic Recommendations</h3>
#     <ul>
#         <li><b>Short-term:</b> Recognize and reward high performers to reinforce behavior. Monitor employees at risk of burnout and reduce non-critical workload.</li>
#         <li><b>Medium-term:</b> Roll out engagement surveys and reskill programs. Establish clearer performance feedback loops.</li>
#         <li><b>Long-term:</b> Invest in leadership development and adaptive task allocation based on live KPIs.</li>
#     </ul>
#
#     <h3>📌 Final Notes</h3>
#     <p>This report was auto-generated by the CorePlan AI Assistant using real-time data. All recommendations are based on historical trends and predictive modeling aligned with best practices in organizational performance analysis.</p>
#     """
#
#     return html
