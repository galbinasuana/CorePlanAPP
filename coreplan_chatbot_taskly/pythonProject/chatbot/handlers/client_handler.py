import uuid
from data.db import get_db_connection
from datetime import datetime, timedelta

def handle_client_request():
    """
    Returns the main HTML message for the Client Management section.
    Includes a professional introduction and action buttons.
    """
    return {
        "html": """
            <div class="workflow-intro">
                <h3>👥 Client Management</h3>
                <p>
                    Welcome to your client operations panel.<br>
                    Here you can efficiently manage your contacts and sales pipeline:
                </p>

                <p>🔍 <b>View</b> client records and contact details</p>
                <p>➕ <b>Add</b> new leads or prospects</p>
                <p>🗑️ <b>Delete</b> a client from the database</p>
                <p>📝 <b>Update</b> existing client information</p>
                <br>
                <p><b>What action would you like to perform?</b></p>
            </div>

            <div class="bot-options center-options">
                <button class="workflow-button" data-action="view-clients">
                    <span class="emoji">🔍</span> View Clients
                </button>
                <button class="workflow-button" data-action="update-client">
                    <span class="emoji">📝</span> Update Client
                </button>
                <button class="workflow-button" data-action="delete-client">
                    <span class="emoji">🗑️</span> Delete Client
                </button>
                <button class="workflow-button" data-action="add-prospect">
                    <span class="emoji">➕</span> Add Prospect
                </button>
            </div>
            """,
        "status": "success"
    }

def get_clients_dropdown():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT client_id, name, company FROM clients ORDER BY name")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    unique_id = f"client-select-{uuid.uuid4().hex[:8]}"

    options_html = "".join([
        f"<option value='{client['client_id']}'>{client['name']} ({client['company']})</option>"
        for client in clients
    ])

    html = f"""
    <h3>🔍 View Client Details</h3><br>
    <p>Select a client from the list below to view their information:</p>
    <select id="{unique_id}" class="styled-dropdown" onchange="resetClientButton('{unique_id}')">
        <option value="" disabled selected>-- Choose a client --</option>
        {options_html}
    </select>
    <br><br>
    <button class="workflow-button disabled-button" onclick="handleClientSelection('{unique_id}')" disabled>
        🔎 View Client Info
    </button>
    """

    return {
        "html": html,
        "status": "awaiting_selection"
    }

def view_client_details(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close()
    conn.close()

    if not client:
        return {
            "html": "<p>⚠️ Client not found.</p>",
            "status": "not_found"
        }

    next_followup_raw = client.get("next_followup")
    if isinstance(next_followup_raw, datetime):
        next_followup_date = next_followup_raw.strftime("%Y-%m-%d")
    elif isinstance(next_followup_raw, str):
        try:
            next_followup_date = datetime.strptime(next_followup_raw, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except ValueError:
            next_followup_date = next_followup_raw  # fallback dacă formatul nu corespunde
    else:
        next_followup_date = "-"

    client_card  = f"""
    <div class="client-details-card">
        <h3>🧑‍💼 <b>{client['name']}</b></h3>
        <p>🏢 <b>Company:</b> {client.get('company', '-')}</p>
        <p>📧 <b>Email:</b> {client.get('email', '-')}</p>
        <p>📞 <b>Phone:</b> {client.get('phone', '-')}</p>
        <p>🔒 <b>Status:</b> {client.get('status', '-').capitalize()}</p>
        <p>🔥 <b>Interest Level:</b> {client.get('interest_level', '-').capitalize()}</p>
        <p>📅 <b>Last Contact:</b> {client.get('last_contact_date', '-')}</p>
        <p>📆 <b>Next Follow-up:</b> {next_followup_date}</p>
        <p>📝 <b>Notes:</b><br><i>{client.get('notes', 'No notes available.')}</i></p>
    </div>
    """

    ask_more = ask_view_another_client()["html"]

    return {
        "html": client_card + ask_more,
        "status": "success"
    }

def ask_view_another_client():
    return {
        "html": """
            <div class="followup-container center-options">
                <br>
                <p><b>Would you like to view another client?</b></p>
                <button class="workflow-button" data-action="view-another-client-yes">
                    🔄 Yes, show dropdown again
                </button>
                <button class="workflow-button" data-action="view-another-client-no">
                    ❌ No, return to client options
                </button>
            </div>
        """,
        "status": "confirmation"
    }

def get_clients_update_dropdown():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT client_id, name, company FROM clients ORDER BY name")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    options_html = "".join([
        f"<option value='{client['client_id']}'>{client['name']} ({client['company']})</option>"
        for client in clients
    ])

    html = f"""
    <h3>📝 Update Client</h3> <br>
    <p>Select the client you'd like to update:</p>
    <select id="update-client-select" class="styled-dropdown">
        <option value="" disabled selected>-- Choose a client --</option>
        {options_html}
    </select>
    <br><br>
    <button class="workflow-button disabled-button" onclick="fetchUpdateForm()" disabled>✏️ Edit Info</button>
    """
    return {
        "html": html,
        "status": "awaiting_selection"
    }

