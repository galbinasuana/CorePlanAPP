from flask import Flask, render_template, request, jsonify
from chatbot.handlers import appointment_handler
from chatbot.handlers.appointment_handler import generate_appointment_form_html, handle_add_appointment, \
    handle_view_today, get_followup_options_html
from chatbot.handlers.client_handler import (handle_client_request, get_clients_dropdown, view_client_details, generate_client_followup_message, get_clients_update_dropdown,
                                            get_update_form, update_client, get_add_prospect_form, add_new_prospect, get_clients_delete_dropdown, confirm_delete_client, ask_delete_confirmation)
from chatbot.handlers.other_tools_handler import get_tools_intro, get_focus_mode_intro, get_focus_mode_timer_html, \
    generate_focus_mode_followup_message, get_email_generator_form, get_email_template, generate_email_preview, \
    send_email
from chatbot.handlers.reminders_handler import (handle_reminder_request, handle_view_followups, handle_mark_completion_list, mark_followup_as_completed, generate_followup_summary,
                                                get_add_followup_form, save_followup_logic, get_set_reminder_ui, get_manual_reminder_prompt, generate_reminder_followup_message,
                                                set_one_day_reminder, generate_manual_reminder_response)
from chatbot.handlers.report_handler import handle_sales_report_request, handle_monthly_sales_breakdown, get_sales_clients_dropdown, get_client_sales_stats, generate_sales_action_dropdown, generate_sales_improvement_suggestions
from chatbot.handlers.notes_handler import get_notes_intro, view_notes, generate_add_note_form, handle_save_note, \
    handle_edit_note_intro, generate_edit_note_form, handle_update_note, handle_delete_note_confirm, \
    handle_delete_note_final, handle_delete_note_cancel
from data.db import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    if "schedule" in user_message.lower():
        response = "Sure! Would you like to add, view, or reschedule an appointment?"
    elif "hello" in user_message.lower():
        response = "Hello! How can I assist you today?"
    else:
        response = f"Received: {user_message}. (test response)"

    return jsonify({'response': response})

deid = int(os.getenv("EMPLOYEE_ID"))

@app.route("/section/workflow")
def section_workflow():
    return jsonify(appointment_handler.handle_appointment_request())

@app.route("/workflow/view_today")
def view_today():
    return jsonify({"html": handle_view_today()})

@app.route("/workflow/delete")
def view_delete_appointments():
    return jsonify(appointment_handler.handle_delete_appointment_form())

@app.route("/workflow/delete_confirm", methods=["POST"])
def delete_appointment_confirm():
    data = request.get_json()
    appt_id = data.get("appointment_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM appointments WHERE appointment_id = %s AND employee_id = %s", (appt_id, deid))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "✅ Appointment successfully deleted.",
        "html": get_followup_options_html()
    })


@app.route("/workflow/date", methods=["POST"])
def get_schedule_for_date():
    from chatbot.handlers.appointment_handler import handle_schedule_for_date
    from flask import request

    data = request.get_json()
    selected_date = data.get("date")

    return jsonify(handle_schedule_for_date(selected_date))

@app.route("/workflow/add_form")
def add_appointment_form():
    html = generate_appointment_form_html()
    return jsonify({"html": html})

@app.route("/workflow/add_appointment", methods=["POST"])
def add_appointment():
    data = request.get_json()
    return jsonify(handle_add_appointment(data))




# CLIENTS
@app.route("/section/clients")
def section_clients():
    return jsonify(handle_client_request())

@app.route("/client/view-dropdown")
def client_view_dropdown():
    return jsonify(get_clients_dropdown())

@app.route("/client/view/<int:client_id>")
def view_client_by_id(client_id):
    return jsonify(view_client_details(client_id))

@app.route("/clients/followup")
def client_followup():
    return jsonify(generate_client_followup_message())

@app.route("/clients/dropdown", methods=["GET"])
def show_clients_dropdown():
    return jsonify(get_clients_dropdown())

@app.route("/clients/update-dropdown")
def update_dropdown():
    return jsonify(get_clients_update_dropdown())

@app.route("/clients/update-form/<int:client_id>")
def update_form(client_id):
    return jsonify(get_update_form(client_id))

@app.route("/clients/update-save", methods=["POST"])
def update_save():
    data = request.get_json()
    return jsonify(update_client(data))

@app.route("/clients/add-form")
def add_prospect_form():
    return jsonify(get_add_prospect_form())

@app.route("/clients/add-save", methods=["POST"])
def add_save():
    data = request.get_json()
    return jsonify(add_new_prospect(data))

@app.route("/clients/delete-dropdown")
def delete_dropdown():
    return jsonify(get_clients_delete_dropdown())

