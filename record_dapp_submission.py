#!/usr/bin/env python3
"""
Utility script to record DApp submission notes into the Google Sheet.

Usage:
    python3 record_dapp_submission.py --shop "Go Ask Alice" \
        --status "Shortlisted" \
        --remarks "Interested in cacao tasting next week." \
        --submitted-by "Field Team"
"""

import argparse
import uuid
from datetime import datetime, timezone
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
SERVICE_ACCOUNT_EMAIL = "agroverse-market-research@get-data-io.iam.gserviceaccount.com"
DAPP_REMARKS_SHEET = "DApp Remarks"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_google_sheets_client():
    creds_path = Path(__file__).parent / "google_credentials.json"
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Google credentials not found at {creds_path}. "
            "Please add google_credentials.json with service account credentials."
        )

    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=SCOPES,
    )

    return gspread.authorize(creds)


def ensure_dapp_remarks_sheet(client):
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    headers = [
        "Submission ID",
        "Shop Name",
        "Status",
        "Remarks",
        "Submitted By",
        "Submitted At",
        "Processed",
        "Processed At",
    ]

    try:
        worksheet = spreadsheet.worksheet(DAPP_REMARKS_SHEET)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=DAPP_REMARKS_SHEET,
            rows=1000,
            cols=len(headers),
        )
        worksheet.append_row(headers)
        return worksheet

    existing_headers = worksheet.row_values(1)
    if existing_headers != headers:
        worksheet.clear()
        worksheet.append_row(headers)

    return worksheet


def append_submission(worksheet, shop_name, status, remarks, submitted_by):
    submission_id = str(uuid.uuid4())
    submitted_at = datetime.now(timezone.utc).isoformat()

    row = [
        submission_id,
        shop_name,
        status,
        remarks,
        submitted_by,
        submitted_at,
        "No",
        "",
    ]

    worksheet.append_row(row)
    print(f"✅ Recorded submission {submission_id} for {shop_name}")


def parse_args():
    parser = argparse.ArgumentParser(description="Record DApp status/remarks submission.")
    parser.add_argument("--shop", required=True, help="Shop name as recorded in the Hit List.")
    parser.add_argument(
        "--status",
        required=True,
        help="New status submitted via DApp (e.g. Research, Shortlisted, Contacted).",
    )
    parser.add_argument(
        "--remarks",
        default="",
        help="Free-form notes captured from the DApp submission.",
    )
    parser.add_argument(
        "--submitted-by",
        default="DApp",
        help="Identifier for who submitted the update (optional).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    client = get_google_sheets_client()
    worksheet = ensure_dapp_remarks_sheet(client)
    append_submission(
        worksheet,
        shop_name=args.shop,
        status=args.status,
        remarks=args.remarks,
        submitted_by=args.submitted_by,
    )


if __name__ == "__main__":
    main()

