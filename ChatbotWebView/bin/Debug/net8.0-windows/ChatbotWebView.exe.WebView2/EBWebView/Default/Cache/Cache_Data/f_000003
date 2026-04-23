const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const chatbotToggler = document.querySelector("#chatbot-toggler");
const closeChatbot = document.querySelector("#close-chatbot");

const API_URL = "/api/message";
const typingEnabled = false;

// Creează un element de mesaj
const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};

// Afișează mesajul de utilizator
const appendUserMessage = (text) => {
    const msg = createMessageElement(`<div class="message-text">${text}</div>`, "user-message");
    chatBody.appendChild(msg);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
};

const parseAMPMToDate = (dateStr, timeStr) => {
    const [time, modifier] = timeStr.split(" ");
    let [hours, minutes, seconds] = time.split(":").map(Number);

    if (modifier === "PM" && hours < 12) hours += 12;
    if (modifier === "AM" && hours === 12) hours = 0;

    const isoString = `${dateStr}T${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    return new Date(isoString);
};

function appendThinkingIndicator() {
    const chat = document.querySelector(".chat-messages");

    const thinkingMsg = document.createElement("div");
    thinkingMsg.classList.add("message", "bot", "thinking-indicator");

    thinkingMsg.innerHTML = `
        <div class="avatar bot-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        </div>
    `;

    chat.appendChild(thinkingMsg);
    chat.scrollTop = chat.scrollHeight;
}

function removeThinkingIndicator() {
    const indicator = document.querySelector(".thinking-indicator");
    if (indicator) indicator.remove();
}


// Efect typing cu suport HTML complet
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

    if (!typingEnabled) {
        nodes.forEach(node => {
            try {
                textContainer.appendChild(node);
            } catch (e) {
                console.warn("Eroare la adăugare nod:", e);
            }
        });
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
        return;
    }

    setTimeout(() => {
        const stack = [];
        const typeChar = () => {
            if (charList.length === 0) return;
            const next = charList.shift();
            const current = stack.length ? stack[stack.length - 1] : textContainer;

            if (next.type === 'text') {
                current.appendChild(document.createTextNode(next.value));
            } else if (next.type === 'open') {
                const el = next.value.cloneNode();
                current.appendChild(el);
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

// Mesaj principal la inițializare
const appendMainOptions = () => {
    const welcomeText = `
        <p>👋 Welcome back, <b>Richard Hayes</b></p>
        <p>I'm here to help you plan, follow up, and stay focused on what really moves the needle in your sales process. Here’s what I can help you with today:</p>
        <ul class="chat-list">
            <li>👥 <b>Client Management</b> – view and update client records, follow up, or add new prospects</li>
            <li>🔁 <b>Smart Reminders</b> – see missed follow-ups, set personal alerts, and plan ahead</li>
            <li>📈 <b>Sales Reports</b> – view your progress for today, this week, or month</li>
            <li>📝 <b>Interaction Notes</b> – add notes after meetings or review past conversations</li>
            <li>🛠️ <b>Other Tools</b> – set focus time, track inactive clients, and more</li>
        </ul>
        <p><b>What would you like to start with?</b></p>
        <p><i>Just type a keyword (like <b>workflow</b>, <b>clients</b>, or <b>reports</b>) or select a section below 👇</i></p>
    `;

    const dropdown = `
        <select id="section-select" class="dropdown-select">
            <option value="" disabled selected>Choose a section</option>
            <option value="clients">👥 Client Management</option>
            <option value="reminders">🔁 Smart Reminders</option>
            <option value="reports">📈 Sales Reports</option>
            <option value="notes">📝 Interaction Notes</option>
            <option value="tools">🛠️ Other Tools</option>
        </select>
    `;

    appendBotMessage(welcomeText + dropdown);
};

document.addEventListener("change", async (e) => {
    if (e.target.id === "section-select") {
        const selected = e.target.value;
        const label = e.target.options[e.target.selectedIndex].text;
        appendUserMessage(label);

        const res = await fetch(`/section/${selected}`);
        const data = await res.json();
        appendBotMessage(data.html);
    }

    if (e.target && e.target.id === "alt-date-picker") {
        const selectedDate = e.target.value;

        fetch("/workflow/date", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ date: selectedDate })
        })
        .then(response => response.json())
        .then(data => {
            appendBotMessage(data.html);

            appendBotMessage(`
                <div class="followup-question">
                    <p>📅 Would you like to check your schedule for another day?<br>
                    Please select a date below, or click <b>Skip</b> to return to the main menu.</p>
                    <div class="date-picker-section">
                        <input type="date" id="alt-date-picker" class="bot-date-picker" />
                        <button class="workflow-button secondary" id="skip-btn">⏩ Skip</button>
                    </div>
                </div>
            `);
        })
        .catch(err => {
            console.error("Error:", err);
            appendBotMessage("<p>⚠️ An error occurred while retrieving your schedule.</p>");
        });
    }
});


//###################################################################################
//###############################   APPOINTMENTS     ################################
//###################################################################################
document.addEventListener("change", async (e) => {
    if (e.target && e.target.id === "followup-select") {
        const selected = e.target.value;
        const label = e.target.options[e.target.selectedIndex].text;
        appendUserMessage(label);

        if (selected === "add") {
            const res = await fetch("/workflow/add_form");
            const data = await res.json();
            appendBotMessage(data.html);
        }
        else if (selected === "view") {
            const res = await fetch("/workflow/view_today");

            if (!res.ok) {
                const errorText = await res.text();
                appendBotMessage(`<p>❌ Server error: ${res.status}</p><pre>${errorText}</pre>`);
                return;
            }

            const data = await res.json();
            appendBotMessage(data.html);
            appendFollowupOptions();
        }
        else if (selected === "reschedule") {
            const res = await fetch("/workflow/reschedule");
            const data = await res.json();
            appendBotMessage(data.html);
        }
        else if (selected === "delete") {
            const res = await fetch("/workflow/delete");
            const data = await res.json();
            appendBotMessage(data.html);
            appendFollowupOptions();
        }
        else if (selected === "exit") {
            const res = await fetch("/section/workflow");
            const data = await res.json();
            appendBotMessage(data.html);
        }
    }
});

document.addEventListener("change", (e) => {
    if (e.target && e.target.id === "delete-appt-select") {
        const btn = document.getElementById("confirm-delete-btn");
        if (btn) btn.disabled = false;
    }
});

// Text scris → trimis spre NLP backend
const sendUserMessage = async (text) => {
    appendUserMessage(text);

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
};

// Event Listeners
sendMessageButton.addEventListener("click", (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (!text) return;
    messageInput.value = "";
    sendUserMessage(text);
});

chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
closeChatbot.addEventListener("click", () => document.body.classList.remove("show-chatbot"));

window.addEventListener("load", () => {
    chatBody.innerHTML = "";
    appendMainOptions();
});

document.addEventListener("click", async (e) => {
    if (e.target && e.target.dataset.action === "skip") {
        const res = await fetch("/section/workflow");
        const data = await res.json();
        appendBotMessage(data.html);
        return;
    }

    if (e.target.matches(".workflow-button")) {
        const action = e.target.dataset.action;
        const label = e.target.innerText;
//        appendUserMessage(label);

        const thinking = createMessageElement(`
            <div class="message-text">
                <div class="thinking-indicator">
                    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
            </div>
        `, "bot-message");
        chatBody.appendChild(thinking);
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

        let response = null;

        try {
            if (action === "view") {
                const res = await fetch("/workflow/view_today");
                response = await res.json();
            } else if (action === "add") {
                const res = await fetch("/workflow/add_form");
                response = await res.json();
            }
            // poți adăuga și alte acțiuni aici (reschedule, delete etc.)
        } catch (err) {
            console.error("⚠️ Eroare la fetch:", err);
            thinking.remove();
            appendBotMessage("<p>❌ Something went wrong.</p>");
            return;
        }

        thinking.remove();

        if (response && response.html) {
            appendBotMessage(response.html);
        }
    }

    if (e.target && e.target.id === "confirm-delete-btn") {
        const select = document.getElementById("delete-appt-select");
        const apptId = select.value;
        const apptText = select.options[select.selectedIndex].text;

        const confirmArea = document.getElementById("delete-confirmation-area");
        confirmArea.innerHTML = `
            <p>🗑️ Are you sure you want to delete this appointment?<br><b>${apptText}</b></p>
            <button class="workflow-button danger" data-action="delete-confirm" data-id="${apptId}">✅ Yes, delete it</button>
            <button class="workflow-button" data-action="delete-cancel">↩️ No, cancel</button>
        `;
    }

    if (e.target && e.target.id === "delete-appt-select") {
        const btn = document.getElementById("confirm-delete-btn");
        btn.disabled = false;
    }

    if (e.target && e.target.dataset.action === "delete-confirm") {
        const id = e.target.dataset.id;
        const res = await fetch("/workflow/delete_confirm", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ appointment_id: id })
        });
        const data = await res.json();
        appendBotMessage(`<p>${data.message}</p>${data.html}`);
    }

    if (e.target && e.target.dataset.action === "delete-cancel") {
        const html = await fetch("/section/workflow").then(r => r.json());
        appendBotMessage(html.html);
    }

});

document.addEventListener("click", async function(e) {
    if (e.target && e.target.id === "skip-btn") {
        appendFollowupOptions();
    }

    if (e.target && e.target.id === "alt-date-picker") {
        e.stopPropagation();
    }
});

const appendFollowupOptions = () => {
    const followupHTML = `
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
    `;
    appendBotMessage(followupHTML);
};

function getTodayString() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
}

function parseTime(timeStr) {
    const [time, meridiem] = timeStr.split(" ");
    const [hours, minutes] = time.split(":").map(Number);
    return [hours, minutes, meridiem];
}

function convertTo24Hour(hours, meridiem) {
    if (meridiem === "PM" && hours < 12) return hours + 12;
    if (meridiem === "AM" && hours === 12) return 0;
    return hours;
}


document.addEventListener("submit", async (e) => {
    if (e.target && e.target.id === "add-appointment-form") {
        e.preventDefault();

        const form = e.target;
        const dateInput = form.querySelector("input[name='date']");
        const startTimeInput = form.querySelector("input[name='start_time']");
        const endTimeInput = form.querySelector("input[name='end_time']");
        const titleInput = form.querySelector("input[name='title']");
        const locationInput = form.querySelector("input[name='location']");
        const submitBtn = form.querySelector("button[type='submit']");

        // ⚠️ 1. Validare simplă: toate câmpurile completate
        if (!form.checkValidity()) {
            form.reportValidity(); // Afișează tooltip HTML5
            return;
        }

        // ⚠️ 2. Verificare interval permis (09:00 AM – 06:00 PM)
        const parseTime = (timeStr) => {
            const [time, modifier] = timeStr.split(" ");
            let [hours, minutes] = time.split(":").map(Number);
            if (modifier === "PM" && hours < 12) hours += 12;
            if (modifier === "AM" && hours === 12) hours = 0;
            return hours * 60 + minutes;
        };

        const start = parseTime(startTimeInput.value);
        const end = parseTime(endTimeInput.value);
        const dayStart = parseTime("09:00 AM");
        const dayEnd = parseTime("06:00 PM");

        if (start < dayStart || end > dayEnd) {
            appendBotMessage("<p>🕘 Appointments must be between <b>09:00 AM</b> and <b>06:00 PM</b>.</p>");
            return;
        }

        // ⚠️ 3. Dacă e azi, verifică dacă ora e în trecut
        const today = new Date().toISOString().slice(0, 10);
        if (dateInput.value === today) {
            const now = new Date();
            const nowMinutes = now.getHours() * 60 + now.getMinutes();
            if (start < nowMinutes) {
                appendBotMessage("<p>⏱️ Please choose a start time in the future.</p>");
                return;
            }
        }

        // ✅ Dacă totul e valid, trimite datele
        const appointmentData = {
            date: dateInput.value,
            start_time: startTimeInput.value,
            end_time: endTimeInput.value,
            title: titleInput.value,
            location: locationInput.value
        };

        const response = await fetch("/add-appointment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(appointmentData)
        });

        const result = await response.text();
        appendBotMessage(result);
    }
});



document.addEventListener("click", async (e) => {
    if (e.target && e.target.dataset.action === "confirm-rebook") {
        const date = e.target.dataset.date;
        const start = e.target.dataset.start;
        const end = e.target.dataset.end;
        const title = e.target.dataset.title;
        const location = e.target.dataset.location;

        appendUserMessage(e.target.innerText);

        const thinking = createMessageElement(`
            <div class="message-text">
                <div class="thinking-indicator">
                    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
            </div>
        `, "bot-message");
        chatBody.appendChild(thinking);
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

        try {
            const res = await fetch("/workflow/add_appointment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ date, start, end, title, location })
            });

            const data = await res.json();
            thinking.remove();
            appendBotMessage(`<p>${data.message}</p>`);
        } catch (err) {
            thinking.remove();
            appendBotMessage(`<p>❌ Failed to reschedule.</p>`);
        }
    }

    if (e.target && e.target.dataset.action === "cancel-rebook") {
        appendUserMessage(e.target.innerText);
        appendBotMessage(`<p>↩️ Appointment not scheduled. You can choose another time anytime.</p>`);
        appendFollowupOptions();
    }
});

function generateAppointmentForm(date = "", start = "", end = "", title = "", location = "") {
    const todayMin = getTodayString();
    return `
        <form id="add-appointment-form" class="appointment-form">
            <label>Date:</label>
            <input type="date" id="appt-date" value="${date}" min="${todayMin}" required>

            <label>Time:</label>
            <div class="time-row">
                <input type="time" id="appt-start" value="${start}" required>
                <span>–</span>
                <input type="time" id="appt-end" value="${end}" required>
            </div>

            <label>Title:</label>
            <input type="text" id="appt-title" value="${title}" placeholder="e.g. Zoom" required>

            <label>Location:</label>
            <input type="text" id="appt-location" value="${location}" placeholder="e.g. Online" required>

            <button type="submit" class="workflow-button primary" id="add-appt-button">✅ Add Appointment</button>
        </form>
    `;
}


//###################################################################################
//##################################   CLIENTS     ##################################
//###################################################################################
document.addEventListener("click", function (e) {
    if (e.target && e.target.matches("li[data-section='client_management']")) {
        appendUserMessage("👥 Client Management");

        fetch("/section/clients")
            .then(response => response.json())
            .then(data => {
                appendBotMessage(data.html);
            });
    }
});

document.addEventListener("click", function (e) {
    if (e.target && e.target.dataset.action === "view-clients") {
        fetch("/client/view-dropdown")
            .then(response => response.json())
            .then(data => {
                appendBotMessage(data.html);

                setTimeout(() => {
                    const select = document.getElementById("client-select");
                    if (select) {
                        select.selectedIndex = 0;
                        resetClientButton();
                    }
                }, 50);
            });
    }

    if (e.target && e.target.dataset.action === "view-another-client-yes") {
        fetch("/clients/dropdown")
            .then(r => r.json())
            .then(data => {
                appendBotMessage(data.html);

                // Adăugăm acest bloc pentru a forța resetarea dropdown-ului
                setTimeout(() => {
                    const select = document.getElementById("client-select");
                    if (select) {
                        select.selectedIndex = 0;
                        resetClientButton();
                    }
                }, 50);
            });
    }


    if (e.target && e.target.dataset.action === "view-another-client-no") {
//        appendUserMessage("❌ No, return to client options");
        fetch("/clients/followup")
            .then(r => r.json())
            .then(data => appendBotMessage(data.html));
    }

    if (e.target && e.target.dataset.action === "update-client") {
//        appendUserMessage(e.target.innerHTML);

        fetch("/clients/update-dropdown")
            .then(response => response.json())
            .then(data => {
                appendBotMessage(data.html);
            })
            .catch(err => {
                console.error("Error fetching update client dropdown:", err);
                appendBotMessage("<p>❌ Could not load client update form.</p>");
            });
    }

    if (e.target && e.target.dataset.action === "add-prospect") {
        appendUserMessage("➕ Add New Prospect");

        fetch("/clients/add-form")
            .then(response => response.json())
            .then(data => appendBotMessage(data.html))
            .catch(err => {
                console.error("Error loading add prospect form:", err);
                appendBotMessage("❌ Could not load form to add prospect.");
            });
    }

    if (e.target && e.target.dataset.action === "delete-client") {
        fetch("/clients/delete-dropdown")
            .then(response => response.json())
            .then(data => {
                appendBotMessage(data.html);
            })
            .catch(error => {
                console.error("Error loading delete dropdown:", error);
                appendBotMessage("❌ Failed to load client list for deletion.");
            });
    }

});

function handleClientSelection(selectId) {
    const selectedId = document.getElementById(selectId)?.value;
    if (!selectedId) return;

    fetch("/client/view/" + selectedId)
        .then(response => response.json())
        .then(data => {
            appendBotMessage(data.html);
        });
}

document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "client-select") {
        const button = e.target.closest(".bot-message").querySelector("button[onclick='handleClientSelection()']");
        if (e.target.value) {
            button.disabled = false;
            button.classList.remove("disabled-button");
        } else {
            button.disabled = true;
            button.classList.add("disabled-button");
        }
    }
});

function resetClientButton(selectId) {
    const select = document.getElementById(selectId);
    const button = select?.closest(".bot-message")?.querySelector("button[onclick*='handleClientSelection']");

    if (select && button) {
        if (select.value) {
            button.disabled = false;
            button.classList.remove("disabled-button");
        } else {
            button.disabled = true;
            button.classList.add("disabled-button");
        }
    }
}

document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "update-client-select") {
        const btn = e.target.closest(".bot-message").querySelector("button[onclick='fetchUpdateForm()']");
        btn.disabled = false;
        btn.classList.remove("disabled-button");
    }
});

function fetchUpdateForm() {
    const clientId = document.getElementById("update-client-select").value;
    if (!clientId) return;

    fetch("/clients/update-form/" + clientId)
        .then(r => r.json())
        .then(data => appendBotMessage(data.html));
}

function submitClientUpdate(event) {
    event.preventDefault();

    const payload = {
        client_id: document.getElementById("update-client-id").value,
        name: document.getElementById("update-name").value,
        company: document.getElementById("update-company").value,
        email: document.getElementById("update-email").value,
        phone: document.getElementById("update-phone").value,
        status: document.getElementById("update-status").value,
        interest_level: document.getElementById("update-interest").value,
        notes: document.getElementById("update-notes").value,
    };

    appendUserMessage("💾 Save Changes");

    fetch("/clients/update-save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        console.error("Eroare la update:", err);
        appendBotMessage("❌ A apărut o eroare la actualizarea datelor.");
    });
}

document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "client-followup-select") {
        const action = e.target.value;
        e.target.value = ""; // resetăm selecția

        switch (action) {
            case "view-clients":
                appendUserMessage("🔍 View Another Client");
                fetch("/clients/dropdown")
                    .then(response => response.json())
                    .then(data => appendBotMessage(data.html));
                break;
            case "update-client":
                appendUserMessage("📝 Update Client Info");
                fetch("/clients/update-dropdown")
                    .then(response => response.json())
                    .then(data => appendBotMessage(data.html));
                break;
            case "delete-client":
                appendUserMessage("🗑️ Delete a Client");
                fetch("/clients/delete-dropdown")
                    .then(response => response.json())
                    .then(data => appendBotMessage(data.html));
                break;
            case "add-prospect":
                appendUserMessage("➕ Add New Prospect");
                fetch("/clients/add-form")
                    .then(response => response.json())
                    .then(data => appendBotMessage(data.html));
                break;
            case "exit-clients":
                appendUserMessage("🚪 Exit to Main Menu");
                fetch("/main-menu")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;
        }
    }
});

document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "delete-client-select") {
        resetDeleteClientButton();
    }
});

function submitAddProspect(event) {
    event.preventDefault();

    const data = {
        name: document.getElementById("add-name").value,
        company: document.getElementById("add-company").value,
        email: document.getElementById("add-email").value,
        phone: document.getElementById("add-phone").value,
        status: document.getElementById("add-status").value,
        interest_level: document.getElementById("add-interest").value,
        notes: document.getElementById("add-notes").value
    };

    appendUserMessage("💾 Save Prospect");

    fetch("/clients/add-save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        appendBotMessage(result.html);
    })
    .catch(error => {
        console.error("Error saving prospect:", error);
        appendBotMessage("<p>❌ Something went wrong while saving the prospect.</p>");
    });
}

function resetProspectButton() {
    const name = document.getElementById("add-name");
    const company = document.getElementById("add-company");
    const email = document.getElementById("add-email");
    const phone = document.getElementById("add-phone");
    const notes = document.getElementById("add-notes");
    const button = document.getElementById("save-prospect-btn");

    const allFilled =
        name?.value.trim() &&
        company?.value.trim() &&
        email?.value.trim() &&
        phone?.value.trim() &&
        notes?.value.trim();

    if (allFilled) {
        button.disabled = false;
        button.classList.remove("disabled-button");
    } else {
        button.disabled = true;
        button.classList.add("disabled-button");
    }
}


function confirmClientDeletion() {
    const clientId = document.getElementById("delete-client-select").value;
    if (!clientId) return;

    fetch(`/clients/delete-confirm/${clientId}`)
        .then(response => response.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(error => {
            console.error("Error fetching confirmation:", error);
            appendBotMessage("❌ Could not fetch confirmation step.");
        });
}

function deleteConfirmedClient(clientId) {
    fetch(`/clients/delete/${clientId}`, {
        method: "DELETE"
    })
        .then(response => response.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(error => {
            console.error("Error deleting client:", error);
            appendBotMessage("❌ Error occurred while deleting client.");
        });
}

function cancelClientDeletion() {
    fetch("/clients/followup")
        .then(response => response.json())
        .then(data => appendBotMessage(data.html));
}

function resetDeleteClientButton() {
    const select = document.getElementById("delete-client-select");
    const button = select?.closest(".bot-message")?.querySelector("button[onclick='confirmClientDeletion()']");

    if (!select || !button) return;

    if (select.value) {
        button.disabled = false;
        button.classList.remove("disabled-button");
    } else {
        button.disabled = true;
        button.classList.add("disabled-button");
    }
}


//###################################################################################
//##############################    SMART REMINDERS    ##############################
//###################################################################################
document.addEventListener("change", function (e) {
    const target = e.target;

    if (target.classList.contains("followup-select")) {
        const selected = target.value;

        if (selected === "reminders") {
            fetch("/section/reminders")
                .then(res => res.json())
                .then(data => {
                    displayBotMessage(data.html);
                });
        }
    }
});

function handleViewFollowups() {
    fetch("/reminders/view")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        });
}

function handleMarkCompleted() {
    fetch("/reminders/mark")
        .then(res => res.json())
        .then(data => appendBotMessage(data.html))
        .catch(error => console.error("Error loading mark completed view:", error));
}

function handleConfirmCompletion() {
    const dropdown = document.querySelector("#followup-complete-select");
    const followupId = dropdown?.value;

    if (!followupId) return;

    fetch("/reminders/mark/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ followup_id: followupId })
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    });
}

function handleFollowupSummary() {
    fetch('/reminders/summary', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(error => {
        console.error("Error loading follow-up summary:", error);
        renderBotMessage("❌ Error loading follow-up summary.");
    });
}

function validateFollowUpForm() {
    const form = document.querySelector(".followup-form");
    if (!form) return;

    const dateInput = form.querySelector("#followup-date");
    const clientSelect = form.querySelector("#followup-client");
    const purposeInput = form.querySelector("#followup-purpose");
    const saveBtn = form.querySelector("#save-followup-btn");

    function checkValidity() {
        const allFilled =
            dateInput.value.trim() !== "" &&
            clientSelect.value.trim() !== "" &&
            purposeInput.value.trim() !== "";

        saveBtn.disabled = !allFilled;

        saveBtn.style.opacity = allFilled ? "1" : "0.5";
        saveBtn.style.cursor = allFilled ? "pointer" : "not-allowed";
    }

    checkValidity();

    [dateInput, clientSelect, purposeInput].forEach((el) => {
        el.addEventListener("input", checkValidity);
        el.addEventListener("change", checkValidity);
    });
}

function activateManualReminderButton() {
    const followup = document.getElementById("manual-reminder-select");
    const days = document.getElementById("reminder-days");
    const btn = document.getElementById("set-reminder-btn");

    if (!followup || !days || !btn) return;

    function checkValidity() {
        const valid = followup.value && days.value;
        btn.disabled = !valid;
        btn.style.opacity = valid ? "1" : "0.5";
        btn.style.cursor = valid ? "pointer" : "not-allowed";
    }

    checkValidity(); // Inițial
    followup.addEventListener("change", checkValidity);
    days.addEventListener("change", checkValidity);
}


function handleAddFollowup() {
    fetch("/reminders/add")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);

            setTimeout(() => {
                const dateInput = document.getElementById("followup-date");
                if (dateInput) {
                    const today = new Date().toISOString().split("T")[0];
                    dateInput.setAttribute("min", today);
                }

                validateFollowUpForm();
            }, 200); // așteptăm DOM-ul să fie inserat
        });
}


function handleSetReminder() {
    fetch("/reminders/set")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);

            setTimeout(() => {
                const followupSelect = document.getElementById("manual-reminder-select");
                const daysSelect = document.getElementById("reminder-days");
                const saveBtn = document.getElementById("set-reminder-btn");

                // 🛑 Dacă nu există formularul, ne oprim aici
                if (!followupSelect || !daysSelect || !saveBtn) {
                    return;
                }

                function validateManualReminder() {
                    const valid = followupSelect.value && daysSelect.value;
                    saveBtn.disabled = !valid;
                    saveBtn.style.opacity = valid ? "1" : "0.5";
                    saveBtn.style.cursor = valid ? "pointer" : "not-allowed";
                }

                validateManualReminder();
                followupSelect.addEventListener("change", validateManualReminder);
                daysSelect.addEventListener("change", validateManualReminder);

                saveBtn.addEventListener("click", () => {
                    handleSetManualReminder(saveBtn);
                });
            }, 200);
        });
}






function handleSkipReminder() {
    fetch("/reminders/skip", {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => appendBotMessage(data.html))
    .catch(error => console.error("Error skipping reminder:", error));
}

function handleSetOneDayReminder(followupId) {
    if (!followupId) return;

    fetch("/chatbot/set_reminder_one_day", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ followup_id: followupId })
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        console.error("❌ Failed to set 1-day reminder:", err);
        appendBotMessage("❗ Something went wrong while setting your reminder.");
    });
}

function handleManualReminderConfirmation() {
    const followupSelect = document.getElementById("manual-reminder-select");
    const daysSelect = document.getElementById("reminder-days");

    const followupId = followupSelect?.value;
    const daysBefore = daysSelect?.value;

    if (!followupId || !daysBefore) return;

    fetch("/chatbot/set_manual_reminder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ followup_id: followupId, days_before: daysBefore })
    })
    .then(res => res.json())
    .then(data => appendBotMessage(data.html))
    .catch(err => {
        console.error("❌ Error setting manual reminder:", err);
        appendBotMessage("❗ Something went wrong while setting your reminder.");
    });
}

function handleSetManualReminder(btn) {
    const followupSelect = document.getElementById("manual-reminder-select");
    const daysSelect = document.getElementById("reminder-days");

    const followupId = followupSelect?.value;
    const daysBefore = daysSelect?.value;

    if (!followupId || !daysBefore) {
        appendBotMessage("❗ Please select both follow-up and days.");
        return;
    }

    fetch("/chatbot/set_manual_reminder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ followup_id: followupId, days_before: daysBefore })
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        console.error("❌ Error setting manual reminder:", err);
        appendBotMessage("❗ Something went wrong while setting your reminder.");
    });
}


document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "followup-complete-select") {
        const confirmBtn = document.getElementById("confirm-complete-btn");
        if (confirmBtn) {
            confirmBtn.disabled = !e.target.value;
        }
    }
});

document.addEventListener("change", function (e) {
    const dropdown = e.target.closest("#followup-complete-select");
    if (!dropdown) return;

    const confirmBtn = dropdown
        .closest(".reminders-mark-container")
        .querySelector("button[data-action='confirm-followup-completion']");

    if (dropdown.value) {
        confirmBtn.disabled = false;
    } else {
        confirmBtn.disabled = true;
    }
});

document.addEventListener("click", function (e) {
    const btn = e.target.closest("#save-followup-btn");
    if (!btn) return;

    const form = btn.closest(".followup-form");
    if (!form) return;

    const date = form.querySelector("#followup-date")?.value;
    const client_id = form.querySelector("#followup-client")?.value;
    const purpose = form.querySelector("#followup-purpose")?.value;

    if (!date || !client_id || !purpose) {
        appendBotMessage("❗ Please fill in all the fields.");
        return;
    }

    fetch("/reminders/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date, client_id, purpose })
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        console.error("Error saving follow-up:", err);
        appendBotMessage("❌ Something went wrong while saving your follow-up.");
    });
});

document.addEventListener("change", function () {
    const followup = document.getElementById("manual-reminder-select");
    const days = document.getElementById("reminder-days");
    const btn = document.getElementById("set-reminder-btn");

    if (followup && days && btn) {
        if (followup.value && days.value) {
            btn.disabled = false;
        } else {
            btn.disabled = true;
        }
    }
});

document.addEventListener("click", function (event) {
    if (event.target.matches('[data-action="exit-reminders"]')) {
        fetch('/chatbot/exit_reminders')
            .then(response => response.json())
            .then(data => {
                appendBotMessage(data.html);
            });
    }
});

document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "reminder-followup-select") {
        const selected = e.target.value;

        setTimeout(() => {
            e.target.selectedIndex = 0;
        }, 100);

        const selectedText = e.target.options[e.target.selectedIndex].text;
        appendUserMessage(selectedText);

        switch (selected) {
            case "view-followups":
                fetch("/reminders/view")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "mark-followup-completed":
                fetch("/reminders/mark")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "add-followup":
                fetch("/reminders/add")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "set-reminder":
                fetch("/reminders/set")
                    .then(res => res.json())
                    .then(data => {
                        appendBotMessage(data.html);
                        const checkFormReady = setInterval(() => {
                            const select = document.getElementById("manual-reminder-select");
                            if (select) {
                                clearInterval(checkFormReady);
                                handleSetReminder();
                            }
                        }, 100);
                    });
                break;



            case "followup-summary":
                fetch("/reminders/summary")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "exit-reminders":
                fetch("/main-menu")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;
            default:
                appendBotMessage("❗ Unexpected selection. Please try again.");
                break;
        }
    }
});

document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.getAttribute("data-action");

    switch (action) {
        case "view-followups":
            handleViewFollowups();
            break;
        case "mark-followup-completed":
            handleMarkCompleted();
            break;
        case "confirm-followup-completion":
            handleConfirmCompletion();
            break;
        case "add-followup":
            handleAddFollowup();
            break;
        case "set-reminder":
            handleSetReminder();
            break;
        case "set-manual-reminder":
            handleSetManualReminder(btn);
            break;
        case "confirm-reminder":
            const followupId = btn.dataset.id;
            handleSetOneDayReminder(followupId);
            break;
        case "confirm-manual-reminder":
            handleSetManualReminder(btn);
            break;
        case "skip-reminder":
            handleSkipReminder();
            break;
        case "followup-summary":
            handleFollowupSummary();
            break;
        default:
            console.log("Unknown action: " + action);
    }
});


//###################################################################################
//###############################    SALES REPORTS    ###############################
//###################################################################################

document.addEventListener("change", function (e) {
    const target = e.target;

    if (target.id === "section-select") {
        const selected = target.value;

        if (selected === "reports") {
            handleSalesReports();
        }
    }

    if (e.target.id === "client-stats-select") {
        const btn = document.querySelector("button[onclick='fetchClientStats()']");
        if (btn) {
            btn.disabled = false;
            btn.classList.remove("disabled-button");
        }
    }
});

function handleSalesReports() {
    fetch("/sales-reports", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            employee_id: 1
        })
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        appendBotMessage("❌ Error loading sales reports. Please try again later.");
        console.error("Sales Reports Error:", err);
    });
}

function handleMonthlyBreakdown() {
    fetch("/monthly-breakdown", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ employee_id: 1 })
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        appendBotMessage("❌ Error loading monthly breakdown. Please try again later.");
        console.error("Monthly Breakdown Error:", err);
    });
}

function handleClientStats() {
    document.querySelectorAll("#client-stats-select").forEach(el => el.parentElement.remove());

    fetch("/sales/client-stats-dropdown")
        .then(response => response.json())
        .then(data => {
            if (data && data.html) {
                appendBotMessage(data.html);
//                setupClientDropdownEvents();
            } else {
                appendBotMessage("<div class='bot-message error'>⚠️ Could not load client list (invalid response).</div>");
            }
        })
        .catch(error => {
            appendBotMessage("<div class='bot-message error'>⚠️ Could not load client list.</div>");
            console.error("Client Stats Dropdown Error:", error);
        });
}


function fetchClientStats() {
    const select = document.getElementById("client-stats-select");
    const clientId = select.value;
    fetch(`/sales/client-stats/${clientId}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.html) {
                appendBotMessage(data.html);
            } else {
                appendBotMessage("⚠️ No data available for this client.");
            }
        })
        .catch(err => {
            appendBotMessage("❌ Error loading client statistics.");
            console.error("Client Stats Error:", err);
        });
}

