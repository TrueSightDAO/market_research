# Agroverse.shop Blog Post Management

Complete guide for managing blog content scheduling, Wix integration, and blog post publishing for Agroverse.shop.

## 📁 Directory Structure

```
online_content/agroverse_shop/blog_post/
├── README.md                          # This file (consolidated documentation)
├── sync_blog_schedule.py             # Sync blog schedule to Google Sheets
├── create_blog_drafts.py             # Create Wix drafts from schedule
├── update_blog_draft.py              # Update Wix drafts by primary key
├── generate_blog_html.py             # Generate blog HTML
├── publish_okanogan_post.py          # Publish specific post
├── publish_full_okanogan_post.py     # Publish full post version
├── wix_blog_publisher.py            # Wix API integration library
├── get_wix_member_id.py             # Get Wix member ID
├── test_wix_api.py                  # Test Wix API connection
├── update_wix_metadata_only.py      # Update Wix metadata only
├── prepare_github_secret.py         # Prepare GitHub secret for credentials
├── blog_schedule.csv                # Blog content schedule
├── blog_schedule_template.csv       # Blog schedule template
├── blog_schedule_old.csv            # Old blog schedule backup
└── agroverse_blog_posts/            # Markdown blog post content
    ├── 20251014_4098f184_okanogan_journey.md
    ├── 20251020_8ce2eb53_bahia_amazon_origins.md
    ├── 20251027_flavor_profiles_tasting_tools.md
    └── 20260126_167165b7_bulk_vs_gourmet_cacao.md
```

## 🎯 Overview

This directory manages blog content publishing for Agroverse.shop, including:
- Blog schedule management and synchronization
- Wix blog integration and API automation
- Blog draft creation and updates
- SEO optimization
- Integration with Instagram content strategy

## 🔗 Integration with Instagram

**Key Principle**: Blog posts should support and expand on Instagram themes, creating a content ecosystem where each channel amplifies the other.

### Recommended Flow:
1. **Instagram teases** the topic with bite-sized content
2. **Blog provides** deep educational content  
3. **Instagram CTAs** drive traffic to blog
4. **Blog CTAs** drive to product pages/email signup

## 📊 Google Sheets Integration

**Spreadsheet ID:** `1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ`

**Worksheet:** "Blog Content Schedule"

**Service Account:** Configured in `google_credentials.json`

## 🔑 Primary Key System

Primary keys are generated using: `Publish Date + Blog Title`

**Example:**
- `"20260113" + "The Ultimate Guide to Criollo Cacao..."` = `4949370d`

**Important**: If you change Publish Date or Blog Title, the primary key changes, and status preservation fails for that row.

## 📋 Blog Schedule Structure

**CSV File:** `blog_schedule.csv`

**Structure:**
```csv
primary_key,status,Week,Date Range,Publish Date,Day of Week,Blog Title,Theme,Target Word Count,SEO Keywords,Content Outline,Instagram Tie-In,CTA,Internal Links,Tool Suggestions
```

### Column Descriptions:

| Column | Purpose | Example |
|--------|---------|---------|
| `primary_key` | Auto-generated ID | `4949370d` |
| `status` | Manual tracking in Sheets | `DRAFT`, `SCHEDULED`, `PUBLISHED` |
| `Week` | Aligns with Instagram | `Week 17` |
| `Date Range` | Weekly range | `"Jan 13-19, 2026"` |
| `Publish Date` | Exact publish date | `20260113` |
| `Day of Week` | Day name | `Monday` |
| `Blog Title` | Full post title | `"The Ultimate Guide to Criollo Cacao..."` |
| `Theme` | Content category | `Cacao Education` |
| `Target Word Count` | Length goal | `1500-2000` |
| `SEO Keywords` | Focus keywords | `criollo cacao, rare cacao varieties` |
| `Content Outline` | Section breakdown | `1. Intro / 2. History / 3. Varieties...` |
| `Instagram Tie-In` | Cross-promotion notes | `Links to Jan 14 carousel, embeds reels` |
| `CTA` | Call-to-action | `Shop our collection...` |
| `Internal Links` | SEO linking strategy | `Link to: Farmers page, Shop page...` |
| `Tool Suggestions` | Production tools | `WordPress, Yoast SEO, Canva...` |

## 📅 Recommended Publishing Cadence

### Option 1: Weekly (Recommended for Starting)
- **1 post every Monday** (or Tuesday)
- Sustainable, allows quality focus
- Builds consistent audience expectation
- ~50 blog posts per year

### Option 2: Bi-Weekly (Growth Phase)
- **2 posts per week** (Monday + Thursday)
- Faster content accumulation
- Better SEO momentum
- More Instagram tie-in opportunities
- ~100 blog posts per year

### Timing Strategy:
```
Monday Morning: Blog publishes
Monday-Sunday: Instagram series supports/promotes blog
Instagram CTAs: "Read the full guide (link in bio)"
Blog CTAs: "Follow us on Instagram for daily cacao tips"
```

