const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const chatbotToggler = document.querySelector("#chatbot-toggler");
const closeChatbot = document.querySelector("#close-chatbot");
const languageButton = document.querySelector("#language-button");
const historyButton = document.querySelector("#history-button");

const API_URL = "/api/message";
const TRANSLATE_URL = "/translate";
const HISTORY_URL = "/appointments/today";
let currentLang = "en";

const APPT_FORM_URL = "/appointments/form";
const APPT_TODAY_URL = "/appointments/today";
const APPT_WEEKDAY_URL = "/appointments/weekday";


const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};

const appendUserMessage = (text) => {
    const msg = createMessageElement(`<div class="message-text">${text}</div>`, "user-message");
    chatBody.appendChild(msg);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
};

const appendBotMessage = (html, withAvatar = true, typingSpeed = 15, initialDelay = 400) => {
    const msg = document.createElement("div");
    msg.classList.add("message", "bot-message");

    if (withAvatar) {
        const avatar = document.createElement("img");
        avatar.src = "/static/bot.png";
        avatar.alt = "Bot Avatar";
        avatar.classList.add("bot-avatar");
        avatar.width = 50;
        avatar.height = 50;
        msg.appendChild(avatar);
    }

    const textContainer = document.createElement("div");
    textContainer.classList.add("message-text");
    msg.appendChild(textContainer);
    chatBody.appendChild(msg);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

    const temp = document.createElement("div");
    temp.innerHTML = html.trim();
    const nodes = Array.from(temp.childNodes);

    let charList = [];

    // Recursiv extrage caractere păstrând structura HTML
    const extractCharacters = (node) => {
        if (node.nodeType === Node.TEXT_NODE) {
            node.textContent.split('').forEach(c => charList.push({ type: 'text', value: c }));
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            const openTag = document.createElement(node.tagName);
            [...node.attributes].forEach(attr => openTag.setAttribute(attr.name, attr.value));
            charList.push({ type: 'open', value: openTag });

            node.childNodes.forEach(child => extractCharacters(child));

            charList.push({ type: 'close', value: node.tagName });
        }
    };

    nodes.forEach(n => extractCharacters(n));

    setTimeout(() => {
        const stack = [];
        const typeChar = () => {
            if (charList.length === 0) return;

            const next = charList.shift();

            if (next.type === 'text') {
                const current = stack.length ? stack[stack.length - 1] : textContainer;
                current.appendChild(document.createTextNode(next.value));
            } else if (next.type === 'open') {
                const el = next.value.cloneNode();
                const parent = stack.length ? stack[stack.length - 1] : textContainer;
                parent.appendChild(el);
                stack.push(el);
            } else if (next.type === 'close') {
                stack.pop();
            }

            chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
            setTimeout(typeChar, typingSpeed);
        };

        typeChar();
    }, initialDelay);
};

const generateAppointmentForm = (date = "", start = "", end = "", title = "", location = "") => {
    const todayStr = new Date().toISOString().split("T")[0];
    return `
        <div class="appointment-form">
            <label>Date:</label>
            <input type="date" id="appt-date" value="${date}" min="${todayStr}">

            <label>Time:</label>
            <div class="time-row">
                <input type="time" id="start-time" value="${start}">
                <span>–</span>
                <input type="time" id="end-time" value="${end}">
            </div>

            <label>Title:</label>
            <input type="text" id="appt-title" value="${title}" placeholder="e.g. Zoom">

            <label>Location:</label>
            <input type="text" id="appt-location" value="${location}" placeholder="e.g. Online">

            <button class="confirm-button" id="btn-add-appt">Add Appointment</button>
        </div>
    `;
};

const generateWeekdaySelector = () => {
    const today = new Date();
    const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay() + 1)); // luni
    let options = "";

    for (let i = 0; i < 5; i++) {
        const d = new Date(startOfWeek);
        d.setDate(startOfWeek.getDate() + i);
        const dateStr = d.toISOString().split("T")[0];
        const label = d.toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric" });
        options += `<option value="${dateStr}">${label}</option>`;
    }

    return `
        <label for="day-select"><b>Select day:</b></label><br>
        <select id="day-select">${options}</select><br><br>
        <button class="option-button" id="load-day">🔍 Show Appointments</button>
    `;
};

function appendActionOptionsAfter() {
    const actionsHTML = `
        <div class="bot-options">
            <button class="option-button" data-action="add">📅 Add Appointment</button>
            <button class="option-button" data-action="view">📖 View Today</button>
            <button class="option-button" data-action="delete">❌ Delete</button>
            <button class="option-button" data-action="exit">🚪 Exit</button>
        </div>
    `;
    // 👇 Aici avatarul botului va apărea corect
    appendBotMessage("🤖 Would you like to do anything else?");
    appendBotMessage(actionsHTML); // păstrăm și aici avatarul
}

