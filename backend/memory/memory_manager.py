from memory.session_memory import SessionMemory
from memory.persistent_memory import PersistentMemory
from utils.logger import log_event

class MemoryManager:

    def __init__(self):
        self.session = SessionMemory()
        self.persistent = PersistentMemory()

    def store_user_message(self, user_id, message):
        self.session.add_message(user_id, "user", message)

    def store_assistant_message(self, user_id, message):
        self.session.add_message(user_id, "assistant", message)

    def get_context(self, user_id):
        history = self.session.get_last_messages(user_id)
        medicines = self.persistent.get_user_medicines(user_id)

        log_event(f"Memory fetched for user {user_id} | Medicines: {medicines}")

        return {
            "history": history,
            "medicines": medicines
        }
