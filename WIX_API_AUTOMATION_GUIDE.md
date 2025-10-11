# 🤖 Wix Blog API Automation Guide

## ✨ Yes, You Can Automate Blog Publishing to Wix!

Wix provides a comprehensive **Blog API** that allows you to create and publish blog posts programmatically. This means you could potentially write your blog content in Google Docs or your CSV schedule, and automatically publish it to Wix!

**References:**
- [Wix Blog API Documentation](https://dev.wix.com/docs/sdk/backend-modules/blog/posts/introduction)
- [How to Create a Blog Post with Wix API](https://dev.wix.com/digor/api/get-article-content?articleUrl=https%3A%2F%2Fdev.wix.com%2Fdocs%2Fkb-only%2FMCP_REST_RECIPES_KB_ID%2FTRAIN_how-to-create-a-blog-post)

---

## 🎯 What You Can Automate

### **Current Workflow (Manual):**
```
Write in Google Docs
    ↓
Copy to Wix Editor
    ↓
Format (headings, images, links)
    ↓
Add SEO settings
    ↓
Embed Instagram posts
    ↓
Click Publish
```

### **Potential Automated Workflow:**
```
Write in Google Docs or Markdown
    ↓
Run Python script
    ↓
Automatically published to Wix
    (with formatting, images, SEO, embeds)
```

---

## 🔧 Technical Requirements

### **1. Wix Developer Platform Setup**

You'll need to set up Wix's developer platform:

**Steps:**
1. Go to [Wix Developers](https://dev.wix.com/)
2. Create a Developer Account (free)
3. Install **Wix Blocks** or use **Velo by Wix** (Wix's development platform)
4. Generate API Keys with Blog permissions

**Authentication Options:**
- **API Keys**: For server-side automation
- **OAuth 2.0**: For user-authorized access
- **Wix Velo (Backend Code)**: For site-specific automation

### **2. Wix Blog API Access**

**Required Permissions:**
- `blog.posts.write` - Create and edit posts
- `blog.posts.publish` - Publish posts
- `media.files.write` - Upload images

---

## 📝 API Capabilities

### **What You Can Do:**

✅ **Create Draft Posts**
```javascript
draftPosts.createDraftPost({
  draftPost: {
    title: 'Your Blog Title',
    excerpt: 'Post summary...',
    richContent: { /* Ricos JSON format */ },
    seoData: {
      title: 'SEO Title',
      description: 'Meta description',
      slug: 'url-slug'
    }
  },
  publish: true // Publish immediately
})
```

✅ **Upload Images**
```javascript
files.importFile({
  url: 'https://example.com/image.jpg',
  mediaType: files.MediaType.IMAGE,
  displayName: 'Cover Image.jpg'
})
```

✅ **Set Categories & Tags**
✅ **Schedule Posts** (future publish date)
✅ **Update Existing Posts**
✅ **Set SEO Metadata**
✅ **Embed Media** (images, videos)

---

## 🐍 Python Automation Script (Concept)

Here's a conceptual Python script that could automate blog publishing from your CSV schedule:

```python
import requests
import json
from datetime import datetime

class WixBlogPublisher:
    def __init__(self, api_key, site_id):
        self.api_key = api_key
        self.site_id = site_id
        self.base_url = "https://www.wixapis.com/v1/blog"
        
    def create_post(self, title, content, excerpt, seo_data, cover_image_url=None, publish=False):
        """
        Create and optionally publish a blog post to Wix
        """
        # Convert content to Ricos JSON format
        ricos_content = self.markdown_to_ricos(content)
        
        # Upload cover image if provided
        media_id = None
        if cover_image_url:
            media_id = self.upload_image(cover_image_url)
        
        # Prepare post data
        post_data = {
            "draftPost": {
                "title": title,
                "excerpt": excerpt,
                "richContent": ricos_content,
                "seoData": seo_data,
                "media": {
                    "wixMedia": {
                        "image": {"id": media_id}
                    } if media_id else None
                }
            },
            "publish": publish
        }
        
        # Make API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/posts",
            headers=headers,
            json=post_data
        )
        
        return response.json()
    
    def upload_image(self, image_url):
        """Upload external image to Wix Media Manager"""
        # Implementation here
        pass
    
    def markdown_to_ricos(self, markdown_content):
        """Convert Markdown to Ricos JSON format"""
        # Implementation here
        pass
    
    def publish_from_csv(self, csv_file):
        """Read blog schedule CSV and publish posts"""
        import pandas as pd
        df = pd.read_csv(csv_file)
        
        for idx, row in df.iterrows():
            if row['status'] == 'READY_TO_PUBLISH':
                result = self.create_post(
                    title=row['Blog Title'],
                    content=row['Content'],  # You'd need to store full content somewhere
                    excerpt=row['Caption'][:200],
                    seo_data={
                        "title": row['Blog Title'][:60],
                        "description": row['Caption'][:160],
                        "slug": self.slugify(row['Blog Title'])
                    },
                    publish=True
                )
                print(f"Published: {row['Blog Title']}")

# Usage
publisher = WixBlogPublisher(api_key="your_api_key", site_id="your_site_id")
publisher.publish_from_csv('blog_schedule.csv')
```

---

## 🚀 Implementation Options

### **Option 1: Simple REST API (Recommended for Starting)**

**Pros:**
- Relatively straightforward
- Can use Python/JavaScript
- Good for batch publishing

**Cons:**
- Requires API key management
- Need to convert content to Ricos JSON format
- More setup work initially

**Best For:**
- Publishing 1-2 posts per week
- Batch publishing multiple posts
- Automating repetitive tasks

### **Option 2: Wix Velo Backend Code**

**Pros:**
- Native Wix integration
- No external hosting needed
- Access to all Wix functionality

**Cons:**
- Must write JavaScript
- Code lives within Wix site
- Learning curve for Velo

**Best For:**
- Real-time integrations
- Complex workflows within Wix
- If you're already using Velo

### **Option 3: Zapier/Make.com Integration**

**Pros:**
- No coding required
- Visual workflow builder
- Many pre-built connectors

**Cons:**
- Monthly subscription cost
- Limited to available connectors
- May not support all Wix Blog API features

**Best For:**
- Quick automation without coding
- Connecting multiple platforms
- Simple workflows

---

## 📋 Content Format: Ricos JSON

Wix uses **Ricos JSON** format for rich content. Here's an example:

```json
{
  "nodes": [
    {
      "type": "PARAGRAPH",
      "nodes": [{
        "type": "TEXT",
        "textData": {
          "text": "This is a paragraph with some text.",
          "decorations": []
        }
      }],
      "paragraphData": {}
    },
    {
      "type": "HEADING",
      "nodes": [{
        "type": "TEXT",
        "textData": {
          "text": "This is a Heading",
          "decorations": []
        }
      }],
      "headingData": {
        "level": 2
      }
    },
    {
      "type": "IMAGE",
      "imageData": {
        "image": {
          "src": {
            "id": "image-media-id"
          }
        }
      }
    }
  ]
}
```

**You'll need to convert from:**
- Markdown → Ricos JSON
- HTML → Ricos JSON
- Plain text → Ricos JSON

---

## 🛠️ Setup Steps

### **Phase 1: Research & Setup** (1-2 hours)

1. **Create Wix Developer Account**
   - Go to https://dev.wix.com/
   - Register with your Agroverse.shop email

2. **Enable Wix API for Your Site**
   - Dashboard → Settings → API Keys
   - Create new API Key with Blog permissions

3. **Test API Access**
   - Use Postman or curl to test authentication
   - Try creating a draft post manually

### **Phase 2: Content Conversion** (2-4 hours)

1. **Choose Content Format**
   - Write in Markdown (easier)
   - Store in Google Docs
   - Or keep in CSV with content column

2. **Build Converter**
   - Markdown → Ricos JSON converter
   - Handle headings, paragraphs, images, links

3. **Test with Sample Post**
   - Convert one blog post manually
   - Publish via API
   - Verify formatting looks good

### **Phase 3: Automation** (4-8 hours)

1. **Build Python Script**
   - Read from CSV schedule
   - Convert content to Ricos
   - Upload images to Media Manager
   - Create post via API
   - Set SEO metadata

2. **Add Error Handling**
   - Retry logic for failed uploads
   - Validation before publishing
   - Logging for debugging

3. **Test Workflow**
   - Run with 1-2 test posts
   - Verify everything works
   - Document any issues

### **Phase 4: Production** (Ongoing)

1. **Weekly Publishing**
   - Prepare content in your preferred format
   - Run automation script
   - Review post in Wix before making live
   - Publish or schedule

---

## ⚠️ Important Considerations

### **1. Content Complexity**

**Simple Content (Easy to Automate):**
- ✅ Headings
- ✅ Paragraphs
- ✅ Bold/italic text
- ✅ Links
- ✅ Images

**Complex Content (Harder to Automate):**
- ⚠️ Instagram embeds (may need custom code)
- ⚠️ Complex layouts
- ⚠️ Custom styling
- ⚠️ Video embeds
- ⚠️ Interactive elements

### **2. Image Handling**

**Challenge**: Images must be uploaded to Wix Media Manager first

**Solution**:
- Store images in cloud (S3, Cloudinary)
- Script downloads and uploads to Wix
- Get Wix media ID
- Reference in blog post

### **3. Preview Before Publishing**

**Recommendation**: Create as draft first, review manually, then publish

```python
# Create as draft
publisher.create_post(..., publish=False)

# Review in Wix dashboard
# Then publish via API or manually
```

---

## 💰 Cost Considerations

### **Wix API Access:**
- ✅ **Free** for basic usage
- May have rate limits
- Check current Wix API pricing

### **Development Time:**
- Initial setup: 8-15 hours
- Ongoing maintenance: 1-2 hours/month

### **Alternative: Pay for Automation Service:**
- Zapier: $20-50/month
- Make.com: $9-29/month
- Custom developer: $500-2,000 one-time

---

## 🎯 Recommendation for Agroverse

### **Short Term (Next 3 Months):**
**Stick with Manual Publishing**

**Why:**
- You're just starting (first 12 posts)
- Manual gives you more control
- Learn what works before automating
- Manual publishing: ~30 min/post
- Total time saved with automation: ~3-4 hours over 3 months
- **Not worth the 10-15 hour setup investment yet**

**Focus instead on:**
- Writing great content
- Testing what resonates
- Building the habit
- Tracking what converts

### **Medium Term (Months 4-6):**
**Consider Semi-Automation**

**If you're publishing 2+ posts/week:**
- Time saved becomes significant (8-10 hours/month)
- You know your content formula
- Automation ROI becomes positive

**Start with:**
- Template-based approach in Wix
- Copy-paste from standardized Markdown
- Maybe use Zapier for simple automation

### **Long Term (6+ months):**
**Full Automation Makes Sense**

**When:**
- Publishing 3+ posts/week
- Content format is standardized
- You have development resources
- Want to scale content production

**Invest in:**
- Custom Python script
- Markdown → Ricos converter
- Image upload automation
- Scheduled publishing pipeline

---

## 🚦 Decision Framework

**Should you automate NOW?**

Answer these questions:

1. **How many posts per week?**
   - 1 post: Manual is fine
   - 2-3 posts: Consider semi-automation
   - 4+ posts: Automation worth it

2. **How technical are you?**
   - Non-technical: Use Zapier or stay manual
   - Some coding: Try simple API script
   - Developer: Full custom automation

3. **Is content standardized?**
   - No: Stay manual (formatting varies)
   - Somewhat: Templates + manual
   - Yes: Automation-ready

4. **What's your bottleneck?**
   - Writing: Automation won't help
   - Publishing mechanics: Automation helps
   - Both: Fix writing first

---

## 📚 Resources

### **Official Documentation:**
- [Wix Blog API](https://dev.wix.com/docs/sdk/backend-modules/blog/posts/introduction)
- [Wix Media API](https://dev.wix.com/docs/sdk/backend-modules/media/files/introduction)
- [Ricos Editor Format](https://github.com/wix/ricos)

### **Code Examples:**
- [Wix API Code Examples](https://dev.wix.com/docs/sdk/backend-modules/blog/posts/introduction)
- GitHub: Search "wix blog api python" or "wix ricos converter"

### **Alternative Tools:**
- [Markdown to Ricos Converter](https://github.com/search?q=markdown+ricos) (check GitHub)
- Zapier Wix Integration
- Make.com Wix Connector

---

## 🎬 Next Steps

### **If You Want to Explore Automation:**

1. **Week 1: Research**
   - Create Wix Developer account
   - Review API documentation
   - Test with one manual API call

2. **Week 2: Prototype**
   - Write simple script to create draft post
   - Test content conversion
   - Upload one image via API

3. **Week 3: Test**
   - Publish one full blog post via API
   - Compare with manual result
   - Decide if worth continuing

4. **Week 4: Decision**
   - If successful: Build full automation
   - If too complex: Stick with manual
   - If partial: Use for image uploads only

### **If Staying Manual (Recommended for Now):**

1. **Optimize Manual Workflow**
   - Create Wix templates
   - Standardize image sizes
   - Use consistent formatting
   - Build checklist (see WIX_BLOG_GUIDE.md)

2. **Track Time**
   - Monitor how long each post takes
   - Identify most time-consuming parts
   - Automate those specific parts later

---

## 💡 My Recommendation

**For Agroverse right now:**

### ✅ **Start Manual** (Next 3 months)
- Focus on content quality
- Learn what resonates
- Build publishing habit
- ~30 min per post = manageable

### 🤔 **Evaluate at Month 3**
- If you're consistently publishing 2+/week
- If format is standardized
- If time is becoming a bottleneck
- **Then** revisit automation

### 🚀 **Consider Automation When:**
- Publishing 8+ posts/month
- Content format is consistent
- You have 10-15 hours for setup
- OR you hire a developer

**Bottom Line**: Don't over-engineer early. Automation is powerful, but manual publishing for 12 posts over 3 months is totally reasonable and lets you focus on what matters most: **great content that drives conversions**.

---

**Questions about Wix API?** Let me know and I can create a more detailed implementation guide or starter script!

