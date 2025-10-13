#!/usr/bin/env python3
"""
Pull Instagram Content Schedule FROM Google Sheets and update local CSV
This is the reverse of sync - Google Sheets becomes source of truth
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import sys

# Google Sheets setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'google_credentials.json'
SPREADSHEET_NAME = '20250924 - Instagram Content Marketing Schedule'
WORKSHEET_NAME = 'Instagram Content Schedule'
LOCAL_CSV = 'agroverse_schedule_till_easter_cleaned.csv'

def pull_from_sheets():
    """Pull data from Google Sheets and save to local CSV"""
    
    print("\n" + "="*80)
    print("PULLING FROM GOOGLE SHEETS TO LOCAL CSV")
    print("="*80)
    
    try:
        # Connect to Google Sheets
        print("\n📡 Connecting to Google Sheets...")
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open(SPREADSHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        
        print(f"✅ Connected to: {SPREADSHEET_NAME}")
        print(f"   Worksheet: {WORKSHEET_NAME}")
        
        # Get all values from sheet
        print("\n📖 Reading data from Google Sheets...")
        all_values = worksheet.get_all_values()
        
        if not all_values:
            print("❌ No data found in worksheet")
            return False
        
        # Convert to DataFrame
        headers = all_values[0]
        data = all_values[1:]
        
        df = pd.DataFrame(data, columns=headers)
        
        print(f"✅ Retrieved {len(df)} rows from Google Sheets")
        print(f"   Columns: {len(df.columns)}")
        
        # Show sample
        print(f"\n📊 Sample data (first 3 rows):")
        for idx in range(min(3, len(df))):
            row = df.iloc[idx]
            pk = row.get('primary_key', 'N/A')
            status = row.get('status', '(empty)')
            title = row.get('Description', 'N/A')[:50] if 'Description' in row else 'N/A'
            print(f"   {pk}: {title}... [Status: {status}]")
        
        # Backup existing CSV
        print(f"\n💾 Backing up existing CSV...")
        import shutil
        from datetime import datetime
        backup_name = f"{LOCAL_CSV}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            shutil.copy(LOCAL_CSV, backup_name)
            print(f"   ✅ Backup saved: {backup_name}")
        except FileNotFoundError:
            print(f"   ⚠️  No existing CSV to backup")
        
        # Save to CSV
        print(f"\n💾 Saving to local CSV: {LOCAL_CSV}")
        df.to_csv(LOCAL_CSV, index=False)
        
        print(f"✅ Successfully saved!")
        
        # Summary
        print("\n" + "="*80)
        print("✅ PULL COMPLETE!")
        print("="*80)
        print(f"📊 Local CSV now matches Google Sheets")
        print(f"   Rows: {len(df)}")
        print(f"   File: {LOCAL_CSV}")
        
        # Count scheduled posts
        scheduled_count = len(df[df['status'] == 'SCHEDULED'])
        print(f"\n📅 Posts with SCHEDULED status: {scheduled_count}")
        
        if scheduled_count > 0:
            print(f"\nScheduled posts:")
            scheduled = df[df['status'] == 'SCHEDULED'][['primary_key', 'Post Day', 'Description']]
            for idx, row in scheduled.iterrows():
                print(f"   {row['primary_key']}: {row['Description'][:60] if len(row['Description']) > 60 else row['Description']}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = pull_from_sheets()
    sys.exit(0 if success else 1)

