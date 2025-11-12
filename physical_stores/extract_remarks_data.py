#!/usr/bin/env python3
"""
Extract structured information from a specific DApp Remarks submission
and update the corresponding Hit List row with the extracted data.

Usage:
    python3 extract_remarks_data.py <submission_id>
    python3 extract_remarks_data.py 5f15fb03-cb19-4983-8d94-31be4e9a3956 --dry-run
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Optional

import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
HIT_LIST_SHEET = "Hit List"
DAPP_REMARKS_SHEET = "DApp Remarks"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_google_sheets_client() -> gspread.Client:
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
    client = gspread.authorize(creds)
    return client


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    # Match various phone formats: (650) 420-5932, 650-420-5932, 650.420.5932, etc.
    patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\d{10}',  # 10 digits
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            phone = re.sub(r'[^\d]', '', match.group())
            if len(phone) == 10:
                return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    return None


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_website(text: str) -> Optional[str]:
    """Extract website URL from text."""
    patterns = [
        r'https?://[^\s]+',
        r'www\.[^\s]+',
        r'[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?',  # domain.com or domain.co.uk
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            url = match.strip('.,;')
            if not url.startswith('http'):
                url = 'http://' + url
            # Skip common non-website patterns
            if not any(skip in url.lower() for skip in ['instagram.com', 'facebook.com', '@']):
                return url
    return None


def extract_instagram(text: str) -> Optional[str]:
    """Extract Instagram handle or URL from text."""
    patterns = [
        r'instagram\.com/([a-zA-Z0-9_.]+)',
        r'@([a-zA-Z0-9_.]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            handle = match.group(1) if match.lastindex else match.group(0)
            if not handle.startswith('@'):
                handle = '@' + handle
            return handle
    return None


def extract_address(text: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Extract address, city, and state from text."""
    address = None
    city = None
    state = None
    
    # Common state abbreviations
    state_pattern = r'\b([A-Z]{2})\b'
    state_match = re.search(state_pattern, text)
    if state_match:
        state = state_match.group(1)
    
    # Try to find address patterns (number + street name with street suffix)
    # Must end with a street suffix to avoid false positives
    address_patterns = [
        r'(\d+\s+[A-Za-z0-9\s]+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane|Way|Ct|Court|Pl|Place|Blvd|Parkway|Pkwy))',
    ]
    for pattern in address_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            potential_address = match.group(1).strip()
            # Filter out false positives (like "10 o'clock")
            if len(potential_address.split()) >= 2 and not any(word.lower() in ['o', 'clock', 'am', 'pm'] for word in potential_address.split()):
                address = potential_address
                break
    
    # Try to find city (word before state or common city patterns)
    if state:
        city_pattern = rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),?\s*{state}'
        city_match = re.search(city_pattern, text)
        if city_match:
            city = city_match.group(1).strip()
    
    return address, city, state


def extract_contact_person(text: str) -> Optional[str]:
    """Extract contact person name from text."""
    # Look for patterns like "[name] is", "[name] mentioned", "call [name]", etc.
    # Prioritize names that appear before "is", "was", "mentioned", etc.
    patterns = [
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:is|was|will be|mentioned|said|still)',
        r'(?:call|contact|speak with|talk to|meet with|schedule with|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'([A-Z][a-z]+)\s+(?:the|a|an)\s+(?:staff|manager|owner|contact)',
    ]
    found_names = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            name = match.group(1).strip()
            # Filter out common false positives
            if name.lower() not in ['the', 'this', 'that', 'next', 'last', 'first', 'her', 'him', 'them', 'to']:
                if name not in found_names:
                    found_names.append(name)
    
    # Return the first valid name found
    return found_names[0] if found_names else None


