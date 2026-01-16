
# Gmail to Google Sheets Automation

A Python automation tool that monitors unread Gmail messages, extracts key information (From, Subject, Date, Content), and appends each record to a Google Sheet. Processed messages are marked as read to prevent duplication. The project demonstrates Gmail & Google Sheets API integration, OAuth 2.0 authentication, stateful processing, and a modular, testable codebase.

## 📂 screenshot
<img width="1466" height="835" alt="Screenshot 2026-01-16 at 10 05 37 PM" src="https://github.com/user-attachments/assets/1ecceb14-38fa-4342-b3ee-1eb0a1b13eb6" />
<img width="1468" height="830" alt="Screenshot 2026-01-16 at 10 07 18 PM" src="https://github.com/user-attachments/assets/a424a36f-869d-41e1-a543-4caa18f54b10" />

Table of contents
- Overview
- Features
- Design & architecture
- Project structure
- Configuration example
- Prerequisites
- Setup & installation
- Google Cloud & API setup
- Prepare the Google Sheet
- Usage
- Testing
- Security
- Future improvements
- Contributing
- License
- Author

Overview
--------
This application polls unread Gmail messages, parses each message to extract structured fields, and appends them as rows in a Google Sheet. It keeps a persistent state to ensure that emails are processed only once and can safely be re-run or scheduled.

Features
--------
- Fetches unread Gmail messages
- Extracts sender, subject, date, and message content
- Appends extracted data to Google Sheets
- Marks messages as read after successful processing
- Persists processing state to avoid duplicates
- Modular design for maintainability and testing

Design & architecture
---------------------
High-level workflow:
Unread Gmail → Gmail API (OAuth 2.0) → Email parsing → Google Sheets API → Append row → Mark message read → Update state

Design choices:
- Single-responsibility modules (Gmail client, parser, Sheets client, orchestrator)
- Stateless orchestration with a small persistent state file to track processed message IDs
- OAuth 2.0 for secure authentication; tokens stored outside source control
- Centralized configuration for easy changes
## 📂 Project Structure
```text
gmail-sheets-automation/
├── src/
│   └── gmail_sync/
│       ├── core/
│       │   ├── orchestrator.py    # Main logic loop
│       │   └── state_manager.py   # JSON persistence
│       ├── services/
│       │   ├── gmail_api.py       # Gmail-specific methods
│       │   └── sheets_api.py      # Sheets-specific methods
│       ├── utils/
│       │   └── parser.py          # MIME/Body extraction
│       ├── config.py              # Environment & API settings
│       └── main.py                # Application entry point
├── credentials/
│   └── credentials.json           # OAuth Client Secret (Keep Secret!)
├── tests/                         # Pytest suite
├── .gitignore
└── README.md
---------------------
Add these values to `config.py` or set via environment variables:

```python
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
ALL_SCOPES = GMAIL_SCOPES + SHEETS_SCOPES

SPREADSHEET_ID = "1-YRfGovtBzftSpJZG47mErRahqP9vpqGUqD3N8V9HNE"
SHEET_NAME = "gmailsheet"
STATE_FILE = "state.json"
RANGE = f"{SHEET_NAME}!A:D"
CREDENTIALS_PATH = "credentials/credentials.json"
TOKEN_PATH = "credentials/token.json"

POLL_INTERVAL_SECONDS = 60  # If running continuously
```

Example state.json
```json
{
  "processed_message_ids": [
    "17c3a8b1f4e...123",
    "17c3a8b1f4e...124"
  ],
  "last_run": "2026-01-15T10:00:00Z"
}
```

Prerequisites
-------------
- Python 3.8+
- Google Cloud project with Gmail API and Google Sheets API enabled
- OAuth 2.0 client credentials (Desktop app recommended for local runs)
- Basic familiarity with virtual environments and the command line

Setup & installation
--------------------
1. Clone the repository:
   ```
   git clone https://github.com/shashikant-op/gmail_automation.git
   cd gmail_automation
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate       # macOS / Linux
   venv\Scripts\activate          # Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Add OAuth credentials: download `credentials.json` from Google Cloud Console and place it under `credentials/` (or update `CREDENTIALS_PATH`).

Google Cloud & API setup
------------------------
1. Create or select a project in Google Cloud Console.
2. Enable the Gmail API and the Google Sheets API.
3. Configure the OAuth consent screen (External) and add your account as a test user if needed.
4. Create OAuth client credentials (Desktop application).
5. Download `credentials.json` to `credentials/`.
6. On first run, the app will open a browser for authorization; the refresh token is typically saved to `credentials/token.json`.

Prepare the Google Sheet
------------------------
- Create a Google Sheet (or use an existing one) and set `SPREADSHEET_ID` accordingly.
- Create the sheet/tab named as `SHEET_NAME` (default: `gmailsheet`).
- Add header row: From | Subject | Date | Content

Usage
-----
Run the application (from the project root):
```
python -m src.main
```

Typical behavior:
- Authenticate with Gmail and Sheets (first run opens the browser)
- Fetch unread messages (optionally filter with Gmail search queries)
- Parse each message and append a row to the sheet
- Mark messages as read and record processed IDs in `state.json`

Optional CLI flags (if implemented):
- `--once` : run a single poll and exit
- `--continuous` : poll indefinitely with the configured interval
- `--query "is:unread label:inbox"` : custom Gmail search query

Testing
-------
Manual:
1. Send a test email to the monitored Gmail account and leave it unread.
2. Run the application: `python -m src.main`
3. Verify a new row is added to the Google Sheet and the email is marked as read.

Automated:
- Unit test parsing logic (`email_parser.py`) with `pytest`.
- Mock Gmail and Sheets API calls using `unittest.mock` or libraries like `pytest-mock`.
- Use recorded fixtures for API responses (HTML emails, multi-part, encoding edge cases).

Security
--------
- Do NOT commit `credentials/credentials.json`, `credentials/token.json`, or `state.json`. Add them to `.gitignore`.
- Use environment variables or a secret manager for production deployments.
- Request minimal OAuth scopes required for functionality (e.g., `gmail.modify`).
- Rotate credentials periodically and remove test users from the OAuth consent screen before moving to production.

Future improvements
-------------------
- Support attachments (store in cloud storage and add links to the sheet)
- Label-based filtering and routing
- Improved HTML-to-text extraction and sanitization
- Rate-limiting and exponential backoff for API quotas
- Logging, metrics, and a small dashboard for monitoring
- Containerization (Docker) and cloud deployment options (Cloud Run, Cloud Functions)



License
-------
Specify the license (e.g., MIT). If no license is present, the repository is proprietary; contributors should contact the maintainer for permission.

Author
------
Shashi Kant Sharma — Backend & Automation Developer

Contact
-------
For questions or support, open an issue in this repository.
```
