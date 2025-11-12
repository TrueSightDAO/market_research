#!/usr/bin/env python3
"""
TrueSight Blog Content Schedule Sync Script
Syncs truesight_blog_schedule.csv to Google Sheets while preserving status values
Based on the Agroverse blog schedule sync system
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import hashlib
import json
import sys

# Google Sheets setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'google_credentials.json'
SPREADSHEET_NAME = '20250924 - Instagram Content Marketing Schedule'  # Same spreadsheet
BLOG_WORKSHEET_NAME = 'TrueSight Blog Content Schedule'  # New worksheet for TrueSight
CSV_FILE = 'truesight_blog_schedule.csv'

def connect_to_sheets():
    """Connect to Google Sheets"""
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open(SPREADSHEET_NAME)
        print(f"✅ Successfully connected to Google Sheets: {SPREADSHEET_NAME}")
        return spreadsheet
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
        sys.exit(1)

def generate_primary_key(row):
    """
    Generate deterministic primary key based on publish date and title
    Format: {Publish Date}_{Blog Title}
    """
    date_str = str(row.get('Publish Date', ''))
    title = str(row.get('Blog Title', ''))
    unique_string = f'{date_str}_{title}'
    hash_object = hashlib.md5(unique_string.encode())
    return hash_object.hexdigest()[:8]

def get_or_create_worksheet(spreadsheet, worksheet_name):
    """Get existing worksheet or create new one"""
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        print(f"📝 Found existing worksheet: {worksheet_name}")
        return worksheet
    except gspread.exceptions.WorksheetNotFound:
        print(f"🆕 Creating new worksheet: {worksheet_name}")
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=500, cols=20)
        return worksheet

def retrieve_existing_status(worksheet):
    """Retrieve existing status values from Google Sheets"""
    status_map = {}
    
    try:
        all_values = worksheet.get_all_values()
        
        if len(all_values) < 2:
            print("📝 No existing data found in worksheet")
            return status_map
        
        headers = all_values[0]
        
        # Find column indices
        try:
            pk_col = headers.index('primary_key')
            status_col = headers.index('status') if 'status' in headers else None
        except ValueError as e:
            print(f"⚠️ Column not found: {e}")
            return status_map
        
        # Build status map
        for row in all_values[1:]:
            if len(row) > pk_col:
                primary_key = row[pk_col]
                status = row[status_col] if (status_col is not None and len(row) > status_col) else ''
                
                if primary_key and status:
                    status_map[primary_key] = status
        
        print(f"✅ Retrieved {len(status_map)} existing status values")
        return status_map
    
    except Exception as e:
        print(f"⚠️ Error retrieving status: {e}")
        return status_map

def sync_to_sheets(spreadsheet, worksheet_name, csv_file):
    """Sync CSV data to Google Sheets while preserving status"""
    
    # Read CSV
    print(f"\n📖 Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Generate primary keys if not present
    if 'primary_key' not in df.columns or df['primary_key'].isna().all():
        print("🔑 Generating primary keys...")
        df['primary_key'] = df.apply(generate_primary_key, axis=1)
    
    # Ensure primary_key is first column
    cols = ['primary_key'] + [col for col in df.columns if col != 'primary_key']
    df = df[cols]
    
    # Add status column if not present
    if 'status' not in df.columns:
        print("📝 Adding status column...")
        df.insert(1, 'status', '')
    
    print(f"📊 CSV contains {len(df)} rows")
    
    # Get or create worksheet
    worksheet = get_or_create_worksheet(spreadsheet, worksheet_name)
    
    # Retrieve existing status values
    print("\n🔍 Retrieving existing status values...")
    status_map = retrieve_existing_status(worksheet)
    
    # Preserve status values
    preserved_count = 0
    for idx, row in df.iterrows():
        pk = row['primary_key']
        if pk in status_map and status_map[pk]:
            df.at[idx, 'status'] = status_map[pk]
            preserved_count += 1
            print(f"  📝 Keeping status '{status_map[pk]}' for {pk}")
    
    if preserved_count > 0:
        print(f"✅ Successfully preserved {preserved_count} status values")
    
    # Clean data for JSON serialization
    print("\n🧹 Cleaning data for JSON serialization...")
    df = df.fillna('')
    df = df.astype(str)
    
    # Clear existing content
    print(f"\n🗑️ Clearing existing worksheet content...")
    worksheet.clear()
    
    # Write new data
    print(f"📝 Writing new data...")
    data = [df.columns.tolist()] + df.values.tolist()
    worksheet.update(data, value_input_option='RAW')
    
    print(f"✅ Successfully synced {len(df)} rows to Google Sheets!")
    print(f"🔒 Preserved {preserved_count} existing status values")
    
    return len(df), preserved_count

def main():
    print("\n" + "="*80)
    print("TRUESIGHT BLOG CONTENT SCHEDULE SYNC")
    print("="*80)
    
    # Connect to Google Sheets
    spreadsheet = connect_to_sheets()
    
    # Sync data
    total_rows, preserved = sync_to_sheets(spreadsheet, BLOG_WORKSHEET_NAME, CSV_FILE)
    
    # Get spreadsheet ID
    spreadsheet_id = spreadsheet.id
    
    print("\n" + "="*80)
    print("🎉 TrueSight Blog Schedule sync completed successfully!")
    print("="*80)
    print(f"📊 Updated {total_rows} content entries")
    print(f"🔗 View your sheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

if __name__ == "__main__":
    main()

