# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key=API_KEY)


# def call_llm(messages):

#     # Convert OpenAI style messages to prompt
#     prompt = ""

#     for msg in messages:
#         role = msg.get("role")
#         content = msg.get("content")

#         if role == "system":
#             prompt += f"{content}\n\n"
#         elif role == "user":
#             prompt += f"User: {content}\n"
#         elif role == "assistant":
#             prompt += f"Assistant: {content}\n"

#     try:

#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=prompt
#         )

#         return response.text

#     except Exception as e:
#         print("LLM ERROR:", e)
#         return "System temporarily unavailable."



import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def call_llm(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as e:
        print("LLM RESPONSE:", response.text)  # VERY IMPORTANT
        print("LLM ERROR:", e)
        return "System temporarily unavailable."