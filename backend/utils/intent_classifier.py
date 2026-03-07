from tools.llm_client import call_llm

def classify_intent(user_input):

    text = user_input.lower()

    # Deterministic rules first (high confidence)
    if text.startswith("add medicine"):
        return "DRUG"

    if "remind me" in text:
        return "REMINDER"

    if "upload" in text or "report" in text:
        return "REPORT"

    if any(word in text for word in ["pain", "fever", "headache", "symptom"]):
        return "SYMPTOM"

    # Fallback to LLM classification
    messages = [
        {
            "role": "system",
            "content": (
                "Classify intent strictly as one of:\n"
                "SYMPTOM\nREPORT\nDRUG\nREMINDER\nCHAT\n"
                "Respond with only one word."
            )
        },
        {"role": "user", "content": user_input}
    ]

    result = call_llm(messages)
    return result.strip().upper()