def get_update_form(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close()
    conn.close()

    if not client:
        return {"html": "<p>⚠️ Client not found.</p>", "status": "error"}

    statuses = ["lead", "active", "inactive"]
    interests = ["cold", "warm", "hot"]

    status_options = "".join([
        f'<option value="{s}" {"selected" if s == client["status"] else ""}>{s.capitalize()}</option>'
        for s in statuses
    ])
    interest_options = "".join([
        f'<option value="{i}" {"selected" if i == client["interest_level"] else ""}>{i.capitalize()}</option>'
        for i in interests
    ])

    form = f"""
        <div class="chatbot-wide-message" style="width: 100%;">
            <form id="update-client-form" class="client-update-form wide" style="padding-left: 20px; margin-left: -6px; margin-right: 14px;" onsubmit="submitClientUpdate(event)">
                <h3>✏️ Update Client Info</h3>
        
                <input type="hidden" id="update-client-id" value="{client['client_id']}">
        
                <div class="form-group">
                    <label for="update-name">Name:</label> 
                    <input type="text" id="update-name" value="{client['name']}">
                </div>
        
                <div class="form-group">
                    <label for="update-company">Company:</label>
                    <input type="text" id="update-company" value="{client['company']}">
                </div>
        
                <div class="form-group">
                    <label for="update-email">Email:</label>
                    <input type="email" id="update-email" value="{client['email']}">
                </div>
        
                <div class="form-group">
                    <label for="update-phone">Phone:</label>
                    <input type="text" id="update-phone" value="{client['phone']}">
                </div>
        
                <div class="form-group">
                    <label for="update-status">Status:</label>
                    <select id="update-status">{status_options}</select>
                </div>
        
                <div class="form-group">
                    <label for="update-interest">Interest Level:</label>
                    <select id="update-interest">{interest_options}</select>
                </div>
        
                <div class="form-group">
                    <label for="update-notes">Notes:</label>
                    <textarea id="update-notes">{client['notes']}</textarea>
                </div>
        
                <div class="form-actions">
                    <button type="submit">💾 Save Changes</button>
                </div>
            </form>
        </div>
    """

    return {
        "html": form,
        "status": "form_ready"
    }

def update_client(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE clients SET name=%s, company=%s, email=%s, phone=%s,
        status=%s, interest_level=%s, notes=%s WHERE client_id=%s
    """
    cursor.execute(sql, (
        data["name"], data["company"], data["email"], data["phone"],
        data["status"], data["interest_level"], data["notes"], data["client_id"]
    ))
    conn.commit()

    # Reîncarcă datele clientului din DB
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients WHERE client_id = %s", (data["client_id"],))
    client = cursor.fetchone()
    cursor.close()
    conn.close()

    # Formatăm data următorului follow-up
    next_followup_date = "-"
    if isinstance(client.get("next_followup"), datetime):
        next_followup_date = client["next_followup"].strftime("%Y-%m-%d")
    elif isinstance(client.get("next_followup"), str):
        try:
            next_followup_date = datetime.strptime(client["next_followup"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except ValueError:
            next_followup_date = client["next_followup"]

    # Construim cardul
    client_card = f"""
        <div class="client-details-card">
            <h3>🧑‍💼 <b>{client['name']}</b></h3>
            <p>🏢 <b>Company:</b> {client.get('company', '-')}</p>
            <p>📧 <b>Email:</b> {client.get('email', '-')}</p>
            <p>📞 <b>Phone:</b> {client.get('phone', '-')}</p>
            <p>🔒 <b>Status:</b> {client.get('status', '-').capitalize()}</p>
            <p>🔥 <b>Interest Level:</b> {client.get('interest_level', '-').capitalize()}</p>
            <p>📅 <b>Last Contact:</b> {client.get('last_contact_date', '-')}</p>
            <p>📆 <b>Next Follow-up:</b> {next_followup_date}</p>
            <p>📝 <b>Notes:</b><br><i>{client.get('notes', 'No notes available.')}</i></p>
        </div>
    """

    followup = generate_client_followup_message()["html"]

    return {
        "html": "<p>✅ Client info updated successfully!</p>" + client_card + followup,
        "status": "updated"
    }

def get_add_prospect_form():
    statuses = ["lead", "active", "inactive"]
    interests = ["cold", "warm", "hot"]

    status_options = "".join([f'<option value="{s}" {"selected" if s == "lead" else ""}>{s.capitalize()}</option>' for s in statuses])
    interest_options = "".join([f'<option value="{i}" {"selected" if i == "cold" else ""}>{i.capitalize()}</option>' for i in interests])

    form = f"""
        <div class="chatbot-wide-message" style="width: 100%;">
            <form id="add-prospect-form" class="client-update-form wide" style="padding-left: 20px; margin-left: -6px; margin-right: 14px;" onsubmit="submitAddProspect(event)">
                <h3>➕ Add New Prospect</h3>

                <div class="form-group">
                    <label for="add-name">Name:</label>
                    <input type="text" id="add-name" required oninput="resetProspectButton()">
                </div>

                <div class="form-group">
                    <label for="add-company">Company:</label>
                    <input type="text" id="add-company" oninput="resetProspectButton()">
                </div>

                <div class="form-group">
                    <label for="add-email">Email:</label>
                    <input type="email" id="add-email" required oninput="resetProspectButton()">
                </div>

                <div class="form-group">
                    <label for="add-phone">Phone:</label>
                    <input type="text" id="add-phone" required oninput="resetProspectButton()">
                </div>

                <div class="form-group">
                    <label for="add-status">Status:</label>
                    <select id="add-status">{status_options}</select>
                </div>

                <div class="form-group">
                    <label for="add-interest">Interest Level:</label>
                    <select id="add-interest">{interest_options}</select>
                </div>

                <div class="form-group">
                    <label for="add-notes">Notes:</label>
                    <textarea id="add-notes" oninput="resetProspectButton()"></textarea>
                </div>

                <div class="form-actions">
                    <button type="submit" id="save-prospect-btn" class="disabled-button" disabled>
                        💾 Save Prospect
                    </button>
                </div>
            </form>
        </div>
    """
    return {
        "html": form,
        "status": "form_ready"
    }


def add_new_prospect(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO clients (name, company, email, phone, status, interest_level, notes, last_contact_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(sql, (
        data["name"],
        data.get("company", ""),
        data["email"],
        data.get("phone", ""),
        data.get("status", "lead"),
        data.get("interest_level", "cold"),
        data.get("notes", "")
    ))

    conn.commit()

    # Obține datele clientului tocmai inserat
    cursor.execute("SELECT * FROM clients WHERE email = %s ORDER BY last_contact_date DESC LIMIT 1", (data["email"],))

    result = cursor.fetchone()
    desc = cursor.description
    client = dict(zip([col[0] for col in desc], result))

    cursor.close()
    conn.close()

    next_followup = datetime.today().date() + timedelta(days=3)

    client_card = f"""
        <div class="client-details-card">
            <h3>🧑‍💼 <b>{client['name']}</b></h3>
            <p>🏢 <b>Company:</b> {client.get('company', '-')}</p>
            <p>📧 <b>Email:</b> {client.get('email', '-')}</p>
            <p>📞 <b>Phone:</b> {client.get('phone', '-')}</p>
            <p>🔒 <b>Status:</b> {client.get('status', '-').capitalize()}</p>
            <p>🔥 <b>Interest Level:</b> {client.get('interest_level', '-').capitalize()}</p>
            <p>📅 <b>Last Contact:</b> {client.get('last_contact_date', '-')}</p>
            <p>📆 <b>Next Follow-up:</b> {next_followup}</p>
            <p>📝 <b>Notes:</b><br><i>{client.get('notes', 'No notes available.')}</i></p>
        </div>
    """

    followup_html = generate_client_followup_message()["html"]

    return {
        "html": f"""
            <p>✅ Prospect added successfully!</p>
            {client_card}
            {followup_html}
        """,
        "status": "success"
    }

def confirm_delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obținem numele pentru mesajul final
    cursor.execute("SELECT name FROM clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    if not client:
        cursor.close()
        conn.close()
        return {"html": "<p>⚠️ Client not found.</p>", "status": "not_found"}

    client_name = client["name"]

    # Ștergere efectivă
    cursor.execute("DELETE FROM clients WHERE client_id = %s", (client_id,))
    conn.commit()
    cursor.close()
    conn.close()

    followup_html = generate_client_followup_message()["html"]

    return {
        "html": f"<p>✅ Client <b>{client_name}</b> was deleted successfully.</p>{followup_html}",
        "status": "deleted"
    }

def get_clients_delete_dropdown():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT client_id, name, company FROM clients ORDER BY name")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    options_html = "".join([
        f"<option value='{client['client_id']}'>{client['name']} ({client['company']})</option>"
        for client in clients
    ])

    html = f"""
    <h3>🗑️ Delete Client</h3><br>
    <p>Select the client you'd like to delete:</p>
    <select id="delete-client-select" class="styled-dropdown" onchange="enableDeleteButton()">
        <option value="" disabled selected>-- Choose a client --</option>
        {options_html}
    </select>
    <br><br>
    <button class="workflow-button disabled-button" onclick="confirmClientDeletion()" disabled>
        🗑️ Delete Client
    </button>
    """

    return {
        "html": html,
        "status": "awaiting_selection"
    }

def ask_delete_confirmation(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close()
    conn.close()

    if not client:
        return {"html": "<p>⚠️ Client not found.</p>", "status": "not_found"}

    name = client["name"]

    html = f"""
    <p>⚠️ Are you sure you want to permanently delete <b>{name}</b> from the database?</p> <br>
    <div class="center-options">
        <button class="workflow-button" onclick="deleteConfirmedClient('{client_id}')">✅ Yes, delete</button>
        <button class="workflow-button" onclick="cancelClientDeletion()">❌ Cancel</button>
    </div>
    """

    return {
        "html": html,
        "status": "confirmation"
    }

def generate_client_followup_message():
    return {
        "html": """
            <div class="followup-container">
                <p><br><b>Would you like to do anything else related to clients?</b><br>
                Please choose an option below 👇</p>
                <select id="client-followup-select" class="dropdown-select">
                    <option value="" disabled selected>Choose an action</option>
                    <option value="view-clients">🔍 View Another Client</option>
                    <option value="update-client">📝 Update Client Info</option>
                    <option value="delete-client">🗑️ Delete a Client</option>
                    <option value="add-prospect">➕ Add New Prospect</option>
                    <option value="exit-clients">🚪 Exit and return to main menu</option>
                </select>
            </div>
        """,
        "status": "followup"
    }
