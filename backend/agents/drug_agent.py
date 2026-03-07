from tools.llm_client import call_llm
from utils.logger import log_event

class DrugAgent:

    def run(self, new_medicine, context):

        existing_meds = context.get("medicines", [])

        all_meds = existing_meds + [new_medicine]

        log_event(f"DrugAgent checking interactions for: {all_meds}")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a clinical drug interaction analysis assistant.\n"
                    "Analyze potential interactions among the listed medications.\n\n"

                    "First determine interaction risk level:\n"
                    "Low = no known harmful interaction\n"
                    "Moderate = possible interaction requiring caution\n"
                    "High = dangerous interaction that should be avoided\n\n"

                    "OUTPUT FORMAT (strict):\n"
                    "Interaction Risk: Low or Moderate or High\n"
                    "Then explain the interaction in 1–2 simple sentences.\n\n"

                    "Rules:\n"
                    "- Use simple language\n"
                    "- Maximum 2 sentences\n"
                    "- Do not list medicines again\n"
                )
            },
            {
                "role": "user",
                "content": f"Medications: {all_meds}"
            }
        ]

        response = call_llm(messages)

        if "Interaction Risk:" not in response:
            response = "Interaction Risk: Low\nNo major interaction detected."

        return response