const appendMainOptions = () => {
    const welcomeText = `
        <p>👋 Welcome back, <b>Richard Hayes</b></p>

        <p>I'm here to help you plan, follow up, and stay focused on what really moves the needle in your sales process. Here’s what I can help you with today:</p>

        <ul class="chat-list">
          <li>🧭 <b>Daily Workflow</b> – manage appointments, review your schedule, and reschedule on the fly</li>
          <li>👥 <b>Client Management</b> – view and update client records, follow up, or add new prospects</li>
          <li>🔁 <b>Smart Reminders</b> – see missed follow-ups, set personal alerts, and plan ahead</li>
          <li>📈 <b>Sales Reports</b> – view your progress for today, this week, or month</li>
          <li>💡 <b>Smart Suggestions</b> – optimize your schedule, avoid conflicts, and focus on top priorities</li>
          <li>🧾 <b>Notes & Follow-up</b> – add notes after meetings or review past conversations</li>
          <li>🛠️ <b>Other Tools</b> – set focus time, track inactive clients, and more</li>
        </ul>

        <p><b>What would you like to start with?</b><br> Just type a keyword (like <i>workflow</i>, <i>clients</i>, or <i>reports</i>) or select a section below 👇</p>
    `;

    const dropdown = `
        <select id="section-select" class="dropdown-select">
            <option value="" disabled selected>Choose a section</option>
            <option value="workflow">🧭 Daily Workflow</option>
            <option value="clients">👥 Client Management</option>
            <option value="reminders">🔁 Smart Reminders</option>
            <option value="reports">📈 Sales Reports</option>
            <option value="suggestions">💡 Smart Suggestions</option>
            <option value="notes">🧾 Notes & Follow-up</option>
            <option value="extras">🛠️ Other Tools</option>
        </select>
    `;

    appendBotMessage(welcomeText + dropdown);
};

document.addEventListener("change", async (e) => {
    if (e.target.id === "followup-select") {
        const action = e.target.value;
        const label = e.target.options[e.target.selectedIndex].text;

        appendUserMessage(label);

        if (action === "add") {
            const res = await fetch(APPT_FORM_URL);
            const data = await res.json();
            appendBotMessage(data.html);
        } else if (action === "view") {
            const res = await fetch(APPT_TODAY_URL);
            const data = await res.json();
            appendBotMessage(data.html);
            appendFollowupOptions();
        } else if (action === "reschedule") {
            appendBotMessage("🔁 Rescheduling feature coming soon.");
        } else if (action === "delete") {
            const res = await fetch(APPT_WEEKDAY_URL);
            const data = await res.json();
            appendBotMessage("Please choose the day of the appointment you want to delete:");
            appendBotMessage(data.html);
        } else if (action === "exit") {
            const text = `
                🌟 Great job today. Every step counts!
                Need to check something else or pick up where you left off? <br>
            `;

            const button = `
                <div class="bot-options center-options" style="margin-top: 12px;">
                    <p>👋 I'm right here whenever you need support or assistance.<br> <br> </p>
                    <button class="option-button primary" id="start-new-chat">🔄 Start a New Conversation</button>
                </div>
            `;

            appendBotMessage(text + button);

        } else if (action === "workflow") {
            const introText = `
                <div class="workflow-intro">
                    <h3>🧭 Daily Workflow</h3>
                    <p>
                        Your daily productivity command center.<br>
                        Here you can schedule new appointments, check what’s next, move meetings around, or clean up old ones — all in just a few clicks.
                    </p>
                    <p><b>What do you want to do right now?</b></p>
                </div>
            `;

            const workflowButtons = `
                <div class="bot-options center-options">
                    <button class="workflow-button" data-action="add"><span class="emoji">📅</span> Add Appointment</button>
                    <button class="workflow-button" data-action="view"><span class="emoji">📖</span> View Today</button>
                    <button class="workflow-button" data-action="reschedule"><span class="emoji">🔁</span> Reschedule</button>
                    <button class="workflow-button" data-action="delete"><span class="emoji">❌</span> Delete</button>
                </div>
            `;

            appendBotMessage(introText + workflowButtons);
        }
    }
    else if (e.target.id === "section-select") {
        const selected = e.target.value;
        const label = e.target.options[e.target.selectedIndex].text;

        appendUserMessage(label);

        if (selected === "workflow") {
            const introText = `
                <div class="workflow-intro">
                    <h3>🧭 Daily Workflow</h3>
                    <p>
                        Your daily productivity command center.<br>
                        Here you can schedule new appointments, check what’s next, move meetings around, or clean up old ones — all in just a few clicks.
                    </p>
                    <p><b>What do you want to do right now?</b></p>
                </div>
            `;

            const workflowButtons = `
                <div class="bot-options center-options">
                    <button class="workflow-button" data-action="add"><span class="emoji">📅</span> Add Appointment</button>
                    <button class="workflow-button" data-action="view"><span class="emoji">📖</span> View Today</button>
                    <button class="workflow-button" data-action="reschedule"><span class="emoji">🔁</span> Reschedule</button>
                    <button class="workflow-button" data-action="delete"><span class="emoji">❌</span> Delete</button>
                </div>
            `;

            appendBotMessage(introText + workflowButtons);
        }

        // poți adăuga aici și pentru celelalte opțiuni: clients, reminders, etc.
    }
});



