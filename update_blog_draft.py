#!/usr/bin/env python3
"""
Update an existing Wix blog draft by primary key
Usage: python update_blog_draft.py <primary_key> <markdown_file>
"""

import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv
from wix_blog_publisher import WixBlogPublisher

load_dotenv()

API_KEY = os.getenv('WIX_API_KEY')
SITE_ID = os.getenv('WIX_SITE_ID')
MEMBER_ID = os.getenv('WIX_MEMBER_ID')

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "wix-site-id": SITE_ID
}

def update_draft_content(draft_id, title, content_markdown, excerpt=None, seo_slug=None):
    """Update an existing Wix draft post"""
    
    publisher = WixBlogPublisher()
    
    # Convert markdown to Ricos
    ricos_content = publisher.markdown_to_ricos(content_markdown)
    
    # Generate slug if needed
    if not seo_slug:
        seo_slug = publisher._slugify(title)
    
    update_data = {
        "draftPost": {
            "title": title,
            "richContent": ricos_content,
            "excerpt": excerpt or content_markdown[:500],
            "seoSlug": seo_slug,
            "seoData": {
                "slug": seo_slug,
                "description": excerpt or content_markdown[:160],
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
    print("UPDATE WIX BLOG DRAFT BY PRIMARY KEY")
    print("="*80)
    
    if len(sys.argv) < 2:
        print("\n❌ Error: Missing primary_key argument")
        print("\nUsage:")
        print("  python update_blog_draft.py <primary_key> <markdown_file>")
        print("\nExample:")
        print("  python update_blog_draft.py 4098f184 agroverse_blog_posts/okanogan_journey.md")
        print("\nOr interactive mode:")
        print("  python update_blog_draft.py")
        sys.exit(1)
    
    # Get arguments
    if len(sys.argv) >= 3:
        primary_key = sys.argv[1]
        markdown_file = sys.argv[2]
    else:
        # Interactive mode
        primary_key = input("\nEnter primary key from Google Sheets: ").strip()
        markdown_file = input("Enter markdown file path: ").strip()
    
    # Read blog schedule to get draft ID
    df = pd.read_csv('blog_schedule.csv')
    
    # Generate primary keys if not in CSV
    if 'primary_key' not in df.columns or df['primary_key'].isna().all():
        print("🔑 Generating primary keys...")
        import hashlib
        def generate_pk(row):
            date_str = str(row.get('Publish Date', ''))
            title = str(row.get('Blog Title', ''))
            unique_string = f'{date_str}_{title}'
            hash_object = hashlib.md5(unique_string.encode())
            return hash_object.hexdigest()[:8]
        df['primary_key'] = df.apply(generate_pk, axis=1)
    
    # Find the post
    post_row = df[df['primary_key'] == primary_key]
    
    if post_row.empty:
        print(f"\n❌ Error: No post found with primary key: {primary_key}")
        print(f"\nAvailable primary keys:")
        for idx, row in df.iterrows():
            pk = row.get('primary_key', 'N/A')
            title = row.get('Blog Title', 'Unknown')[:50]
            print(f"  {pk}: {title}...")
        sys.exit(1)
    
    post_row = post_row.iloc[0]
    draft_id = post_row.get('Wix Draft ID', '')
    
    if not draft_id or pd.isna(draft_id):
        print(f"\n❌ Error: Post has no Wix Draft ID")
        print(f"   Primary Key: {primary_key}")
        print(f"   Title: {post_row['Blog Title']}")
        print(f"\n💡 Create the draft first with:")
        print(f"   python create_blog_drafts.py")
        sys.exit(1)
    
    print(f"\n📋 Post Details:")
    print(f"   Primary Key: {primary_key}")
    print(f"   Title: {post_row['Blog Title']}")
    print(f"   Wix Draft ID: {draft_id}")
    print(f"   Publish Date: {post_row['Publish Date']}")
    
    # Read markdown content
    if not os.path.exists(markdown_file):
        print(f"\n❌ Error: File not found: {markdown_file}")
        sys.exit(1)
    
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Remove metadata section from markdown
    content_lines = content.split('\n')
    clean_content = []
    skip_until_content = True
    
    for line in content_lines:
        if skip_until_content and line.startswith('# '):
            skip_until_content = False
        if not skip_until_content:
            clean_content.append(line)
    
    clean_markdown = '\n'.join(clean_content)
    
    print(f"\n📄 Content loaded:")
    print(f"   File: {markdown_file}")
    print(f"   Length: {len(clean_markdown)} characters")
    print(f"   Words: ~{len(clean_markdown.split())} words")
    
    # Confirm update
    response = input(f"\nUpdate draft {draft_id} with this content? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Cancelled")
        return
    
    # Update the draft
    print(f"\n🔄 Updating Wix draft...")
    
    update_response = update_draft_content(
        draft_id=draft_id,
        title=post_row['Blog Title'],
        content_markdown=clean_markdown,
        excerpt=post_row.get('CTA', ''),
        seo_slug=None  # Auto-generate from title
    )
    
    if update_response.status_code == 200:
        result = update_response.json()
        updated_draft = result.get('draftPost', {})
        
        print("\n" + "="*80)
        print("✅ SUCCESS! Draft Updated!")
        print("="*80)
        print(f"Draft ID: {updated_draft.get('id', 'N/A')}")
        print(f"Title: {updated_draft.get('title', 'N/A')}")
        print(f"Status: {updated_draft.get('status', 'N/A')}")
        print(f"Reading Time: {updated_draft.get('minutesToRead', 'N/A')} min")
        
        print(f"\n📍 Next Steps:")
        print(f"1. Go to Wix Dashboard > Blog > Drafts")
        print(f"2. Find: {post_row['Blog Title'][:50]}...")
        print(f"3. Add images and Instagram embeds")
        print(f"4. Review formatting")
        print(f"5. Schedule for: {post_row['Publish Date']}")
        print(f"\n🔗 Wix Dashboard: https://www.wix.com/dashboard")
    else:
        print(f"\n❌ Update failed:")
        print(f"   Status: {update_response.status_code}")
        print(f"   Response: {update_response.text}")


if __name__ == "__main__":
    main()

