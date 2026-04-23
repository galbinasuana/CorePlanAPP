import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def get_tools_intro():
    return {
        "html": """
        <div class="reminders-followup-container" style="padding: 15px 20px;">
            <div class="bot-section-header" style="margin-bottom: 10px;">
                <h4 style="margin: 0; font-size: 18px;">🛠️ <b>Other Tools</b></h4>
            </div>

            <div class="bot-section-description" style="font-size: 14px; line-height: 1.6;">
                <p>Welcome to your <b>Productivity & Learning Tools</b> hub.<br>
                These features are designed to boost your focus, automate communication, and keep your sales skills sharp.</p>
            </div>

            <ul class="feature-list" style="list-style: none; padding-left: 0; margin-top: 10px;">
                <li style="margin-bottom: 6px;">⏳ <b>Focus Mode:</b> Start a 25-minute work session and get notified when it's time to take a break.</li>
                <li style="margin-bottom: 6px;">📤 <b>Message Generator:</b> Quickly generate email or message templates to send to clients.</li>
            </ul>

            <p style="font-weight: 500; margin-top: 15px;">Choose a tool to get started:</p>

            <div class="bot-options bot-options-centered" style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 10px;">
                <button class="workflow-button" data-action="focus-mode">⏳ Focus Mode</button>
                <button class="workflow-button" data-action="generate-message">📤 Message Generator</button>  
            </div>
        </div>
        """
    }

def get_focus_mode_intro():
    return {
        "html": """
        <div class="focus-mode-container" style="padding: 20px;">
            <div class="bot-section-header">
                <h4>⏳ <b>Focus Mode</b></h4>
            </div>

            <p style="font-size: 14px; line-height: 1.6;">
                Boost your productivity with a <b><span id="focus-duration-label">25</span>-minute focus session</b>.<br>
                Set your preferences below and start when ready.
            </p>

            <form id="focus-mode-settings-form" style="margin-top: 15px;">
                <label style="font-size: 13px;">⏱️ Focus Duration: <span id="focus-duration-value">25</span> min</label><br>
                <input type="range" name="focus_duration" min="1" max="90" value="25" style="width: 100%;" 
                       oninput="document.getElementById('focus-duration-value').textContent = this.value"><br><br>

                <label style="font-size: 13px;">☕ Break Duration: <span id="break-duration-value">5</span> min</label><br>
                <input type="range" name="break_duration" min="1" max="30" value="5" style="width: 100%;" 
                       oninput="document.getElementById('break-duration-value').textContent = this.value"><br><br>

                <button type="button" id="start-focus-mode" class="workflow-button" style="margin-top: 10px;">
                    ▶️ Start Focus Mode
                </button>
            </form>
        </div>
        """
    }

def get_focus_mode_timer_html(focus_duration):
    return {
        "html": f"""
        <div class="focus-timer-container" style="text-align: center; padding: 20px;">
            <svg width="180" height="180" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" stroke="#ddd" stroke-width="10" fill="none"/>
                <circle id="progress-circle" cx="50" cy="50" r="45" stroke="#3b82f6" stroke-width="10" fill="none"
                        stroke-dasharray="282.6" stroke-dashoffset="0" transform="rotate(-90 50 50)"
                        style="transition: stroke-dashoffset 0.1s linear, stroke 0.3s ease;" />
                <text id="timer-text" x="50" y="55" text-anchor="middle" font-size="16" fill="#333" font-weight="bold">
                    {focus_duration}:00
                </text>
            </svg>

            <button id="pause-resume-btn" class="workflow-button" style="margin-top: 15px;">⏸ Pause</button>

            <script>
                let totalSeconds = {focus_duration} * 60;
                let remaining = totalSeconds;
                let paused = false;
                let intervalId = null;

                const circle = document.getElementById("progress-circle");
                const timerText = document.getElementById("timer-text");
                const btn = document.getElementById("pause-resume-btn");

                const originalColor = "#3b82f6";
                const pulseColors = ["#3b82f6", "#0ea5e9", "#22c55e", "#eab308", "#ef4444"];

                function updateVisuals() {{
                    const mins = String(Math.floor(remaining / 60)).padStart(2, '0');
                    const secs = String(remaining % 60).padStart(2, '0');
                    timerText.textContent = `${{mins}}:${{secs}}`;

                    const progress = (remaining / totalSeconds);
                    const offset = 282.6 * (1 - progress);
                    circle.style.strokeDashoffset = offset;

                    const colorIndex = Math.floor((totalSeconds - remaining) / 30) % pulseColors.length;
                    circle.style.stroke = pulseColors[colorIndex];
                }}

                function startTimer() {{
                    intervalId = setInterval(() => {{
                        if (!paused) {{
                            if (remaining <= 0) {{
                                clearInterval(intervalId);
                                timerText.textContent = "00:00";
                                circle.style.stroke = "#10b981";
                                appendBotMessage("⏰ <b>Time’s up!</b> Take a 5-min break?");
                            }} else {{
                                remaining -= 0.1;
                                updateVisuals();
                            }}
                        }}
                    }}, 100);
                }}

                btn.addEventListener("click", () => {{
                    paused = !paused;
                    btn.textContent = paused ? "▶️ Resume" : "⏸️ Pause";
                }});

                updateVisuals();
                startTimer();
            </script>
        </div>
        """
    }