const appendFollowupDropdown = () => {
    const followupHTML = `
        <div class="message-text wide">
            <p><b>What would you like to do next?</b><br>Select a section below 👇</p>
            <select id="followup-select" class="dropdown-select">
                <option disabled selected value="">👇 Select option</option>
                <option value="workflow">🧭 Daily Workflow</option>
                <option value="clients">👥 Client Management</option>
                <option value="reminders">🔁 Smart Reminders</option>
                <option value="reports">📈 Sales Reports</option>
                <option value="suggestions">💡 Smart Suggestions</option>
                <option value="notes">🧾 Notes & Follow-up</option>
                <option value="extras">🛠️ Other Tools</option>
                <option value="exit">📕 Exit</option>
            </select>
        </div>
    `;
    appendBotMessage(followupHTML);
};


const appendFollowupOptions = () => {
    const followupHTML = `
        <div class="followup-container">
            <p><b>What would you like to do next?</b><br>Select a section below 👇</p>
            <select id="followup-select" class="dropdown-select">
                <option value="" disabled selected>Choose an option</option>
                <option value="add">📅 Add Appointment</option>
                <option value="view">📖 View Today</option>
                <option value="reschedule">🔁 Reschedule</option>
                <option value="delete">❌ Delete</option>
                <option value="exit">🚪 Exit</option>
            </select>
        </div>
    `;
    appendBotMessage(followupHTML);
};


const sendUserMessage = async (text, skipUserMessage = false) => {
    if (!skipUserMessage) {
        appendUserMessage(text);
    }

    const thinking = createMessageElement(`
        <div class="message-text">
            <div class="thinking-indicator">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
    `, "bot-message");
    chatBody.appendChild(thinking);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    thinking.remove();
    appendBotMessage(data.response);

    if (data.response.includes("Appointment") && data.response.includes("added")) {
        appendBotMessage("🎉 Your appointment has been successfully saved!");
//        appendActionOptionsAfter();
        return;
    }

    if (data.actions) {
        const buttonsHTML = data.actions.map(action =>
            `<button class="option-button" data-action="${action.toLowerCase()}">${action}</button>`
        ).join("<br>");
        const buttons = createMessageElement(`
            <div class="message-text">
                <div class="bot-options">${buttonsHTML}</div>
            </div>
        `, "bot-message");
        chatBody.appendChild(buttons);
    }


};

document.addEventListener("click", async (e) => {
    if (e.target.classList.contains("option-button") || e.target.classList.contains("workflow-button")) {

        const label = e.target.textContent;
        const action = e.target.dataset.action;

        const parent = e.target.closest(".message-text");
        const allButtons = parent.querySelectorAll(".option-button");
        allButtons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = 0.5;
            btn.style.cursor = "not-allowed";
        });

        appendUserMessage(label);

        if (action === "view") {
            const res = await fetch(HISTORY_URL);
            const data = await res.json();
            const reply = data.length === 0
                ? "You have no appointments today."
                : "Today's appointments:<br>" + data.map(a =>
                    `🕒 ${a.start_time} - ${a.end_time} | <b>${a.title}</b> (${a.location})`
                ).join("<br>");
            appendBotMessage(reply);
            appendFollowupOptions();
        }

        else if (action === "add") {
            appendBotMessage(generateAppointmentForm());
        }

        else if (action === "delete") {
            appendBotMessage("Please choose the day of the appointment you want to delete:");
            appendBotMessage(generateWeekdaySelector());
        }

        else if (action === "exit") {
            appendBotMessage(`
                <div class="final-message">
                    <p>👋 I'm right here whenever you need support or assistance.<br>
                    Have a <b>productive</b> and <b>fulfilling</b> day!</p>
                    <div class="bot-options center-options" style="margin-top: 12px;">
                        <button class="option-button primary" id="start-new-chat">🔄 Start a New Conversation</button>
                    </div>
                </div>
            `);
        }

        else if (action === "yes") {
            const last = window.lastAppointmentData;
            if (!last) return;
            const message = `${last.date}, ${last.start}-${last.end}, ${last.title}, ${last.location}`;
            messageInput.value = message;
            sendMessageButton.click();
            window.lastAppointmentData = null;
        }

        else if (action === "no") {
            const messageWithCancel = `
                <div class="message-text">
                    <p>❌ <b>Appointment was not added.</b></p>
                    <p>You can either fill in the form below to schedule a new appointment,<br>
                    or press <b>Cancel</b> to return to the main menu.</p>
                    <div class="bot-options center-options" style="margin-top: 10px;">
                        <button class="option-button" data-action="cancel-add">❌ Cancel</button>
                    </div>
                </div>
            `;
            const msg = createMessageElement(messageWithCancel, "bot-message");
            chatBody.appendChild(msg);

            appendBotMessage(generateAppointmentForm(), false);
        }

        else if (action === "cancel-add") {
            appendFollowupOptions();
        }
    }
});

