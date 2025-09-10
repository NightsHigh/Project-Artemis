const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

// Paths for credentials and token
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

// Load client secrets from a local file
function loadCredentials() {
  return JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
}

// Authorize client and get OAuth2 client
async function authorize() {
  const credentials = loadCredentials()
  const { client_secret, client_id, redirect_uris } = credentials.installed

  const oAuth2Client = new google.auth.OAuth2(
    client_id, client_secret, redirect_uris[0]
  )

  // Check if token already exists
  if (fs.existsSync(TOKEN_PATH)) {
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'))
    oAuth2Client.setCredentials(token)
    return oAuth2Client
  }

  // If no token, get a new one
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/calendar'],
  })

  console.log('Authorize this app by visiting this URL:', authUrl)

  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  })

  return new Promise((resolve, reject) => {
    readline.question('Enter the code from that page here: ', (code) => {
      readline.close()
      oAuth2Client.getToken(code, (err, token) => {
        if (err) return reject(err)
        oAuth2Client.setCredentials(token)
        fs.writeFileSync(TOKEN_PATH, JSON.stringify(token))
        console.log('Token stored to', TOKEN_PATH)
        resolve(oAuth2Client)
      })
    })
  })
}

// Add demo event into Google Calendar
async function addEvent(auth) {
  const calendar = google.calendar({ version: 'v3', auth })

  // Hard coded event details
  const event = {
    summary: 'Work',
    start: {
      dateTime: '2025-09-13T04:00:00',
      timeZone: 'Europe/Copenhagen',
    },
    end: {
      dateTime: '2025-09-13T05:00:00',
      timeZone: 'Europe/Copenhagen',
    },
  }

  try {
    const res = await calendar.events.insert({
      calendarId: 'primary',
      resource: event,
    });
    console.log('Event created: %s', res.data.htmlLink)
  } catch (err) {
    console.error('Error creating event:', err)
  }
}

authorize().then(addEvent).catch(console.error)
