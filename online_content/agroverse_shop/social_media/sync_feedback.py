#!/usr/bin/env python3
"""
Sync Feedback Script

This script syncs feedback from the "Feedback on Content" tab in Google Sheets
to a local CSV file for AI processing.

Usage:
    python sync_feedback.py

Requirements:
    - google_credentials.json file with proper Google Sheets API permissions
    - Access to the "Feedback on Content" tab in the target Google Sheet
"""

import os
import sys
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FeedbackSyncer:
    def __init__(self):
        self.credentials_file = "google_credentials.json"
        self.feedback_csv = "community_feedback.csv"
        self.spreadsheet_id = "1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ"
        self.worksheet_name = "Feedback on Content"
        
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
    
    def download_feedback(self):
        """Download feedback from Google Sheets to local CSV"""
        try:
            print(f"📥 Downloading feedback from worksheet: {self.worksheet_name}")
            
            # Get the worksheet
            worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            
            # Get all data from the worksheet
            all_values = worksheet.get_all_values()
            
            if len(all_values) <= 1:  # No data rows (only header or empty)
                print("📊 No feedback data found in sheet")
                return pd.DataFrame(columns=['feedback', 'status'])
            
            # Convert to DataFrame
            headers = all_values[0]
            data_rows = all_values[1:]
            
            print(f"📋 Found {len(data_rows)} feedback entries")
            
            # Ensure we have the expected columns
            if len(headers) < 2:
                print("⚠️  Warning: Expected at least 2 columns (Feedback, Status)")
                # Pad headers if needed
                while len(headers) < 2:
                    headers.append(f"Column_{len(headers)+1}")
            
            # Create DataFrame
            df = pd.DataFrame(data_rows, columns=headers[:2])  # Only use first 2 columns
            
            # Rename columns to standard names
            df.columns = ['feedback', 'status']
            
            # Clean up data
            df['feedback'] = df['feedback'].fillna('')
            df['status'] = df['status'].fillna('')
            
            # Filter out empty feedback rows
            df = df[df['feedback'].str.strip() != '']
            
            print(f"✅ Downloaded {len(df)} valid feedback entries")
            
            # Save to CSV
            df.to_csv(self.feedback_csv, index=False)
            print(f"💾 Saved feedback to: {self.feedback_csv}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error downloading feedback: {str(e)}")
            sys.exit(1)
    
    def upload_status_updates(self, feedback_csv_file):
        """Upload status updates back to Google Sheets"""
        try:
            print(f"📤 Uploading status updates from: {feedback_csv_file}")
            
            if not os.path.exists(feedback_csv_file):
                print(f"❌ Error: {feedback_csv_file} not found!")
                return False
            
            # Read the updated CSV
            df = pd.read_csv(feedback_csv_file)
            
            if len(df) == 0:
                print("📊 No feedback data to upload")
                return True
            
            # Get the worksheet
            worksheet = self.spreadsheet.worksheet(self.worksheet_name)
            
            # Get current data from sheet
            all_values = worksheet.get_all_values()
            
            if len(all_values) <= 1:  # No data rows
                print("📊 No data in sheet to update")
                return True
            
            # Find the status column index (should be column B)
            headers = all_values[0]
            status_col_idx = 1 if len(headers) > 1 else 0  # Default to column B
            
            print(f"📍 Status column index: {status_col_idx}")
            
            # Create a mapping of feedback text to status
            feedback_to_status = dict(zip(df['feedback'], df['status']))
            
            # Update status values in the sheet
            updated_count = 0
            for row_idx, row in enumerate(all_values[1:], start=2):  # Skip header row
                if len(row) > 0:
                    feedback_text = row[0] if len(row) > 0 else ""
                    
                    if feedback_text in feedback_to_status:
                        new_status = feedback_to_status[feedback_text]
                        
                        # Update the status cell
                        status_cell = f"B{row_idx}"
                        worksheet.update(status_cell, new_status)
                        updated_count += 1
                        print(f"  📌 Updated row {row_idx}: '{new_status}'")
            
            print(f"✅ Updated {updated_count} status values in Google Sheets")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading status updates: {str(e)}")
            return False
    
    def run(self, mode="download"):
        """Main execution method"""
        if mode == "download":
            print("🚀 Starting Feedback Download...")
            print("=" * 50)
            self.download_feedback()
            print("=" * 50)
            print("🎉 Feedback download completed successfully!")
            
        elif mode == "upload":
            print("🚀 Starting Status Update Upload...")
            print("=" * 50)
            success = self.upload_status_updates(self.feedback_csv)
            if success:
                print("=" * 50)
                print("🎉 Status updates completed successfully!")
            else:
                print("=" * 50)
                print("❌ Status updates failed!")
                sys.exit(1)
        
        else:
            print(f"❌ Unknown mode: {mode}")
            print("Valid modes: 'download', 'upload'")
            sys.exit(1)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sync feedback between Google Sheets and local CSV')
    parser.add_argument('mode', choices=['download', 'upload'], 
                       help='Mode: download feedback from sheets, or upload status updates')
    
    args = parser.parse_args()
    
    try:
        syncer = FeedbackSyncer()
        syncer.run(args.mode)
    except KeyboardInterrupt:
        print("\n⚠️  Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
