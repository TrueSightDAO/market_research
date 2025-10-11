#!/usr/bin/env python3
"""
Get Wix member/owner ID for blog post creation
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
ACCOUNT_ID = os.getenv('WIX_ACCOUNT_ID')

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID,
    "wix-account-id": ACCOUNT_ID
}

print("\n" + "="*80)
print("RETRIEVING WIX MEMBER/OWNER INFORMATION")
print("="*80)

# Try to get existing posts to see what memberId they use
print("\n1. Querying existing blog posts to find memberId...")
response = requests.post(
    "https://www.wixapis.com/blog/v3/posts/query",
    headers=headers,
    json={"query": {"paging": {"limit": 5}}}
)

if response.status_code == 200:
    result = response.json()
    posts = result.get('posts', [])
    
    if posts:
        print(f"✅ Found {len(posts)} posts\n")
        for i, post in enumerate(posts[:3]):
            print(f"Post {i+1}:")
            print(f"  Title: {post.get('title', 'N/A')}")
            print(f"  Owner ID: {post.get('ownerId', 'N/A')}")
            print(f"  Member ID: {post.get('memberId', 'N/A')}")
            print(f"  Has Owner: {post.get('hasOwner', 'N/A')}")
            print()
        
        # Get the first post's owner info to use
        if posts[0].get('ownerId'):
            owner_id = posts[0]['ownerId']
            print(f"✅ Found Owner ID to use: {owner_id}")
            print(f"\n💡 Add this to your .env file:")
            print(f"   WIX_OWNER_ID={owner_id}")
        elif posts[0].get('memberId'):
            member_id = posts[0]['memberId']
            print(f"✅ Found Member ID to use: {member_id}")
            print(f"\n💡 Add this to your .env file:")
            print(f"   WIX_MEMBER_ID={member_id}")
    else:
        print("⚠️  No posts found")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Response: {response.text}")

# Try to get site members
print("\n2. Trying to get site members...")
response2 = requests.post(
    "https://www.wixapis.com/members/v1/members/query",
    headers=headers,
    json={"query": {"paging": {"limit": 5}}}
)

print(f"Status: {response2.status_code}")
if response2.status_code == 200:
    result2 = response2.json()
    members = result2.get('members', [])
    print(f"Found {len(members)} members")
    if members:
        for member in members[:2]:
            print(f"  Member ID: {member.get('id', 'N/A')}")
            print(f"  Contact ID: {member.get('contactId', 'N/A')}")
else:
    print(f"Response: {response2.text}")

print("\n" + "="*80)

