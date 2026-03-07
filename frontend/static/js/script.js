const BACKEND_URL = "http://127.0.0.1:5000";

/* ================= AUTH ================= */

function register() {
    fetch(`${BACKEND_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-USER-ID": userId
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
            name: "User"
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.user_id) {
            localStorage.setItem("user_id", data.user_id);
            window.location.href = "dashboard.html";
        } else {
            alert(data.error);
        }
    });
}

function login() {
    fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-USER-ID": userId
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.user_id) {
            localStorage.setItem("user_id", data.user_id);
            window.location.href = "dashboard.html";
        } else {
            alert("Invalid credentials");
        }
    });
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

/* ================= DASHBOARD ================= */

let userId = localStorage.getItem("user_id");

if (window.location.pathname.includes("dashboard.html") && !userId) {
    window.location.href = "login.html";
}

window.onload = function() {
    const saved = localStorage.getItem("chatHistory");
    if (saved) {
        document.getElementById("chat-box").innerHTML = saved;
    }
};

// function saveChat() {
//     const chatBox = document.getElementById("chat-box");
//     localStorage.setItem("chatHistory", chatBox.innerHTML);
// }


function saveChatMessage(role, content) {
    let messages = JSON.parse(localStorage.getItem("chatMessages")) || [];

    messages.push({
        role: role,
        content: content
    });

    localStorage.setItem("chatMessages", JSON.stringify(messages));
}

function clearChat() {
    localStorage.removeItem("chatHistory");
    document.getElementById("chat-box").innerHTML = "";
}

/* ================= CHAT ================= */

function sendMessage() {

    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="message user-message">
            ${message}
        </div>
    `;

    saveChatMessage("user", message);

    messageInput.value = "";

    fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-USER-ID": userId
        },
        body: JSON.stringify({
            user_id: userId,
            message: message
        })
    })
    .then(res => res.json())
    .then(data => {
        const responseText = data.response;

        let formattedResponse = "";

        /* ===== SYMPTOM FORMAT ===== */

        if (responseText.includes("Symptom:") && responseText.includes("Urgency:")) {

            const symptomMatch = responseText.match(/Symptom:\s*(.*)/i);
            const urgencyMatch = responseText.match(/Urgency:\s*(Low|Moderate|High)/i);

            const symptom = symptomMatch ? symptomMatch[1] : "Unknown";
            const urgency = urgencyMatch ? urgencyMatch[1] : "Unknown";

            let urgencyColor = "#6c757d";

            if (urgency.toLowerCase() === "low") urgencyColor = "#28a745";
            if (urgency.toLowerCase() === "moderate") urgencyColor = "#ffc107";
            if (urgency.toLowerCase() === "high") urgencyColor = "#dc3545";

            let content = responseText
                .replace(/Symptom:\s*.*?\n?/i, "")
                .replace(/Urgency:\s*(Low|Moderate|High)/i, "")
                .replace(/- /g, "\n• ");

            formattedResponse = `
                <div style="font-weight:bold;margin-bottom:6px;">
                    Symptom: ${symptom}
                </div>

                <div style="white-space:pre-line;margin-top:6px;">
                    ${content.trim()}
                </div>

                <div style="margin-top:8px;font-weight:bold;color:${urgencyColor};">
                    Urgency Level: ${urgency}
                </div>
            `;

        }

        /* ===== DRUG INTERACTION FORMAT ===== */

        else if (responseText.match(/Risk:\s*(Low|Moderate|High)/i)) {

            const riskMatch = responseText.match(/Risk:\s*(Low|Moderate|High)/i);
            const riskLevel = riskMatch[1];

            let riskColor = "#6c757d";

            if (riskLevel.toLowerCase() === "low") riskColor = "#28a745";
            if (riskLevel.toLowerCase() === "moderate") riskColor = "#ffc107";
            if (riskLevel.toLowerCase() === "high") riskColor = "#dc3545";

            let summary = responseText
                .replace(/Risk:\s*(Low|Moderate|High)/i, "")
                .replace("Summary:", "")
                .trim();

            formattedResponse = `
                <div style="font-weight:bold;color:${riskColor};margin-bottom:6px;">
                    Interaction Risk: ${riskLevel}
                </div>
                <div style="white-space:pre-line;">
                    ${summary}
                </div>
            `;
        }

        /* ===== NORMAL RESPONSE ===== */

        else {

            formattedResponse = responseText;

        }

        chatBox.innerHTML += `
            <div class="message assistant-message">
                ${formattedResponse}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

        saveChatMessage("assistant", formattedResponse);

    });
}


function loadChat() {
    const chatBox = document.getElementById("chat-box");
    const messages = JSON.parse(localStorage.getItem("chatMessages")) || [];

    chatBox.innerHTML = "";

    messages.forEach(msg => {
        chatBox.innerHTML += `
            <div class="message ${msg.role}-message">
                ${msg.content}
            </div>
        `;
    });

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* ================= UPLOAD ================= */

function uploadReport() {

    const fileInput = document.getElementById("reportFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Select a file first");
        return;
    }

    const chatBox = document.getElementById("chat-box");

    const formData = new FormData();
    formData.append("file", file);

    fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        headers: {
            "X-USER-ID": userId
        },
        body: formData
    })
    .then(res => res.json())
    .then(uploadData => {

        return fetch(`${BACKEND_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-USER-ID": userId
            },
            body: JSON.stringify({
                user_id: userId,
                message: "Analyze this report",
                image_path: uploadData.path
            })
        });

    })
    .then(res => res.json())
    .then(chatData => {

        chatBox.innerHTML += `
            <div class="message user-message">
                Uploaded report
            </div>
        `;

        saveChatMessage("user", `Uploaded report: ${file.name}`);

        const responseText = chatData.response;

        let riskLevel = "Unknown";
        let summary = responseText;

        const match = responseText.match(/Risk Level:\s*(Low|Moderate|High)/i);

        if (match) {
            riskLevel = match[1];
            summary = responseText.replace(match[0], "").trim();
        }

        let riskColor = "#6c757d";

        if (riskLevel.toLowerCase() === "low") riskColor = "#28a745";
        if (riskLevel.toLowerCase() === "moderate") riskColor = "#ffc107";
        if (riskLevel.toLowerCase() === "high") riskColor = "#dc3545";

        const formattedResponse = `
        <div style="font-weight:bold; color:${riskColor}; margin-bottom:6px;">
        Risk Level: ${riskLevel}
        </div>
        <div>${summary}</div>
        `;

        chatBox.innerHTML += `
            <div class="message assistant-message">
                ${formattedResponse}
            </div>
        `;

        saveChatMessage("assistant", formattedResponse);

        chatBox.scrollTop = chatBox.scrollHeight;

    });
}



