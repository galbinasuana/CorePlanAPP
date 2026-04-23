import random
from data.db import get_db_connection
from datetime import datetime, timedelta, date

def handle_reminder_request():
    """
    Returnează mesajul principal pentru secțiunea Smart Reminders.
    Include introducere profesională și butoane de acțiune.
    """
    return {
        "html": """
            <div class="workflow-intro">
                <h3>🔁 Smart Reminders</h3>
                <p>
                    Welcome to your Smart Reminders dashboard.<br>
                    Here you can manage your follow-ups, track progress and set automated alerts.
                </p>

                <p>📆 <b>View Follow-ups:</b> See upcoming tasks and scheduled check-ins.</p>
                <p>✅ <b>Mark Completed:</b> Mark follow-ups as done when completed.</p>
                <p>➕ <b>Add Follow-up:</b> Schedule a new task or contact point.</p>
                <p>🔔 <b>Set Reminders:</b> Enable alerts to stay on track.</p>
                <p>📊 <b>Summary:</b> Get an overview of your pending and completed follow-ups.</p>
                <br>
                <p><b>What would you like to do next?</b></p>
            </div>

            <div class="bot-options center-options">
                <button class="workflow-button" data-action="view-followups">
                    <span class="emoji">📆</span> View Follow-ups
                </button>
                <button class="workflow-button" data-action="mark-followup-completed">
                    <span class="emoji">✅</span> Mark Completed
                </button>
                <button class="workflow-button" data-action="add-followup">
                    <span class="emoji">➕</span> Add Follow-up
                </button>
                <button class="workflow-button" data-action="set-reminder">
                    <span class="emoji">🔔</span> Set Reminders
                </button>
                <button class="workflow-button" data-action="followup-summary">
                    <span class="emoji">📊</span> Follow-up Summary
                </button>
            </div>
        """,
        "status": "success"
    }

def handle_view_followups():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.purpose, f.followup_date, f.client_id, c.name AS client_name, c.company
        FROM followups f
        LEFT JOIN clients c ON f.client_id = c.client_id
        WHERE f.status = 'Pending'
        ORDER BY f.followup_date
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        return {
            "html": """
                <div class="reminders-card-message">
                    <h4>📭 No Pending Follow-ups</h4>
                    <p>You currently have no scheduled follow-up tasks. You're all caught up! ✅</p>
                </div>
            """,
            "status": "empty"
        }

    rows = ""
    for row in results:
        date_str = row['followup_date'].strftime("%B %d, %Y") if isinstance(row['followup_date'], datetime) else row['followup_date']
        client = row.get('client_name', 'Unknown')
        company = row.get('company', '-')
        rows += f"""
            <div class="reminders-item">
                <p>📌 <b>{row['purpose']}</b></p>
                <p>👤 Client: <i>{client}</i> from <b>{company}</b></p>
                <p>📅 Scheduled: <b>{date_str}</b></p>
            </div>
            <hr class="reminders-divider">
        """

    html = f"""
        <div class="reminders-card-message">
            <div class="reminders-title">📆 Upcoming Follow-ups</div>
            <div class="reminders-subtitle">Here is a list of all your scheduled follow-up tasks:</div>
            <div class="reminders-scroll-container">
                <div class="reminders-list">
                    {rows}
                </div>
            </div>
        </div>
    """

    followup_select_html = generate_reminder_followup_message()["html"]

    return {
        "html": html + followup_select_html,
        "status": "success"
    }