@app.route("/clients/delete/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    return jsonify(confirm_delete_client(client_id))

@app.route("/clients/delete-confirm/<int:client_id>")
def delete_confirm(client_id):
    return jsonify(ask_delete_confirmation(client_id))



# SMART REMINDERS
@app.route("/section/reminders")
def section_reminders():
    return jsonify(handle_reminder_request())

@app.route("/reminders/view")
def reminders_view():
    return jsonify(handle_view_followups())

@app.route("/reminders/mark")
def reminders_mark():
    return jsonify(handle_mark_completion_list())

@app.route("/reminders/mark/confirm", methods=["POST"])
def confirm_mark_completed():
    data = request.get_json()
    return jsonify(mark_followup_as_completed(data.get("followup_id")))

@app.route("/reminders/add")
def add_followup_form():
    return jsonify(get_add_followup_form())

@app.route("/reminders/save", methods=["POST"])
def save_followup():
    data = request.get_json()
    date = data.get("date")
    client_id = data.get("client_id")
    purpose = data.get("purpose")

    result = save_followup_logic(date, client_id, purpose)
    return jsonify(result)

@app.route("/reminders/set", methods=["GET"])
def show_set_reminder():
    result = get_set_reminder_ui()
    return jsonify(result)

@app.route("/reminders/skip", methods=["POST"])
def skip_reminder():
    response = get_manual_reminder_prompt()
    return jsonify(response)

@app.route('/chatbot/exit_reminders')
def exit_reminders():
    return jsonify(generate_reminder_followup_message())

@app.route("/chatbot/set_reminder_one_day", methods=["POST"])
def handle_set_one_day_reminder():
    data = request.get_json()
    followup_id = data.get("followup_id")

    if not followup_id:
        return jsonify({"html": "❗ Missing follow-up ID.", "status": "error"})

    return jsonify(set_one_day_reminder(followup_id))

@app.route("/chatbot/set_manual_reminder", methods=["POST"])
def set_manual_reminder():
    data = request.get_json()
    followup_id = data.get("followup_id")
    days_before = data.get("days_before")

    if not followup_id or not days_before:
        return jsonify({"html": "❗ Missing follow-up ID or reminder days."}), 400

    html = generate_manual_reminder_response(followup_id, days_before)
    return jsonify({"html": html})

@app.route('/reminders/summary', methods=['GET', 'POST'])
def reminders_summary():
    return jsonify(generate_followup_summary())



# SALES REPORTS
@app.route("/sales-reports", methods=["POST"])
def sales_reports():
    #data = request.get_json()
    # employee_id = data.get("employee_id")
    employee_id = 1
    result = handle_sales_report_request(employee_id)
    return jsonify(result)

@app.route("/monthly-breakdown", methods=["POST"])
def monthly_breakdown():
    data = request.get_json()
    employee_id = data.get("employee_id", 1)
    result = handle_monthly_sales_breakdown(employee_id)
    return jsonify(result)

@app.route("/sales/client-stats-dropdown", methods=["GET"])
def sales_clients_dropdown():
    try:
        result = get_sales_clients_dropdown(employee_id=1)  # TODO: Din sesiune în viitor
        return jsonify(result)
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Error loading client list: {e}</div>"})

@app.route("/sales/client-stats/<int:client_id>", methods=["GET"])
def sales_client_stats(client_id):
    try:
        result = get_client_sales_stats(client_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Error loading client stats: {e}</div>"})

@app.route("/sales/exit", methods=["GET"])
def sales_exit():
    try:
        result = generate_sales_action_dropdown()
        return jsonify(result)
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Error returning to sales menu: {e}</div>"})

@app.route("/sales/improve-suggestions", methods=["POST"])
def improve_suggestions():
    data = request.get_json()
    employee_id = data.get("employee_id", 1)

    try:
        result = generate_sales_improvement_suggestions(employee_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Error generating suggestions: {e}</div>"})


# INTERACTION NOTES
@app.route("/section/notes", methods=["GET"])
def section_notes_intro():
    try:
        return jsonify(get_notes_intro())
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Failed to load Interaction Notes section: {e}</div>"})


@app.route("/section/notes/view", methods=["GET"])
def section_notes_view():
    try:
        return jsonify(view_notes())
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Failed to load meeting notes: {e}</div>"})

@app.route("/section/notes/add", methods=["GET"])
def section_notes_add():
    try:
        return jsonify(generate_add_note_form())
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Could not load add-note form: {e}</div>"})

@app.route("/section/notes/save", methods=["POST"])
def section_notes_save():
    try:
        return handle_save_note()
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Could not save the note: {e}</div>",
            "user_message": "❌ Failed to Save"
        })

@app.route("/section/notes/edit", methods=["GET"])
def section_notes_edit_intro():
    try:
        return handle_edit_note_intro()
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Failed to load edit-note options: {e}</div>",
            "user_message": "❌ Failed to Load Edit"
        })

@app.route("/section/notes/edit/form/<int:note_id>", methods=["GET"])
def section_notes_edit_form(note_id):
    try:
        return generate_edit_note_form(note_id)
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Failed to load note form: {e}</div>",
            "user_message": "❌ Failed to Load Note"
        })

