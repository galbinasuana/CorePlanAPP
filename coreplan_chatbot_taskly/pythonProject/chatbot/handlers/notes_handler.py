from datetime import datetime, date
from data.db import get_db_connection

def get_notes_intro():
    return {
        "html": """
        <div class="reminders-followup-container" style="padding: 15px 20px;">
            <div class="bot-section-header" style="margin-bottom: 10px;">
                <h4 style="margin: 0; font-size: 18px;">📝 <b>Interaction Notes</b></h4>
            </div>

            <div class="bot-section-description" style="font-size: 14px; line-height: 1.6;">
                <p>Welcome to your <b>Interaction Notes</b> dashboard.<br>
                Here you can <span style="font-weight: 600;">log key meeting summaries</span>, track important discussions,
                and <span style="font-weight: 600;">review client interactions</span> for better follow-up.</p>
            </div>

            <ul class="feature-list" style="list-style: none; padding-left: 0; margin-top: 10px;">
                <li style="margin-bottom: 6px;">🔍 <b>View Notes:</b> Browse notes from past meetings.</li>
                <li style="margin-bottom: 6px;">➕ <b>Add Note:</b> Record details from a recent interaction.</li>
                <li style="margin-bottom: 6px;">✏️ <b>Edit Note:</b> Update an existing note if needed.</li>
                <li style="margin-bottom: 6px;">🗑️ <b>Delete Note:</b> Remove outdated or incorrect notes.</li>
            </ul>

            <p style="font-weight: 500; margin-top: 15px;">What would you like to do next?</p>

            <div class="bot-options bot-options-centered" style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 10px;">
                <button class="workflow-button" data-action="view-notes">🔍 View Notes</button>
                <button class="workflow-button" data-action="add-note">➕ Add Note</button>
                <button class="workflow-button" data-action="edit-note">✏️ Edit Note</button>
                <button class="workflow-button" data-action="delete-note">🗑️ Delete Note</button>
            </div>
        </div>
        """
    }