def get_email_generator_form():
    return {
        "html": """
        <div class="email-generator-container" style="padding: 20px;">
            <p><b>✉️ Generate Smart Client Email</b></p><br>
            <p>Fill in the details below and I’ll generate a professional email tailored to the context and tone you choose.</p>

            <div class="form-group">
                <br><label>👤 Client Name:</label><br>
                <input type="text" id="client_name" placeholder="e.g. Ana Ionescu" required> 
            </div>

            <div class="form-group">
                <br><label>📧 Client Email Address:</label><br>
                <input type="email" id="client_email" placeholder="e.g. ana@example.com" required>
            </div>

            <div class="form-group">
                <br><label>✉️ Message Type:</label><br>
                <select id="message_type">
                    <option value="followup">Follow-up</option>
                    <option value="reminder">Reminder</option>
                    <option value="thankyou">Thank You</option>
                    <option value="warning">Warning</option>
                </select>
            </div>

            <div class="form-group">
                <br><label>😶 Emotion Tone:</label><br>
                <select id="emotion_tone">
                    <option value="neutral">Neutral</option>
                    <option value="friendly">Friendly</option>
                    <option value="assertive">Assertive</option>
                    <option value="upset">Upset</option>
                </select>
            </div>

            <div class="form-group">
                <br><label>👤 Client Gender:</label><br>
                <select id="client_gender">
                    <option value="female">Female</option>
                    <option value="male">Male</option>
                    <option value="neutral">Neutral</option>
                </select>
            </div>

            <div class="form-group">
                <br><label>🧭 Context:</label><br>
                <select id="message_context">
                    <option value="missed_meeting">Missed Meeting</option>
                    <option value="no_reply">No Reply</option>
                    <option value="refused_offer">Refused Offer</option>
                    <option value="confirmed">Meeting Confirmed</option>
                </select>
            </div>

            <div class="form-group">
                <br><label>🎯 Strategic Goal:</label><br>
                <select id="message_goal">
                    <option value="inform">Inform</option>
                    <option value="pressure">Soft Pressure</option>
                    <option value="gratitude">Gratitude</option>
                    <option value="reschedule">Reschedule</option>
                </select>
            </div>

            <div class="form-group">
                <br><label>📝 Subject Line:</label><br>
                <input type="text" id="subject" placeholder="e.g. Reminder: Offer Expires Friday">
            </div>

            <div class="form-group">
                <br><label>📎 Additional Info (optional):</label><br>
                <textarea id="extra_info" placeholder="e.g. The 15% discount offer ends in 2 days..." style="width: 100%; min-height: 100px;"></textarea>
            </div>

            <div class="form-group" style="margin-top: 20px; display: flex; gap: 10px;">
                <br><button class="workflow-button" id="generate-email-btn" data-action="generate-email" disabled>
                    ✨ Generate Email
                </button>
                <button class="workflow-button secondary-button" id="cancel-email-btn" data-action="cancel-email">
                    ❌ Cancel
                </button>
            </div>
        </div>
        """
    }

