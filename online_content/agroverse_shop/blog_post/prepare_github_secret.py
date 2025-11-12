#!/usr/bin/env python3
"""
Prepare Google Credentials for GitHub Secrets

This script helps convert your Google service account JSON file
into the format needed for GitHub Actions secrets.

Usage:
    python prepare_github_secret.py

Requirements:
    - google_credentials.json file in the same directory
    - jq (optional, for better JSON formatting)
"""

import os
import json
import sys

def prepare_github_secret():
    """Convert Google credentials JSON to GitHub secret format"""
    
    credentials_file = "google_credentials.json"
    
    # Check if credentials file exists
    if not os.path.exists(credentials_file):
        print(f"❌ Error: {credentials_file} not found!")
        print("Please ensure your Google service account credentials file is in this directory.")
        return False
    
    try:
        # Read the JSON file
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        
        # Validate required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in credentials]
        
        if missing_fields:
            print(f"❌ Error: Missing required fields in credentials: {missing_fields}")
            return False
        
        # Convert to single line JSON
        single_line_json = json.dumps(credentials, separators=(',', ':'))
        
        print("✅ Google credentials successfully prepared for GitHub Secrets!")
        print("=" * 60)
        print("📋 Copy the following content to your GitHub Secret:")
        print("=" * 60)
        print()
        print(single_line_json)
        print()
        print("=" * 60)
        print("🔧 GitHub Secret Setup Instructions:")
        print("=" * 60)
        print("1. Go to your GitHub repository")
        print("2. Navigate to Settings → Secrets and variables → Actions")
        print("3. Click 'New repository secret'")
        print("4. Name: GOOGLE_CREDENTIALS_JSON")
        print("5. Value: Paste the JSON content above")
        print("6. Click 'Add secret'")
        print()
        print("🎉 Your GitHub Actions workflow will now have access to Google Sheets!")
        
        # Also save to a file for easy copying
        output_file = "github_secret_credentials.txt"
        with open(output_file, 'w') as f:
            f.write(single_line_json)
        
        print(f"💾 Also saved to: {output_file}")
        print("⚠️  Remember to delete this file after copying to GitHub!")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {credentials_file}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials file: {e}")
        return False

def main():
    """Main function"""
    print("🔑 Google Credentials → GitHub Secret Converter")
    print("=" * 50)
    
    success = prepare_github_secret()
    
    if not success:
        print("\n💡 Troubleshooting Tips:")
        print("- Ensure google_credentials.json is a valid JSON file")
        print("- Check that the file contains all required Google service account fields")
        print("- Verify the file is in the same directory as this script")
        sys.exit(1)
    
    print("\n✅ Setup complete! Your GitHub Actions are ready to sync to Google Sheets.")

if __name__ == "__main__":
    main()