## 🔄 Content Synchronization Examples

### Example 1: Educational Deep Dive
```
Week 17: "Cacao Varieties Deep Dive"

📝 Blog (Monday, Jan 13):
   "The Ultimate Guide to Criollo Cacao" (1,800 words)
   
📱 Instagram Series (Wed-Sat):
   ├── Wed: Criollo intro carousel → CTA to blog
   ├── Sat: Porcelana reel → CTA to blog  
   ├── Wed: Flavor profile carousel → CTA to blog
   └── Sat: Conservation reel → CTA to blog

🔗 Cross-Promotion:
   - Blog embeds Instagram posts
   - Instagram bio link → Blog post
   - Blog CTA → Instagram follow
```

### Example 2: Behind-the-Scenes Story
```
Week 18: "Farm Visit Story"

📝 Blog (Monday, Jan 20):
   "Visiting Oscar's Farm: A Journey to Regenerative Cacao" (2,000 words)
   
📱 Instagram Series (Mon-Thu):
   ├── Mon: Farm arrival reel → CTA to blog
   ├── Tue: Tree planting carousel → CTA to blog
   ├── Wed: Farmer interview reel → CTA to blog
   └── Thu: Processing carousel → CTA to blog
```

## 🔧 Key Scripts

### `sync_blog_schedule.py`
Sync blog schedule from CSV to Google Sheets:
```bash
python3 sync_blog_schedule.py
```

**What it does:**
- Reads `blog_schedule.csv`
- Generates primary keys based on Publish Date + Blog Title
- Retrieves existing status values from Google Sheets
- Preserves manual status updates
- Uploads to "Blog Content Schedule" worksheet

### `create_blog_drafts.py`
Create Wix drafts from blog schedule:
```bash
python3 create_blog_drafts.py
```

**What it does:**
- Reads blog schedule
- Creates draft posts in Wix
- Tracks Wix Draft ID in Google Sheets
- Allows collaborative editing workflow

### `update_blog_draft.py`
Update Wix drafts by primary key:
```bash
python3 update_blog_draft.py <primary_key>
```

### `wix_blog_publisher.py`
Wix API integration library for blog publishing automation.

## 🌐 Wix Blog Setup

**Blog URL**: https://www.agroverse.shop/blog  
**Platform**: Wix  
**Current Posts**: 4 published posts (as of Jan 2025)

### Existing Content Analysis:

1. ✅ **"Vote for the Artwork on the First Series..."** (May 8, 2024)
   - Strong community engagement approach
   - Limited edition product launch

2. ✅ **"Ceremonial Cacao and the Art of Being..."** (Mar 4, 2025)
   - Deep educational content (8 min read)
   - Philosophical/wellness angle

3. ✅ **"The Connection Between Wildfires and Climate Change"** (Jan 19, 2025)
   - Environmental awareness (8 min read)
   - Regeneration tie-in

4. ✅ **"Agroverse and The Center SF Partnership"** (Jan 10, 2025)
   - Community partnership announcement
   - Short format (1 min read)

## 🛠️ Wix Blog Publishing Workflow

### Step 1: Create New Post in Wix

1. **Log into Wix Dashboard**
   - Go to https://www.wix.com/dashboard
   - Navigate to "Blog" section

2. **Create New Post**
   - Click "+ New Post"
   - Choose "Blog Post" (not Event or Product)

3. **Post Settings to Configure:**
   - ✅ Post Title (H1 - auto-generated from title)
   - ✅ Author (Admin TrueSight or Nathani Baesso)
   - ✅ Publish Date & Time
   - ✅ Categories (create as needed)
   - ✅ Featured Image (1200 x 628px recommended)

### Step 2: SEO Optimization in Wix

**Wix SEO Wiz Settings:**

1. **Page Title Tag** (60 characters max)
   - Include primary keyword
   - Example: *"Criollo Cacao Guide | Rare Varieties & Conservation | Agroverse"*

2. **Meta Description** (160 characters max)
   - Compelling summary with CTA
   - Example: *"Discover Criollo cacao - the rarest variety representing <5% of global production. Learn about Porcelana, flavor profiles & conservation. Shop regenerative cacao →"*

3. **URL Slug** (Wix calls this "Post URL")
   - Keep short, include primary keyword
   - Example: `/criollo-cacao-guide` or `/criollo-cacao-varieties`
   - **Important**: Wix auto-generates, but you can edit before publishing

4. **Alt Text for Images**
   - Every image needs descriptive alt text
   - Include keywords naturally
   - Example: *"White Porcelana cacao beans from Venezuela regenerative farm"*

5. **Structured Data (Automatic in Wix)**
   - Wix automatically adds Article schema
   - Verify with Google Rich Results Test after publishing

### Step 3: Content Formatting in Wix