def get_followup_templates():
    return {
        "friendly_missed_meeting": """
        Hi {name},
        
        We noticed we missed our scheduled meeting. I hope everything is okay!
        I'd love to reconnect and hear your thoughts. Let me know what works for you.
        
        Cheers,
        Your Sales Team
        """,
                "neutral_no_reply": """
        Hello {name},
        
        Just following up on our recent conversation. I haven’t heard back from you and wanted to check in.
        
        Looking forward to your reply.
        
        Best regards,
        Sales Team
        """,
                "assertive_no_reply": """
        Dear {name},
        
        We’ve been trying to reach you without success. Please let us know if you're still interested so we can adjust our planning accordingly.
        
        Respectfully,
        Sales Department
        """
    }

def get_reminder_templates():
    return {
        "friendly_missed_meeting": """
        Hi {name},
        
        Just a friendly reminder that we missed our last meeting. If you’re still interested, I’d be happy to reschedule.
        
        Best,
        Sales Team
        """,
                "neutral_confirmed": """
        Dear {name},
        
        This is a quick reminder about your confirmed meeting with us. We’re looking forward to our discussion.
        
        Kind regards,
        CorePlan Team
        """,
                "assertive_missed_meeting": """
        Hello {name},
        
        You’ve missed a previously scheduled meeting. Please confirm if you'd still like to proceed.
        
        Best,
        Account Management
        """
    }

def get_thankyou_templates():
    return {
        "friendly_confirmed": """
        Hi {name},
        
        Thank you for confirming the meeting! We're excited to connect and explore the next steps together.
        
        Warm regards,
        CorePlan Team
        """,
                "neutral_no_reply": """
        Hello {name},
        
        I wanted to thank you for your previous time and interest. If you ever wish to reconnect, I’ll be here.
        
        Best,
        Sales Team
        """
    }

def get_warning_templates():
    return {
        "assertive_refused_offer": """
        Dear {name},
        
        We've noted that our offer was declined. If there’s any specific feedback or concern, we’d appreciate hearing it, as we may still find a mutually beneficial path forward.
        
        Regards,
        Strategic Accounts
        """,
                "upset_no_reply": """
        {name},
        
        We've made multiple attempts to reach you regarding our previous offer. If you are no longer interested, a short confirmation would be appreciated.
        
        Thank you,
        Sales Team
        """
    }

def get_email_template(message_type, tone, context):
    key = f"{tone}_{context}"
    template = None

    if message_type == "followup":
        template = get_followup_templates().get(key)
    elif message_type == "reminder":
        template = get_reminder_templates().get(key)
    elif message_type == "thankyou":
        template = get_thankyou_templates().get(key)
    elif message_type == "warning":
        template = get_warning_templates().get(key)

    if template is None:
        return f"""
        Hi {{name}},<br><br>
        We're following up regarding our recent interaction. Please let us know if you'd like to continue the conversation.<br><br>
        Best regards,<br>
        CorePlan Team
        """

    return template


def generate_email_preview(email_html: str) -> str:
    return f"""
    <div id="email-preview" class="email-preview-container">
        <h3>📬 Email Preview</h3>
        <div id="editable-email-body"
             class="generated-email-body"
             contenteditable="false"
             style="background:#f8f9fc; padding:15px; border-radius:10px; margin-top:10px; min-height:150px; border:1px solid #ccc;">
            {email_html}
        </div>
        <div class="email-preview-actions" style="margin-top:15px; display:flex; gap:10px;">
            <button class="workflow-button primary-button" id="send-email-btn">📤 Send Email</button>
            <button class="workflow-button secondary-button" id="edit-email-btn">✏️ Edit Email</button>
        </div>
    </div>
    """

def send_email(to_email, subject, body_html):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email

        part = MIMEText(body_html, "html")
        msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())

        return True
    except Exception as e:
        print("Email error:", e)
        return False



def generate_focus_mode_followup_message():
    return {
        "html": """
            <div class="reminders-followup-container">
                <p><br><b>Would you like to start another focus session or explore other tools?</b><br>
                Please choose one below 👇</p>
                <select id="focus-followup-select" class="dropdown-select">
                    <option value="" disabled selected>Choose an action</option>
                    <option value="focus-mode">⏳ Start New Focus Session</option>
                    <option value="message-generator">📤 Message Generator</option>
                    <option value="exit-main-menu">🚪 Exit to Main Menu</option>
                </select>
            </div>
        """,
        "status": "followup"
    }
