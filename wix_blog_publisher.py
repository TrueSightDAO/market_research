#!/usr/bin/env python3
"""
Wix Blog Publisher
Publishes blog posts to Wix using their REST API
"""

import os
import requests
import json
import re
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class WixBlogPublisher:
    def __init__(self):
        self.api_key = os.getenv('WIX_API_KEY')
        self.site_id = os.getenv('WIX_SITE_ID')
        self.account_id = os.getenv('WIX_ACCOUNT_ID')
        self.member_id = os.getenv('WIX_MEMBER_ID')
        
        if not all([self.api_key, self.site_id, self.member_id]):
            raise ValueError("Missing Wix API credentials in .env file (need API_KEY, SITE_ID, MEMBER_ID)")
        
        # Wix Blog API v3 endpoints
        self.base_url = "https://www.wixapis.com/blog/v3"
        self.draft_posts_url = f"{self.base_url}/draft-posts"
        self.posts_url = f"{self.base_url}/posts"
        self.media_url = "https://www.wixapis.com/v1/files"
        
        print(f"✅ Initialized Wix Blog Publisher")
        print(f"   Site ID: {self.site_id}")
    
    def get_headers(self):
        """Generate request headers with authentication"""
        return {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "wix-site-id": self.site_id
        }
    
    def markdown_to_ricos(self, markdown_content):
        """
        Convert Markdown to Wix Ricos JSON format
        Simplified version - handles basic elements
        """
        nodes = []
        
        # Split content by lines
        lines = markdown_content.strip().split('\n')
        
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines between elements
            if not line:
                if current_paragraph:
                    # Add accumulated paragraph
                    paragraph_text = ' '.join(current_paragraph)
                    nodes.append(self._create_paragraph(paragraph_text))
                    current_paragraph = []
                continue
            
            # Check for headings
            if line.startswith('# '):
                if current_paragraph:
                    nodes.append(self._create_paragraph(' '.join(current_paragraph)))
                    current_paragraph = []
                nodes.append(self._create_heading(line[2:], 1))
            elif line.startswith('## '):
                if current_paragraph:
                    nodes.append(self._create_paragraph(' '.join(current_paragraph)))
                    current_paragraph = []
                nodes.append(self._create_heading(line[3:], 2))
            elif line.startswith('### '):
                if current_paragraph:
                    nodes.append(self._create_paragraph(' '.join(current_paragraph)))
                    current_paragraph = []
                nodes.append(self._create_heading(line[4:], 3))
            # Check for list items
            elif line.startswith('- ') or line.startswith('* '):
                if current_paragraph:
                    nodes.append(self._create_paragraph(' '.join(current_paragraph)))
                    current_paragraph = []
                # For now, treat list items as paragraphs (Ricos lists are complex)
                nodes.append(self._create_paragraph(f"• {line[2:]}"))
            elif re.match(r'^\d+\.', line):
                if current_paragraph:
                    nodes.append(self._create_paragraph(' '.join(current_paragraph)))
                    current_paragraph = []
                nodes.append(self._create_paragraph(line))
            # Skip certain markdown elements for now
            elif line.startswith('**') or line.startswith('*[') or line.startswith('---'):
                continue
            else:
                # Regular paragraph text
                current_paragraph.append(line)
        
        # Add any remaining paragraph
        if current_paragraph:
            nodes.append(self._create_paragraph(' '.join(current_paragraph)))
        
        return {
            "nodes": nodes,
            "metadata": {
                "version": 1,
                "createdTimestamp": datetime.now().isoformat()
            }
        }
    
    def _create_paragraph(self, text):
        """Create a paragraph node in Ricos format"""
        # Handle bold text **text**
        decorations = []
        clean_text = text
        
        # Simple bold handling (Wix Ricos uses more complex decoration system)
        # For now, keeping it simple
        clean_text = clean_text.replace('**', '')
        
        return {
            "type": "PARAGRAPH",
            "id": self._generate_id(),
            "nodes": [{
                "type": "TEXT",
                "id": self._generate_id(),
                "nodes": [],
                "textData": {
                    "text": clean_text,
                    "decorations": decorations
                }
            }],
            "paragraphData": {
                "textStyle": {
                    "textAlignment": "AUTO"
                },
                "indentation": 0
            }
        }
    
    def _create_heading(self, text, level):
        """Create a heading node in Ricos format"""
        return {
            "type": "HEADING",
            "id": self._generate_id(),
            "nodes": [{
                "type": "TEXT",
                "id": self._generate_id(),
                "nodes": [],
                "textData": {
                    "text": text,
                    "decorations": []
                }
            }],
            "headingData": {
                "level": level,
                "textStyle": {
                    "textAlignment": "AUTO"
                },
                "indentation": 0
            }
        }
    
    def _generate_id(self):
        """Generate a random ID for Ricos nodes"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    def create_draft_post(self, title, content_markdown, excerpt=None, seo_slug=None, 
                         cover_image_url=None, publish_immediately=False, scheduled_date=None):
        """
        Create a blog post on Wix
        
        Args:
            title: Blog post title
            content_markdown: Content in Markdown format
            excerpt: Short description/excerpt
            seo_slug: URL slug (auto-generated from title if not provided)
            cover_image_url: URL of cover image
            publish_immediately: Whether to publish or save as draft
            scheduled_date: ISO 8601 date string for scheduled publishing (e.g., '2025-10-14T09:00:00Z')
        """
        print(f"\n{'='*80}")
        print(f"Creating blog post: {title}")
        print(f"{'='*80}")
        
        # Convert markdown to Ricos JSON
        print("📝 Converting content to Wix Ricos format...")
        ricos_content = self.markdown_to_ricos(content_markdown)
        
        # Generate slug if not provided
        if not seo_slug:
            seo_slug = self._slugify(title)
        
        # Prepare post data for Wix Blog API v3
        post_data = {
            "draftPost": {
                "title": title,
                "memberId": self.member_id,  # Required: Author/owner ID
                "excerpt": excerpt or content_markdown[:200],
                "richContent": ricos_content,
                "slug": seo_slug,
                "seoData": {
                    "slug": seo_slug,
                    "description": excerpt or content_markdown[:160]
                }
            }
        }
        
        # Add scheduled date if provided
        if scheduled_date:
            post_data["draftPost"]["scheduledPublishDate"] = scheduled_date
            print(f"📅 Scheduled for: {scheduled_date}")
        
        # Add cover image if provided
        if cover_image_url:
            print(f"🖼️  Adding cover image from: {cover_image_url}")
            # Note: For production, you'd upload to Wix Media Manager first
            # For now, we'll skip the image
        
        print(f"🌐 Making API request to Wix...")
        print(f"   Endpoint: {self.draft_posts_url}")
        
        try:
            response = requests.post(
                self.draft_posts_url,
                headers=self.get_headers(),
                json=post_data
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                post_id = result.get('post', {}).get('id', 'Unknown')
                
                print(f"✅ Successfully created draft post!")
                print(f"   Post ID: {post_id}")
                
                if publish_immediately:
                    print(f"\n📢 Publishing post...")
                    publish_result = self.publish_post(post_id)
                    return publish_result
                else:
                    print(f"\n📝 Post saved as DRAFT")
                    print(f"   Review in Wix dashboard before publishing")
                
                return result
            else:
                print(f"❌ Error creating post:")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            return None
    
    def publish_post(self, post_id):
        """Publish a draft post"""
        try:
            response = requests.post(
                f"{self.base_url}/{post_id}/publish",
                headers=self.get_headers()
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Post published successfully!")
                return response.json()
            else:
                print(f"❌ Error publishing post:")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Exception publishing: {e}")
            return None
    
    def _slugify(self, text):
        """Convert title to URL-friendly slug"""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces with hyphens
        text = re.sub(r'\s+', '-', text)
        # Remove special characters
        text = re.sub(r'[^a-z0-9\-]', '', text)
        # Remove multiple hyphens
        text = re.sub(r'\-+', '-', text)
        # Trim hyphens from ends
        text = text.strip('-')
        # Limit length
        return text[:100]
    
    def test_connection(self):
        """Test API connection"""
        print("\n🔍 Testing Wix API connection...")
        try:
            # Try to query posts (read operation)
            response = requests.post(
                f"{self.posts_url}/query",
                headers=self.get_headers(),
                json={"query": {"paging": {"limit": 1}}}
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully connected to Wix API!")
                result = response.json()
                posts = result.get('posts', [])
                total = result.get('pagingMetadata', {}).get('total', len(posts))
                print(f"   Current blog posts: {total}")
                return True
            else:
                print(f"❌ Connection failed:")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False


def main():
    """Main function to test the publisher"""
    print("\n" + "="*80)
    print("WIX BLOG PUBLISHER - TEST")
    print("="*80)
    
    # Initialize publisher
    publisher = WixBlogPublisher()
    
    # Test connection
    if not publisher.test_connection():
        print("\n❌ Cannot proceed without valid API connection")
        print("   Check your WIX_API_KEY and WIX_SITE_ID in .env file")
        return
    
    print("\n✅ Ready to publish blog posts!")
    print("\nNext steps:")
    print("1. Review blog_posts/okanogan_journey.md")
    print("2. Run: python publish_okanogan_post.py")
    print("3. Or manually copy content to Wix dashboard")


if __name__ == "__main__":
    main()