function handleExitSales() {
    fetch("/sales/exit")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("⚠️ Could not return to sales menu.");
            console.error("Exit Sales Error:", err);
        });
}

function handleImproveSuggestions() {
    fetch("/sales/improve-suggestions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ employee_id: 1 })  // În viitor, din sesiune
    })
    .then(res => res.json())
    .then(data => {
        appendBotMessage(data.html);
    })
    .catch(err => {
        appendBotMessage("⚠️ Could not generate suggestions.");
        console.error("Improve Suggestions Error:", err);
    });
}

document.addEventListener("click", function (e) {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;

    const action = btn.getAttribute("data-action");

    switch (action) {
        case "sales-reports":
            handleSalesReports();
            break;
        case "monthly-breakdown":
            handleMonthlyBreakdown();
            break;
        case "client-stats":
            handleClientStats();
            break;
        case "client-stats-another":
            handleClientStats();
            break;
        case "exit-sales":
            handleExitSales();
            break;
        case "improve-suggestions":
            handleImproveSuggestions();
            break;

        default:
            console.warn("Unknown action:", action);
    }
});

document.addEventListener("change", function (e) {
    const select = e.target.closest("select#sales-action-select");
    if (!select) return;

    const selectedValue = select.value;

    let userMessage = "";
    switch (selectedValue) {
        case "view-monthly-breakdown":
            userMessage = "📊 View Monthly Breakdown";
            break;
        case "client-stats":
            userMessage = "👥 Client Stats";
            break;
        case "improve-suggestions":
            userMessage = "💡 Suggestions to Improve";
            break;
        case "exit-sales-report":
            userMessage = "🚪 Exit and return to main menu";
            break;

        default:
            userMessage = "❓ Unknown action";
    }

    appendUserMessage(userMessage);

    switch (selectedValue) {
        case "view-monthly-breakdown":
            handleMonthlyBreakdown();
            break;
        case "client-stats":
            handleClientStats();
            break;
        case "improve-suggestions":
            handleImproveSuggestions();
            break;
        case "exit-sales-report":
            fetch("/main-menu")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
            break;
        case "client-stats-another":
            handleClientStats();
            break;
        default:
            displayBotResponse("<p>❌ Unknown sales action selected.</p>");
    }

    select.selectedIndex = 0;
});



