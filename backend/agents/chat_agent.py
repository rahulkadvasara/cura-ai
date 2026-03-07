from tools.llm_client import call_llm

class ChatAgent:

    def run(self, user_input, context):
        messages = context["history"] + [
            {"role": "user", "content": user_input}
        ]

        messages.insert(0, {
            "role": "system",
            "content": "You are a helpful healthcare assistant."
        })

        return call_llm(messages)
