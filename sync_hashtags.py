#!/usr/bin/env python3
"""
Sync Instagram Hashtags Script

This script syncs the instagram_hashtags.csv file with the 
"Hashtag suggestions" tab in the Google Sheets document.

Usage:
    python sync_hashtags.py

Requirements:
    - google_credentials.json file with proper Google Sheets API permissions
    - instagram_hashtags.csv file in the same directory
"""

import os
import sys
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HashtagSyncer:
    def __init__(self):
        self.credentials_file = "google_credentials.json"
        self.csv_file = "instagram_hashtags.csv"
        self.spreadsheet_id = "1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ"
        self.worksheet_name = "Hashtag suggestions"
        
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
        """Load and prepare CSV data"""
        try:
            print(f"📖 Reading CSV file: {self.csv_file}")
            df = pd.read_csv(self.csv_file)
            print(f"✅ Loaded {len(df)} hashtags from CSV")
            
            # Convert DataFrame to list of lists (including headers)
            data = [df.columns.tolist()] + df.values.tolist()
            return data
            
        except Exception as e:
            print(f"❌ Error reading CSV file: {str(e)}")
            sys.exit(1)
    
    def sync_to_sheets(self, data):
        """Sync data to Google Sheets"""
        try:
            print(f"🔄 Syncing to worksheet: {self.worksheet_name}")
            
            # Get the worksheet
            worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            
            # Clear existing content
            print("🧹 Clearing existing content...")
            worksheet.clear()
            
            # Update with new data
            print("📝 Writing new data...")
            worksheet.update('A1', data)
            
            # Format the header row
            worksheet.format('A1:Z1', {
                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
            })
            
            # Auto-resize columns
            print("📏 Auto-resizing columns...")
            worksheet.columns_auto_resize(0, len(data[0]) - 1)
            
            print(f"✅ Successfully synced {len(data)-1} hashtags to Google Sheets!")
            
        except Exception as e:
            print(f"❌ Error syncing to Google Sheets: {str(e)}")
            sys.exit(1)
    
    def run(self):
        """Main execution method"""
        print("🚀 Starting Instagram Hashtags Sync...")
        print("=" * 50)
        
        # Load CSV data
        data = self.load_csv_data()
        
        # Sync to Google Sheets
        self.sync_to_sheets(data)
        
        print("=" * 50)
        print("🎉 Instagram Hashtags sync completed successfully!")
        print(f"📊 Updated {len(data)-1} hashtags")
        print(f"🔗 View your sheet: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}")

def main():
    """Main function"""
    try:
        syncer = HashtagSyncer()
        syncer.run()
    except KeyboardInterrupt:
        print("\n⚠️  Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