//###################################################################################
//##############################   INTERACTION NOTES   ##############################
//###################################################################################

function handleNotesIntro() {
    fetch("/section/notes")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Error loading notes section. Please try again later.");
            console.error("Notes Intro Error:", err);
        });
}

function handleExitNotes() {
    fetch("/main-menu")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("⚠️ Could not return to main menu.");
            console.error("Exit Notes Error:", err);
        });
}

function handleViewNotes() {
    fetch("/section/notes/view")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Error loading notes. Please try again later.");
            console.error("View Notes Error:", err);
        });
}

function handleAddNote() {
    fetch("/section/notes/add")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
            attachClientDblClick();
            attachParticipantAutoFill();
            attachClientParticipantSync();

            const today = new Date().toISOString().split("T")[0];
            const todayDisplay = document.getElementById("today-date");
            const hiddenDateInput = document.getElementById("hidden-date");

            if (todayDisplay) todayDisplay.textContent = today;
            if (hiddenDateInput) hiddenDateInput.value = today;
        })
        .catch(err => {
            appendBotMessage("❌ Error loading note form. Please try again.");
            console.error("Add Note Error:", err);
        });
}

document.addEventListener("submit", function (e) {
    if (e.target && e.target.id === "add-note-form") {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        fetch("/section/notes/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                date: formData.get("date"),
                meeting_type: formData.get("meeting_type"),
                participants: formData.get("participants"),
                summary: formData.get("summary")
            })
        })

        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Failed to save note.");
            console.error("Save Note Error:", err);
        });
    }

    if (e.target && e.target.id === "edit-note-form") {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        fetch("/section/notes/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                note_id: formData.get("note_id"),
                date: formData.get("date"),
                meeting_type: formData.get("meeting_type"),
                participants: formData.get("participants"),
                summary: formData.get("summary")
            })
        })
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Failed to update note.");
            console.error("Update Note Error:", err);
        });
    }

});

