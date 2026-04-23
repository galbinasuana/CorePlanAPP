from data.db import get_db_connection
from datetime import datetime
import calendar

def handle_sales_report_request(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    current_year = datetime.now().year

    # 1. Total sales & number of deals closed (YTD)
    cursor.execute("""
        SELECT SUM(sd.total_amount) AS total_sales
        FROM sales_data sd
        WHERE sd.employee_id = %s AND YEAR(sd.sale_date) = %s
    """, (employee_id, current_year))
    sales_result = cursor.fetchone()
    total_sales = sales_result['total_sales'] or 0

    cursor.execute("""
        SELECT COUNT(*) AS deals_closed
        FROM client_deals cd
        JOIN clients c ON cd.client_id = c.client_id
        WHERE cd.deal_stage = 'Closed Won'
          AND YEAR(cd.close_date) = %s
          AND cd.client_id IN (
              SELECT client_id FROM sales_data WHERE employee_id = %s
          )
    """, (current_year, employee_id))
    deals_result = cursor.fetchone()
    deals_closed = deals_result['deals_closed'] or 0

    # 2. Target cumulative YTD
    cursor.execute("""
        SELECT SUM(target_amount) AS total_target
        FROM sales_targets
        WHERE employee_id = %s AND YEAR(target_month) = %s
    """, (employee_id, current_year))
    target = cursor.fetchone()
    target_amount = target['total_target'] or 0

    # 3. Conversion rate (deals vs leads/contact attempts - aprox cu closed vs all deals)
    cursor.execute("""
        SELECT COUNT(*) AS total_deals
        FROM client_deals
        WHERE client_id IN (
            SELECT client_id FROM sales_data WHERE employee_id = %s
        )
        AND YEAR(close_date) = %s
    """, (employee_id, current_year))
    all_deals = cursor.fetchone()['total_deals'] or 1  # evit div/0
    conversion_rate = round((deals_closed / all_deals) * 100, 2)

    # 4. Pending follow-ups (all time)
    cursor.execute("""
        SELECT COUNT(*) AS pending
        FROM followups
        WHERE status = 'Pending'
          AND client_id IN (
              SELECT client_id FROM sales_data WHERE employee_id = %s
          )
    """, (employee_id,))
    pending = cursor.fetchone()['pending'] or 0

    conn.close()

    # Calcul procent target
    target_percent = round((total_sales / target_amount) * 100, 2) if target_amount else 0

    # HTML răspuns
    html = f"""
    <div class='bot-message'>
        <p style="font-weight: 600; font-size: 16px; margin-bottom: 10px;">
            📊 Your Sales Performance - {current_year}
        </p>
        <div style="line-height: 1.8;">
            <span>💰 <strong>Total Sales:</strong> €{total_sales:,.2f}</span><br>
            <span>🎯 <strong>Target Achieved:</strong> {target_percent}%</span><br>
            <span>📎 <strong>Deals Closed:</strong> {deals_closed}</span><br>
            <span>📈 <strong>Conversion Rate:</strong> {conversion_rate}%</span><br>
            <span>⏳ <strong>Pending Follow-ups:</strong> {pending}</span>
        </div>
        <div class="bot-options bot-options-centered" style="margin-top: 15px;">
            <button class="workflow-button" data-action="monthly-breakdown">📊 See Monthly Breakdown</button>
            <button class="workflow-button" data-action="client-stats">👤 Client Stats</button>
            <button class="workflow-button" data-action="improve-suggestions">💡 Suggestions to Improve</button>
        </div>
    </div>
    """

    return {"html": html}

def handle_monthly_sales_breakdown(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    current_year = datetime.now().year
    current_month = datetime.now().month

    html = """
    <div class="reminders-card-message">
        <div class="reminders-title">📊 Monthly Sales Performance</div>
        <div class="reminders-subtitle">Here is a breakdown of your sales metrics from January to {}</div>
        <div class="reminders-scroll-container">
            <div class="reminders-list">
    """.format(calendar.month_name[current_month])

    for month_num in range(1, current_month + 1):
        month_name = calendar.month_name[month_num]

        cursor.execute("""
            SELECT SUM(sd.total_amount) AS total_sales
            FROM sales_data sd
            WHERE sd.employee_id = %s 
              AND YEAR(sd.sale_date) = %s 
              AND MONTH(sd.sale_date) = %s
        """, (employee_id, current_year, month_num))
        total_sales = cursor.fetchone()['total_sales'] or 0

        cursor.execute("""
            SELECT SUM(target_amount) AS total_target
            FROM sales_targets
            WHERE employee_id = %s 
              AND YEAR(target_month) = %s 
              AND MONTH(target_month) = %s
        """, (employee_id, current_year, month_num))
        target_amount = cursor.fetchone()['total_target'] or 0

        target_percent = round((total_sales / target_amount) * 100, 2) if target_amount else 0
        if target_percent == 0:
            status_color = "status-red"
        elif target_percent < 75:
            status_color = "status-yellow"
        else:
            status_color = "status-green"

        cursor.execute("""
            SELECT COUNT(*) AS deals_closed
            FROM sales_data
            WHERE employee_id = %s
              AND YEAR(sale_date) = %s
              AND MONTH(sale_date) = %s
        """, (employee_id, current_year, month_num))
        deals_closed = cursor.fetchone()['deals_closed'] or 0

        cursor.execute("""
            SELECT COUNT(*) AS total_clients
            FROM clients
            WHERE assigned_to = %s
        """, (employee_id,))
        total_clients = cursor.fetchone()['total_clients'] or 1

        conversion_rate = round((deals_closed / total_clients) * 100, 2)

        html += f"""
        <div class='sales-card {status_color}'>
            <h4>📅 {month_name}</h4>
            <p>💰 <b>Total Sales:</b> €{total_sales:,.2f}</p>
            <p>🎯 <b>Target Achieved:</b> {target_percent}%</p>
            <p>🤝 <b>Deals Closed:</b> {deals_closed}</p>
            <p>📈 <b>Conversion Rate:</b> {conversion_rate}%</p>
        </div>
        """

    html += """
            </div>
        </div>
    </div>
    """

    sales_dropdown_html = generate_sales_action_dropdown().get("html", "")
    html += f"{sales_dropdown_html}"

    cursor.close()
    conn.close()

    return {"html": html}

def get_sales_clients_dropdown(employee_id=1):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT client_id, name, company
        FROM clients
        WHERE assigned_to = %s
        ORDER BY name ASC
    """, (employee_id,))
    clients = cursor.fetchall()
    conn.close()

    options = "\n".join(
        f'<option value="{c["client_id"]}">{c["name"]} – {c["company"]}</option>'
        for c in clients
    )

    html = f"""
    <div class="bot-message">
        <p><strong>👥 Client Stats</strong><br>
        Please select a client to view their statistics:</p>
        <select id="client-stats-select" class="dropdown-select">
            <option disabled selected>Select a client</option>
            {options}
        </select>
        <button onclick="fetchClientStats()" class="workflow-button disabled-button" disabled>🔍 View Stats</button>
    </div>
    """
    return {"html": html}

def get_client_sales_stats(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Date despre client
    cursor.execute("""
        SELECT name, company, status, interest_level, last_contact_date
        FROM clients
        WHERE client_id = %s
    """, (client_id,))
    client = cursor.fetchone()

    # Dealuri câștigate / pierdute / în desfășurare
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN deal_stage = 'Closed Won' THEN 1 ELSE 0 END) AS won,
            SUM(CASE WHEN deal_stage = 'Closed Lost' THEN 1 ELSE 0 END) AS lost,
            SUM(CASE WHEN deal_stage NOT IN ('Closed Won', 'Closed Lost') THEN 1 ELSE 0 END) AS pending
        FROM client_deals
        WHERE client_id = %s
    """, (client_id,))
    deals = cursor.fetchone()

    # Total vânzări generate
    cursor.execute("""
        SELECT SUM(total_amount) AS total_sales
        FROM sales_data
        WHERE client_id = %s
    """, (client_id,))
    sales = cursor.fetchone()
    total_sales = sales['total_sales'] or 0

    # Follow-up-uri active
    cursor.execute("""
        SELECT COUNT(*) AS pending_followups
        FROM followups
        WHERE client_id = %s AND status = 'Pending'
    """, (client_id,))
    followups = cursor.fetchone()

    conn.close()

    won = deals['won'] or 0
    pending = deals['pending'] or 0
    pending_followups = followups['pending_followups'] or 0

    recommendation = "✅ This client is performing well."
    if total_sales == 0 and won == 0:
        recommendation = "📌 Consider re-engaging this client — no activity detected."
    elif pending > 0 and pending_followups == 0:
        recommendation = "🔔 You might want to schedule a follow-up soon."

    # HTML final
    html = f"""
    <div class="client-details-card">
        <h3>👤 {client['name']} ({client['company']})</h3>
        <p><b>Status:</b> {client['status'].capitalize()}<br>
           <b>Interest Level:</b> {client['interest_level'].capitalize()}<br>
           <b>Last Contact:</b> {client['last_contact_date'] or 'N/A'}<br>
           <b>Deals:</b> ✅ {deals['won']} | ❌ {deals['lost']} | 🔄 {deals['pending']}<br>
           <b>Total Sales:</b> €{total_sales:,.2f}<br>
           <b>Active Follow-ups:</b> {followups['pending_followups']}
        </p>
        <div class="summary-card">{recommendation}</div>

        <div class="button-row-stats">
            <button class="workflow-button" data-action="client-stats-another">📈 Another Client</button>
            <button class="workflow-button" data-action="exit-sales">↩️ Exit</button>
        </div>

    </div>
    """
    return {"html": html}

def generate_sales_improvement_suggestions(employee_id):
    from datetime import datetime
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    current_year = datetime.now().year

    # Total sales
    cursor.execute("""
        SELECT SUM(sd.total_amount) AS total_sales
        FROM sales_data sd
        WHERE sd.employee_id = %s AND YEAR(sd.sale_date) = %s
    """, (employee_id, current_year))
    total_sales = cursor.fetchone()['total_sales'] or 0

    # Target
    cursor.execute("""
        SELECT SUM(target_amount) AS total_target
        FROM sales_targets
        WHERE employee_id = %s AND YEAR(target_month) = %s
    """, (employee_id, current_year))
    target_amount = cursor.fetchone()['total_target'] or 0
    target_percentage = round((total_sales / target_amount) * 100, 2) if target_amount else 0

    # Deals
    cursor.execute("""
        SELECT COUNT(*) AS deals_closed
        FROM client_deals cd
        JOIN clients c ON cd.client_id = c.client_id
        WHERE cd.deal_stage = 'Closed Won'
          AND YEAR(cd.close_date) = %s
          AND cd.client_id IN (
              SELECT client_id FROM sales_data WHERE employee_id = %s
          )
    """, (current_year, employee_id))
    deals_closed = cursor.fetchone()['deals_closed'] or 0

    cursor.execute("""
        SELECT COUNT(*) AS total_deals
        FROM client_deals
        WHERE client_id IN (
            SELECT client_id FROM sales_data WHERE employee_id = %s
        )
        AND YEAR(close_date) = %s
    """, (employee_id, current_year))
    total_deals = cursor.fetchone()['total_deals'] or 1
    conversion_rate = round((deals_closed / total_deals) * 100, 2)

    # Follow-ups
    cursor.execute("""
        SELECT COUNT(*) AS pending
        FROM followups
        WHERE status = 'Pending'
          AND client_id IN (
              SELECT client_id FROM sales_data WHERE employee_id = %s
          )
    """, (employee_id,))
    pending_followups = cursor.fetchone()['pending'] or 0

    conn.close()

    # Sugestii pe capitole
    summary = f"""
    <div class="bot-message">
        <p><strong>💡 Suggestions to Improve</strong></p>

        <br><p><strong>📈 Target Achievement:</strong><br>
        You’ve reached <strong>{target_percentage}%</strong> of your sales target this year.
        {"Performance is below expectations — a more aggressive outreach strategy is recommended." if target_percentage < 60 else "You're progressing well, but there’s still room to maximize your monthly targets."}</p>

        <br><p><strong>🤝 Conversion Rate:</strong><br>
        Your current rate is <strong>{conversion_rate}%</strong> based on {deals_closed} closed deals out of {total_deals}.
        {"This is a sign to revisit deal qualification criteria and pitch alignment." if conversion_rate < 25 else "Conversion looks healthy. Keep refining what works."}</p>

        <br><p><strong>🔁 Follow-Up Activity:</strong><br>
        You have <strong>{pending_followups}</strong> pending follow-ups.
        {"Consider prioritizing these clients immediately — neglected follow-ups often result in lost opportunities." if pending_followups > 5 else "Follow-up load is manageable. Maintain timely communication."}</p>

        <br><p><strong>🧭 Final Recommendation:</strong><br>
        Focus your efforts where improvement is most needed, while reinforcing the areas where performance is strong. Consistent follow-up, lead scoring, and monthly target reviews can elevate your outcomes significantly.</p>
    </div>
    """

    # Adaugăm dropdownul final cu acțiuni
    actions_dropdown = generate_sales_action_dropdown()["html"]
    return {"html": summary + actions_dropdown}
















def generate_sales_action_dropdown():
    return {
        "html": """
            <div class="reminders-followup-container">
                <p><br><b>Would you like to take another action related to Sales?</b><br>
                Please choose one below 👇</p>
                <select id="sales-action-select" class="dropdown-select">
                    <option value="" disabled selected>Choose an action</option>
                    <option value="view-monthly-breakdown">📊 View Monthly Breakdown</option>
                    <option value="client-stats">👥 Client Stats</option>
                    <option value="improve-suggestions">💡 Suggestions to Improve</option>
                    <option value="exit-sales-report">🚪 Exit and return to main menu</option>
                </select>
            </div>
        """
    }


