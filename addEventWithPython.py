import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Webhook url can be found after creating a webhook node in n8n and then using HTTP Method POST, you get a test url just use that for testing and then the production url (can be found above/beside the test url)
# Can be used for the actual application
#Remember to make the webhook url a string in the .env
WEB_HOOK_CREATE = os.getenv('WEB_HOOK_CREATE')

# Full API_KEY cant be used as value since n8n has a max value which it forces after saving the API_KEY in the auth so just save part of it,
# or something else as the value if you know what you are doing.
N8N_AUTH_KEY = os.getenv('N8N_AUTH_KEY')

headers = {
    # "Name in the Header Auth settings": Value in the Header Auth Settings
    "Artemis-API-Key": N8N_AUTH_KEY,
    "Content-Type": "application/json"
}

# Hard-coded meeting data
data = {
    "title": "DND Night",
    "date": "2025-09-20",
    "time": "16:00",
    "location": "Ved Troels",
    "participants": ["Troels", "Søren", "Eske", "Rasmus", "Gamemaster / Emil"]
}

response = requests.post(WEB_HOOK_CREATE, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response Body:", response.text)


# def detect_intent(user_input: str) -> str:
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are an intent detector. Reply only with 'schedule_event' or 'none'"},
#             {"role": "user", "content": user_input}
#         ]
#     )
#     return response.choices[0].message.content.strip()

# user_input = "Can you schedule a meeting with Peter from openai at Friday 3PM?"
# intent = detect_intent(user_input)

# if intent == "schedule_event":
#   print("Status Code:", response.status_code)
#   print("Response Body:", response.text)
