from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load APIkey from .env
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)