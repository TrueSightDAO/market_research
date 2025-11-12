#!/usr/bin/env python3
"""
Pull the latest Holistic Wellness Hit List from Google Sheets into a local CSV.

Use this before running any scripts that modify the Hit List so the repository
has an up-to-date snapshot.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
WORKSHEET_NAME = "Hit List"
OUTPUT_PATH = Path("data/hit_list.csv")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def ensure_output_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def backup_existing(path: Path) -> None:
    if path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".csv.backup_{timestamp}")
        path.replace(backup_path)
        print(f"  ✅ Existing CSV backed up to: {backup_path}")


def fetch_hit_list() -> pd.DataFrame:
    # Look for credentials in parent directory (repository root)
    creds_path = Path(__file__).parent.parent / "google_credentials.json"
    if not creds_path.exists():
        raise FileNotFoundError(
            f"google_credentials.json not found at {creds_path}. Please place your service account "
            "credentials in the repository root."
        )

    creds = Credentials.from_service_account_file(str(creds_path), scopes=SCOPES)
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

    print(f"✅ Connected to spreadsheet: {SPREADSHEET_ID}")
    print(f"   Worksheet: {WORKSHEET_NAME}")

    values = worksheet.get_all_values()
    if len(values) < 1:
        raise ValueError("Worksheet is empty.")

    headers = values[0]
    rows = values[1:]
    df = pd.DataFrame(rows, columns=headers)
    print(f"📊 Retrieved {len(df)} rows with {len(df.columns)} columns.")

    return df


def save_to_csv(df: pd.DataFrame, path: Path) -> None:
    ensure_output_directory(path)

    # Use UTF-8 with BOM to retain compatibility with Excel
    df.to_csv(path, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    print(f"💾 Saved Hit List snapshot to {path}")


def main() -> None:
    print("=" * 80)
    print("PULLING HIT LIST FROM GOOGLE SHEETS")
    print("=" * 80)
    try:
        df = fetch_hit_list()
        backup_existing(OUTPUT_PATH)
        save_to_csv(df, OUTPUT_PATH)

        print("\nSummary:")
        status_counts = df["Status"].value_counts().to_dict() if "Status" in df else {}
        for status, count in status_counts.items():
            print(f"  - {status}: {count}")

        print("\nDone. Local copy is now in sync with Google Sheets.")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Error pulling Hit List: {exc}")
        raise


if __name__ == "__main__":
    main()