@app.route("/section/notes/update", methods=["POST"])
def section_notes_update():
    try:
        return handle_update_note()
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Failed to update the note: {e}</div>",
            "user_message": "❌ Failed to Update"
        })

@app.route("/section/notes/delete", methods=["GET"])
def section_notes_delete_intro():
    try:
        from chatbot.handlers.notes_handler import handle_delete_note_intro
        return handle_delete_note_intro()
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Failed to load delete-note options: {e}</div>",
            "user_message": "❌ Failed to Load Delete Options"
        })

@app.route("/section/notes/delete/confirm/<int:note_id>", methods=["GET"])
def section_notes_delete_confirm(note_id):
    try:
        return handle_delete_note_confirm(note_id)
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Could not load delete confirmation: {e}</div>",
            "user_message": "❌ Confirm Delete Failed"
        })

@app.route("/section/notes/delete/final/<int:note_id>", methods=["DELETE"])
def section_notes_delete_final(note_id):
    try:
        return handle_delete_note_final(note_id)
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>❌ Failed to delete the note: {e}</div>",
            "user_message": "❌ Delete Failed"
        })

@app.route("/section/notes/delete/cancel", methods=["GET"])
def section_notes_delete_cancel():
    try:
        return handle_delete_note_cancel()
    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>⚠️ Cancel action failed: {e}</div>",
            "user_message": "❌ Cancel Failed"
        })

# OTHER TOOLS
@app.route("/section/tools", methods=["GET"])
def section_other_tools():
    try:
        return jsonify(get_tools_intro())
    except Exception as e:
        return jsonify({"html": f"<div class='bot-message error'>⚠️ Failed to load Other Tools section: {e}</div>"})

@app.route("/section/tools/focus-mode/start", methods=["GET"])
def focus_mode_intro():
    return jsonify(get_focus_mode_intro())

@app.route("/section/tools/focus-mode/timer", methods=["POST"])
def focus_mode_timer():
    data = request.json
    focus_duration = int(data.get("focus_duration", 25))
    return jsonify(get_focus_mode_timer_html(focus_duration))

@app.route("/section/tools/message-generator", methods=["GET"])
def message_generator_channel():
    return jsonify(get_email_generator_form())

@app.route("/section/tools/message-generator/generate", methods=["POST"])
def generate_client_email():
    data = request.json

    client_name = data.get("client_name", "").strip()
    message_type = data.get("message_type", "").strip()
    tone = data.get("emotion_tone", "").strip()
    context = data.get("message_context", "").strip()
    extra_info = data.get("extra_info", "").strip()
    subject = data.get("subject", "").strip()

    template = get_email_template(message_type, tone, context)
    if not template:
        return jsonify({"error": "No suitable template found."}), 400

    body = template.format(name=client_name).replace('\n', '<br>')
    full_email = f"""
    <b>Subject:</b> {subject or '(no subject)'}<br><br>
    {body}
    {f"<br><br><i>{extra_info}</i>" if extra_info else ""}
    <br><br>
    —
    <br>CorePlan Sales Team
    """.strip()

    preview = generate_email_preview(full_email)
    return jsonify({"email_html": preview})


@app.route("/section/tools/message-generator/send", methods=["POST"])
def send_generated_email():
    data = request.json
    to_email = data.get("client_email")
    subject = data.get("subject")
    body_html = data.get("body_html")

    if not to_email or not subject or not body_html:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    success = send_email(to_email, subject, body_html)

    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Failed to send email"}), 500


@app.route("/section/tools/focus-mode/followup")
def focus_mode_followup():
    return jsonify(generate_focus_mode_followup_message())




# EXIT SECTION
@app.route("/main-menu")
def main_menu():
    html = """
        <div style="background-color: #f4f7fe; padding: 12px 16px; border-radius: 10px; width: fit-content; max-width: 100%%; font-size: 15px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);">
            <strong>All set! ✅</strong><br>
            What would you like to do next? 👇<br>
            <select class="dropdown-select followup-select" style="margin-top: 10px; padding: 8px 12px; border-radius: 8px; border: 1px solid #ccc; font-size: 15px;">
                <option selected disabled>Choose an action</option>
                <option value="clients">👥 Client Management</option>
                <option value="reminders">🔁 Smart Reminders</option>
                <option value="reports">📈 Sales Reports</option>
                <option value="notes">🧾 Notes & Follow-up</option>
                <option value="extras">🛠️ Other Tools</option>
                <option value="exit">📕 Exit</option>
            </select>
        </div>
    """
    return jsonify({"html": html})

@app.route("/exit")
def exit_chat():
    html = """
        <div class="final-message">
            <p>👋 That’s all for now. If you need anything else, I’m just one click away.<br>
            Wishing you a <b>productive</b>, <b>focused</b>, and <b>successful</b> day ahead!</p>
            <div class="bot-options center-options" style="margin-top: 14px;">
                <button class="option-button primary" id="start-new-chat">🔄 Start a New Conversation</button>
            </div>
        </div>
    """
    return jsonify({"html": html})



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