def get_meeting_notes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT note_id, date, participants, summary, meeting_type, created_at
        FROM meeting_notes
        WHERE employee_id = 1
        ORDER BY date DESC
        LIMIT 10
    """
    cursor.execute(query)
    notes = cursor.fetchall()

    cursor.close()
    conn.close()
    return notes

def view_notes():
    notes = get_meeting_notes()

    if not notes:
        return {
            "html": """
                <div class="reminders-card-message">
                    <h4>📭 No Meeting Notes Found</h4>
                    <p>You currently have no recorded meeting notes. 📝</p>
                </div>
            """,
            "status": "empty"
        }

    rows = ""
    for note in notes:
        date_str = note['date'].strftime("%B %d, %Y") if isinstance(note['date'], datetime) else note['date']
        created_at_str = note['created_at'].strftime("%B %d, %Y %H:%M") if isinstance(note['created_at'], datetime) else note['created_at']
        rows += f"""
            <div class="reminders-item">
                <p>📅 <b>{date_str}</b> — <i>{note['meeting_type'].capitalize()}</i></p>
                <p>👥 Participants: <b>{note['participants']}</b></p>
                <p>📝 Summary: <span>{note['summary']}</span></p>
                <p>🕓 Logged at: <small>{created_at_str}</small></p>
            </div>
            <hr class="reminders-divider">
        """

    html = f"""
        <div class="reminders-card-message">
            <div class="reminders-title">📝 Recent Meeting Notes</div>
            <div class="reminders-subtitle">Here are the most recent interaction notes from meetings:</div>
            <div class="reminders-scroll-container">
                <div class="reminders-list">
                    {rows}
                </div>
            </div>
        </div>
    """

    html += generate_notes_followup_message()["html"]

    return {
        "html": html,
        "status": "success"
    }


def generate_add_note_form():
    today = date.today().isoformat()

    # Obține toți clienții direct aici
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT client_id, name FROM clients ORDER BY name")
    clients = cursor.fetchall()

    cursor.execute("SELECT employee_id, CONCAT(first_name, ' ', last_name) AS name  FROM employees WHERE department_id = 3 ORDER BY name")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    client_options = '<option value="" disabled selected hidden>-- Select Client --</option>' + "".join([
        f'<option value="{client["client_id"]}">{client["name"]}</option>'
        for client in clients
    ])

    employee_options = "".join([
        f'<option value="{emp["employee_id"]}">{emp["name"]}</option>' for emp in employees
    ])

    return {
        "html": f"""
            <div class="bot-message">
                <h4 style="margin-bottom: 5px;">➕ <span>Add a New Meeting Note</span></h4>
                <p style="margin-top: 0;">Fill in the details below to log your meeting:</p>

                <form id="add-note-form" class="form-styled" style="display: flex; flex-direction: column; gap: 12px; margin-top: 15px;">

                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span><b>📅 Date:</b></span>
                        <span id="today-date"></span>
                    </div>
                    <input type="hidden" name="date" id="hidden-date">

                    <div>
                        <label for="meeting_type"><b>📌 Meeting Type:</b></label>
                        <select name="meeting_type" style="margin-top: 3px;" required>
                            <option value="" disabled selected hidden>-- Select Meeting Type --</option>
                            <option value="call">📞 Call</option>
                            <option value="video">🎥 Video</option>
                            <option value="on-site">🏢 On-site</option>
                        </select>
                    </div>

                    <div>
                        <label for="client_id"><b>👤 Client:</b></label>
                        <select id="client-select" name="client_id" required style="margin-top: 3px; width: 100%;">
                            {client_options}
                        </select>
                    </div>
                    
                    <div>
                        <label for="participants_employees"><b>👥 Employees in Meeting:</b></label>
                        <select id="employee-select" name="participants_employees" multiple required size="6" style="margin-top: 3px; width: 100%; overflow-y: auto;">
                            {employee_options}
                        </select>
                        <p style="font-size: 12px; color: #666;">💡 Select multiple using Ctrl or Shift.</p>
                    </div>

                    <div>
                        <label for="participants"><b>👥 Participants:</b></label>
                        <input type="text" name="participants" placeholder="E.g. John Smith, Maria Lopez" style="margin-top: 3px;" required>
                    </div>

                    <div>
                        <label for="summary"><b>📝 Summary:</b></label>
                        <textarea name="summary" rows="4" required style="width: 100%; margin-top: 3px;" placeholder="Brief summary of the meeting..."></textarea>
                    </div>

                    <button type="submit" class="workflow-button" style="align-self: flex-start;" disabled>💾 Save Note</button>
                </form>
            </div>
        """
    }


def insert_meeting_note(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 🔍 Extrage primul nume din lista participanților
        first_participant = data["participants"].split(",")[0].strip()

        # 🔎 Caută client_id pe baza numelui complet
        cursor.execute("SELECT client_id FROM clients WHERE name = %s", (first_participant,))
        client_result = cursor.fetchone()

        if not client_result:
            raise ValueError(f"No client found with name: {first_participant}")

        client_id = client_result["client_id"]
        employee_id = 1

        query = """
                    INSERT INTO meeting_notes (date, meeting_type, client_id, participants, summary, employee_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """
        cursor.execute(query, (
            data["date"],
            data["meeting_type"],
            client_id,
            data["participants"],
            data["summary"],
            employee_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "status": "success",
            "date_str": datetime.strptime(data["date"], "%Y-%m-%d").strftime("%B %d, %Y"),
            "meeting_type": data["meeting_type"],
            "participants": data["participants"],
            "summary": data["summary"]
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }



def handle_save_note():
    from flask import request, jsonify

    data = request.json
    result = insert_meeting_note(data)

    if result["status"] != "success":
        return jsonify({
            "user_message": "💾 Save Note",
            "html": f"<div class='bot-message error'>❌ Failed to save note: {result['error']}</div>"
        })

    confirmation = f"""
        <div class="bot-message">
            <div class="note-card" style="border-left: 4px solid #4CAF50; padding-left: 12px;">
                <p style="margin-bottom: 8px;">✅ <b>Note saved successfully!</b></p>

                <ul style="list-style: none; padding-left: 0; font-size: 14px; line-height: 1.6;">
                    <li>📅 <b>Date:</b> {result['date_str']}</li>
                    <li>📌 <b>Meeting Type:</b> {result['meeting_type'].capitalize()}</li>
                    <li>👥 <b>Participants:</b> {result['participants']}</li>
                    <li>📝 <b>Summary:</b><br>
                        <p style="font-style: italic; color: #333;">{result['summary']}</p>
                    </li>
                </ul>
            </div>
        </div>
    """

    followup = generate_notes_followup_message()["html"]

    return jsonify({
        "user_message": "💾 Save Note",
        "html": confirmation + followup
    })

def handle_edit_note_intro():
    from flask import jsonify
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT note_id, date, meeting_type, c.name AS client_name
        FROM meeting_notes mn
        JOIN clients c ON mn.client_id = c.client_id
        WHERE employee_id = 1
        ORDER BY date DESC
    """)
    notes = cursor.fetchall()
    cursor.close()
    conn.close()

    if not notes:
        return jsonify({
            "html": "<div class='bot-message'>ℹ️ No notes available to edit.</div>",
            "user_message": "✏️ Edit Note"
        })

    options = "".join([
        f"<option value='{note['note_id']}'>📅 {note['date']} – {note['client_name']} ({note['meeting_type']})</option>"
        for note in notes
    ])

    html = f"""
    <div class="bot-message">
        <p>✏️ <strong>Choose a note to edit:</strong></p>
        <select id="note-to-edit" class="custom-select">
            <option value="">-- Select a note --</option>
            {options}
        </select>
        <button id="continue-edit-note" class="workflow-button" style="margin-top: 10px;" disabled>📋 Modify This Note</button>
    </div>
    """

    return jsonify({
        "html": html,
        "user_message": "✏️ Edit Note"
    })