document.addEventListener("input", function (e) {
    const form = document.getElementById("add-note-form");
    if (!form) return;

    const hiddenDateInput = form.querySelector("input[name='date']");
    const type = form.querySelector("select[name='meeting_type']").value.trim();
    const participants = form.querySelector("input[name='participants']").value.trim();
    const summary = form.querySelector("textarea[name='summary']").value.trim();
    const submitBtn = form.querySelector("button[type='submit']");

    if (hiddenDateInput && hiddenDateInput.value && type && participants && summary) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
});

document.addEventListener('DOMContentLoaded', attachClientDblClick);

function attachClientDblClick() {
    const clientSelect = document.getElementById("client-select");
    const participantsInput = document.querySelector('input[name="participants"]');

    if (clientSelect && participantsInput) {
        clientSelect.addEventListener('dblclick', function () {
            const selected = Array.from(clientSelect.selectedOptions).map(opt => opt.textContent.trim());
            let current = participantsInput.value.split(',').map(s => s.trim()).filter(Boolean);

            selected.forEach(name => {
                if (!current.includes(name)) {
                    current.push(name);
                }
            });

            participantsInput.value = current.join(', ');
        });
    }
}

function attachParticipantAutoFill() {
    const clientSelect = document.getElementById("client-select");
    const employeeSelect = document.getElementById("employee-select");
    const participantsInput = document.querySelector('input[name="participants"]');

    if (!clientSelect || !employeeSelect || !participantsInput) return;

    function updateParticipants() {
        const current = participantsInput.value.split(',').map(s => s.trim()).filter(Boolean);
        const selectedClient = clientSelect.options[clientSelect.selectedIndex]?.text.trim();
        const selectedEmployees = Array.from(employeeSelect.selectedOptions).map(opt => opt.text.trim());

        // Excludem clientul deja adăugat de funcția ce îl pune primul
        const filteredCurrent = current.filter(name => name !== selectedClient);

        selectedEmployees.forEach(name => {
            if (!filteredCurrent.includes(name)) {
                filteredCurrent.push(name);
            }
        });

        // Adaugă clientul primul
        filteredCurrent.unshift(selectedClient);

        participantsInput.value = filteredCurrent.join(", ");
    }

    employeeSelect.addEventListener("change", updateParticipants);
}


