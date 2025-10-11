#!/usr/bin/env python3
"""
Publish the Okanogan Journey blog post to Wix
"""

from wix_blog_publisher import WixBlogPublisher

def main():
    print("\n" + "="*80)
    print("PUBLISHING: From Okanogan to Your Table")
    print("="*80)
    
    # Initialize publisher
    publisher = WixBlogPublisher()
    
    # Test connection first
    if not publisher.test_connection():
        print("\n❌ Cannot proceed - API connection failed")
        return
    
    # Read the blog post content
    print("\n📖 Reading blog post content...")
    with open('blog_posts/okanogan_journey.md', 'r') as f:
        content = f.read()
    
    # Extract metadata from the content
    title = "From Okanogan to Your Table: The Journey of Regenerative Cacao"
    
    excerpt = ("Experience the journey of Brazilian regenerative cacao from Pará & Bahia farms "
               "to Okanogan Fall Barter Faire. Behind-the-scenes logistics, border crossings, "
               "and community impact stories.")
    
    seo_slug = "okanogan-regenerative-cacao-journey"
    
    # Remove metadata section from content (lines starting with ** at the top)
    content_lines = content.split('\n')
    clean_content = []
    skip_metadata = True
    
    for line in content_lines:
        if skip_metadata and line.startswith('---') and len(clean_content) > 0:
            skip_metadata = False
            continue
        if not skip_metadata:
            clean_content.append(line)
        elif line.startswith('# '):
            # Found the actual title, start including
            skip_metadata = False
            clean_content.append(line)
    
    clean_content_str = '\n'.join(clean_content)
    
    print(f"\n📝 Post Details:")
    print(f"   Title: {title}")
    print(f"   Excerpt: {excerpt[:80]}...")
    print(f"   Slug: {seo_slug}")
    print(f"   Content Length: {len(clean_content_str)} characters")
    
    # Ask for confirmation
    print(f"\n⚠️  IMPORTANT: This will create a SCHEDULED post on your Wix site.")
    print(f"   Scheduled to publish: October 14, 2025 at 9:00 AM UTC")
    print(f"   You can review/edit in Wix dashboard before the scheduled date.")
    
    response = input("\n   Proceed? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Cancelled by user")
        return
    
    # Schedule post for October 14, 2025 at 9:00 AM UTC
    scheduled_date = "2025-10-14T09:00:00Z"
    
    print(f"\n📅 Scheduling post for: October 14, 2025 at 9:00 AM UTC")
    
    # Create draft post with scheduled date
    result = publisher.create_draft_post(
        title=title,
        content_markdown=clean_content_str,
        excerpt=excerpt,
        seo_slug=seo_slug,
        publish_immediately=False,  # Don't publish immediately
        scheduled_date=scheduled_date  # Schedule for future
    )
    
    if result:
        print("\n" + "="*80)
        print("✅ SUCCESS! Post Scheduled for October 14, 2025!")
        print("="*80)
        print("\n📍 Next Steps:")
        print("1. Go to your Wix Dashboard: https://www.wix.com/dashboard")
        print("2. Navigate to Blog > Posts > Scheduled tab")
        print("3. Find the scheduled post and review it")
        print("4. Add featured image (1200 x 628px recommended)")
        print("5. Add Instagram embeds manually where noted")
        print("6. Post will auto-publish on Oct 14 at 9:00 AM UTC")
        print("7. OR click 'Publish Now' to publish immediately")
        print("\n🔗 Your blog: https://www.agroverse.shop/blog")
    else:
        print("\n❌ Failed to create post - check error messages above")


if __name__ == "__main__":
    main()

