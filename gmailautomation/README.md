Gmail to Google Sheets Automation

A Python-based automation tool that reads unread Gmail emails, extracts key information, and logs them into Google Sheets automatically.
After processing, emails are marked as read to prevent duplication.

This project demonstrates Google API integration, OAuth 2.0 authentication, stateful processing, and modular backend design.

🚀 Features

✅ Fetches unread emails from Gmail

✅ Extracts sender, subject, date, and email body

✅ Appends data into Google Sheets

✅ Marks processed emails as READ

✅ Maintains state to avoid duplicate processing

✅ Clean modular architecture (easy to scale)

🧠 Design & Architecture Explanation
1️⃣ High-Level Workflow
Gmail Inbox (Unread)
        ↓
Gmail API (OAuth)
        ↓
Email Parser
        ↓
Google Sheets API
        ↓
Spreadsheet (Rows Appended)

2️⃣ Architecture Overview
gmailproject/
│
├── src/
│   ├── main.py            # Application entry point
│   ├── gmail_service.py   # Gmail API authentication & helpers
│   ├── sheet_service.py   # Google Sheets API logic
│   ├── email_parser.py    # Email content extraction
│
├── credentials/
│   └── credentials.json   # Google OAuth credentials
│
├── state.json             # Stores last processed email timestamp
├── config.py              # Central configuration
├── requirements.txt
└── README.md

3️⃣ Design Decisions
🔹 Modular Services

Each responsibility is separated:

gmail_service.py → Gmail authentication & state handling

sheet_service.py → Sheet write operations

email_parser.py → Email parsing logic

This improves:

Maintainability

Testability

Scalability

🔹 Stateful Processing

The app stores the last processed Gmail internalDate in state.json.

Why?

Prevents duplicate writes

Ensures idempotent execution

Safe to run multiple times

🔹 OAuth 2.0 (Secure Access)

Uses Google OAuth with limited scopes:

Gmail modify (read + mark read)

Google Sheets write access

No passwords are stored.

⚙️ Configuration

All configuration is centralized in config.py.

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

ALL_SCOPES = GMAIL_SCOPES + SHEETS_SCOPES

SPREADSHEET_ID = "1-YRfGovtBzftSpJZG47mErRahqP9vpqGUqD3N8V9HNE"
SHEET_NAME = "gmailsheets"

STATE_FILE = "state.json"
RANGE = "gmailsheet!A:D"

⚡ Quick Setup Guide
1️⃣ Clone the Repository
git clone <repo-url>
cd gmailproject

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Google Cloud Setup

Go to Google Cloud Console

Create a new project

Enable:

Gmail API

Google Sheets API

Configure OAuth Consent Screen

User Type: External

Add your Gmail ID as Test User

Create OAuth Client ID

Application type: Desktop App

Download credentials.json

📁 Place it here:

credentials/credentials.json

5️⃣ Prepare Google Sheet

Create a Google Sheet

Rename the sheet to:

gmailsheet


Add headers in Row 1:

From | Subject | Date | Content

6️⃣ Run the Application
python -m src.main


First run will:

Open browser for Google authentication

Ask Gmail + Sheets permission

Create token.json

Start processing unread emails

🧪 Testing the Project

Send yourself a test email

Keep it unread

Run:

python -m src.main


Verify:

New row added in Google Sheets

Email marked as read

🔐 Security Notes

credentials.json and token.json should never be committed

Use .gitignore:

credentials/
token.json
state.json

📈 Future Enhancements

Email attachments support

Scheduled execution (cron)

Label-based filtering

HTML email parsing

Dashboard for monitoring

👨‍💻 Author

Shashi Kant Sharma
Backend / Automation Developer
Tech Stack: Python, Google APIs, OAuth 2.0