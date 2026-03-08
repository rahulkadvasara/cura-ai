from database.db import get_connection
from scheduler.email_service import send_email
from tools.llm_client import call_llm
from utils.logger import log_event
from utils.crypto_utils import encrypt_data

class ReminderAgent:

    def schedule_reminder(self, user_id, medicine, time_str, context):

        existing_meds = context.get("medicines", [])
        all_meds = existing_meds + [medicine]

        # Run interaction analysis
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a clinical drug interaction analyzer.\n"
                    "Given a list of medications, respond strictly in this format:\n\n"
                    "Interaction Risk: Low or Moderate or High\n"
                    "Then explain the interaction in 1-2 sentences.\n\n"
                    "Do not repeat medication lists."
                )
            },
            {
                "role": "user",
                "content": f"Medications: {all_meds}"
            }
        ]


        result = call_llm(messages)

        log_event(f"Drug interaction result: {result}")

        if "Interaction Risk: High" in result:
            return (
                "⚠ High interaction risk detected.\n"
                + result +
                "\nReminder not scheduled. Please consult a doctor."
            )

        elif "Interaction Risk: Moderate" in result:
            log_event("Moderate interaction detected, scheduling with warning.")
            warning_message = (
                "⚠ Moderate interaction risk detected.\n"
                + result +
                "\nReminder scheduled, but please consult a healthcare professional."
            )
        else:
            warning_message = None


        # If safe, store medicine and reminder
        conn = get_connection()
        cursor = conn.cursor()

        # cursor.execute(
        #     "INSERT INTO medicines (user_id, name) VALUES (?, ?)",
        #     (user_id, medicine)
        # )

        # cursor.execute(
        #     "INSERT INTO reminders (user_id, medicine, time) VALUES (?, ?, ?)",
        #     (user_id, medicine, time_str)
        # )

        # cursor.execute(
        #     "INSERT INTO medicines (user_id, name) VALUES (?, ?)",
        #     (user_id, encrypt_data(medicine))
        # )

        cursor.execute(
            "SELECT 1 FROM medicines WHERE user_id=? AND name=?",
            (user_id, medicine)
        )

        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                "INSERT INTO medicines (user_id, name) VALUES (?, ?)",
                (user_id, medicine)
            )

        cursor.execute(
            "INSERT INTO reminders (user_id, medicine, time) VALUES (?, ?, ?)",
            (user_id, encrypt_data(medicine), time_str)
        )

        conn.commit()
        conn.close()

        if warning_message:
            return warning_message

        log_event(f"Reminder safely scheduled for {medicine} at {time_str}")

        return f"Reminder set for {medicine} at {time_str}."