document.addEventListener("click", async (e) => {
    if (e.target.id === "btn-add-appt") {
        const date = document.getElementById("appt-date")?.value || "06/19/2025";
        const start = document.getElementById("start-time")?.value || "10:00";
        const end = document.getElementById("end-time")?.value || "11:00";
        const title = document.getElementById("appt-title")?.value.trim() || "Team Sync";
        const location = document.getElementById("appt-location")?.value.trim() || "Meeting Room A";

        // Validează dacă există toate câmpurile
        if (!date || !start || !end || !title || !location) {
            appendBotMessage("⚠️ Please fill in all the fields.");
            return;
        }

        // Afișează un rezumat frumos în UI, ca mesaj de utilizator
        const summary = `
            <b>📌 Appointment Summary</b><br><br>
            <b>Title:</b> ${title}<br>
            <b>Date:</b> ${date}<br>
            <b>Time:</b> ${start} – ${end}<br>
            <b>Location:</b> ${location}
        `;
        appendUserMessage(summary); // NU mai afișezi niciun bot response, doar rezumatul

        // Șterge formularul de pe ecran dacă vrei (opțional)
        const lastMessage = document.querySelector(".message.bot:last-child");
        if (lastMessage) lastMessage.remove();

        setTimeout(() => {
            appendBotMessage("🎉 Your appointment has been successfully saved!");
        }, 300);

        setTimeout(() => {
            appendFollowupOptions();
        }, 1000);
    }
    else if (e.target.id === "confirm-delete") {
        const selectId = e.target.dataset.selectId;
        const value = document.getElementById(selectId).value;
        const [title, date, start_time, end_time] = value.split("|");

        const res = await fetch("/appointments/delete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, date, start_time, end_time })
        });

        const data = await res.json();
        appendBotMessage(data.message || data.error || "⚠️ Something went wrong.");
        appendActionOptionsAfter();
    }
    else if (e.target.id === "cancel-delete") {
        appendBotMessage("🛑 Deletion canceled.");
        appendActionOptionsAfter();
    }
    else if (e.target.id === "start-new-chat") {
        chatBody.innerHTML = "";
        appendBotMessage("💡 Just let me know what you'd like to do next.");
        appendFollowupDropdown();
    }
});

sendMessageButton.addEventListener("click", (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (!text) return;
    messageInput.value = "";
    sendUserMessage(text);
});

chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
closeChatbot.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
historyButton.addEventListener("click", () => sendUserMessage("See my schedule today"));

window.addEventListener("load", () => {
    chatBody.innerHTML = "";
    appendMainOptions();
});

document.getElementById('chatbot-toggler').addEventListener('click', function () {
    const popup = document.querySelector('.chatbot-popup');
    const closeIcon = document.getElementById('close-icon');
    const botStatic = document.getElementById('bot-static');
    const botVideo = document.getElementById('bot-video');

    const isOpen = popup.classList.toggle('open');

    if (isOpen) {
        // chat deschis → ascunde bot, arată X
        botStatic.style.display = 'none';
        botVideo.style.display = 'none';
        closeIcon.style.display = 'block';

        // ✅ Afișează opțiunile doar prima dată
        if (!document.querySelector('.chatbot-popup .bot-message')) {
            appendMainOptions();
        }

    } else {
        // chat închis → revine botul
        botStatic.style.display = 'block';
        botVideo.style.display = 'block';
        closeIcon.style.display = 'none';
    }
});