**Wix Editor Best Practices:**

1. **Headings Hierarchy:**
   ```
   H1: Blog Post Title (automatic)
   H2: Main Sections
   H3: Subsections
   H4: Minor points (use sparingly)
   ```

2. **Text Formatting:**
   - Use **bold** for important points
   - Use *italics* for emphasis
   - Use bullet points and numbered lists
   - Keep paragraphs short (3-4 sentences max)

3. **Images:**
   - Optimize images before uploading (compress for web)
   - Use descriptive file names
   - Add alt text to all images
   - Recommended size: 1200px width for featured images

4. **Links:**
   - Internal links to other blog posts
   - External links to authoritative sources
   - Product links to shop pages
   - Social media links

### Step 4: Publishing

1. **Preview** - Check how it looks on mobile and desktop
2. **SEO Check** - Review SEO Wiz recommendations
3. **Publish** - Click "Publish" when ready
4. **Share** - Share on social media, email list

## 📝 Blog Post Strategy

### Content Themes

**Theme 1: Cacao Education**
- Varieties, origins, processing
- Nutritional benefits
- Flavor profiles
- Example: "The Ultimate Guide to Criollo Cacao"

**Theme 2: Regenerative Farming**
- Farm visits, farmer stories
- Agroforestry practices
- Environmental impact
- Example: "Visiting Oscar's Farm: A Journey to Regenerative Cacao"

**Theme 3: Community & Wellness**
- Ceremonial use
- Wellness benefits
- Community stories
- Example: "Ceremonial Cacao and the Art of Being"

### Content Length Guidelines

- **Short Posts**: 500-800 words (announcements, quick tips)
- **Medium Posts**: 1,000-1,500 words (standard educational content)
- **Long Posts**: 1,500-2,500 words (deep dives, comprehensive guides)

### SEO Best Practices

1. **Keyword Research**
   - Use SEO Keywords column in schedule
   - Include primary keyword in title
   - Use keywords naturally throughout content
   - Include in headings (H2, H3)

2. **Internal Linking**
   - Link to other blog posts
   - Link to product pages
   - Link to farmer pages
   - Use descriptive anchor text

3. **External Linking**
   - Link to authoritative sources
   - Link to research studies
   - Link to partner websites
   - Use nofollow for affiliate links

4. **Image Optimization**
   - Compress images (use tools like TinyPNG)
   - Use descriptive file names
   - Add alt text with keywords
   - Include images in content (not just featured)

5. **Meta Tags**
   - Optimize title tag (60 characters)
   - Write compelling meta description (160 characters)
   - Include primary keyword in both

## 🔄 Workflow Examples

### Creating a New Blog Post

1. **Plan in Schedule**
   - Add entry to `blog_schedule.csv`
   - Fill in all required fields
   - Set publish date

2. **Sync to Google Sheets**
   ```bash
   python3 sync_blog_schedule.py
   ```

3. **Create Draft in Wix**
   - Use `create_blog_drafts.py` or create manually
   - Write content in Wix editor
   - Add images, format text

4. **Optimize SEO**
   - Set page title tag
   - Write meta description
   - Add alt text to images
   - Check SEO Wiz recommendations

5. **Publish**
   - Preview on mobile and desktop
   - Publish when ready
   - Share on social media

### Updating Existing Post

1. **Update in CSV or Google Sheets**
2. **Sync changes**
3. **Update in Wix** (if using API) or manually
4. **Republish if needed**

## 📚 Documentation Files

This directory contains detailed documentation:

- **BLOG_SCHEDULE_GUIDE.md** - Complete blog schedule management guide
- **WIX_BLOG_GUIDE.md** - Wix blog publishing guide with SEO tips
- **BLOG_POST_ADDED_20260126.md** - Notes on specific blog post additions

## 💡 Best Practices

1. **Consistency** - Publish on schedule (weekly or bi-weekly)
2. **Quality** - Focus on value, not just quantity
3. **SEO** - Optimize every post for search
4. **Integration** - Link blog and Instagram content
5. **Internal Linking** - Build internal link structure
6. **Image Optimization** - Compress and optimize all images
7. **Mobile-Friendly** - Check mobile view before publishing
8. **Analytics** - Track performance and adjust strategy

## 🚨 Common Mistakes to Avoid

**Don't:**
- ❌ Change Publish Date or Blog Title without understanding primary key impact
- ❌ Skip SEO optimization
- ❌ Forget to add alt text to images
- ❌ Publish without previewing on mobile
- ❌ Ignore Instagram tie-in opportunities

**Do:**
- ✅ Understand primary key system before making changes
- ✅ Optimize SEO for every post
- ✅ Add descriptive alt text to all images
- ✅ Preview on mobile and desktop
- ✅ Link blog and Instagram content strategically

---

*Last updated: November 2025*
*This README consolidates all Agroverse.shop blog post documentation for easy reference by Cursor AI*

