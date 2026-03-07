class SessionMemory:
    def __init__(self):
        self.sessions = {}

    def add_message(self, user_id, role, content):
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        self.sessions[user_id].append({"role": role, "content": content})

    def get_last_messages(self, user_id, limit=5):
        return self.sessions.get(user_id, [])[-limit:]
