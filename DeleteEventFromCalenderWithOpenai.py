import requests
import os
import re
import dotenv

dotenv.load_dotenv()

N8N_AUTH_KEY = os.getenv("N8N_AUTH_KEY")
WEBHOOK_URL_DELETE = os.getenv("WEBHOOK_URL_DELETE")

payload = {"event": "test", "status": "ok"}

headers = {
    "Content-Type": "application/json",
    "Artemis-API-Key": N8N_AUTH_KEY
}

response = requests.post(WEBHOOK_URL_DELETE, json=payload, headers=headers)

print(response.status_code, response.text)