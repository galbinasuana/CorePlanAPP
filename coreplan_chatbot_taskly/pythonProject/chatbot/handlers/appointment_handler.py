from datetime import datetime, timedelta, time
from data.db import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

def handle_appointment_request():
    """
    Returns the main HTML message for the Daily Workflow section.
    Includes a professional introduction and action buttons.
    """
    return {
        "html": """
        <div class="workflow-intro">
            <h3>🧭 Daily Workflow</h3>
            <p>
                Welcome to your <b>daily productivity command center</b>.<br>
                From here, you can <b>schedule new appointments</b>, check what’s next on your calendar,
                <b>reschedule meetings</b> on the fly, or <b>clean up completed tasks</b> — all in just a few clicks.
            </p>
            <p>
                <br>
                <b>What would you like to do right now?</b>
            </p>
        </div>

        <div class="bot-options center-options">
            <button class="workflow-button" data-action="add">
                <span class="emoji">📅</span> Add Appointment
            </button>
            <button class="workflow-button" data-action="view">
                <span class="emoji">📖</span> View Today
            </button>
            <button class="workflow-button" data-action="reschedule">
                <span class="emoji">🔁</span> Reschedule
            </button>
            <button class="workflow-button" data-action="delete">
                <span class="emoji">❌</span> Delete
            </button>
        </div>
        """
    }
deid = int(os.getenv("EMPLOYEE_ID"))
def format_time(t):
    if isinstance(t, timedelta):
        total_seconds = int(t.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}"
    elif hasattr(t, "strftime"):
        return t.strftime("%I:%M %p")  # AM/PM
    return str(t)


def handle_view_today():
    conn = get_db_connection()
    cursor = conn.cursor()

    today = datetime.today().date()

    cursor.execute("""
        SELECT title, location, start_time, end_time
        FROM appointments
        WHERE employee_id = %s AND appointment_date = %s
        ORDER BY start_time ASC
    """, (deid, today))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "<i>📭 No appointments scheduled for today.</i>"

    html = "<div class='appointment-list'>"
    for title, location, start_time, end_time in rows:
        html += f"""
            <div class="appointment-item">
                <div><b>{title}</b></div>
                <div>📍 {location}</div>
                <div>🕒 {format_time(start_time)} – {format_time(end_time)}</div><br>
            </div>
        """
    html += "</div>"
    html += get_followup_options_html()
    return html



def handle_schedule_for_date( date_str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, location, start_time, end_time
        FROM appointments
        WHERE employee_id = %s AND appointment_date = %s
        ORDER BY start_time ASC
    """, (deid, date_str))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "<i>📭 No appointments scheduled for that day.</i>"

    html = "<div class='appointment-list'>"
    for title, location, start_time, end_time in rows:
        html += f"""
            <div class="appointment-item">
                <div><b>{title}</b></div>
                <div>📍 {location}</div>
                <div>🕒 {start_time.strftime('%H:%M')} – {end_time.strftime('%H:%M')}</div>
            </div>
        """
    html += "</div>"
    return html



def generate_appointment_form_html(date="", start="", end="", title="", location=""):
    today_str = datetime.today().strftime("%Y-%m-%d")

    if start:
        try:
            start = datetime.strptime(start, "%H:%M").strftime("%H:%M")
        except:
            pass
    if end:
        try:
            end = datetime.strptime(end, "%H:%M").strftime("%H:%M")
        except:
            pass

    html = f"""
            <form id="add-appointment-form" class="appointment-form">
                <label>Date:</label>
                <input type="date" id="appt-date" value="{date}" min="{today_str}">

                <label>Time:</label>
                <div class="time-row">
                    <input type="time" id="appt-start" value="{start}">
                    <span>–</span>
                    <input type="time" id="appt-end" value="{end}">
                </div>

                <label>Title:</label>
                <input type="text" id="appt-title" value="{title}" placeholder="e.g. Zoom">

                <label>Location:</label>
                <input type="text" id="appt-location" value="{location}" placeholder="e.g. Online">

                <button type="submit" class="workflow-button primary" id="add-appt-button">✅ Add Appointment</button>
            </form>
        """
    return html

from datetime import datetime
from data.db import get_db_connection  # dacă folosești un fișier separat pentru db


def handle_add_appointment(data):
    try:
        employee_id = deid
        client_id = int(data.get("client_id"))
        title = data.get("title", "").strip()
        appt_date = data.get("appointment_date", "").strip()
        start_time = data.get("start_time", "").strip()
        end_time = data.get("end_time", "").strip()
        location = data.get("location", "").strip()
        color_tag = data.get("color_tag", "blue").strip()

        if not all([employee_id, client_id, title, appt_date, start_time, end_time]):
            return {"status": "error", "message": "Missing required appointment fields."}

        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO appointments (
                employee_id, client_id, title, appointment_date,
                start_time, end_time, location, color_tag
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            employee_id, client_id, title, appt_date,
            start_time_obj, end_time_obj, location, color_tag
        ))

        conn.commit()
        conn.close()

        return {"status": "success", "message": "Appointment added successfully."}

    except Exception as e:
        print("Error in handle_add_appointment:", e)
        return {"status": "error", "message": "Failed to add appointment."}

def handle_delete_appointment_form():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT appointment_id, title, location, appointment_date, start_time, end_time
        FROM appointments
        WHERE employee_id = %s
        ORDER BY appointment_date, start_time
    """, (deid,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"html": "<i>📭 You have no scheduled appointments to delete.</i>" + get_followup_options_html()}

    options = ""
    for appt_id, title, loc, date, start, end in rows:
        label = f"{date.strftime('%Y-%m-%d')} • {title} • {format_time(start)} – {format_time(end)}"
        options += f'<option value="{appt_id}" data-summary="{label}" data-title="{title}">{label}</option>'

    html = f"""
        <div class="delete-container">
            <p><b>Select an appointment you want to cancel:</b></p>
            <select id="delete-appt-select" class="dropdown-select">
                <option disabled selected>Choose appointment</option>
                {options}
            </select>
            <br><br>
            <button id="confirm-delete-btn" class="workflow-button danger" disabled>❌ Delete Appointment</button>
            <div id="delete-confirmation-area"></div>
        </div>
    """
    return {"html": html}



def get_followup_options_html():
    return """
        <div class="followup-container">
            <p><b>Would you like to do anything else related to your schedule?</b><br>
            Please choose an option below 👇</p>

            <select id="followup-select" class="dropdown-select">
                <option value="" disabled selected>Choose an action</option>
                <option value="add">📅 Add Appointment</option>
                <option value="view">📖 View Today</option>
                <option value="reschedule">🔁 Reschedule</option>
                <option value="delete">❌ Cancel an appointment</option>
                <option value="exit">🚪 Exit and return to main menu</option>
            </select>
        </div>
    """
