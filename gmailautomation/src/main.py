from src.gmail_service import get_gmail_service, load_state, save_state
from src.sheet_service import get_sheets_service, append_row
from src.email_parser import parse_email

def main():
    gmail = get_gmail_service()
    sheets = get_sheets_service()
    last_ts = load_state()

    results = gmail.users().messages().list(
        userId="me",
        q="is:unread"
    ).execute()
   

    messages = results.get("messages", [])
    latest_ts = last_ts

    for msg in messages:
        full = gmail.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        parsed = parse_email(full)

        if parsed["internalDate"] <= last_ts:
            continue
        
        append_row(
            sheets,
                [
            parsed.get("from", ""),
            parsed.get("subject", ""),
            parsed.get("date", ""),
            parsed.get("content", "")
        ]
        )

        gmail.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        latest_ts = max(latest_ts, parsed["internalDate"])

    save_state(latest_ts)


if __name__ == "__main__":
    main()