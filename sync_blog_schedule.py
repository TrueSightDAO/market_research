#!/usr/bin/env python3
"""
Blog Content Schedule Sync Script
Syncs blog_schedule.csv to Google Sheets while preserving status values
Based on the Instagram content schedule sync system
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
BLOG_WORKSHEET_NAME = 'Agroverse Blog Content Schedule'  # New worksheet in same spreadsheet
CSV_FILE = 'blog_schedule.csv'

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
        
        if not all_values or len(all_values) < 2:
            print("ℹ️  No existing data found in worksheet")
            return status_map
        
        headers = all_values[0]
        print(f"📋 Sheet headers: {headers}")
        
        # Find column indices
        try:
            primary_key_col = headers.index('primary_key')
            status_col = headers.index('status')
            print(f"📍 Found primary_key at column {primary_key_col}, status at column {status_col}")
        except ValueError as e:
            print(f"⚠️  Column not found in headers: {e}")
            return status_map
        
        # Build status map (skip header row)
        for row in all_values[1:]:
            if len(row) > max(primary_key_col, status_col):
                primary_key = row[primary_key_col]
                status = row[status_col]
                if primary_key:  # Only add if primary_key exists
                    status_map[primary_key] = status
                    print(f"  🔍 Found: {primary_key} -> '{status}'")
        
        print(f"📊 Retrieved {len(status_map)} existing status values")
        
    except Exception as e:
        print(f"⚠️  Error retrieving status values: {e}")
        print("   Continuing without status preservation...")
    
    return status_map

def clean_for_json(obj):
    """Clean data for JSON serialization"""
    if pd.isna(obj):
        return ''
    if isinstance(obj, (int, float)):
        if pd.isna(obj):
            return ''
        return obj
    return str(obj)

def sync_blog_schedule():
    """Main sync function"""
    print("🚀 Starting Blog Schedule Sync...")
    print("=" * 50)
    
    # Read CSV
    print(f"📖 Reading CSV file: {CSV_FILE}")
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✅ Loaded {len(df)} rows from CSV")
    except FileNotFoundError:
        print(f"❌ Error: {CSV_FILE} not found!")
        print("   Please create blog_schedule.csv first")
        sys.exit(1)
    
    # Generate primary keys
    print("🔑 Generating primary keys based on date and title...")
    df['primary_key'] = df.apply(generate_primary_key, axis=1)
    print(f"✅ Generated primary keys for {len(df)} rows")
    print("ℹ️  Primary keys are generated deterministically - no need to save CSV")
    
    # Sort by Publish Date in ascending order
    print("📅 Sorting by Publish Date (ascending order)...")
    df['Publish Date'] = pd.to_numeric(df['Publish Date'], errors='coerce')
    df = df.sort_values('Publish Date', ascending=True)
    df = df.reset_index(drop=True)
    print(f"✅ Sorted {len(df)} entries by date")
    
    # Connect to Google Sheets
    spreadsheet = connect_to_sheets()
    
    # Get or create worksheet
    print(f"🔄 Syncing to worksheet: {BLOG_WORKSHEET_NAME}")
    worksheet = get_or_create_worksheet(spreadsheet, BLOG_WORKSHEET_NAME)
    
    # Retrieve existing status values
    print("📖 Retrieving existing status values...")
    existing_status = retrieve_existing_status(worksheet)
    
    # Preserve status values
    print("🔧 Preparing data with preserved status values...")
    preserved_count = 0
    new_count = 0
    
    for idx, row in df.iterrows():
        pk = row['primary_key']
        if pk in existing_status:
            # Preserve existing status
            df.at[idx, 'status'] = existing_status[pk]
            if existing_status[pk]:  # Only count non-empty status
                preserved_count += 1
                print(f"  📌 Preserved status for {pk}: '{existing_status[pk]}'")
            else:
                print(f"  📝 Keeping empty status for {pk}")
        else:
            # New row - keep empty status
            new_count += 1
            print(f"  🆕 New row {pk} - keeping empty status")
    
    print(f"✅ Successfully preserved {preserved_count} status values")
    
    # Reorder columns to put primary_key and status first
    cols = df.columns.tolist()
    cols.remove('primary_key')
    if 'status' in cols:
        cols.remove('status')
    new_order = ['primary_key', 'status'] + cols
    df = df[new_order]
    
    # Clear existing content
    print("🧹 Clearing existing content...")
    worksheet.clear()
    
    # Clean data for JSON serialization
    print("🧹 Cleaning data for JSON serialization...")
    cleaned_data = []
    for idx, row in df.iterrows():
        cleaned_row = [clean_for_json(val) for val in row.values]
        cleaned_data.append(cleaned_row)
    
    # Add headers
    cleaned_data.insert(0, df.columns.tolist())
    
    # Write new data
    print("📝 Writing new data...")
    worksheet.update('A1', cleaned_data)
    print("📌 Data updated - data validation rules may need to be recreated if lost")
    
    print(f"✅ Successfully synced {len(df)} rows to Google Sheets!")
    print(f"🔒 Preserved {len(existing_status)} existing status values")
    print("=" * 50)
    print("🎉 Blog Schedule sync completed successfully!")
    print(f"📊 Updated {len(df)} blog entries")
    print(f"🔗 View your sheet: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")

if __name__ == "__main__":
    sync_blog_schedule()

