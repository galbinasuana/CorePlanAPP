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

const appendBotMessage = (text, withAvatar = true) => {
    const avatar = `<img src="/static/bot.png" alt="Bot Avatar" class="bot-avatar" width="50" height="50">`;
    const msg = createMessageElement(`${withAvatar ? avatar : ""}<div class="message-text">${text}</div>`, "bot-message");
    chatBody.appendChild(msg);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
};

const generateAppointmentForm = (date = "", start = "", end = "", title = "", location = "") => {
    const todayStr = new Date().toISOString().split("T")[0];
    return `
        <div>
            <label><b>Date:</b></label><br>
            <input type="date" id="appt-date" value="${date}" min="${todayStr}"><br><br>

            <label><b>Time:</b></label><br>
            <input type="time" id="start-time" value="${start}"> -
            <input type="time" id="end-time" value="${end}"><br><br>

            <label><b>Title:</b></label><br>
            <input type="text" id="appt-title" value="${title}" placeholder="e.g. Zoom"><br><br>

            <label><b>Location:</b></label><br>
            <input type="text" id="appt-location" value="${location}" placeholder="e.g. Online"><br><br>

            <button class="option-button" id="confirm-add">✅ Add Appointment</button>
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
    const sectionButtons = `
        <div class="bot-options center-options">
            <button class="option-button" data-section="workflow">🧭 Daily Workflow</button>
            <button class="option-button" data-section="clients">👥 Client Management</button>
            <button class="option-button" data-section="reminders">🔁 Smart Reminders</button>
            <button class="option-button" data-section="reports">📈 Sales Reports</button>
            <button class="option-button" data-section="suggestions">💡 Smart Suggestions</button>
            <button class="option-button" data-section="notes">🧾 Notes & Follow-up</button>
            <button class="option-button" data-section="extras">🛠️ Other Tools</button>
        </div>
    `;

    const welcome = `
        <p>👋 Welcome back, <b>Richard Hayes</b> (Sales Specialist)<br>
        I'm here to help you plan, follow up, and focus only on what really brings results – while I take care of the rest.<br>
        Let’s make your day easier, smarter, and fully optimized. Please choose a section to begin:</p>
    `;

    appendBotMessage(welcome + sectionButtons);
};


const appendFollowupOptions = () => {
    const actionsHTML = `
        <div class="bot-options">
            <button class="option-button" data-action="add">📅 Add Appointment</button>
            <button class="option-button" data-action="view">📖 View Today</button>
            <button class="option-button" data-action="delete">❌ Delete</button>
            <button class="option-button" data-action="exit">🚪 Exit</button>
        </div>
    `;
    appendBotMessage(`Can I help you with anything else?<br>${actionsHTML}`);
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
        appendActionOptionsAfter();
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
    if (e.target.classList.contains("option-button")) {
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
    if (e.target.id === "confirm-add") {
        const date = document.getElementById("appt-date").value;
        const start = document.getElementById("start-time").value;
        const end = document.getElementById("end-time").value;
        const title = document.getElementById("appt-title").value.trim();
        const location = document.getElementById("appt-location").value.trim();

        if (!date || !start || !end || !title || !location) {
            appendBotMessage("⚠️ Please fill out <b>all fields</b> before confirming.");
            return appendBotMessage(generateAppointmentForm(date, start, end, title, location));
        }

        const startDateTime = new Date(`${date}T${start}`);
        const endDateTime = new Date(`${date}T${end}`);
        if (startDateTime >= endDateTime) {
            appendBotMessage("⚠️ Start time must be earlier than end time.");
            return appendBotMessage(generateAppointmentForm(date, start, end, title, location));
        }

        window.lastAppointmentData = { date, start, end, title, location };
        const message = `${date}, ${start}-${end}, ${title}, ${location}`;

        sendUserMessage(message);
    }
    else if (e.target.id === "load-day") {
        const date = document.getElementById("day-select").value;
        const res = await fetch("/appointments/day", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ date })
        });
        const appointments = await res.json();

        if (!appointments.length) {
            appendBotMessage("⚠️ No appointments found on this day.");
            appendFollowupOptions();
            return;
        }

        // 👇 Aici adaugi linia necesară
        const uniqueId = `appt-select-${Date.now()}`;

        const selectHTML = `
            <label for="${uniqueId}"><b>Select appointment to delete:</b></label><br>
            <select id="${uniqueId}" name="appt-select">
                ${appointments.map(a => {
                    const value = `${a.title}|${a.date}|${a.start_time}|${a.end_time}`;
                    const label = `${a.start_time} - ${a.end_time} | ${a.title}`;
                    return `<option value="${value}">${label}</option>`;
                }).join("")}
            </select><br><br>
            <div class="bot-options">
                <button class="option-button" id="confirm-delete" data-select-id="${uniqueId}">🗑️ Confirm Delete</button>
                <button class="option-button" id="cancel-delete">❌ Cancel</button>
            </div>
        `;

        appendBotMessage(selectHTML);
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
        appendMainOptions();
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

document.addEventListener("click", (e) => {
    if (e.target.id === "start-new-chat") {
        chatBody.innerHTML = "";
        appendMainOptions();
    }
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
    } else {
        // chat închis → revine botul
        botStatic.style.display = 'block';
        botVideo.style.display = 'block';
        closeIcon.style.display = 'none';
    }
});
