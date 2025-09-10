# Project Artemis – Google Calendar Integration

This project lets you add events to your **Google Calendar** using Node.js and the Google Calendar API.  
The first run will authenticate your Google account, then save a token for future use.

---

## 1. Create a Google Cloud project
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable the **Google Calendar API**:
   - Go to **APIs & Services → Enabled APIs & Services → + ENABLE APIS AND SERVICES**.
   - Search for "Google Calendar API" and enable it.

---

## 2. Create OAuth credentials
1. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
2. If you haven’t yet, configure the **OAuth consent screen** first:
   - Set **User type** to **External**.
   - Fill in the required fields (App name, your email).
3. Choose **Application type: Desktop app**.
4. Name it anything you like.
5. Click **Create** and then **Download JSON**.

⚠️ **Never upload this JSON file to GitHub!**  
Add it to your `.gitignore` to stay safe.

Save the file as `credentials.json` in your project folder.

---

## 3. Add yourself as a test user
1. Go to **APIs & Services → OAuth consent screen → Test users**.
2. Add the Gmail account you want to use.
3. Save.

---

## 4. Install dependencies
Inside your project folder, run:

```bash
npm install
