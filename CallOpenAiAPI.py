import os, json, subprocess, sys
from dotenv import load_dotenv
import requests 

load_dotenv()  # Load APIkey from .env
client = OpenAI()

url = "https://projectartemis.app.n8n.cloud/webhook-test/create/eventInCalender"


payload = {
    ""
}

headers = {
    "Content-Type": "application/json",
    "Artemis-API-Key": "Insert Secret Key Here"
}


response = client.responses.create(
    model="gpt-5",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)