def generate_edit_note_form(note_id):
    from flask import jsonify
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            mn.note_id,
            mn.date,
            mn.meeting_type,
            mn.participants,
            mn.summary,
            mn.client_id,
            c.name AS client_name
        FROM meeting_notes mn
        JOIN clients c ON mn.client_id = c.client_id
        WHERE mn.note_id = %s
    """, (note_id,))
    note = cursor.fetchone()

    cursor.close()
    conn.close()

    if not note:
        return jsonify({
            "html": "<div class='bot-message'>⚠️ Could not find the selected note.</div>"
        })

    html = f"""
    <div class="bot-message">
        <form id="edit-note-form">
            <input type="hidden" name="note_id" value="{note['note_id']}">
            <input type="hidden" name="client_id" value="{note['client_id']}">
            <input type="hidden" name="meeting_type" value="{note['meeting_type']}">
            <input type="hidden" name="participants" value="{note['participants']}">

            <p class="form-title">✏️<b> Edit Meeting Note</b></p>
            <p class="form-instructions">Only the summary can be updated. Other fields are shown for context.</p> <br>

            <label><span class="icon">📅</span> Date:</label>
            <input type="text" value="{note['date']}" readonly class="readonly-date" style="margin-top: 5px;">

            <label><span class="icon">📌</span> Meeting Type:</label>
            <input type="text" value="{note['meeting_type'].capitalize()}" readonly style="margin-top: 5px;">

            <label><span class="icon">👤</span> Client:</label>
            <input type="text" value="{note['client_name']}" readonly style="margin-top: 5px;">

            <label><span class="icon">👥</span> Participants:</label>
            <input type="text" value="{note['participants']}" readonly style="margin-top: 5px;">

            <label><span class="icon">📝</span> Summary:</label><br>
            <textarea name="summary" placeholder="Brief summary of the meeting..." required style="margin-top: 5px; width: 100%; height: 80px;">{note['summary']}</textarea>

            <br><br><button type="submit" class="workflow-button">✅ Save Changes</button>
        </form>
    </div>
    """

    return jsonify({
        "html": html
    })

def handle_update_note():
    from flask import request, jsonify
    data = request.json

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        update_query = """
            UPDATE meeting_notes
            SET summary = %s
            WHERE note_id = %s
        """
        cursor.execute(update_query, (
            data["summary"],
            data["note_id"]
        ))
        conn.commit()

        cursor.execute("""
            SELECT date, meeting_type, participants
            FROM meeting_notes
            WHERE note_id = %s
        """, (data["note_id"],))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        formatted_date = result["date"].strftime("%B %d, %Y") if isinstance(result["date"], datetime) else result["date"]

        html = f"""
            <div class="bot-message">
                <p><b>✅ Note updated successfully!</b></p>
                <ul style="list-style: none; padding-left: 0; font-size: 14px; line-height: 1.6; margin-top: 10px;">
                    <li>📅 <b>Date:</b> {formatted_date}</li>
                    <li>📌 <b>Meeting Type:</b> {result['meeting_type']}</li>
                    <li>👥 <b>Participants:</b> {result['participants']}</li>
                    <li>📝 <b>Summary:</b><br>
                        <p style="font-style: italic; margin-top: 5px;">{data['summary']}</p>
                    </li>
                </ul>
            </div>
        """

        html += generate_notes_followup_message()["html"]

        return jsonify({
            "html": html,
            "user_message": "✅ Note Updated"
        })

    except Exception as e:
        return jsonify({
            "html": f"<div class='bot-message error'>❌ Failed to update note: {e}</div>",
            "user_message": "❌ Update Failed"
        })



def handle_delete_note_intro():
    from flask import jsonify
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT note_id, date, meeting_type, c.name AS client_name
        FROM meeting_notes mn
        JOIN clients c ON mn.client_id = c.client_id
        WHERE employee_id = 1
        ORDER BY date DESC
    """)
    notes = cursor.fetchall()
    cursor.close()
    conn.close()

    if not notes:
        return jsonify({
            "html": "<div class='bot-message'>ℹ️ No notes available to delete.</div>",
            "user_message": "🗑️ Delete Note"
        })

    options = "".join([
        f"<option value='{note['note_id']}'>📅 {note['date']} – {note['client_name']} ({note['meeting_type']})</option>"
        for note in notes
    ])

    html = f"""
    <div class="bot-message">
        <p>🗑️ <strong>Select a note to delete:</strong></p>
        <select id="note-to-delete" class="custom-select">
            <option value="">-- Select a note --</option>
            {options}
        </select>
        <button id="continue-delete-note" data-action="confirm-delete" class="workflow-button" style="margin-top: 10px;" disabled>❌ Delete This Note</button>
    </div>
    """

    return jsonify({
        "html": html,
        "user_message": "🗑️ Delete Note"
    })

