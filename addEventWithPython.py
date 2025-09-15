import subprocess, json

event = {
    "title": "Dentist",
    "date": "2025-09-13",
    "startTime": "09:30",
    "endTime": "10:00"
}

subprocess.run(
    ["node", "addEventFromAi.js"],
    input=json.dumps(event),
    text=True
)