def extract_follow_up_date(text: str) -> Optional[str]:
    """Extract follow-up date information from text."""
    # Look for date patterns
    patterns = [
        r'(?:next|this|on)\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)',
        r'(?:next|this)\s+week',
        r'(?:next|this)\s+Friday',
        r'until\s+(?:this|next)\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return None


def extract_structured_data(remarks: str) -> Dict[str, Optional[str]]:
    """Extract structured data from remarks text."""
    extracted = {
        'address': None,
        'city': None,
        'state': None,
        'phone': None,
        'email': None,
        'website': None,
        'instagram': None,
        'contact_person': None,
        'follow_up_date': None,
    }
    
    if not remarks:
        return extracted
    
    # Extract phone
    extracted['phone'] = extract_phone(remarks)
    
    # Extract email
    extracted['email'] = extract_email(remarks)
    
    # Extract website
    extracted['website'] = extract_website(remarks)
    
    # Extract Instagram
    extracted['instagram'] = extract_instagram(remarks)
    
    # Extract address components
    address, city, state = extract_address(remarks)
    extracted['address'] = address
    extracted['city'] = city
    extracted['state'] = state
    
    # Extract contact person
    extracted['contact_person'] = extract_contact_person(remarks)
    
    # Extract follow-up date
    extracted['follow_up_date'] = extract_follow_up_date(remarks)
    
    return extracted


def find_submission_by_id(client: gspread.Client, submission_id: str) -> Optional[Dict]:
    """Find a submission in DApp Remarks by submission ID."""
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    
    try:
        remarks_ws = spreadsheet.worksheet(DAPP_REMARKS_SHEET)
    except gspread.WorksheetNotFound:
        raise ValueError(f'Worksheet "{DAPP_REMARKS_SHEET}" not found.')
    
    remarks_values = remarks_ws.get_all_values()
    if len(remarks_values) < 2:
        return None
    
    headers = remarks_values[0]
    headers_idx = {header: idx for idx, header in enumerate(headers)}
    
    if "Submission ID" not in headers_idx:
        raise ValueError('Missing "Submission ID" column in DApp Remarks worksheet.')
    
    submission_idx = headers_idx["Submission ID"]
    
    for row_num, row in enumerate(remarks_values[1:], start=2):
        if row[submission_idx].strip() == submission_id:
            return {
                'row_num': row_num,
                'headers': headers,
                'row': row,
                'headers_idx': headers_idx,
            }
    
    return None


def find_shop_in_hit_list(client: gspread.Client, shop_name: str) -> Optional[Dict]:
    """Find a shop in Hit List by name."""
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    
    try:
        hit_list_ws = spreadsheet.worksheet(HIT_LIST_SHEET)
    except gspread.WorksheetNotFound:
        raise ValueError(f'Worksheet "{HIT_LIST_SHEET}" not found.')
    
    hit_values = hit_list_ws.get_all_values()
    if len(hit_values) < 2:
        return None
    
    headers = hit_values[0]
    headers_idx = {header: idx for idx, header in enumerate(headers)}
    
    if "Shop Name" not in headers_idx:
        raise ValueError('Missing "Shop Name" column in Hit List worksheet.')
    
    shop_name_idx = headers_idx["Shop Name"]
    
    for row_num, row in enumerate(hit_values[1:], start=2):
        if row[shop_name_idx].strip().lower() == shop_name.lower():
            return {
                'row_num': row_num,
                'headers': headers,
                'row': row,
                'headers_idx': headers_idx,
            }
    
    return None


def update_hit_list_row(
    client: gspread.Client,
    shop_data: Dict,
    extracted_data: Dict[str, Optional[str]],
    dry_run: bool = False
) -> None:
    """Update Hit List row with extracted data."""
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    hit_list_ws = spreadsheet.worksheet(HIT_LIST_SHEET)
    
    row_num = shop_data['row_num']
    headers_idx = shop_data['headers_idx']
    
    updates = []
    
    # Map extracted fields to Hit List columns
    field_mapping = {
        'address': 'Address',
        'city': 'City',
        'state': 'State',
        'phone': 'Phone',
        'email': 'Email',
        'website': 'Website',
        'instagram': 'Instagram',
        'contact_person': 'Contact Person',
        'follow_up_date': 'Follow Up Date',
    }
    
    for field, column_name in field_mapping.items():
        if column_name in headers_idx and extracted_data[field]:
            col_idx = headers_idx[column_name] + 1  # 1-indexed
            current_value = shop_data['row'][headers_idx[column_name]].strip()
            
            # Only update if current value is empty or different
            if not current_value or current_value != extracted_data[field]:
                updates.append({
                    'col': col_idx,
                    'value': extracted_data[field],
                    'column_name': column_name,
                    'current': current_value,
                })
    
    if not updates:
        print("  ℹ️  No new data to update (all fields already filled or no data extracted).")
        return
    
    print(f"\n  📝 Updates to apply:")
    for update in updates:
        print(f"    - {update['column_name']}: '{update['current']}' → '{update['value']}'")
    
    if not dry_run:
        for update in updates:
            hit_list_ws.update_cell(row_num, update['col'], update['value'])
        print(f"\n  ✅ Successfully updated {len(updates)} field(s) in Hit List.")
    else:
        print(f"\n  🔍 DRY RUN: Would update {len(updates)} field(s) in Hit List.")


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from DApp Remarks submission and update Hit List."
    )
    parser.add_argument(
        "submission_id",
        help="Submission ID to process (e.g., 5f15fb03-cb19-4983-8d94-31be4e9a3956)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions without updating the sheet."
    )
    args = parser.parse_args()
    
    print("=" * 80)
    print("EXTRACTING DATA FROM DAPP REMARKS SUBMISSION")
    print("=" * 80)
    print(f"\n🔍 Looking for submission ID: {args.submission_id}")
    
    client = get_google_sheets_client()
    
    # Find the submission
    submission = find_submission_by_id(client, args.submission_id)
    if not submission:
        print(f"\n❌ Submission ID '{args.submission_id}' not found in DApp Remarks.")
        return
    
    print(f"✅ Found submission in DApp Remarks (row {submission['row_num']})")
    
    # Extract submission data
    headers_idx = submission['headers_idx']
    row = submission['row']
    
    shop_name = row[headers_idx.get("Shop Name", -1)].strip() if "Shop Name" in headers_idx else ""
    status = row[headers_idx.get("Status", -1)].strip() if "Status" in headers_idx else ""
    remarks = row[headers_idx.get("Remarks", -1)].strip() if "Remarks" in headers_idx else ""
    submitted_by = row[headers_idx.get("Submitted By", -1)].strip() if "Submitted By" in headers_idx else ""
    
    print(f"\n📋 Submission Details:")
    print(f"  - Shop Name: {shop_name}")
    print(f"  - Status: {status}")
    print(f"  - Submitted By: {submitted_by}")
    print(f"  - Remarks: {remarks[:200]}{'...' if len(remarks) > 200 else ''}")
    
    if not shop_name:
        print("\n❌ Shop Name is missing in submission. Cannot proceed.")
        return
    
    # Find shop in Hit List
    shop_data = find_shop_in_hit_list(client, shop_name)
    if not shop_data:
        print(f"\n❌ Shop '{shop_name}' not found in Hit List.")
        return
    
    print(f"\n✅ Found shop in Hit List (row {shop_data['row_num']})")
    
    # Extract structured data from remarks
    print(f"\n🔍 Extracting structured data from remarks...")
    extracted = extract_structured_data(remarks)
    
    print(f"\n📊 Extracted Data:")
    for field, value in extracted.items():
        if value:
            print(f"  - {field.capitalize()}: {value}")
        else:
            print(f"  - {field.capitalize()}: (not found)")
    
    # Update Hit List
    print(f"\n🔄 Updating Hit List...")
    update_hit_list_row(client, shop_data, extracted, dry_run=args.dry_run)
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()

