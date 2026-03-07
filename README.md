# Cura AI
A Safety-Aware Multi-Agent Healthcare Assistant

---

## 📌 Overview

The **Cura AI** is a full-stack AI-powered system that integrates multiple intelligent agents to provide:

- Symptom guidance
- Medicine reminder scheduling
- Drug interaction risk analysis
- Medical report analysis from images (OCR-based)
- Layman-friendly health explanations
- Multi-user authentication and persistent memory

The system is designed as a **safety-aware, memory-augmented, multi-agent architecture** suitable for healthcare AI research.

---

## 🏗 System Architecture

The project follows a **Multi-Agent Orchestration Model**.

### Core Agents

1. **Coordinator Agent**
   - Routes user requests based on detected intent.
   - Handles chat, reminders, drug interactions, and report analysis.

2. **Chat Agent**
   - Handles symptom-related and general health queries.
   - Uses contextual memory for personalized responses.

3. **Reminder Agent**
   - Extracts medicine name and time.
   - Performs safety check before scheduling.
   - Uses risk-based gating:
     - Low → Schedule
     - Moderate → Schedule with warning
     - High → Block scheduling

4. **Drug Interaction Agent**
   - Analyzes interactions among stored medicines.
   - Returns risk level (Low / Moderate / High).
   - Ensures safe reminder scheduling.

5. **Report Agent**
   - Uses Tesseract OCR to extract text from medical report images.
   - Converts technical medical reports into layman-friendly summaries.
   - Removes markdown, lab ranges, and technical jargon.
   - Provides simplified health explanation with recommendation.

---

## 🧠 Memory Design

### Persistent Memory (SQLite)
- Users (id, email, password, name)
- Medicines
- Reminders

### Short-Term Context
- Stored medicines retrieved per session
- Used for contextual reasoning and interaction checks

### Safety Logic
- Drug interaction verification before database insertion
- Conditional scheduling based on risk classification

---

## 🔐 Authentication

- Secure Register & Login
- Password hashing using bcrypt
- Multi-user support
- Session stored via localStorage (frontend)

---

## 🩺 Features

- AI-powered symptom explanation
- Medicine tracking
- Reminder scheduling
- Drug interaction detection
- Risk-based execution gating
- OCR-based medical report analysis
- Layman health summary generation
- Persistent user memory
- Modern chat-based UI

---

## 🛠 Tech Stack

### Backend
- Flask
- SQLite
- bcrypt
- pytesseract (OCR)
- Groq LLM API
- Custom Multi-Agent Orchestration

### Frontend
- HTML
- CSS
- JavaScript
- Modern chat UI
- Local storage session management

---

## 📂 Project Structure

```
cura-ai/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── coordinator_agent.py      # Routes user intent to appropriate agent
│   │   ├── chat_agent.py             # Handles symptom & health queries
│   │   ├── reminder_agent.py         # Schedules reminders with safety checks
│   │   ├── interaction_agent.py      # Performs drug interaction analysis
│   │   └── report_agent.py           # Analyzes medical reports via OCR + LLM
│   │
│   ├── tools/
│   │   └── report_image_processor.py # Extracts text from report images (Tesseract OCR)
│   │
│   ├── memory/
│   │   └── memory_manager.py         # Handles user medicine memory retrieval
│   │
│   ├── database/
│   │   └── db.py                     # SQLite database connection & schema
│   │
│   ├── uploads/                      # Uploaded medical report images
│   │
│   ├── scheduler.py                  # Background reminder scheduler
│   ├── app.py                        # Main Flask application entry point
│   ├── requirements.txt              # Backend dependencies
│   └── .env                          # Environment variables (API keys)
│
├── frontend/
│   │
│   ├── pages/
│   │   ├── login.html                # User authentication page
│   │   └── dashboard.html            # Main chat interface
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css             # UI styling
│   │   │
│   │   └── js/
│   │       └── script.js             # Frontend logic & API calls
│   │
│   └── (served via http.server)      # Local frontend server
│
├── README.md                         # Project documentation
└── .gitignore                        # Ignored files
```

## 🚀 Setup Instructions

### 1️⃣ Clone Repository

git clone <repository-url>  
cd cura-ai

---

### 2️⃣ Backend Setup

cd backend  

python -m venv venv  
venv\Scripts\activate      # Windows  

pip install -r requirements.txt  

Create a `.env` file inside backend:

GROQ_API_KEY=your_groq_api_key_here  

Run backend:

python app.py  

Backend will start at:  
http://127.0.0.1:5000  

---

### 3️⃣ Frontend Setup

cd frontend  

python -m http.server 5500  

Open in browser:

http://localhost:5500/pages/login.html  

---

## 🔐 Authentication Flow

1. Register with email and password  
2. Password is securely hashed using bcrypt  
3. Login returns user_id  
4. user_id is stored in localStorage  
5. All chat and reminder requests use this user_id  

---

## 🧠 System Workflow

1. User sends message or uploads report  
2. Coordinator Agent detects intent  
3. Request is routed to:
   - ChatAgent
   - ReminderAgent
   - InteractionAgent
   - ReportAgent
4. Persistent memory is retrieved from SQLite  
5. Safety checks performed if needed  
6. Response returned to frontend  

---

## 🩺 Drug Interaction Safety Logic

Before scheduling a reminder:

1. Retrieve stored medicines  
2. Add new medicine to temporary list  
3. Send list to InteractionAgent  
4. Risk classified as:
   - Low → Schedule normally  
   - Moderate → Schedule with warning  
   - High → Block scheduling  
5. Save reminder only if safe  

This ensures conditional execution in healthcare context.

---

## 📷 OCR Configuration

Install Tesseract OCR.

Ensure correct path in:

backend/tools/report_image_processor.py  

Example:

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

Make sure:
- "Run as administrator" is NOT enabled for tesseract.exe

---

## 🎯 Key Features

- Multi-agent orchestration
- Intent-based routing
- Persistent medical memory
- Risk-based decision gating
- OCR-based report analysis
- Layman-friendly explanation
- Multi-user authentication
- Modern chat UI

---

## 📄 Research Focus

This project demonstrates:

- Memory-augmented LLM agents
- Safety-aware healthcare AI
- Conditional execution logic
- Agent orchestration architecture
- Risk classification for medical decisions

---

## 🧪 Future Improvements

- Vector database memory
- PDF report support
- Structured evaluation metrics
- Model comparison experiments
- Role-based healthcare deployment
- Docker containerization

---

## 👨‍💻 Author

Rahul Kadvasara  
B.Tech CSE (AIML)  