def handle_delete_note_confirm(note_id):
    from flask import jsonify
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT date, meeting_type, participants, summary
        FROM meeting_notes
        WHERE note_id = %s
    """, (note_id,))
    note = cursor.fetchone()
    cursor.close()
    conn.close()

    if not note:
        return jsonify({
            "html": "<div class='bot-message error'>⚠️ Could not find the selected note.</div>",
            "user_message": "⚠️ Note Not Found"
        })

    # Pregătim detaliile notei
    html = f"""
        <div class="bot-message">
            <p><b>🗑️ Are you sure you want to delete this note?</b></p> <br>
            <ul style="list-style: none; padding-left: 0; font-size: 14px; line-height: 1.6;">
                <li>📅 <b>Date:</b> {note['date']}</li>
                <li>📌 <b>Meeting Type:</b> {note['meeting_type'].capitalize()}</li>
                <li>👥 <b>Participants:</b> {note['participants']}</li>
                <li>📝 <b>Summary:</b><br><p style="font-style: italic; color: #444;">{note['summary']}</p></li>
            </ul>
            <p>⚠️ This action cannot be undone.</p>

            <div style="display: flex; gap: 10px; margin-top: 12px;">
                <button class="workflow-button" data-action="confirm-delete" data-id="{note_id}">✅ Yes, Delete</button>
                <button class="workflow-button" data-action="cancel-delete">❌ No, Cancel</button>
            </div>
        </div>
    """
    return jsonify({
        "html": html,
        "user_message": "🗑️ Confirm Delete"
    })

def handle_delete_note_final(note_id):
    from flask import jsonify
    conn = get_db_connection()
    cursor = conn.cursor()

    # Pentru confirmare, extragem și detaliile înainte de ștergere
    cursor.execute("""
        SELECT date, meeting_type, participants, summary
        FROM meeting_notes
        WHERE note_id = %s
    """, (note_id,))
    note = cursor.fetchone()

    if not note:
        cursor.close()
        conn.close()
        return jsonify({
            "html": "<div class='bot-message error'>⚠️ Note not found or already deleted.</div>",
            "user_message": "❌ Delete Failed"
        })

    # Ștergem nota
    cursor.execute("DELETE FROM meeting_notes WHERE note_id = %s", (note_id,))
    conn.commit()
    cursor.close()
    conn.close()

    html = f"""
        <div class="bot-message">
            <p><b>✅ Note deleted successfully!</b></p>
            <ul style="list-style: none; padding-left: 0; font-size: 14px; line-height: 1.6;">
                <li>📅 <b>Date:</b> {note[0]}</li>
                <li>📌 <b>Meeting Type:</b> {note[1].capitalize()}</li>
                <li>👥 <b>Participants:</b> {note[2]}</li>
                <li>📝 <b>Summary:</b><br><p style="font-style: italic;">{note[3]}</p></li>
            </ul>
        </div>
    """

    html += generate_notes_followup_message()["html"]

    return jsonify({
        "html": html,
        "user_message": "✅ Note Deleted"
    })

def handle_delete_note_cancel():
    from flask import jsonify
    return jsonify({
        "html": generate_notes_followup_message()["html"],
        "user_message": "❌ Delete Cancelled"
    })









def generate_notes_followup_message():
    return {
        "html": """
            <div class="reminders-followup-container">
                <p><br><b>Would you like to take another action related to notes?</b><br>
                Please choose one below 👇</p>
                <select id="notes-followup-select" class="dropdown-select">
                    <option value="" disabled selected>Choose an action</option>
                    <option value="view-notes">🔍 View Notes</option>
                    <option value="add-note">➕ Add Note</option>
                    <option value="edit-note">✏️ Edit Note</option>
                    <option value="delete-note">🗑️ Delete Note</option>
                    <option value="exit-notes">🚪 Exit to Main Menu</option>
                </select>
            </div>
        """,
        "status": "followup"
    }

