from flask import Flask, request, jsonify
from flask_cors import CORS
from memory.memory_manager import MemoryManager
from agents.coordinator_agent import CoordinatorAgent
from scheduler.reminder_scheduler import start_scheduler
from database.db import init_db, get_connection
from werkzeug.utils import secure_filename
import os
import traceback
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Upload configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Initialize memory and coordinator
memory_manager = MemoryManager()
coordinator = CoordinatorAgent(memory_manager)
start_scheduler()



# -----------------------------
# Helper Functions
# -----------------------------

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Health Check Endpoint
# -----------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Backend running"}), 200


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid JSON input"}), 400

        data = request.get_json()

        user_id = data.get("user_id", 1)
        user_input = data.get("message")
        image_path = data.get("image_path")

        if not user_input and not image_path:
            return jsonify({"error": "Message or image required"}), 400

        response = coordinator.route(user_id, user_input, image_path)

        return jsonify({"response": response})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


# -----------------------------
# File Upload Endpoint
# -----------------------------

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        return jsonify({"path": path})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Upload failed"}), 500
    

@app.route("/create_user", methods=["POST"])
def create_user():
    from database.db import get_connection

    data = request.json
    email = data.get("email")
    name = data.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, name) VALUES (?, ?)",
            (email, name)
        )
        conn.commit()

        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        # If email already exists, fetch existing user
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        user_id = user["id"]

    finally:
        conn.close()

    return jsonify({"user_id": user_id})


import bcrypt

@app.route("/register", methods=["POST"])
def register():

    from database.db import get_connection

    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
            (email, hashed_pw, name)
        )
        conn.commit()
        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    conn.close()

    return jsonify({"user_id": user_id})

@app.route("/login", methods=["POST"])
def login():

    from database.db import get_connection

    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return jsonify({"user_id": user["id"]})

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/get_reminders", methods=["GET"])
def get_reminders():
    user_id = int(request.args.get("user_id"))

    conn = get_connection()
    reminders = conn.execute(
        "SELECT id, medicine, time FROM reminders WHERE user_id = ? ORDER BY time ASC",
        (user_id,)
    ).fetchall()
    conn.close()

    return jsonify({
        "reminders": [
            {
                "id": r["id"],
                "medicine": r["medicine"],
                "time": r["time"]
            }
            for r in reminders
        ]
    })



@app.route("/delete_reminder/<int:reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):

    conn = get_connection()
    conn.execute(
        "DELETE FROM reminders WHERE id = ?",
        (reminder_id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True})

# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
   app.run(debug=False)


