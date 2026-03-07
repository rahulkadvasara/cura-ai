from tools.report_image_processor import extract_text_from_image
from tools.llm_client import call_llm

class ReportAgent:

    def run(self, image_path):
        text = extract_text_from_image(image_path)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a patient-friendly medical report analyzer.\n"
                    "Your job is to identify abnormal findings and explain them simply.\n\n"

                    "First determine a risk level:\n"
                    "Low = minor or no abnormal findings\n"
                    "Moderate = some abnormal values that may need medical attention\n"
                    "High = serious abnormal values that may indicate organ problems\n\n"

                    "OUTPUT FORMAT (strict):\n"
                    "Risk Level: Low or Moderate or High\n"
                    "Then give a short summary in simple language.\n\n"

                    "Rules:\n"
                    "- Maximum 2–3 short sentences\n"
                    "- No medical jargon\n"
                    "- Ignore patient name, age, hospital, dates\n"
                    "- Only mention abnormal findings\n"
                )
            },
            {
                "role": "user",
                "content": f"Explain this report simply:\n{text}"
            }
        ]



        return call_llm(messages)
