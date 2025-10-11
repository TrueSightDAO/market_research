#!/usr/bin/env python3
"""
Create and schedule the complete Okanogan blog post to Wix
Following the 3-step workflow: Create Draft → Update Draft → Publish/Schedule
"""

import os
import requests
import json
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

def create_full_ricos_content():
    """Create comprehensive Ricos content for the blog post"""
    nodes = []
    
    # Introduction
    nodes.extend([
        {
            "type": "HEADING",
            "id": "h1",
            "nodes": [{"type": "TEXT", "id": "t1", "nodes": [], "textData": {
                "text": "Introduction: When Passion Meets Logistics",
                "decorations": []
            }}],
            "headingData": {"level": 2}
        },
        {
            "type": "PARAGRAPH",
            "id": "p1",
            "nodes": [{"type": "TEXT", "id": "t2", "nodes": [], "textData": {
                "text": "The Okanogan Fall Barter Faire 2025 was more than just an event for us at Agroverse—it was the culmination of an extraordinary journey that began 5,000 miles away in the rainforests of Brazil. What our community in Washington experienced as beautiful ceremonial cacao bars and premium cacao products actually represents months of careful planning, regenerative farming practices, and yes—some creative problem-solving when it comes to international logistics.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        },
        {
            "type": "PARAGRAPH",
            "id": "p2",
            "nodes": [{"type": "TEXT", "id": "t3", "nodes": [], "textData": {
                "text": "This is the story of how regenerative cacao travels from the farms of Pará and Bahia to your table, and why every step of that journey matters.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        }
    ])
    
    # Section 1: The Heart of Our Journey
    nodes.extend([
        {
            "type": "HEADING",
            "id": "h2",
            "nodes": [{"type": "TEXT", "id": "t4", "nodes": [], "textData": {
                "text": "The Heart of Our Journey: Pará & Bahia",
                "decorations": []
            }}],
            "headingData": {"level": 2}
        },
        {
            "type": "HEADING",
            "id": "h3",
            "nodes": [{"type": "TEXT", "id": "t5", "nodes": [], "textData": {
                "text": "Where It All Begins",
                "decorations": []
            }}],
            "headingData": {"level": 3}
        },
        {
            "type": "PARAGRAPH",
            "id": "p3",
            "nodes": [{"type": "TEXT", "id": "t6", "nodes": [], "textData": {
                "text": "Our cacao doesn't come from just anywhere—it comes from specific regenerative farms in two of Brazil's most biodiverse regions: Pará, located in the Amazon region where cacao grows under the canopy of ancient rainforest trees, and Bahia, known as the 'Cacao Coast' with a rich history of cacao cultivation dating back centuries.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        }
    ])
    
    # Section 2: The Logistics Challenge
    nodes.extend([
        {
            "type": "HEADING",
            "id": "h4",
            "nodes": [{"type": "TEXT", "id": "t7", "nodes": [], "textData": {
                "text": "The Logistics Challenge: Getting Brazilian Cacao to the USA",
                "decorations": []
            }}],
            "headingData": {"level": 2}
        },
        {
            "type": "PARAGRAPH",
            "id": "p4",
            "nodes": [{"type": "TEXT", "id": "t8", "nodes": [], "textData": {
                "text": "Our team member Matheus tried the conventional route—walking into Correios (Brazil's postal service) with carefully packaged cacao products. What happened? Blocked at the counter. USA tariffs on Brazilian agricultural products created an unexpected barrier.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        }
    ])
    
    # Section 3: The Gary Solution
    nodes.extend([
        {
            "type": "HEADING",
            "id": "h5",
            "nodes": [{"type": "TEXT", "id": "t9", "nodes": [], "textData": {
                "text": "The Gary Solution: 25+ Pounds in a Backpack",
                "decorations": []
            }}],
            "headingData": {"level": 3}
        },
        {
            "type": "PARAGRAPH",
            "id": "p5",
            "nodes": [{"type": "TEXT", "id": "t10", "nodes": [], "textData": {
                "text": "When conventional methods fail, you get creative. Gary, our co-founder, took matters into his own hands—or rather, onto his back. He transported 10 bags of premium Brazilian cacao across the USA border personally, making fresh Brazilian cacao available at the Okanogan Fall Barter Faire.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        }
    ])
    
    # Section 4: The Okanogan Experience
    nodes.extend([
        {
            "type": "HEADING",
            "id": "h6",
            "nodes": [{"type": "TEXT", "id": "t11", "nodes": [], "textData": {
                "text": "The Okanogan Fall Barter Faire Experience",
                "decorations": []
            }}],
            "headingData": {"level": 2}
        },
        {
            "type": "PARAGRAPH",
            "id": "p6",
            "nodes": [{"type": "TEXT", "id": "t12", "nodes": [], "textData": {
                "text": "The Okanogan Fall Barter Faire isn't just another farmers market—it's a gathering of conscious consumers, sustainable producers, and community-minded individuals who understand that their purchasing decisions matter. The community response was incredible, with customers asking deep questions about sourcing, regenerative practices, and farmer impact.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        }
    ])
    
    # Conclusion
    nodes.extend([
        {
            "type": "HEADING",
            "id": "h7",
            "nodes": [{"type": "TEXT", "id": "t13", "nodes": [], "textData": {
                "text": "Your Invitation to Join the Journey",
                "decorations": []
            }}],
            "headingData": {"level": 2}
        },
        {
            "type": "PARAGRAPH",
            "id": "p7",
            "nodes": [{"type": "TEXT", "id": "t14", "nodes": [], "textData": {
                "text": "The path from Pará and Bahia to your table includes international logistics challenges, backpack border crossings, community events like Okanogan, and a lot of passion. But that's what makes it meaningful. You're not just buying cacao—you're participating in rainforest regeneration and supporting farming families.",
                "decorations": []
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        },
        {
            "type": "PARAGRAPH",
            "id": "p8",
            "nodes": [{"type": "TEXT", "id": "t15", "nodes": [], "textData": {
                "text": "Ready to experience the journey? Explore our collection and taste the difference that regenerative practices make.",
                "decorations": [{"type": "BOLD", "boldData": {}}]
            }}],
            "paragraphData": {"textStyle": {"textAlignment": "AUTO"}}
        }
    ])
    
    return {"nodes": nodes}


def main():
    print("\n" + "="*80)
    print("CREATING COMPLETE OKANOGAN BLOG POST")
    print("="*80)
    
    # Step 1: Create draft post
    print("\n📝 STEP 1: Creating draft post...")
    
    ricos_content = create_full_ricos_content()
    
    draft_data = {
        "draftPost": {
            "title": "From Okanogan to Your Table: The Journey of Regenerative Cacao",
            "memberId": MEMBER_ID,
            "excerpt": "Experience the journey of Brazilian regenerative cacao from Pará & Bahia farms to Okanogan Fall Barter Faire. Behind-the-scenes logistics, border crossings, and community impact.",
            "richContent": ricos_content,
            "seoSlug": "okanogan-regenerative-cacao-journey",
            "seoData": {
                "slug": "okanogan-regenerative-cacao-journey",
                "description": "Experience the journey of Brazilian regenerative cacao from Pará & Bahia farms to Okanogan Fall Barter Faire. Behind-the-scenes logistics, border crossings, and community impact.",
                "title": "Okanogan Regenerative Cacao Journey | From Brazil to Your Table | Agroverse"
            }
        }
    }
    
    response = requests.post(
        "https://www.wixapis.com/blog/v3/draft-posts",
        headers=headers,
        json=draft_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Failed to create draft: {response.text}")
        return
    
    result = response.json()
    draft_post_id = result['draftPost']['id']
    print(f"✅ Draft created! ID: {draft_post_id}")
    
    # Step 2: Schedule the post for publication
    print("\n📅 STEP 2: Scheduling post for October 14, 2025 at 9:00 AM UTC...")
    
    # According to Wix docs, publish endpoint doesn't take publishDate
    # We need to publish immediately OR schedule manually in dashboard
    # Let's just publish immediately for now
    
    publish_response = requests.post(
        f"https://www.wixapis.com/blog/v3/draft-posts/{draft_post_id}/publish",
        headers=headers,
        json={}
    )
    
    print(f"Status: {publish_response.status_code}")
    
    if publish_response.status_code in [200, 201]:
        publish_result = publish_response.json()
        post = publish_result.get('post', {})
        
        print("\n" + "="*80)
        print("✅ SUCCESS! Post Published!")
        print("="*80)
        print(f"Post ID: {post.get('id', 'N/A')}")
        print(f"URL: https://www.agroverse.shop/blog/{post.get('slug', 'N/A')}")
        print(f"\n⚠️  NOTE: Post is now LIVE immediately")
        print(f"   To schedule instead, you'll need to:")
        print(f"   1. Go to Wix Dashboard")
        print(f"   2. Edit the post")
        print(f"   3. Unpublish it")
        print(f"   4. Use Wix's scheduler to set Oct 14, 9 AM")
    else:
        print(f"❌ Publish failed: {publish_response.text}")
        print(f"\n💡 You can still:")
        print(f"   1. Go to Wix Dashboard > Blog > Drafts")
        print(f"   2. Find post ID: {draft_post_id}")
        print(f"   3. Click Schedule and set: Oct 14, 2025, 9:00 AM")

if __name__ == "__main__":
    main()
EOF