function attachClientParticipantSync() {
    const clientSelect = document.getElementById("client-select");
    const participantsInput = document.querySelector('input[name="participants"]');

    if (!clientSelect || !participantsInput) return;

    clientSelect.addEventListener("change", function () {
        const clientName = clientSelect.options[clientSelect.selectedIndex]?.text.trim();
        let current = participantsInput.value.split(',').map(x => x.trim()).filter(Boolean);

        if (current.length > 0) {
            current.shift();
        }

        current.unshift(clientName);

        participantsInput.value = current.join(", ");
    });
}

function handleEditNoteIntro() {
    fetch("/section/notes/edit")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Error loading editable notes.");
            console.error("Edit Note Intro Error:", err);
        });
}


function handleEditNoteForm(noteId) {
    fetch(`/section/notes/edit/form/${noteId}`)
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
            attachClientDblClick();
            attachParticipantAutoFill();
            attachClientParticipantSync();
        })
        .catch(err => {
            appendBotMessage("❌ Error loading note for editing.");
            console.error("Edit Note Form Error:", err);
        });
}

document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "continue-edit-note") {
        const select = document.getElementById("note-to-edit");
        const selectedNoteId = select ? select.value : null;

        if (selectedNoteId) {
            handleEditNoteForm(selectedNoteId);
        } else {
            appendBotMessage("⚠️ Please select a note to edit first.");
        }
    }
});

document.addEventListener("change", function (e) {
    if (e.target && e.target.id === "note-to-edit") {
        const selected = e.target.value;
        const button = document.querySelector("#continue-edit-note");
        if (button) {
            button.disabled = !selected;
        }
    }
});


function handleDeleteNoteIntro() {
    fetch("/section/notes/delete")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);

            setTimeout(() => {
                const select = document.getElementById("note-to-delete");
                const button = document.getElementById("continue-delete-note");

                if (button) {
                    button.disabled = true;
                }

                if (select && button) {
                    select.addEventListener("change", function () {
                        button.disabled = !select.value;
                    });
                }
            }, 100);
        })
        .catch(err => {
            appendBotMessage("❌ Error loading delete options.");
            console.error("Delete Note Intro Error:", err);
        });
}

function handleDeleteConfirm(noteId) {
    fetch(`/section/notes/delete/confirm/${noteId}`)
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Error loading delete confirmation.");
            console.error("Delete Note Confirm Error:", err);
        });
}

