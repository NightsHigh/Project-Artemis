import os, json, subprocess, sys
from dotenv import load_dotenv
from openai import OpenAI

# --- setup ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

USER_NAME = "NightsHigh" # Change the your name
SYSTEM = (
    f"You are a chat assistant for {USER_NAME} (Europe/Copenhagen). "
    "When the user asks to schedule or change an event, output a JSON object with:\n"
    "{intent: 'schedule_event', data: {title, date(YYYY-MM-DD), start_time(HH:MM 24h), end_time(HH:MM 24h), timezone}}\n"
    "Otherwise output {intent: 'chat', data: {reply}}.\n"
    "Always resolve relative dates (‘tomorrow’, ‘next week’) to absolute dates."
)

ROUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": ["schedule_event", "chat"]},
        "data": {
            "oneOf": [
                {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "date": {"type": "string"},
                        "start_time": {"type": "string"},
                        "end_time": {"type": "string"},
                        "timezone": {"type": "string"}
                    },
                    "required": ["title", "date", "start_time", "end_time"],
                    "additionalProperties": False
                },
                {
                    "type": "object",
                    "properties": {
                        "reply": {"type": "string"}
                    },
                    "required": ["reply"],
                    "additionalProperties": False
                }
            ]
        }
    },
    "required": ["intent", "data"],
    "additionalProperties": False
}

def ask_llm(user_text: str) -> dict:
    resp = client.responses.create(
        model="gpt-5",
        instructions=SYSTEM,
        input=f"User: {user_text}",
        text={
            "format": {
                "type": "json_schema",
                "name": "router",
                "schema": ROUTER_SCHEMA,
                "strict": True
            }
        }
    )
    return json.loads(resp.output_text)

def schedule_event_via_node(event: dict) -> str:
    # Normalize field names for the Node tool
    payload = {
        "title": event["title"],
        "date": event["date"],
        "startTime": event["start_time"],
        "endTime": event["end_time"],
        "timezone": event.get("timezone", "Europe/Copenhagen"),
    }

    # Call your Node adapter that reads JSON from STDIN
    result = subprocess.run(
        ["node", "addEventFromAi.js"],
        input=json.dumps(payload),
        text=True,
        capture_output=True
    )

    # Surface any errors
    if result.returncode != 0:
        return f"Calendar tool error: {result.stderr.strip() or 'Unknown error'}"
    return result.stdout.strip() or "Event created."

def chat(user_text: str) -> str:
    routed = ask_llm(user_text)
    print("[router]", json.dumps(routed, indent=2))  # <-- helpful debug

    if routed["intent"] == "chat":
        return routed["data"].get("reply", "(no reply)")
    if routed["intent"] == "schedule_event":
        confirm = schedule_event_via_node(routed["data"])
        return f"Okay — {confirm}"
    return "Sorry, I didn't understand that."



if __name__ == "__main__":
    # One-shot usage: python CallOpenAiAPI.py "your message here"
    if len(sys.argv) > 1:
        print(chat(" ".join(sys.argv[1:])))
    else:
        # Simple REPL
        print("Assistant ready. Type a message (Ctrl+C to exit).")
        try:
            while True:
                msg = input("> ")
                print(chat(msg))
        except KeyboardInterrupt:
            print("\nBye!")