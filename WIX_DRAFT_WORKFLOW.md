# 🔄 Wix Blog Draft Workflow

## ✅ System Overview

You now have a streamlined workflow where:
1. **Blog posts created as Wix drafts** via API
2. **Wix Draft IDs stored in Google Sheets** alongside primary keys
3. **You reference posts by primary key** for updates/edits
4. **Manual scheduling in Wix** for final control

---

## 📊 Google Sheets Structure

Your Blog Content Schedule now has:

| Column | Purpose | Example |
|--------|---------|---------|
| `primary_key` | Unique ID for tracking | `4098f184` |
| `Wix Draft ID` | Wix post identifier | `cef32f29-37dc-4d41-9fec-61218f22d4fa` |
| `status` | Manual status tracking | `DRAFT`, `IN REVIEW`, `SCHEDULED`, `PUBLISHED` |
| `Blog Title` | Post title | "From Okanogan to Your Table..." |
| ... | Other columns | ... |

---

## 🚀 Workflow Steps

### **Step 1: Create Drafts in Wix**

```bash
cd /Users/garyjob/Applications/market_research
source venv/bin/activate

# Create drafts for all posts without Wix Draft IDs
python create_blog_drafts.py
```

**What this does:**
- ✅ Reads `blog_schedule.csv`
- ✅ Creates Wix drafts for posts without draft IDs
- ✅ Saves draft IDs back to CSV
- ✅ Syncs to Google Sheets automatically
- ✅ Shows confirmation and next steps

**Result**: Placeholder drafts created in Wix, ready for you to edit

---

### **Step 2: Review Drafts in Wix**

1. Go to **Wix Dashboard**: https://www.wix.com/dashboard
2. Navigate to: **Blog > Drafts**
3. Find your draft posts (sorted by creation date)
4. **Edit each draft:**
   - Add full content (use `/blog_posts/*.md` files as reference)
   - Add featured image (1200 x 628px recommended)
   - Add Instagram embeds where noted
   - Format headings, bold text, lists
   - Add internal links to products
   - Add CTAs

---

### **Step 3: Schedule in Wix**

Once a draft is ready:
1. In Wix editor, click **"Schedule Post"** (top right)
2. Set date/time (use dates from your schedule)
3. Click **"Schedule"**
4. ✅ Post will auto-publish on that date

---

### **Step 4: Update Status in Google Sheets**

Manually update the `status` column:
- `DRAFT` = Created in Wix, needs editing
- `IN REVIEW` = Content complete, reviewing
- `SCHEDULED` = Scheduled in Wix for auto-publish
- `PUBLISHED` = Live on blog
- `PROMOTED` = Currently promoting on Instagram

This tracking helps you see what's in progress!

---

## 🔄 Making Updates to Existing Drafts

### **Scenario: You reviewed a draft and want to update it**

**Option A: Update via API (Quick changes)**

```bash
# Update specific draft by primary key
python update_blog_draft.py 4098f184 blog_posts/okanogan_journey.md
```

**What happens:**
1. Script looks up primary key `4098f184` in CSV
2. Finds Wix Draft ID `cef32f29-37dc-4d41-9fec-61218f22d4fa`
3. Converts markdown to Ricos format
4. Updates the draft via Wix API
5. You review in Wix dashboard

**Option B: Edit Directly in Wix (Recommended for formatting)**

1. Go to Wix Dashboard > Blog > Drafts
2. Find post by title
3. Edit directly in Wix editor
4. Save changes
5. Schedule when ready

---

## 📋 Quick Reference Commands

### **Create all missing drafts:**
```bash
python create_blog_drafts.py
```

### **Update specific draft:**
```bash
python update_blog_draft.py <primary_key> <markdown_file>

# Example:
python update_blog_draft.py 4098f184 blog_posts/okanogan_journey.md
```

### **Sync to Google Sheets:**
```bash
python sync_blog_schedule.py
```

### **Test Wix API connection:**
```bash
python wix_blog_publisher.py
```

---

## 🎯 Typical Weekly Workflow

### **Monday: Content Creation**
1. Write blog post in Google Docs or Markdown
2. Save as `.md` file in `blog_posts/` folder
3. Run: `python create_blog_drafts.py` (if new post)
4. Or: `python update_blog_draft.py <primary_key> <file>`

### **Tuesday Morning: Wix Review**
1. Go to Wix Dashboard > Drafts
2. Open the draft
3. Add images and Instagram embeds
4. Format and polish
5. Click "Schedule" for publish date

### **Tuesday: Update Google Sheets**
1. Open Google Sheets
2. Find the post by primary key
3. Update status to "SCHEDULED"
4. Add any notes

### **Publish Date: Auto-Publish**
1. Wix automatically publishes at scheduled time
2. Update Instagram bio link
3. Share on social media
4. Update status to "PUBLISHED" in sheets

---

## 💡 Communication with AI Assistant

### **When requesting updates, say:**

❌ **Less Clear:**
"Update the Okanogan post"

✅ **Better:**
"Update post with primary key 4098f184"

✅ **Or:**
"Update the Okanogan post (4098f184)"

**Why**: Primary key uniquely identifies the post and its Wix Draft ID

---

## 📊 Current Status

### **Post Created:**
- ✅ **Primary Key**: `4098f184`
- ✅ **Wix Draft ID**: `cef32f29-37dc-4d41-9fec-61218f22d4fa`
- ✅ **Title**: "From Okanogan to Your Table: The Journey of Regenerative Cacao"
- ✅ **Content**: Full markdown in `blog_posts/okanogan_journey.md`
- ✅ **Status**: DRAFT (ready for you to edit/schedule in Wix)

**Next Steps for This Post:**
1. Go to Wix Dashboard > Blog > Drafts
2. Find: "From Okanogan to Your Table..."
3. Add images (farm photos, Okanogan event, Gary's journey)
4. Embed Instagram reels:
   - Gary's border crossing reel
   - Matheus at Correios
   - Santos facility processing
5. Schedule for: **October 14, 2025, 9:00 AM**

---

## 🔗 Quick Links

- **Google Sheets**: [Blog Schedule](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ)
- **Wix Dashboard**: [Blog Manager](https://www.wix.com/dashboard)
- **Your Blog**: [https://www.agroverse.shop/blog](https://www.agroverse.shop/blog)
- **Instagram**: [@agroverse.shop](https://instagram.com/agroverse.shop)

---

## 🛠️ Troubleshooting

### **"Primary key not found"**
- Run: `python sync_blog_schedule.py` to regenerate keys
- Check Google Sheets for the correct primary key

### **"No Wix Draft ID"**
- Run: `python create_blog_drafts.py` to create the draft first
- Sync will update Google Sheets with the ID

### **"API connection failed"**
- Check `.env` file has: `WIX_API_KEY`, `WIX_SITE_ID`, `WIX_MEMBER_ID`
- Verify API key is valid
- Run: `python wix_blog_publisher.py` to test connection

### **"Content looks weird in Wix"**
- The Markdown → Ricos conversion is basic
- Edit directly in Wix for better formatting
- Or use: `python generate_blog_html.py` for HTML version

---

**Questions?** This system gives you the best of both worlds:
- ✅ Automated draft creation saves time
- ✅ Manual editing in Wix gives full control
- ✅ Google Sheets tracks everything
- ✅ Easy to communicate about specific posts via primary key

Ready to schedule your first post! 🚀