def handle_mark_completion_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # ← asta e cheia!

    cursor.execute("""
        SELECT f.followup_id, f.purpose, f.followup_date, c.name, c.company
        FROM followups f
        JOIN clients c ON f.client_id = c.client_id
        WHERE f.status = 'Pending'
        ORDER BY f.followup_date ASC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        return {
            "html": "<div class='no-followups'>No pending follow-ups found. 🎉</div>"
        }

    options_html = ""
    for row in results:
        fid = row["followup_id"]
        title = row["purpose"]
        date = row["followup_date"]
        client = row["name"]
        company = row["company"]

        label = f'📌 {title} – 👤 {client} @ 🏢 {company} – 📅 {date.strftime("%Y-%m-%d")}'
        options_html += f"<option value='{fid}'>{label}</option>"

    html = f"""
    <div class="reminders-mark-container">
        <div class="reminders-mark-intro">
            📝 Select a follow-up to mark as completed:
        </div>
        <select id="followup-complete-select" class="followup-dropdown">
            <option value="">— Select a follow-up —</option>
            {options_html}
        </select>
        <button id="confirm-complete-btn" class="workflow-button" data-action="confirm-followup-completion" disabled>
            ✅ Confirm Completion
        </button>
    </div>
    """

    return { "html": html }


def mark_followup_as_completed(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT purpose FROM followups WHERE followup_id = %s", (followup_id,))
        row = cursor.fetchone()
        task_title = row["purpose"] if row else "This task"

        cursor.execute("UPDATE followups SET status = 'Completed' WHERE followup_id = %s", (followup_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # ✅ Apelează funcția și extrage direct HTML-ul
        followup_html = generate_reminder_followup_message().get("html", "")

        return {
            "html": f"""
                <div class="reminders-mark-success">
                    ✅ The follow-up "<b>{task_title}</b>" has been successfully marked as <b>Completed</b>!<br><br>
                    Great job keeping everything on track. 🚀
                </div>
                {followup_html}
            """
        }

    except Exception as e:
        return {
            "html": f"<div class='error-message'>❌ An error occurred: {str(e)}</div>"
        }

def get_add_followup_form():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT client_id, name, company FROM clients ORDER BY name ASC")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    options_html = ""
    for c in clients:
        label = f"{c['name']} ({c['company']})" if c['company'] else c['name']
        options_html += f"<option value='{c['client_id']}'>{label}</option>"

    today = date.today().isoformat()

    html = f"""
        <div class="followup-form" style="display: flex; flex-direction: column; gap: 2px;">
            <h4 style="margin-bottom: 8px;">📌 Schedule a New Follow-up</h4>
             <p style="margin-bottom: 20px;">Please complete the form below:</p>

            <label for="followup-date">📅 Follow-up Date:</label>
            <input type="date" id="followup-date" min="{today}" />

            <label for="followup-client">👤 Client:</label>
            <select id="followup-client" class="form-field" required>
                <option value="" selected disabled>Select client</option>
                {options_html}
            </select>

            <label for="followup-purpose">📌 Purpose:</label>
            <input type="text" id="followup-purpose" class="form-field" placeholder="e.g. Send proposal" required>

            <br><button id="save-followup-btn" class="workflow-button" disabled>💾 Save Follow-up</button>
        </div>
    """

    return {"html": html}

def save_followup_logic(date, client_id, purpose):
    if not all([date, client_id, purpose]):
        return {
            "html": "❗ Missing data. Please fill all fields.",
            "status": "error"
        }

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, company FROM clients WHERE client_id = %s", (client_id,))
    client_row = cursor.fetchone()
    client_name = client_row['name']
    company = client_row['company'] or "Independent"

    status = "Pending"
    reminder_days_before = random.randint(0, 7)  # valoare random între 0 și 7
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO followups (client_id, followup_date, purpose, status, reminder_days_before, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (client_id, date, purpose, status, reminder_days_before, now, now))
    conn.commit()

    cursor.close()
    conn.close()

    confirmation = f"""
        <div class="chatbot-message success">
            ✅ <b>Follow-up saved successfully!</b><br><br>

            <p>📌 <b>{purpose}</b></p>
            <p>👤 Client: <i>{client_name}</i> from <b>{company}</b></p>
            <p>📅 Scheduled: <b>{date}</b></p>
            <p>⏰ Reminder set for <b>{reminder_days_before} day(s)</b> before</p>
        </div>
    """

    followup_dropdown = generate_reminder_followup_message()["html"]

    return {
        "html": confirmation + followup_dropdown,
        "status": "success"
    }

def get_set_reminder_ui():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT f.followup_id, f.purpose, f.followup_date, c.name AS client_name, c.company
        FROM followups f
        JOIN clients c ON f.client_id = c.client_id
        WHERE f.followup_date BETWEEN CURDATE() + INTERVAL 2 DAY AND CURDATE() + INTERVAL 7 DAY
          AND f.reminder_days_before = 0
          AND f.status = 'Pending'
    """)
    rows = cursor.fetchall()

    if rows:
        row = rows[0]
        html = f"""
            <div class="chatbot-message warning">
                🔔 <b>Reminder not set!</b><br><br>
                You have a follow-up scheduled soon, but no reminder is set. Would you like to set one now to stay on track?<br><br>
                📌 <b>{row['purpose']}</b><br>
                👤 Client: <i>{row['client_name']}</i> from <b>{row['company']}</b><br>
                📅 Scheduled: <b>{row['followup_date']}</b><br><br>

                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button class="workflow-button" data-action="confirm-reminder" data-id="{row['followup_id']}">✅ Set 1-day reminder</button>
                    <button class="workflow-button" data-action="skip-reminder">❌ Skip this time</button>
                </div>
            </div>
        """
    else:
        two_days_later = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT f.followup_id, f.purpose, f.followup_date
            FROM followups f
            WHERE f.followup_date >= %s 
              AND f.reminder_days_before = 0 
              AND f.status = 'Pending'
            ORDER BY f.followup_date ASC
        """, (two_days_later,))

        options = cursor.fetchall()
        if options:
            options_html = "\n".join([
                f'<option value="{opt["followup_id"]}">{opt["purpose"]} – {opt["followup_date"]}</option>' for opt in
                options
            ])
            html = f"""
                <div class="chatbot-message">
                    ⏰ <b>Set a reminder for one of your upcoming follow-ups:</b><br><br>
                    Select a follow-up and the number of days in advance you'd like to be reminded.<br><br>

                    <select id="manual-reminder-select" class="dropdown-select">
                        <option disabled selected>Choose a follow-up</option>
                        {options_html}
                    </select><br><br>

                    <label for="reminder-days">Remind me:</label>
                    <select id="reminder-days" class="dropdown-select">
                        {''.join([f'<option value="{i}">{i} day(s) before</option>' for i in range(1, 8)])}
                    </select><br><br>

                    <div style="display: flex; gap: 10px;">
                        <button id="set-reminder-btn" class="workflow-button" data-action="confirm-manual-reminder" disabled>💾 Set Reminder</button>
                        <button class="workflow-button" data-action="exit-reminders">↩️ Exit</button>
                    </div>
                </div>
            """
        else:
            html = "<div class='chatbot-message'>✅ All upcoming follow-ups already have reminders set.</div>"

    cursor.close()
    conn.close()

    return { "html": html, "status": "success" }

def get_manual_reminder_prompt():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    two_days_later = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT f.followup_id, f.purpose, f.followup_date
        FROM followups f
        WHERE f.followup_date >= %s
          AND f.reminder_days_before = 0 
          AND f.status = 'Pending'
    """, (two_days_later,))

    options = cursor.fetchall()

    if options:
        options_html = "\n".join([
            f'<option value="{opt["followup_id"]}">{opt["purpose"]} – {opt["followup_date"]}</option>' for opt in options
        ])
        html = f"""
            <div class="chatbot-message">
                ⏰ <b>Would you like to set a reminder for another follow-up?</b><br><br>
                Select a follow-up and the number of days in advance you'd like to be reminded.<br>

                <select id="manual-reminder-select" class="dropdown-select">
                    <option disabled selected>Choose a follow-up</option>
                    {options_html}
                </select><br><br>

                <label for="reminder-days">Remind me:</label>
                <select id="reminder-days" class="dropdown-select">
                    {''.join([f'<option value="{i}">{i} day(s) before</option>' for i in range(1, 8)])}
                </select><br><br>

                <div style="display: flex; gap: 10px;">
                    <button id="set-reminder-btn" class="workflow-button" data-action="confirm-manual-reminder" disabled>💾 Set Reminder</button>
                    <button class="workflow-button" data-action="exit-reminders">↩️ Exit</button>
                </div>
            </div>
        """
    else:
        html = "<div class='chatbot-message'>✅ All upcoming follow-ups already have reminders set.</div>"

    cursor.close()
    conn.close()

    return {"html": html, "status": "success"}

