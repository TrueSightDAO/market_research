#!/usr/bin/env python3
"""
Test creating post with absolute minimal Ricos format
Based on Wix documentation examples
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
MEMBER_ID = os.getenv('WIX_MEMBER_ID')

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID
}

print("\n" + "="*80)
print("TEST: Minimal Scheduled Post")
print("="*80)

# Absolute minimal Ricos content
minimal_ricos = {
    "nodes": [
        {
            "type": "PARAGRAPH",
            "id": "p1",
            "nodes": [
                {
                    "type": "TEXT",
                    "id": "t1",
                    "nodes": [],
                    "textData": {
                        "text": "This is the introduction paragraph for the Okanogan journey blog post.",
                        "decorations": []
                    }
                }
            ],
            "paragraphData": {
                "textStyle": {
                    "textAlignment": "AUTO"
                }
            }
        },
        {
            "type": "HEADING",
            "id": "h1",
            "nodes": [
                {
                    "type": "TEXT",
                    "id": "t2",
                    "nodes": [],
                    "textData": {
                        "text": "The Heart of Our Journey",
                        "decorations": []
                    }
                }
            ],
            "headingData": {
                "level": 2
            }
        },
        {
            "type": "PARAGRAPH",
            "id": "p2",
            "nodes": [
                {
                    "type": "TEXT",
                    "id": "t3",
                    "nodes": [],
                    "textData": {
                        "text": "Our cacao comes from specific regenerative farms in Pará and Bahia, Brazil.",
                        "decorations": []
                    }
                }
            ],
            "paragraphData": {
                "textStyle": {
                    "textAlignment": "AUTO"
                }
            }
        }
    ]
}

post_data = {
    "draftPost": {
        "title": "From Okanogan to Your Table: The Journey of Regenerative Cacao",
        "memberId": MEMBER_ID,
        "richContent": minimal_ricos,
        "scheduledPublishDate": "2025-10-14T09:00:00.000Z"
    }
}

print(f"Member ID: {MEMBER_ID}")
print(f"\nPayload size: {len(json.dumps(post_data))} characters")
print(f"\nSending request...\n")

response = requests.post(
    "https://www.wixapis.com/blog/v3/draft-posts",
    headers=headers,
    json=post_data
)

print(f"Status Code: {response.status_code}")
print(f"Response:\n{response.text}\n")

if response.status_code in [200, 201]:
    result = response.json()
    draft_post = result.get('draftPost', {})
    post_id = draft_post.get('id', 'Unknown')
    
    print("="*80)
    print("✅ SUCCESS! Post Created and Scheduled!")
    print("="*80)
    print(f"Post ID: {post_id}")
    print(f"Title: {draft_post.get('title', 'N/A')}")
    print(f"Scheduled For: {draft_post.get('scheduledPublishDate', 'N/A')}")
    print(f"\n🎉 Check your Wix Dashboard > Blog > Posts > Scheduled tab")
else:
    print("❌ Failed to create post")
    print("\nTrying without scheduledPublishDate to see if that's the issue...")
    
    # Try without schedule
    post_data_no_schedule = {
        "draftPost": {
            "title": "From Okanogan to Your Table: Journey (Test)",
            "memberId": MEMBER_ID,
            "richContent": minimal_ricos
        }
    }
    
    response2 = requests.post(
        "https://www.wixapis.com/blog/v3/draft-posts",
        headers=headers,
        json=post_data_no_schedule
    )
    
    print(f"\nWithout schedule - Status: {response2.status_code}")
    print(f"Response: {response2.text}")

