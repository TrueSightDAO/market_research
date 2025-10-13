#!/usr/bin/env python3
"""
Update Wix blog draft metadata only (title, excerpt, SEO)
Leaves body content untouched to avoid Ricos JSON conversion issues

Usage: python update_wix_metadata_only.py <primary_key>
"""

import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID
}

def update_draft_metadata(draft_id, title, excerpt, seo_slug):
    """Update only the metadata of a Wix draft post"""
    
    update_data = {
        "draftPost": {
            "title": title,
            "excerpt": excerpt,
            "seoSlug": seo_slug,
            "seoData": {
                "slug": seo_slug,
                "description": excerpt,
                "title": title[:60]
            }
        }
    }
    
    response = requests.patch(
        f"https://www.wixapis.com/blog/v3/draft-posts/{draft_id}",
        headers=headers,
        json=update_data
    )
    
    return response


def main():
    print("\n" + "="*80)
    print("UPDATE WIX BLOG DRAFT METADATA ONLY")
    print("="*80)
    
    if len(sys.argv) < 2:
        print("\n❌ Error: Missing primary_key argument")
        print("\nUsage:")
        print("  python update_wix_metadata_only.py <primary_key>")
        print("\nExample:")
        print("  python update_wix_metadata_only.py 4098f184")
        sys.exit(1)
    
    primary_key = sys.argv[1]
    
    # Read blog schedule from Google Sheets to get draft ID
    print(f"\n🔍 Looking up post {primary_key}...")
    
    # For now, read from local CSV (could be enhanced to read from Google Sheets)
    try:
        df = pd.read_csv('blog_schedule.csv')
        
        # Generate primary keys if not in CSV
        if 'primary_key' not in df.columns or df['primary_key'].isna().all():
            import hashlib
            def generate_pk(row):
                date_str = str(row.get('Publish Date', ''))
                title = str(row.get('Blog Title', ''))
                unique_string = f'{date_str}_{title}'
                hash_object = hashlib.md5(unique_string.encode())
                return hash_object.hexdigest()[:8]
            df['primary_key'] = df.apply(generate_pk, axis=1)
        
        post_row = df[df['primary_key'] == primary_key]
        
        if post_row.empty:
            print(f"\n❌ Error: No post found with primary key: {primary_key}")
            sys.exit(1)
        
        post_row = post_row.iloc[0]
        draft_id = post_row.get('Wix Draft ID', '')
        
        if not draft_id or pd.isna(draft_id):
            print(f"\n❌ Error: Post has no Wix Draft ID")
            print(f"   Create the draft first with: python create_blog_drafts.py")
            sys.exit(1)
        
        title = post_row['Blog Title']
        excerpt = post_row.get('CTA', 'Blog post content coming soon.')
        
        # Generate SEO slug from title
        seo_slug = title.lower()
        seo_slug = seo_slug.replace(' ', '-')
        seo_slug = ''.join(c for c in seo_slug if c.isalnum() or c == '-')
        
        print(f"\n📋 Post Details:")
        print(f"   Primary Key: {primary_key}")
        print(f"   Wix Draft ID: {draft_id}")
        print(f"   Title: {title}")
        print(f"   Excerpt: {excerpt[:80]}...")
        print(f"   SEO Slug: {seo_slug}")
        
        print(f"\n🔄 Updating draft metadata...")
        
        response = update_draft_metadata(draft_id, title, excerpt, seo_slug)
        
        if response.status_code == 200:
            result = response.json()
            updated_draft = result.get('draftPost', {})
            
            print("\n" + "="*80)
            print("✅ SUCCESS! Draft Metadata Updated!")
            print("="*80)
            print(f"Draft ID: {updated_draft.get('id', 'N/A')}")
            print(f"Title: {updated_draft.get('title', 'N/A')}")
            print(f"Status: {updated_draft.get('status', 'N/A')}")
            print(f"SEO Slug: {updated_draft.get('seoSlug', 'N/A')}")
            
            # Find markdown file
            publish_date = post_row['Publish Date']
            md_file = f"agroverse_blog_posts/{publish_date}_{primary_key}_*.md"
            github_url = f"https://github.com/TrueSightDAO/market_research/blob/main/agroverse_blog_posts/{publish_date}_{primary_key}_*"
            
            print(f"\n📍 Next Steps:")
            print(f"1. Go to Wix Dashboard > Blog > Drafts")
            print(f"2. Find: {title}")
            print(f"3. Manually paste content from GitHub:")
            print(f"   {github_url}")
            print(f"4. Add images and Instagram embeds")
            print(f"5. Review formatting")
            print(f"6. Schedule for: {post_row['Publish Date']}")
            print(f"\n🔗 Wix Dashboard: https://www.wix.com/dashboard/{SITE_ID}/blog/drafts")
        else:
            print(f"\n❌ Update failed:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