def set_one_day_reminder(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE followups
        SET reminder_days_before = 1
        WHERE followup_id = %s
    """, (followup_id,))
    conn.commit()

    cursor.execute("""
        SELECT f.purpose, f.followup_date, c.name AS client_name, c.company
        FROM followups f
        JOIN clients c ON f.client_id = c.client_id
        WHERE f.followup_id = %s
    """, (followup_id,))
    row = cursor.fetchone()

    date_str = datetime.strptime(str(row['followup_date']), "%Y-%m-%d").strftime("%A, %B %d")

    confirmation = f"""
        <div class="chatbot-message success">
            ✅ <b>1-day reminder set successfully!</b><br><br>
            <p>📌 <b>{row['purpose']}</b></p>
            <p>👤 Client: <i>{row['client_name']}</i> from <b>{row['company']}</b></p>
            <p>📅 Scheduled: <b>{date_str}</b></p>
        </div>
    """

    next_prompt = get_manual_reminder_prompt()["html"]

    cursor.close()
    conn.close()

    return {
        "html": confirmation + next_prompt,
        "status": "success"
    }

def generate_manual_reminder_response(followup_id, days_before):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Update reminder
    cursor.execute("""
        UPDATE followups
        SET reminder_days_before = %s
        WHERE followup_id = %s
    """, (days_before, followup_id))
    conn.commit()

    # 2. Get updated data
    cursor.execute("""
        SELECT f.purpose, f.followup_date, c.name AS client_name, c.company, f.reminder_days_before
        FROM followups f
        JOIN clients c ON f.client_id = c.client_id
        WHERE f.followup_id = %s
    """, (followup_id,))
    followup = cursor.fetchone()

    cursor.close()
    conn.close()

    if not followup:
        return "<div class='chatbot-message'>❗ Follow-up not found.</div>"

    # Format date
    try:
        date_obj = datetime.strptime(str(followup['followup_date']), "%Y-%m-%d")
        date_str = date_obj.strftime("%B %d, %Y")
    except:
        date_str = followup['followup_date']

    # 3. Build HTML
    html = f"""
        <div class="chatbot-message">
            ✅ <b>Reminder set successfully!</b><br><br>
            <b>Updated Follow-up Details:</b><br>
            <p>📌 <b>{followup['purpose']}</b></p>
            <p>👤 Client: <i>{followup['client_name']}</i> from <b>{followup['company']}</b></p>
            <p>📅 Scheduled: <b>{date_str}</b></p>
            <p>⏰ Reminder: <b>{followup['reminder_days_before']} day(s) before</b></p>
            <br>
    """

    html += get_manual_reminder_prompt()["html"]
    html += "</div>"

    return html






def generate_followup_summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM followups")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS pending FROM followups WHERE status = 'Pending'")
    pending = cursor.fetchone()["pending"]

    cursor.execute("SELECT COUNT(*) AS completed FROM followups WHERE status = 'Completed'")
    completed = cursor.fetchone()["completed"]

    completion_rate = int((completed / total) * 100) if total > 0 else 0

    cursor.execute("""
        SELECT f.purpose, f.followup_date, c.name
        FROM followups f
        JOIN clients c ON f.client_id = c.client_id
        WHERE f.status = 'Pending'
        ORDER BY f.followup_date ASC
        LIMIT 3
    """)
    upcoming = cursor.fetchall()

    cursor.close()
    conn.close()

    upcoming_html = ""
    for item in upcoming:
        date_str = item["followup_date"].strftime("%Y-%m-%d")
        upcoming_html += f"""
            <div class='followup-item'>
                📅 <strong>{date_str}</strong> – {item['purpose']} for <em>{item['name']}</em>
            </div>
        """

    followup_html = generate_reminder_followup_message().get("html", "")

    html = f"""
        <div class="followup-summary-box">
            <h3>📊 <strong>Follow-up Summary</strong></h3> <br>
            <p><strong>Total follow-ups:</strong> {total}</p>
            <p>⏳ <strong>Pending:</strong> {pending}</p>
            <p>✅ <strong>Completed:</strong> {completed}</p><br>
            <div class="progress-bar">
                <div class="progress" style="width: {completion_rate}%"></div>
            </div>
            <p><strong>Completion Rate:</strong> {completion_rate}%</p> <br>
            <p><b>📌 Upcoming follow-ups:</b></p>
            {upcoming_html}
            {followup_html}
        </div>
    """

    return {"html": html}

def generate_reminder_followup_message():
    return {
        "html": """
            <div class="reminders-followup-container">
                <p><br><b>Would you like to take another action related to follow-ups?</b><br>
                Please choose one below 👇</p>
                <select id="reminder-followup-select" class="dropdown-select">
                    <option value="" disabled selected>Choose an action</option>
                    <option value="view-followups">📆 View Follow-ups</option>
                    <option value="mark-followup-completed">✅ Mark Completed</option>
                    <option value="add-followup">➕ Add Follow-up</option>
                    <option value="set-reminder">🔔 Set Reminders</option>
                    <option value="followup-summary">📊 Follow-up Summary</option>
                    <option value="exit-reminders">🚪 Exit and return to main menu</option>
                </select>
            </div>
        """,
        "status": "followup"
    }