function handleDeleteFinal(noteId) {
    fetch(`/section/notes/delete/final/${noteId}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Failed to delete the note.");
            console.error("Delete Note Final Error:", err);
        });
}

function handleDeleteCancel() {
    fetch("/section/notes/delete/cancel")
        .then(res => res.json())
        .then(data => {
            appendBotMessage(data.html);
        })
        .catch(err => {
            appendBotMessage("❌ Cancel action failed.");
            console.error("Delete Note Cancel Error:", err);
        });
}

document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "continue-delete-note") {
        const select = document.getElementById("note-to-delete");
        const selectedNoteId = select ? select.value : null;

        if (selectedNoteId) {
            handleDeleteConfirm(selectedNoteId);
        } else {
            appendBotMessage("⚠️ Please select a note to delete first.");
        }
    }
});



document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.getAttribute("data-action");

    switch (action) {
        case "notes-intro":
            handleNotesIntro();
            break;
        case "view-notes":
            handleViewNotes();
            break;
        case "add-note":
            handleAddNote();
            break;
        case "edit-note":
            handleEditNoteIntro();
            break;
        case "delete-note":
            handleDeleteNoteIntro();
            break;
        case "confirm-delete":
            const confirmId = btn.getAttribute("data-id");
            if (confirmId) {
                handleDeleteFinal(confirmId);
            }
            break;
        case "cancel-delete":
            handleDeleteCancel();
            break;
        case "exit-notes":
            appendUserMessage("🚪 Exit to Main Menu");
            handleExitNotes();
            break;
    }
});

document.addEventListener("change", function (e) {
    const select = e.target;
    const value = select.value;

    if (select.id === "notes-followup-select") {
        switch (value) {
            case "view-notes":
                appendUserMessage("🔍 View Notes");
                handleViewNotes();
                break;
            case "add-note":
                appendUserMessage("➕ Add Note");
                handleAddNote();
                break;
            case "edit-note":
                appendUserMessage("✏️ Edit Note");
                handleEditNoteIntro();
                break;
            case "delete-note":
                appendUserMessage("🗑️ Delete Note");
                handleDeleteNoteIntro();
                break;
            case "exit-notes":
                appendUserMessage("🚪 Exit");
                handleExitNotes();
                break;
        }

        // Resetăm dropdown-ul la valoarea inițială
        select.selectedIndex = 0;
    }
});


//###################################################################################
//###############################     OTHER TOOLS    ################################
//###################################################################################

function handleOtherToolsAction(action) {
    switch (action) {
        case "other-tools-intro":
            fetch("/section/tools")
                .then(res => res.json())
                .then(data => {
                    appendBotMessage(data.html);
                })
                .catch(err => {
                    appendBotMessage("❌ Error loading Other Tools section.");
                    console.error("Other Tools Intro Error:", err);
                });
            break;

        case "focus-mode":
            appendUserMessage("⏳ Focus Mode");
            fetch("/section/tools/focus-mode/start")
            .then(res => res.json())
            .then(data => {
                appendBotMessage(data.html);

                setTimeout(() => {
                    const containers = document.querySelectorAll(".focus-timer-box");
                    const latest = containers[containers.length - 1];
                    if (!latest) return;

                    const focusSlider = latest.querySelector("input[name='focus_duration']");
                    const statusText = latest.querySelector(".focus-status");

                    if (focusSlider && statusText) {
                        const updateLabel = () => {
                            const value = focusSlider.value;
                            statusText.innerHTML = `🧘 Focus Mode — Boost your productivity with a <b>${value}-minute focus session</b>`;
                        };

                        focusSlider.addEventListener("input", updateLabel);
                        updateLabel();
                    }

                }, 100);
            })
            break;

        case "generate-message":
        appendUserMessage("✉️ Generate Client Message");
        fetch("/section/tools/message-generator")
            .then(res => res.json())
            .then(data => {
                appendBotMessage(data.html);

                const checkFormReady = setInterval(() => {
                    const name = document.getElementById("client_name");
                    const email = document.getElementById("client_email");
                    const btn = document.getElementById("generate-email-btn");

                    if (name && email && btn) {
                        clearInterval(checkFormReady);

                        const validate = () => {
                            const isNameValid = name.value.trim().length > 0;
                            const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
                            btn.disabled = !(isNameValid && isEmailValid);
                        };

                        name.addEventListener("input", validate);
                        email.addEventListener("input", validate);
                        validate();
                    }
                }, 50);
            })
            .catch(err => {
                appendBotMessage("❌ Failed to load message generator.");
                console.error("Message Generator Error:", err);
            });
        break;


        case "daily-tip":
            appendUserMessage("🧠 Micro-learning Tip of the Day");
            fetch("/section/tools/tip-of-day")
                .then(res => res.json())
                .then(data => {
                    appendBotMessage(data.html);
                })
                .catch(err => {
                    appendBotMessage("❌ Failed to load tip of the day.");
                    console.error("Tip of the Day Error:", err);
                });
            break;

        case "exit-other-tools":
            appendUserMessage("🚪 Exit to Main Menu");
            fetch("/main-menu")
                .then(res => res.json())
                .then(data => {
                    appendBotMessage(data.html);
                })
                .catch(err => {
                    appendBotMessage("⚠️ Could not return to main menu.");
                    console.error("Exit Other Tools Error:", err);
                });
            break;

        case "start-break":
            const breakMinutes = parseInt(e.target.getAttribute("data-break-minutes")) || 5;
            const targetId = currentActiveFocusTimerId || "focus-timer-static";

            const parent = e.target.closest(".chatbot-message");
            if (parent) parent.remove();

            startBreakCountdown(breakMinutes, targetId);
            break;


        default:
            appendBotMessage("⚠️ Unknown tool selected.");
            break;
    }
}

document.addEventListener("change", function (e) {
    const dropdown = e.target;

    if (dropdown && dropdown.id === "focus-followup-select") {
        const selectedValue = dropdown.value;

        const resetDropdown = () => {
            setTimeout(() => {
                dropdown.selectedIndex = 0;
            }, 100); // mic delay ca să nu „taie” execuția fetch
        };

        switch (selectedValue) {
            case "focus-mode":
                appendUserMessage("⏳ Focus Mode");
                fetch("/section/tools/focus-mode/start")
                    .then(res => res.json())
                    .then(data => {
                        document.querySelectorAll(".focus-timer-box").forEach(el => el.remove());
                        appendBotMessage(data.html);
                        resetDropdown();

                        setTimeout(() => {
                            const containers = document.querySelectorAll(".focus-timer-box");
                            const latest = containers[containers.length - 1];
                            if (!latest) return;

                            const focusSlider = latest.querySelector("input[name='focus_duration']");
                            const statusText = latest.querySelector(".focus-status");

                            if (focusSlider && statusText) {
                                const updateLabel = () => {
                                    const value = focusSlider.value;
                                    statusText.innerHTML = `🧘 Focus Mode — Boost your productivity with a <b>${value}-minute focus session</b>`;
                                };

                                focusSlider.addEventListener("input", updateLabel);
                                updateLabel();
                            }
                        }, 100);
                    });
                break;

            case "tip-of-the-day":
                fetch("/section/tools/tip-of-the-day")
                    .then(res => res.json())
                    .then(data => {
                        appendBotMessage(data.html);
                        resetDropdown();
                    })
                    .catch(err => {
                        appendBotMessage("❌ Failed to load tip of the day.");
                        console.error(err);
                        resetDropdown();
                    });
                break;

            case "message-generator":
            appendUserMessage("✉️ Generate Client Message");
            fetch("/section/tools/message-generator")
                .then(res => res.json())
                .then(data => {
                    appendBotMessage(data.html);

                    const checkFormReady = setInterval(() => {
                        const name = document.getElementById("client_name");
                        const email = document.getElementById("client_email");
                        const btn = document.getElementById("generate-email-btn");

                        if (name && email && btn) {
                            clearInterval(checkFormReady);

                            const validate = () => {
                                const isNameValid = name.value.trim().length > 0;
                                const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
                                btn.disabled = !(isNameValid && isEmailValid);
                            };

                            name.addEventListener("input", validate);
                            email.addEventListener("input", validate);
                            validate();
                        }
                    }, 50);

                    resetDropdown();
                })
                .catch(err => {
                    appendBotMessage("❌ Failed to load message generator.");
                    console.error(err);
                    resetDropdown();
                });
            break;


            case "exit-main-menu":
                appendUserMessage("🚪 Exit to Main Menu");
                fetch("/main-menu")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
            break;

            default:
                resetDropdown();
                break;
        }
    }
});



document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.getAttribute("data-action");

    if (
        [
            "other-tools-intro",
            "focus-mode",
            "generate-message",
            "daily-tip",
            "exit-other-tools"
        ].includes(action)
    ) {
        handleOtherToolsAction(action);
    }
});

document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "start-focus-mode") {
        const form = document.getElementById("focus-mode-settings-form");
        const focusDuration = parseInt(form.querySelector("input[name='focus_duration']").value);
        const breakDuration = parseInt(form.querySelector("input[name='break_duration']").value);

        window.lastFocusSettings = { focusDuration, breakDuration };

        // 🔁 Șterge ultimul mesaj de utilizator dacă este "Start Focus Mode"
        const userMessages = document.querySelectorAll(".message[data-role='user']");
        if (userMessages.length > 0) {
            const lastUserMessage = userMessages[userMessages.length - 1];
            if (lastUserMessage.innerText.trim().includes("Start Focus Mode")) {
                lastUserMessage.remove();
            }
        }

        const startSessionFollowup = document.querySelector("[data-id='start-session-followup']");
        if (startSessionFollowup) {
            const messageWrapper = startSessionFollowup.closest(".message");
            if (messageWrapper) messageWrapper.remove();
            else startSessionFollowup.remove();
        }

        showFocusTimer(focusDuration, breakDuration);

    }
});

document.addEventListener("click", function (e) {
    if (e.target && e.target.matches("[data-action='start-new-focus-session']")) {
        const { focusDuration, breakDuration } = window.lastFocusSettings || { focusDuration: 25, breakDuration: 5 };

        // 🧼 Elimină timerul vechi
        const oldTimerBox = document.querySelector(".focus-timer-box");
        if (oldTimerBox) oldTimerBox.remove();

        // 🧹 Elimină follow-up
        const sessionFollowup = document.querySelector("[data-id='start-session-followup']");
        if (sessionFollowup) {
            const wrapper = sessionFollowup.closest(".message");
            if (wrapper) wrapper.remove();
            else sessionFollowup.remove();
        }

        // 🧹 Elimină și ultimul mesaj de utilizator
        const userMessages = document.querySelectorAll(".message[data-role='user']");
        if (userMessages.length > 0) {
            const lastUserMessage = userMessages[userMessages.length - 1];
            if (lastUserMessage.innerText.trim().includes("Start New Session")) {
                lastUserMessage.remove();
            }
        }

        window.focusSessionAborted = false;
        removeFollowupMessages();

        // 🔁 Pornește un nou timer curat
        showFocusTimer(focusDuration, breakDuration);
    }
});






let currentActiveFocusTimerId = null;

function showFocusTimer(focusMinutes, breakMinutes) {
    const uniqueId = `focus-timer-${Date.now()}`;
    const html = `
        <div class="focus-timer-box" id="${uniqueId}">
            <div class="circle-wrapper">
                <svg class="circle-timer" width="180" height="180">
                    <circle class="circle-bg" r="80" cx="90" cy="90" />
                    <circle class="circle-progress" r="80" cx="90" cy="90"
                        stroke="#00c6ff"
                        stroke-dasharray="${2 * Math.PI * 80}"
                        stroke-dashoffset="0"
                        transform="rotate(-90 90 90)" />
                </svg>
                <div class="circle-text" id="${uniqueId}-time">00:00</div>
            </div>
            <p class="focus-status">🧘 Focus Mode — Stay sharp and avoid distractions</p>
            <div class="focus-buttons">
                <button id="${uniqueId}-pause" class="focus-btn blue">⏸️ Pause</button>
                <button id="${uniqueId}-exit" class="focus-btn gray">🔙 Exit</button>
            </div>
        </div>
    `;
    appendBotMessage(html);

    const container = document.getElementById(uniqueId);
    const timeEl = container.querySelector(".circle-text");
    const ring = container.querySelector(".circle-progress");
    const statusEl = container.querySelector(".focus-status");

    let totalSeconds = focusMinutes * 60;
    let remainingSeconds = totalSeconds;
    let paused = false;

    timeEl.textContent = `${String(focusMinutes).padStart(2, '0')}:00`;
    statusEl.innerHTML = "🧘 Focus Mode — Stay sharp and avoid distractions";
    ring.style.strokeDashoffset = 0;

    clearInterval(container.timerId); // 💣 oprește orice timer anterior

    const interval = setInterval(() => {
        if (paused) return;

        const mins = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
        const secs = String(remainingSeconds % 60).padStart(2, '0');
        timeEl.textContent = `${mins}:${secs}`;

        const progress = remainingSeconds / totalSeconds;
        const offset = (1 - progress) * 2 * Math.PI * 80;
        ring.style.strokeDashoffset = offset;

        if (remainingSeconds > 0) {
            remainingSeconds--;
        } else {
            clearInterval(interval);
            container.timerId = null;

            appendBotMessage(`
                <div data-id="break-followup">
                    ⏰ <b>Time’s up!</b> Take a ${breakMinutes}-minute break?<br><br>
                    <div class="focus-followup-buttons">
                        <button class="workflow-button" data-action="start-break" data-break-minutes="${breakMinutes}" data-target-id="${container.id}">☕ Take Break</button>
                        <button class="workflow-button" data-action="start-new-focus-session">🔁 Start New Session</button>
                    </div>
                </div>
            `);
        }
    }, 1000);

    container.timerId = interval;

    const pauseBtn = container.querySelector(`#${container.id}-pause`);
    const exitBtn = container.querySelector(`#${container.id}-exit`);

    pauseBtn.onclick = () => {
        paused = !paused;
        pauseBtn.innerHTML = paused ? "▶️ Resume" : "⏸️ Pause";
    };

    exitBtn.onclick = () => {
        clearInterval(interval);
        appendUserMessage("🔙 Exit Focus Mode");
        fetch("/section/tools/focus-mode/followup")
            .then(res => res.json())
            .then(data => appendBotMessage(data.html));
    };
}


function removeFollowupMessages() {
    const followups = document.querySelectorAll("[data-id='break-followup'], [data-id='start-new-focus-session']");
    followups.forEach(followup => {
        const wrapper = followup.closest(".message");
        if (wrapper) wrapper.remove();
        else followup.remove();
    });
}




function startBreakCountdown(breakMinutes, targetId) {
    const container = document.getElementById(targetId);
    if (!container) return;

    const timeEl = container.querySelector(".circle-text");
    const ring = container.querySelector(".circle-progress");
    const statusEl = container.querySelector(".focus-status");

    const breakSeconds = breakMinutes * 60;
    let remaining = breakSeconds;

    if (timeEl) timeEl.textContent = `${String(breakMinutes).padStart(2, '0')}:00`;
    if (statusEl) statusEl.innerHTML = "☕ Break Time — Relax and recharge";

    const totalCircumference = 2 * Math.PI * 80;
    if (ring) ring.style.strokeDashoffset = 0;

    const interval = setInterval(() => {
        const mins = String(Math.floor(remaining / 60)).padStart(2, '0');
        const secs = String(remaining % 60).padStart(2, '0');
        if (timeEl) timeEl.textContent = `${mins}:${secs}`;

        const progress = remaining / breakSeconds;
        const offset = (1 - progress) * totalCircumference;
        if (ring) ring.style.strokeDashoffset = offset;

        if (remaining > 0) {
            remaining--;
        } else {
            clearInterval(interval);
            appendBotMessage(`
                <div data-id="start-session-followup">
                    ✅ <b>Break’s over!</b> Ready to dive back in?<br><br>
                    <div class="focus-followup-buttons">
                        <button class="workflow-button" data-action="start-new-focus-session">🔁 Start New Session</button>
                    </div>
                </div>
            `);

        }
    }, 1000);
}


document.addEventListener("click", function (e) {
    if (e.target && e.target.matches("[data-action='start-break']")) {
        const breakMinutes = parseInt(e.target.getAttribute("data-break-minutes")) || 5;
        const targetId = e.target.getAttribute("data-target-id");

        startBreakCountdown(breakMinutes, targetId);

        // curățare mesaj bot + user
        const breakFollowup = document.querySelector("[data-id='break-followup']");
        if (breakFollowup) {
            const messageWrapper = breakFollowup.closest(".message");
            if (messageWrapper) messageWrapper.remove();
            else breakFollowup.remove();
        }

        const userMessages = document.querySelectorAll(".message[data-role='user']");
        if (userMessages.length > 0) {
            const lastUserMessage = userMessages[userMessages.length - 1];
            if (lastUserMessage.innerText.trim().includes("Take a Break")) {
                lastUserMessage.remove();
            }
        }
    }
});


function removeBreakFollowupMessage(triggerText) {
    const breakFollowup = document.querySelector("[data-id='break-followup']");
    if (breakFollowup) {
        const wrapper = breakFollowup.closest(".message");
        if (wrapper) wrapper.remove();
        else breakFollowup.remove();
    }

    const userMessages = document.querySelectorAll(".message[data-role='user']");
    if (userMessages.length > 0) {
        const lastUserMessage = userMessages[userMessages.length - 1];
        if (lastUserMessage.innerText.trim().includes(triggerText)) {
            lastUserMessage.remove();
        }
    }
}

window.focusSessionAborted = false;

document.addEventListener("click", function (e) {
    if (e.target && e.target.matches("button.focus-btn.gray")) {
        const btn = e.target;
        const id = btn.id;

        if (id && id.endsWith("-exit")) {
            window.focusSessionAborted = true;

            const followups = document.querySelectorAll("[data-id='start-new-focus-session'], [data-id='break-followup']");
            followups.forEach(f => {
                const wrapper = f.closest(".message");
                if (wrapper) wrapper.remove();
                else f.remove();
            });

            const userMessages = document.querySelectorAll(".message[data-role='user']");
            if (userMessages.length > 0) {
                const lastUser = userMessages[userMessages.length - 1];
                const txt = lastUser.innerText.trim();
                if (txt.includes("Start New Session") || txt.includes("Take a Break")) {
                    lastUser.remove();
                }
            }

            const oldTimers = document.querySelectorAll(".focus-timer-container");
            oldTimers.forEach(timer => timer.remove());

            console.log("Focus session aborted. Timer removed.");
        }
    }
});


function onFocusEnd() {
    if (window.focusSessionAborted) return;
    showBotMessageAfterFocus();
}

function onBreakEnd() {
    if (window.focusSessionAborted) return;
    showBotMessageAfterBreak();
}

document.addEventListener("click", function (e) {
    if (e.target && e.target.matches("button.start-focus-btn")) {
        const focusId = e.target.dataset.focusId;

        const focusSlider = document.querySelector(`#${focusId}-focus-range`);
        const breakSlider = document.querySelector(`#${focusId}-break-range`);

        const focusDuration = focusSlider ? parseInt(focusSlider.value) : 25;
        const breakDuration = breakSlider ? parseInt(breakSlider.value) : 5;

        window.lastFocusSettings = { focusDuration, breakDuration };
        window.focusSessionAborted = false;

        removeFollowupMessages();

        showFocusTimer(focusDuration, breakDuration);

    }
});

function setupGlobalEmailFormValidation() {
    document.addEventListener("input", function (e) {
        const nameInput = document.getElementById("client_name");
        const emailInput = document.getElementById("client_email");
        const generateBtn = document.getElementById("generate-email-btn");

        if (!nameInput || !emailInput || !generateBtn) return;

        const isNameValid = nameInput.value.trim().length > 1;
        const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim());

        generateBtn.disabled = !(isNameValid && isEmailValid);
    });
}

