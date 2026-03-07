import schedule
import time
import threading
from database.db import get_connection
from scheduler.email_service import send_email
from utils.logger import log_event


def check_reminders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reminders")
    reminders = cursor.fetchall()

    current_time = time.strftime("%I:%M %p")  # Example: "08:05 PM"

    for reminder in reminders:
        if reminder["time"] == current_time:

            # Fetch user email
            cursor.execute("SELECT email FROM users WHERE id=?",
                           (reminder["user_id"],))
            user = cursor.fetchone()

            if user:
                send_email(
                    user["email"],
                    "Medicine Reminder",
                    f"Time to take {reminder['medicine']}."
                )

                log_event(f"Reminder email sent to user {reminder['user_id']}")

    conn.close()


def start_scheduler():
    schedule.every(1).minutes.do(check_reminders)

    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
