from database.db import get_connection
from utils.crypto_utils import decrypt_data
from utils.crypto_utils import encrypt_data
from utils.hash_utils import generate_hash, verify_hash

class PersistentMemory:

    def get_user_profile(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_user_medicines(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM medicines WHERE user_id=?", (user_id,))
        meds = cursor.fetchall()

        conn.close()

        medicines = []

        for m in meds:
            try:
                medicines.append(decrypt_data(m["name"]))
            except:
                medicines.append(m["name"])  # fallback if not encrypted yet

        return medicines

    def add_medicine(self, user_id, medicine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicines (user_id, name) VALUES (?,?)",
                       (user_id, encrypt_data(medicine)))
        conn.commit()
        conn.close()

    def add_report_summary(self, user_id, summary):
        conn = get_connection()
        cursor = conn.cursor()
        summary_hash = generate_hash(summary)

        cursor.execute(
            "INSERT INTO reports (user_id, summary, hash) VALUES (?,?,?)",
            (user_id, summary, summary_hash)
        )
        conn.commit()
        conn.close()


def get_reports(self, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT summary, hash FROM reports WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    conn.close()

    reports = []

    for r in rows:

        summary = r["summary"]
        stored_hash = r["hash"]

        if not verify_hash(summary, stored_hash):
            raise Exception("⚠ Data tampering detected in medical report")

        reports.append(summary)

    return reports