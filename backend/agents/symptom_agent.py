from tools.llm_client import call_llm

class SymptomAgent:

    def run(self, user_input, context):

        medicines = context.get("medicines", [])
        history = context.get("history", [])

        messages = [
            {
                "role": "system",
                "content": (
                        """
                        You are a safety-aware clinical decision-support assistant.

                        Respond in the exact structured format below:

                        Symptom: <short name>

                        Causes:
                        - 3–4 brief bullet points only

                        Urgency:
                        - Low or Moderate or High

                        Actions:
                        - 2–3 short practical steps

                        Emergency:
                        - 1 line on when to seek immediate medical care

                        Keep responses concise.
                        Use simple patient-friendly language.
                        No explanations.
                        No paragraphs.
                        No markdown formatting.
                        Do not repeat the user's question.
                        """
                )
            }
        ]

        if medicines:
            messages.append({
                "role": "system",
                "content": (
                    f"The patient is currently taking: {medicines}. "
                    "Consider potential interactions but do NOT repeat the medication list in the final answer."
                )
            })


        messages.extend(history)
        messages.append({"role": "user", "content": user_input})

        return call_llm(messages)
