#!/usr/bin/env python3
"""
Test Wix API with minimal payload to debug the 400 error
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID
}

# Test 1: Minimal draft post
print("\n" + "="*80)
print("TEST 1: Creating minimal draft post")
print("="*80)

minimal_post = {
    "draftPost": {
        "title": "Test Post from API",
        "richContent": {
            "nodes": [
                {
                    "type": "PARAGRAPH",
                    "id": "abc123",
                    "nodes": [
                        {
                            "type": "TEXT",
                            "id": "xyz789",
                            "nodes": [],
                            "textData": {
                                "text": "This is a simple test paragraph.",
                                "decorations": []
                            }
                        }
                    ],
                    "paragraphData": {}
                }
            ]
        }
    }
}

print(f"Payload:\n{json.dumps(minimal_post, indent=2)}\n")

response = requests.post(
    "https://www.wixapis.com/blog/v3/draft-posts",
    headers=headers,
    json=minimal_post
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}\n")

if response.status_code in [200, 201]:
    print("✅ Success! Draft post created")
    result = response.json()
    print(f"Post ID: {result.get('draftPost', {}).get('id', 'Unknown')}")
else:
    print("❌ Failed - trying alternative format...")
    
    # Test 2: Even simpler without richContent
    print("\n" + "="*80)
    print("TEST 2: Draft post without richContent")
    print("="*80)
    
    simple_post = {
        "draftPost": {
            "title": "Test Post Simple",
            "content": "This is simple plain text content."
        }
    }
    
    response2 = requests.post(
        "https://www.wixapis.com/blog/v3/draft-posts",
        headers=headers,
        json=simple_post
    )
    
    print(f"Status Code: {response2.status_code}")
    print(f"Response: {response2.text}\n")

