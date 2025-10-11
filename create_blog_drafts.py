#!/usr/bin/env python3
"""
Create Wix blog drafts from schedule and update Google Sheets with draft IDs
This allows you to review/edit drafts in Wix and reference them by primary_key
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from wix_blog_publisher import WixBlogPublisher
import subprocess

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
MEMBER_ID = os.getenv('WIX_MEMBER_ID')

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID
}

def create_draft_from_schedule_row(row):
    """Create a basic Wix draft from a schedule row"""
    
    # Create minimal Ricos content with title and excerpt
    ricos_content = {
        "nodes": [
            {
                "type": "HEADING",
                "id": "h1",
                "nodes": [{"type": "TEXT", "id": "t1", "nodes": [], "textData": {
                    "text": row['Blog Title'],
                    "decorations": []
                }}],
                "headingData": {"level": 1}
            },
            {
                "type": "PARAGRAPH",
                "id": "p1",
                "nodes": [{"type": "TEXT", "id": "t2", "nodes": [], "textData": {
                    "text": f"[Content Outline: {row['Content Outline']}]",
                    "decorations": []
                }}],
                "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
            },
            {
                "type": "PARAGRAPH",
                "id": "p2",
                "nodes": [{"type": "TEXT", "id": "t3", "nodes": [], "textData": {
                    "text": "This blog post draft was created automatically. Edit this content in Wix dashboard to add the full article.",
                    "decorations": []
                }}],
                "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
            }
        ]
    }
    
    # Generate slug from title
    slug = row['Blog Title'].lower().replace(' ', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')[:100]
    
    draft_data = {
        "draftPost": {
            "title": row['Blog Title'],
            "memberId": MEMBER_ID,
            "excerpt": row.get('CTA', '')[:500] if pd.notna(row.get('CTA')) else '',
            "richContent": ricos_content,
            "seoSlug": slug,
            "seoData": {
                "slug": slug,
                "description": row.get('CTA', '')[:160] if pd.notna(row.get('CTA')) else '',
                "title": row['Blog Title'][:60]
            }
        }
    }
    
    response = requests.post(
        "https://www.wixapis.com/blog/v3/draft-posts",
        headers=headers,
        json=draft_data
    )
    
    if response.status_code == 200:
        result = response.json()
        draft_id = result['draftPost']['id']
        return draft_id
    else:
        print(f"❌ Error creating draft: {response.text}")
        return None


def main():
    print("\n" + "="*80)
    print("CREATE WIX DRAFTS FROM BLOG SCHEDULE")
    print("="*80)
    
    # Read blog schedule
    df = pd.read_csv('blog_schedule.csv')
    
    # Ensure Wix Draft ID column exists
    if 'Wix Draft ID' not in df.columns:
        df.insert(1, 'Wix Draft ID', '')
    
    # Find posts without draft IDs
    needs_draft = df[df['Wix Draft ID'].isna() | (df['Wix Draft ID'] == '')]
    
    print(f"\n📊 Blog Schedule Status:")
    print(f"   Total posts: {len(df)}")
    print(f"   Has draft ID: {len(df) - len(needs_draft)}")
    print(f"   Needs draft: {len(needs_draft)}")
    
    if len(needs_draft) == 0:
        print("\n✅ All posts already have draft IDs!")
        print("   Nothing to create.")
        return
    
    print(f"\n📝 Posts to create as drafts:")
    for idx, row in needs_draft.iterrows():
        print(f"   - {row['Blog Title'][:60]}...")
    
    response = input("\nCreate drafts for these posts? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Cancelled")
        return
    
    # Create drafts
    created_count = 0
    for idx, row in needs_draft.iterrows():
        print(f"\n📝 Creating draft: {row['Blog Title'][:60]}...")
        
        draft_id = create_draft_from_schedule_row(row)
        
        if draft_id:
            df.at[idx, 'Wix Draft ID'] = draft_id
            created_count += 1
            print(f"   ✅ Created! Draft ID: {draft_id}")
        else:
            print(f"   ❌ Failed")
    
    # Save updated CSV
    df.to_csv('blog_schedule.csv', index=False)
    
    print("\n" + "="*80)
    print(f"✅ Created {created_count} draft posts in Wix")
    print("="*80)
    
    # Sync to Google Sheets
    print("\n🔄 Syncing to Google Sheets...")
    result = subprocess.run(['python', 'sync_blog_schedule.py'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Google Sheets updated with draft IDs!")
    else:
        print("⚠️  Sync may have had issues - check output")
    
    print("\n📍 Next Steps:")
    print("1. View drafts in Wix Dashboard > Blog > Drafts")
    print("2. Edit each draft to add full content, images, Instagram embeds")
    print("3. Schedule each post for its publish date")
    print("4. Update status in Google Sheets (e.g., 'IN REVIEW', 'SCHEDULED')")
    print(f"\n🔗 Google Sheets: https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ")
    print(f"🔗 Wix Dashboard: https://www.wix.com/dashboard")


if __name__ == "__main__":
    main()
EOF
