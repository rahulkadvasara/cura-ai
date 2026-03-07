from agents.symptom_agent import SymptomAgent
from agents.drug_agent import DrugAgent
from agents.report_agent import ReportAgent
from agents.chat_agent import ChatAgent
from utils.intent_classifier import classify_intent
from utils.logger import log_event
from agents.reminder_agent import ReminderAgent


class CoordinatorAgent:

    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.symptom = SymptomAgent()
        self.drug = DrugAgent()
        self.report = ReportAgent()
        self.chat = ChatAgent()
        self.reminder = ReminderAgent()


    def route(self, user_id, user_input, image_path=None):
        log_event(f"User {user_id} input: {user_input}")

        self.memory.store_user_message(user_id, user_input)
        context = self.memory.get_context(user_id)

        intent = classify_intent(user_input)
        log_event(f"Detected intent: {intent}")

        if intent == "SYMPTOM":
            log_event("Routing to SymptomAgent")
            response = self.symptom.run(user_input, context)

        elif intent == "DRUG":
            medicine_name = user_input.replace("Add medicine", "").strip()
            response = self.drug.run(medicine_name, context)
            self.memory.persistent.add_medicine(user_id, medicine_name)
            log_event(f"Medicine stored after interaction check: {medicine_name}")


        elif intent == "REPORT" and image_path:
            log_event("Routing to ReportAgent")
            response = self.report.run(image_path)
        
        elif intent == "REMINDER":
            try:
                parts = user_input.split("at")
                medicine = parts[0].replace("Remind me to take", "").strip()
                time_str = parts[1].strip()

                response = self.reminder.schedule_reminder(
                    user_id, medicine, time_str, context
                )

            except:
                response = "Use format: Remind me to take <medicine> at <time>"



        else:
            log_event("Routing to ChatAgent")
            response = self.chat.run(user_input, context)

        self.memory.store_assistant_message(user_id, response)
        log_event(f"Response generated successfully")

        return response
