#!/usr/bin/env python3
"""
Create Google Calendar reminders for shop follow-ups based on the Hit List sheet.

Usage:
    1. Share the target Google Calendar with the service account:
       agroverse-market-research@get-data-io.iam.gserviceaccount.com
    2. Set the environment variable GOOGLE_CALENDAR_ID to the calendar's ID.
    3. Run: python3 create_followup_events.py

Events are created/updated for rows that have a "Follow Up Date" value. The script
generates deterministic event IDs so it can be re-run without creating duplicates.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, time, timedelta
import hashlib
from typing import Optional, Tuple

from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from zoneinfo import ZoneInfo


SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
SHEET_NAME = "Hit List"
SERVICE_ACCOUNT_FILE = "google_credentials.json"

# Scopes cover both Sheets and Calendar APIs
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar"
]

# Default timezone for events (can be overridden with DEFAULT_TIMEZONE env var)
DEFAULT_TIMEZONE = os.environ.get("DEFAULT_TIMEZONE", "America/Los_Angeles")

# Regex patterns for parsing follow-up date strings
RANGE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})$")
SINGLE_TIME_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})$")


def slugify(value: str) -> str:
    """Convert a string into a Calendar-safe slug for event IDs."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    value = re.sub(r"__+", "_", value)
    return value or "event"


def parse_followup(value: str) -> Optional[Tuple[str, Optional[datetime], Optional[datetime]]]:
    """Parse follow-up date string.

    Returns a tuple of (date_str, start_dt, end_dt).
    If no specific time is provided, start_dt and end_dt are None (all-day event).
    """

    if not value:
        return None

    value = value.strip()

    range_match = RANGE_PATTERN.match(value)
    if range_match:
        date_str, start_time, end_time = range_match.groups()
        tz = ZoneInfo(DEFAULT_TIMEZONE)
        date_obj = datetime.fromisoformat(date_str).date()
        start_dt = datetime.combine(
            date_obj,
            datetime.strptime(start_time, "%H:%M").time(),
            tz
        )
        end_dt = datetime.combine(
            date_obj,
            datetime.strptime(end_time, "%H:%M").time(),
            tz
        )
        return date_str, start_dt, end_dt

    single_match = SINGLE_TIME_PATTERN.match(value)
    if single_match:
        date_str, start_time = single_match.groups()
        tz = ZoneInfo(DEFAULT_TIMEZONE)
        date_obj = datetime.fromisoformat(date_str).date()
        start_dt = datetime.combine(
            date_obj,
            datetime.strptime(start_time, "%H:%M").time(),
            tz
        )
        end_dt = start_dt + timedelta(hours=1)
        return date_str, start_dt, end_dt

    # Try parsing as ISO date
    try:
        datetime.fromisoformat(value)
        return value, None, None
    except ValueError:
        return None


def build_event(shop: dict) -> Optional[dict]:
    followup_value = (
        shop.get("Follow Up Date")
        or shop.get("follow_up_date")
        or ""
    ).strip()
    parsed = parse_followup(followup_value)
    if not parsed:
        return None

    date_str, start_dt, end_dt = parsed
    shop_name = shop.get("Shop Name") or shop.get("shop_name") or "Unknown Shop"
    status = shop.get("Status") or shop.get("status", "")

    contact_person = shop.get("Contact Person") or shop.get("contact_person", "")
    owner_name = shop.get("Owner Name") or shop.get("owner_name", "")
    referral = shop.get("Referral") or shop.get("referral", "")
    product_interest = shop.get("Product Interest") or shop.get("product_interest", "")
    notes = (
        shop.get("Sales Process Notes")
        or shop.get("sales_process_notes")
        or shop.get("sales_notes", "")
    )

    description_lines = []
    if status:
        description_lines.append(f"Status: {status}")
    if contact_person:
        description_lines.append(f"Contact: {contact_person}")
    if owner_name:
        description_lines.append(f"Owner: {owner_name}")
    if referral:
        description_lines.append(f"Referral: {referral}")
    if product_interest:
        description_lines.append(f"Product Interest: {product_interest}")
    if notes:
        description_lines.append("\nNotes:\n" + notes)

    if description_lines:
        description = "\n".join(description_lines)
    else:
        description = "Follow-up reminder generated from the Hit List sheet."

    base_key = f"{shop_name}|{date_str}".encode("utf-8")
    digest = hashlib.sha1(base_key).hexdigest()
    event_id = f"fu{digest}"

    event = {
        "id": event_id,
        "summary": f"Follow-up: {shop_name}",
        "description": description.strip(),
        "source": {
            "title": "Shop Hit List",
            "url": "https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit#gid=0"
        }
    }

    if start_dt and end_dt:
        event["start"] = {
            "dateTime": start_dt.isoformat(),
            "timeZone": DEFAULT_TIMEZONE
        }
        event["end"] = {
            "dateTime": end_dt.isoformat(),
            "timeZone": DEFAULT_TIMEZONE
        }
    else:
        end_date = (datetime.fromisoformat(date_str) + timedelta(days=1)).date().isoformat()
        event["start"] = {"date": date_str}
        event["end"] = {"date": end_date}

    return event


def main() -> None:
    load_dotenv()
    load_dotenv(".env.local", override=True)

    calendar_id = os.environ.get("GOOGLE_CALENDAR_ID")
    if not calendar_id:
        raise RuntimeError("GOOGLE_CALENDAR_ID environment variable is required")

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    values = worksheet.get_all_values()

    if not values or len(values) < 2:
        print("No data rows with follow-up information found.")
        return

    headers = values[0]
    index_map = {header: idx for idx, header in enumerate(headers)}
    follow_up_link_idx = index_map.get("Follow Up Event Link")

    calendar_service = build("calendar", "v3", credentials=credentials)

    created = 0
    updated = 0
    skipped = 0

    for row_number, row in enumerate(values[1:], start=2):
        row_data = {
            header: (row[idx] if idx < len(row) else "")
            for header, idx in index_map.items()
        }

        followup_value = row_data.get("Follow Up Date", "")
        if not followup_value:
            continue

        event = build_event(row_data)

        if not event:
            skipped += 1
            continue

        try:
            event_response = calendar_service.events().update(
                calendarId=calendar_id,
                eventId=event["id"],
                body=event
            ).execute()
            updated += 1
            print(f"Updated calendar event for {event['summary']}")
        except HttpError as err:
            if err.resp.status == 404:
                event_response = calendar_service.events().insert(
                    calendarId=calendar_id,
                    body=event
                ).execute()
                created += 1
                print(f"Created calendar event for {event['summary']}")
            else:
                print(f"⚠️  Failed processing {event['summary']}: {err}")
                skipped += 1
                continue

        event_link = event_response.get("htmlLink", "")
        if follow_up_link_idx is not None and event_link:
            existing_link = row[follow_up_link_idx] if follow_up_link_idx < len(row) else ""
            if existing_link != event_link:
                worksheet.update_cell(row_number, follow_up_link_idx + 1, event_link)

    print("\nSummary:")
    print(f"  Created events: {created}")
    print(f"  Updated events: {updated}")
    print(f"  Skipped rows: {skipped}")


if __name__ == "__main__":
    main()

