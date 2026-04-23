from prompts.summary_generator import generate_section_summary

def format_financial_full(raw_data, question, intent_data, chart1_path=None, chart2_path=None):
    time_range = intent_data.get("time_range", "the recent period")
    department = intent_data.get("department", "the organization")

    section_title = f"Comprehensive Financial Report – {department.title()} ({time_range})"

    example_html = """
<h3>Full Financial Overview – Sales Department (Last 60 Days)</h3>

<p>This report presents an in-depth analysis of key financial metrics gathered across the department within the selected timeframe.</p>

<ul>
  <li><b>Revenue Patterns:</b> Department revenue ranged between <b>$42,000</b> and <b>$124,000</b>. Top contributors consistently exceeded $100K.</li>

  <li><b>Expense Control:</b> Average expenses remained stable, but 2 out of 7 teams reported cost overruns >15%, especially in Q2 marketing spend.</li>

  <li><b>Profit Margins:</b> Margins varied between <b>10.2%</b> and <b>32.5%</b>. Teams with optimized costs (despite lower revenue) showed stronger profitability.</li>

  <li><b>Budget Variance:</b> Negative variance (overspending) was observed in 3 departments. The worst deviation was -18%, due to unexpected travel and logistics costs.</li>

  <li><b>ROI Trends:</b> Return on investment ranged from <b>9%</b> to <b>41%</b>, highlighting disparities in campaign efficiency and sales effectiveness.</li>
</ul>

<p><b>Strategic Recommendations:</b></p>
<ul>
  <li><b>Reevaluate budget planning</b> in teams with consistent overspending.</li>
  <li><b>Expand high-ROI initiatives</b> in West and Central regions where returns exceeded 35%.</li>
  <li><b>Enforce expense tracking</b> in marketing and field operations.</li>
  <li><b>Launch financial coaching</b> for managers with low margin or ROI awareness.</li>
</ul>

<h3>Short-Term Actions</h3>
<ul>
  <li>Conduct a cost audit for Q2 marketing and travel expenditures.</li>
  <li>Review budget variance thresholds and escalation protocols.</li>
  <li>Implement weekly reporting dashboards for ROI monitoring.</li>
</ul>

<h3>Long-Term Strategy</h3>
<ul>
  <li>Integrate predictive analytics to forecast profit margin risks early.</li>
  <li>Shift to zero-based budgeting for underperforming divisions.</li>
  <li>Train financial liaisons in every department for proactive risk tracking.</li>
</ul>
"""

    summary = generate_section_summary(
        question="Generate a full financial report using all aggregated indicators available.",
        intent="full_financial_overview",
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
                <p style="text-align:center; font-size:14px;"><i>Revenue vs Expenses</i></p>
            </div>
            <div style="flex:1;">
                <img src="/{chart2_path}" style="max-width:100%; border-radius:8px; border:1px solid #ccc;">
                <p style="text-align:center; font-size:14px;"><i>ROI per Department</i></p>
            </div>
        </div>
        """

    html += """
    <h3>Final Notes</h3>
    <p>This financial report is designed to support executive decisions and budgeting alignment based on data-driven insights.</p>
    """

    return html