document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "generate-email-btn") {
        e.preventDefault();

        const name = document.getElementById("client_name").value.trim();
        const email = document.getElementById("client_email").value.trim();

        if (!name || !email) {
            appendBotMessage("⚠️ Please enter both client name and email.");
            return;
        }

        const data = {
            client_name: name,
            client_email: email,
            message_type: document.getElementById("message_type").value,
            emotion_tone: document.getElementById("emotion_tone").value,
            client_gender: document.getElementById("client_gender").value,
            message_context: document.getElementById("message_context").value,
            message_goal: document.getElementById("message_goal").value,
            subject: document.getElementById("subject").value.trim(),
            extra_info: document.getElementById("extra_info").value.trim()
        };


        fetch("/section/tools/message-generator/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.email_html) {
                appendBotMessage(result.email_html);

                setTimeout(() => {
                    const sendBtn = document.getElementById("send-email-btn");
                    const editBtn = document.getElementById("edit-email-btn");

                    if (sendBtn) {
                        sendBtn.addEventListener("click", () => {
                            const editable = document.getElementById("editable-email-body");
                            const content = editable?.innerHTML || "";

                            // Încerci să extragi subject-ul din corp (prima linie bold)
                            const subjectMatch = content.match(/<b>Subject:<\/b>\s*(.*?)<br>/i);
                            const subjectText = subjectMatch ? subjectMatch[1].trim() : "No Subject";

                            const toEmail = document.getElementById("client_email")?.value || "";

                            if (!toEmail || !subjectText || !content) {
                                appendBotMessage("❌ Cannot send email. Missing data.");
                                return;
                            }

                            fetch("/section/tools/message-generator/send", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    client_email: toEmail,
                                    subject: subjectText,
                                    body_html: content
                                })
                            })
                            .then(res => res.json())
                            .then(result => {
                                if (result.status === "success") {
                                    appendUserMessage("✅ Email sent.");
                                    appendBotMessage("📨 Your email was sent successfully to <b>" + toEmail + "</b>.");
                                    fetch("/section/tools/focus-mode/followup")
                                    .then(res => res.json())
                                    .then(data => {
                                        if (data.html) {
                                            appendBotMessage(data.html);
                                        }
                                    })
                                  .catch(err => {
                                      appendBotMessage("⚠️ Failed to load follow-up options.");
                                      console.error("Follow-up fetch error:", err);
                                  });
                                } else {
                                    appendBotMessage("❌ Failed to send email: " + result.message);
                                }
                            })
                            .catch(err => {
                                appendBotMessage("❌ Error sending email.");
                                console.error("Send Email Error:", err);
                            });
                        });
                    }

                    if (editBtn) {
                        editBtn.addEventListener("click", () => {
                            const editable = document.getElementById("editable-email-body");
                            if (editable) {
                                editable.setAttribute("contenteditable", "true");
                                editable.focus();
                                editable.style.outline = "2px dashed #4a90e2";
                                appendBotMessage("✏️ You can now edit the email. Click anywhere to start typing.");
                            }

//                            editBtn.textContent = "💾 Save Email";
                            editBtn.id = "save-edited-email-btn";

                            editBtn.addEventListener("click", () => {
                                editable.setAttribute("contenteditable", "false");
                                editable.style.outline = "none";
                                appendBotMessage("✅ Email updated. Ready to send.");
                            }, { once: true });
                        });
                    }
                }, 100);
            } else {
                appendBotMessage("❌ Failed to generate email.");
            }
        })
        .catch(err => {
            appendBotMessage("❌ Failed to generate email.");
            console.error("Generate Email Error:", err);
        });
    }

    if (e.target && e.target.id === "cancel-email-btn") {
    e.preventDefault();

    appendBotMessage("❌ Email composition cancelled.");

    // 🧼 Reset all fields
    const fieldsToClear = [
        "client_name",
        "client_email",
        "message_type",
        "emotion_tone",
        "client_gender",
        "message_context",
        "message_goal",
        "subject",
        "extra_info"
    ];

    fieldsToClear.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });

    fetch("/section/tools/focus-mode/followup")
        .then(res => res.json())
        .then(data => {
            if (data.html) {
                appendBotMessage(data.html);
            }
        })
        .catch(err => {
            appendBotMessage("⚠️ Failed to load follow-up options.");
            console.error("Cancel Email Followup Error:", err);
        });
    }
});


