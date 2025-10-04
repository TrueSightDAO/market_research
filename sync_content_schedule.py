#!/usr/bin/env python3
"""
Sync Content Schedule Script

This script syncs the agroverse_schedule_till_easter.csv file with the 
"Content schedule" tab in the Google Sheets document.

The script preserves existing status values in Column B and uses primary keys
for row matching to avoid overwriting manual status updates.

Usage:
    python sync_content_schedule.py

Requirements:
    - google_credentials.json file with proper Google Sheets API permissions
    - agroverse_schedule_till_easter.csv file in the same directory
"""

import os
import sys
import pandas as pd
import gspread
import hashlib
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ContentScheduleSyncer:
    def __init__(self):
        self.credentials_file = "google_credentials.json"
        self.csv_file = "agroverse_schedule_till_easter_cleaned.csv"
        self.spreadsheet_id = "1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ"
        self.worksheet_name = "Content schedule"
        
        # Check if files exist
        self._check_files()
        
        # Initialize Google Sheets connection
        self._init_connection()
    
    def _check_files(self):
        """Check if required files exist"""
        if not os.path.exists(self.credentials_file):
            print(f"❌ Error: {self.credentials_file} not found!")
            print("Please place your Google service account credentials file in this directory.")
            sys.exit(1)
        
        if not os.path.exists(self.csv_file):
            print(f"❌ Error: {self.csv_file} not found!")
            print("Please ensure the CSV file exists in this directory.")
            sys.exit(1)
    
    def _init_connection(self):
        """Initialize Google Sheets connection"""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=scope)
            
            # Authorize and open the spreadsheet
            self.gc = gspread.authorize(creds)
            self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            
            print(f"✅ Successfully connected to Google Sheets: {self.spreadsheet.title}")
            
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {str(e)}")
            sys.exit(1)
    
    def load_csv_data(self):
        """Load and prepare CSV data with primary keys"""
        try:
            print(f"📖 Reading CSV file: {self.csv_file}")
            df = pd.read_csv(self.csv_file)
            print(f"✅ Loaded {len(df)} rows from CSV")
            
            # Generate deterministic primary keys based on date and content type
            print("🔑 Generating primary keys based on date and content type...")
            
            def generate_primary_key(row):
                # Use only Post Day and Post Type to create a deterministic key
                date_str = str(row.get('Post Day', ''))
                post_type = str(row.get('Post Type', ''))
                
                # Create a unique string from key fields (Post Day + Post Type only)
                unique_string = f"{date_str}_{post_type}"
                
                # Generate a hash and take first 8 characters
                hash_object = hashlib.md5(unique_string.encode())
                return hash_object.hexdigest()[:8]
            
            df['primary_key'] = df.apply(generate_primary_key, axis=1)
            print(f"✅ Generated primary keys for {len(df)} rows")
            
            # Ensure status column exists (add empty if missing)
            if 'status' not in df.columns:
                print("📝 Adding status column...")
                df['status'] = ''
            
            # Reorder columns to put primary_key first, then status, then rest
            columns = ['primary_key', 'status']
            
            # Add remaining columns (excluding primary_key and status)
            remaining_columns = [col for col in df.columns if col not in ['primary_key', 'status']]
            columns.extend(remaining_columns)
            
            df = df[columns]
            
            # Note: We don't save the CSV anymore since primary keys are generated deterministically
            print("ℹ️  Primary keys are generated deterministically - no need to save CSV")
            
            # Convert DataFrame to list of lists (including headers)
            data = [df.columns.tolist()] + df.values.tolist()
            return data, df
            
        except Exception as e:
            print(f"❌ Error reading CSV file: {str(e)}")
            sys.exit(1)
    
    def get_existing_status_values(self, worksheet):
        """Get existing status values from Column B, indexed by primary key from Column A"""
        try:
            # Get all data from the worksheet
            all_values = worksheet.get_all_values()
            
            if len(all_values) <= 1:  # No data rows (only header or empty)
                print("📊 No existing data found in sheet")
                return {}
            
            status_dict = {}
            headers = all_values[0]
            
            print(f"📋 Sheet headers: {headers}")
            
            # Find column indices
            try:
                primary_key_col = headers.index('primary_key')
                status_col = headers.index('status')
                print(f"📍 Found primary_key at column {primary_key_col}, status at column {status_col}")
            except ValueError as e:
                print(f"⚠️  Column not found: {e}")
                # If we can't find the expected columns, try to get status from column B
                if len(headers) > 1:
                    print("🔄 Trying to get status from Column B directly...")
                    primary_key_col = 0  # Assume primary key is in column A
                    status_col = 1       # Assume status is in column B
                else:
                    return {}
            
            # Build status dictionary from existing data
            for row_idx, row in enumerate(all_values[1:], start=2):  # Skip header row
                if len(row) > max(primary_key_col, status_col):
                    primary_key = row[primary_key_col] if len(row) > primary_key_col else ""
                    status_value = row[status_col] if len(row) > status_col else ""
                    if primary_key and primary_key.strip():  # Only store non-empty primary keys
                        status_dict[primary_key.strip()] = status_value.strip()
                        print(f"  🔍 Found: {primary_key.strip()} -> '{status_value.strip()}'")
            
            print(f"📊 Retrieved {len(status_dict)} existing status values")
            return status_dict
            
        except Exception as e:
            print(f"⚠️  Warning: Could not retrieve existing status values: {e}")
            return {}
    
    def sync_to_sheets(self, data, df):
        """Sync data to Google Sheets while preserving existing status values"""
        try:
            print(f"🔄 Syncing to worksheet: {self.worksheet_name}")
            
            # Get the worksheet
            worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            
            # Get existing status values before clearing
            print("📖 Retrieving existing status values...")
            existing_status = self.get_existing_status_values(worksheet)
            
            # Clear existing content
            print("🧹 Clearing existing content...")
            worksheet.clear()
            
            # Prepare data with preserved status values
            print("🔧 Preparing data with preserved status values...")
            data_with_status = data.copy()
            
            # Update status values in data if they exist in the sheet
            if 'status' in df.columns:
                status_col_idx = data_with_status[0].index('status')
                preserved_count = 0
                
                for row_idx, row in enumerate(data_with_status[1:], start=1):  # Skip header
                    primary_key = row[0].strip() if row[0] else ""  # Primary key is in column A
                    
                    if primary_key in existing_status:
                        existing_status_value = existing_status[primary_key]
                        # Only preserve if there's an existing status value
                        if existing_status_value and existing_status_value.strip():  # Check if status is not empty
                            row[status_col_idx] = existing_status_value
                            preserved_count += 1
                            print(f"  📌 Preserved status for {primary_key}: '{existing_status_value}'")
                        else:
                            print(f"  📝 Keeping empty status for {primary_key}")
                    else:
                        print(f"  🆕 New row {primary_key} - keeping empty status")
                
                print(f"✅ Successfully preserved {preserved_count} status values")
            
            # Clean data for JSON serialization
            print("🧹 Cleaning data for JSON serialization...")
            cleaned_data = []
            for row in data_with_status:
                cleaned_row = []
                for cell in row:
                    if cell is None:
                        cleaned_row.append("")
                    elif isinstance(cell, float) and (cell != cell):  # Check for NaN
                        cleaned_row.append("")
                    elif isinstance(cell, float) and (cell == float('inf') or cell == float('-inf')):
                        cleaned_row.append("")
                    else:
                        cleaned_row.append(str(cell))
                cleaned_data.append(cleaned_row)
            
            # Update with new data (preserving data validation on Status column)
            print("📝 Writing new data...")
            
            # Use a more targeted approach to preserve data validation
            # First, clear the sheet completely
            worksheet.clear()
            
            # Update all data
            worksheet.update('A1', cleaned_data)
            
            print("📌 Data updated - data validation rules may need to be recreated if lost")
            
            # Format header cells (excluding Status column B to preserve data validation)
            # Format Column A (primary_key) and Column C onwards, but skip Column B (status)
            if len(cleaned_data[0]) > 1:  # Ensure we have at least 2 columns
                # Format Column A header
                worksheet.format('A1', {
                    'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                })
                
                # Format Column C onwards (skip Column B - status)
                if len(cleaned_data[0]) > 2:
                    worksheet.format('C1:Z1', {
                        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                    })
            
            # Note: Status column (B) formatting and data validation are completely preserved
            
            # Note: Column widths are preserved to maintain user's formatting preferences
            
            print(f"✅ Successfully synced {len(data_with_status)-1} rows to Google Sheets!")
            print(f"🔒 Preserved {len(existing_status)} existing status values")
            
        except Exception as e:
            print(f"❌ Error syncing to Google Sheets: {str(e)}")
            sys.exit(1)
    
    def run(self):
        """Main execution method"""
        print("🚀 Starting Content Schedule Sync...")
        print("=" * 50)
        
        # Load CSV data
        data, df = self.load_csv_data()
        
        # Sync to Google Sheets
        self.sync_to_sheets(data, df)
        
        print("=" * 50)
        print("🎉 Content Schedule sync completed successfully!")
        print(f"📊 Updated {len(data)-1} content entries")
        print(f"🔗 View your sheet: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}")

def main():
    """Main function"""
    try:
        syncer = ContentScheduleSyncer()
        syncer.run()
    except KeyboardInterrupt:
        print("\n⚠️  Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
