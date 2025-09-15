# import subprocess, json

# event = {
#     "title": "Dentist",
#     "date": "2025-09-13",
#     "startTime": "09:30",
#     "endTime": "10:00"
# }

# subprocess.run(
#     ["node", "addEventFromAi.js"],
#     input=json.dumps(event),
#     text=True
# )


import os
import openai
import requests
import re
from dotenv import load_dotenv

load_dotenv()

# Webhook url can be found after creating a webhook node in n8n and then using HTTP Method POST, you get a test url just use that for testing and then the production url (can be found above/beside the test url)
# Can be used for the actual application
#Remember to make the webhook url a string in the .env
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Full API_KEY cant be used as value since n8n has a max value which it forces after saving the API_KEY in the auth so just save part of it,
# or something else as the value if you know what you are doing.
N8N_AUTH_KEY = os.getenv('N8N_AUTH_KEY')

headers = {
    "Artemis-API-Key": N8N_AUTH_KEY,
    "Content-Type": "application/json"
}

# Hard-coded meeting data
data = {
    "title": "Friend Meet Up",
    "date": "2025-09-20",
    "time": "15:00",
    "location": "Bikini Bottom",
    "participants": ["spongebob@example.com", "patrick@example.com"]
}

response = requests.post(WEBHOOK_URL, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response Body:", response.text)






# load_dotenv()
# API_KEY = os.getenv("OPENAI_API_KEY")
# WEBHOOK_URL = "https://projectartemis.app.n8n.cloud/webhook-test/create/ScheduleEvent"
# def call_webhook_for_schedule_meeting(user_input: str)
#     data = {
#         "text": user_input
#     }
# headers = {
#     "Artemis-API-Key": API_KEY,
#     "Content-Type": "application/json"
# }

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
#     requests.post(

#     )