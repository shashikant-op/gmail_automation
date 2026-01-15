# email_parser.py

import base64
from email.utils import parsedate_to_datetime

def parse_email(msg):
    """
    Parses a Gmail API message and returns a dictionary:
    {
        "from": sender,
        "subject": subject,
        "date": ISO string,
        "content": plain text body,
        "internalDate": timestamp in ms
    }
    """
   
    headers = msg.get("payload", {}).get("headers", [])

    print("=================== message===============",msg)
    print("===========================headers",headers)
    data = {}

    # Extract headers
    for h in headers:
        if h["name"] == "From":
            data["from"] = h["value"]
        elif h["name"] == "Subject":
            data["subject"] = h["value"]
        elif h["name"] == "Date":
            try:
                data["date"] = parsedate_to_datetime(h["value"]).isoformat()
            except Exception:
                data["date"] = h["value"]

    # Recursive function to get text/plain from parts
    def get_body(parts):
        body_text = ""
        for part in parts:
            mime = part.get("mimeType", "")
            if mime == "text/plain":
                encoded = part.get("body", {}).get("data", "")
                if encoded:
                    padding = len(encoded) % 4
                    if padding != 0:
                        encoded += "=" * (4 - padding)
                    body_text += base64.urlsafe_b64decode(encoded).decode("utf-8", errors="ignore")
            elif mime.startswith("multipart/"):
                sub_parts = part.get("parts", [])
                body_text += get_body(sub_parts)
        return body_text

    parts = msg.get("payload", {}).get("parts", [])
    if parts:
        body = get_body(parts)
    else:
        body = msg.get("payload", {}).get("body", {}).get("data", "")
        if body:
            padding = len(body) % 4
            if padding != 0:
                body += "=" * (4 - padding)
            body = base64.urlsafe_b64decode(body).decode("utf-8", errors="ignore")

    data["content"] = body
    data["internalDate"] = int(msg.get("internalDate", 0))
    return data