setupGlobalEmailFormValidation();





















//###################################################################################
//###############################    EXIT SECTION    ################################
//###################################################################################

document.addEventListener("change", function (e) {
    // dropdown principal (meniu principal)
    if (e.target && e.target.classList.contains("followup-select")) {
        const selected = e.target.value;

        // Resetăm selecția după scurt timp
        setTimeout(() => {
            e.target.selectedIndex = 0;
        }, 100);

        switch (selected) {
            case "workflow":
                appendUserMessage("🕘 Daily Workflow");
                fetch("/section/workflow")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "clients":
                appendUserMessage("👥 Client Management");
                fetch("/section/clients")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "reminders":
                appendUserMessage("🔁 Smart Reminders");
                fetch("/section/reminders")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

//            case "reports":
//                appendUserMessage("📈 Sales Reports");
//                fetch("/sales-reports")
//                    .then(res => res.json())
//                    .then(data => appendBotMessage(data.html));
//                break;
            case "reports":
                appendUserMessage("📈 Sales Reports");
                fetch("/sales-reports", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ employee_id: 51 })
                })
                .then(res => res.json())
                .then(data => appendBotMessage(data.html));
                break;

            case "notes":
                appendUserMessage("📝 Interaction Notes");
                fetch("/section/notes")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;

            case "extras":
                appendUserMessage("🛠️ Other Tools");
                fetch("/section/tools")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                break;
            case "exit":
                appendUserMessage("📕 Exit");
                fetch("/exit")
                    .then(res => res.json())
                    .then(data => appendBotMessage(data.html));
                return;
        }
    }
});

function resetConversation() {
    const allMessages = document.querySelectorAll(".bot-message, .user-message, .final-message, .option-button, .email-preview, .form-group, .center-options");
    allMessages.forEach(el => el.remove());

    const dropdown = document.getElementById("section-select");
    if (dropdown) dropdown.remove();

    appendMainOptions();
}

document.addEventListener("click", function (e) {
    if (e.target && e.target.id === "start-new-chat") {
        resetConversation();
    }
});



//const clearChat = () => {
//    const chatContainer = document.querySelector(".chat-container");
//    if (chatContainer) {
//        chatContainer.innerHTML = "";
//    }
//};
//
//const waveText = "⏳ Starting a new session...";
//const animatedHTML = `
//  <div class="wave-text-container">
//    ${[...waveText].map((char, i) => `<span class="wave-letter" style="animation-delay:${i * 0.05}s">${char}</span>`).join("")}
//  </div>
//`;
//
//document.addEventListener("click", function (e) {
//    if (e.target && e.target.id === "start-new-chat") {
//        clearChat();
//        appendBotMessage(animatedHTML);
//        setTimeout(() => {
//            appendMainOptions();
//        }, 600);
//    }
//});