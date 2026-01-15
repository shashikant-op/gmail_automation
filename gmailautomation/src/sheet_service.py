# sheet_service.py

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config import ALL_SCOPES, SPREADSHEET_ID, SHEET_NAME

def get_sheets_service():
    """
    Creates and returns an authenticated Google Sheets API service.
    """
    creds = Credentials.from_authorized_user_file(
        "token.json",
        ALL_SCOPES
    )
    return build("sheets", "v4", credentials=creds)



def append_row(service, row):
    # Ensure SHEET_NAME is treated as a sheet reference by adding !A1
    target_range = f"{SHEET_NAME}!A1" 
    
    body = {"values": [row]}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=target_range,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS", # Best practice for appending
        body=body
    ).execute()