function showChat() {
    window.onload = function() {
        loadChat();
    };
    document.getElementById("chat-box").style.display = "block";
    document.querySelector(".input-area").style.display = "flex";
    document.querySelector(".upload-area").style.display = "flex";
    document.getElementById("reminder-section").style.display = "none";
}

function showReminders() {
    console.log("Reminders clicked");

    document.getElementById("chat-box").style.display = "none";
    document.querySelector(".input-area").style.display = "none";
    document.querySelector(".upload-area").style.display = "none";
    document.getElementById("reminder-section").style.display = "block";

    fetchReminders();
}


function fetchReminders() {
    fetch(`${BACKEND_URL}/get_reminders?user_id=${userId}`, {
        headers: {
            "X-USER-ID": userId
        }
    })
    .then(res => res.json())
    .then(data => {

        const reminderList = document.getElementById("reminder-list");

        if (!data.reminders || data.reminders.length === 0) {
            reminderList.innerHTML = "<p>No reminders set.</p>";
            return;
        }

        reminderList.innerHTML = `
            <div class="reminder-container">
                <div class="reminder-title">💊 Your Reminders</div>

                <table class="reminder-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Medicine</th>
                            <th>Time</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.reminders.map((reminder, index) => `
                            <tr>
                                <td class="serial">${index + 1}</td>
                                <td>${reminder.medicine}</td>
                                <td><span class="time-badge">${reminder.time}</span></td>
                                <td>
                                    <button class="delete-btn" onclick="deleteReminder(${reminder.id})">
                                        ❌
                                    </button>
                                </td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        `;
    });
}


function getTimeBadge(time) {
    return `<span class="time-badge">${time}</span>`;
}


function deleteReminder(reminderId) {
    fetch(`${BACKEND_URL}/delete_reminder/${reminderId}`, {
        method: "DELETE",
        headers: {
            "X-USER-ID": userId
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            fetchReminders();
        }
    });
}


window.onload = function() {
    loadChat();
};

/* ================= VOICE INPUT ================= */

let recognition;
let isListening = false;

function startVoiceInput() {

    const micButton = document.querySelector(".mic-btn");

    if (!('webkitSpeechRecognition' in window)) {
        alert("Voice recognition not supported in this browser");
        return;
    }

    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;

            const messageInput = document.getElementById("message");
            // messageInput.value = transcript;
            messageInput.value = transcript;
            sendMessage();

            stopVoiceInput();
        };

        recognition.onerror = function(event) {
            console.error("Voice error:", event.error);
            stopVoiceInput();
        };

        recognition.onend = function() {
            stopVoiceInput();
        };
    }

    if (!isListening) {
        recognition.start();
        isListening = true;

        micButton.style.background = "#28a745"; // GREEN
        micButton.innerText = "🎤 Listening";
    } else {
        stopVoiceInput();
    }
}

function stopVoiceInput() {

    const micButton = document.querySelector(".mic-btn");

    if (recognition) {
        recognition.stop();
    }

    isListening = false;

    micButton.style.background = "#ff4d4f"; // RED
    micButton.innerText = "🎤";
}