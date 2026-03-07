from database.db import get_connection

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
        return [m["name"] for m in meds]

    def add_medicine(self, user_id, medicine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicines (user_id, name) VALUES (?,?)",
                       (user_id, medicine))
        conn.commit()
        conn.close()

    def add_report_summary(self, user_id, summary):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reports (user_id, summary) VALUES (?,?)",
                       (user_id, summary))
        conn.commit()
        conn.close()
