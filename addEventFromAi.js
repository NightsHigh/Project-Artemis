const fs = require('fs')
const path = require('path')
const { google } = require('googleapis')

const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json')
const TOKEN_PATH = path.join(__dirname, 'token.json')

function loadCredentials() {
    return JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'))
}

async function authorize() {
  const credentials = loadCredentials()
  const { client_secret, client_id, redirect_uris } = credentials.installed
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0])

  if (fs.existsSync(TOKEN_PATH)) {
    oAuth2Client.setCredentials(JSON.parse(fs.readFileSync(TOKEN_PATH, "utf8")))
    return oAuth2Client
  }

  throw new Error("No token.json found. Run the interactive setup once to authorize.")
}

async function addEvent(auth, eventData) {
  const calendar = google.calendar({ version: "v3", auth })

  const event = {
    summary: eventData.title,
    start: { dateTime: `${eventData.date}T${eventData.startTime}:00`, timeZone: "Europe/Copenhagen" },
    end: { dateTime: `${eventData.date}T${eventData.endTime}:00`, timeZone: "Europe/Copenhagen" },
  }

  try {
    const res = await calendar.events.insert({
      calendarId: "primary",
      resource: event,
    })
    console.log("✅ Event created:", res.data.htmlLink)
  } catch (err) {
    console.error("❌ Error creating event:", err)
  }
}

(async () => {
  let input = ""

  process.stdin.on("data", chunk => {
    input += chunk
  })
  process.stdin.on("end", async () => {
    let eventData
    try {
      eventData = JSON.parse(input)
    } catch (e) {
      console.error("❌ Invalid JSON input:", e.message)
      process.exit(1)
    }

  const auth = await authorize()
  await addEvent(auth, eventData)
  })
})()