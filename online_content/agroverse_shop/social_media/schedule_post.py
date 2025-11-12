#!/usr/bin/env python3
"""
Schedule an existing draft post for publication
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')

# Post ID from the test
POST_ID = "523d10f0-1ac6-4b3b-96e9-c60f90627f07"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID
}

print("\n" + "="*80)
print("SCHEDULING POST FOR PUBLICATION")
print("="*80)

# Try to publish with scheduled date
schedule_data = {
    "publishDate": "2025-10-14T09:00:00.000Z"
}

print(f"\nScheduling post ID: {POST_ID}")
print(f"Publish date: October 14, 2025 at 9:00 AM UTC\n")

response = requests.post(
    f"https://www.wixapis.com/blog/v3/draft-posts/{POST_ID}/publish",
    headers=headers,
    json=schedule_data
)

print(f"Status Code: {response.status_code}")
print(f"Response:\n{response.text}\n")

if response.status_code in [200, 201]:
    print("="*80)
    print("✅ SUCCESS! Post Scheduled!")
    print("="*80)
    result = response.json()
    post = result.get('post', {})
    print(f"Post ID: {post.get('id', 'N/A')}")
    print(f"Status: {post.get('status', 'N/A')}")
    print(f"First Published: {post.get('firstPublishedDate', 'N/A')}")
    print(f"\n🎉 Check Wix Dashboard > Blog > Posts > Scheduled")
else:
    print("❌ Scheduling failed")
    print("\nNote: If publishDate is not supported, you may need to:")
    print("1. Go to Wix Dashboard manually")
    print("2. Find the draft post")
    print("3. Use Wix's built-in scheduler to set publish date")

