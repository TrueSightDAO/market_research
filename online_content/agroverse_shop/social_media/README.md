# Agroverse.shop Social Media Content Management

Complete guide for managing Instagram content scheduling, hashtag strategy, and community feedback integration for Agroverse.shop.

## 📁 Directory Structure

```
online_content/agroverse_shop/social_media/
├── README.md                          # This file (consolidated documentation)
├── sync_content_schedule.py           # Sync Instagram schedule to Google Sheets
├── sync_hashtags.py                   # Sync hashtags to Google Sheets
├── schedule_post.py                   # Schedule individual posts
├── process_feedback.py                # Process community feedback with AI
├── sync_feedback.py                   # Sync feedback to/from Google Sheets
├── content_creator.py                 # Content creation utilities
├── grok_content_generator.py          # Grok AI content generation
├── hybrid_content_workflow.py         # Hybrid content workflow
├── voice_feedback_capture.gs         # Google Apps Script for voice feedback
├── agroverse_schedule_till_easter_cleaned.csv  # Main content schedule CSV
├── instagram_hashtags.csv             # Hashtag database
├── community_feedback.csv             # Community feedback data
├── grok_content_suggestions.txt      # Grok AI suggestions
└── hybrid_content_results.json       # Hybrid workflow results
```

## 🎯 Overview

This directory manages Instagram content marketing for Agroverse.shop, including:
- Content schedule management and synchronization
- Hashtag strategy and database
- Community feedback integration
- Voice feedback capture (iPhone + Siri)
- Content creation and AI-assisted workflows

## 🌟 Content Marketing Strategy: The 3 Core Themes

**CRITICAL**: All content must align with at least one (ideally multiple) of these strategic pillars.

### 🌱 Theme 1: REGENERATIVE FARMING & TRACEABILITY
**Core Message:** "Know your farmers, heal the planet"

**Key Elements:**
- Direct relationships with Oscar, Paulo, Vivi and farmers in Pará & Bahia
- Cabruca agroforestry system (preserving Atlantic Forest biodiversity)
- **Tree planting impact** - "Each bag plants trees in the Amazon rainforest" (PRIMARY CTA)
- Behind-the-scenes farm visits and sourcing transparency
- Climate-resilient varieties and innovation
- Fair farmer compensation and community empowerment
- Zero middlemen - direct farm partnerships

**Content Types:**
- Farm tour reels and carousels
- Farmer interview content
- Regenerative practice demonstrations
- Impact reports (trees planted, carbon offset)
- Sourcing audit behind-the-scenes
- Community event coverage (Okanogan Barter Faire)

### 📚 Theme 2: CACAO EDUCATION & ORIGINS
**Core Message:** "Brazilian cacao is unique—here's why it matters"

**Key Elements:**
- **Regional distinctions** - Bahia (molasses, red fruits, spices) vs Amazon (tobacco, olive, fudgy)
- Nutritional science - flavonoids, magnesium, theobromine, mood benefits
- How-to guides - eating cacao nibs, ceremonial preparation, recipes
- Variety education - Trinitario, Forastero, native genetics (Catongo, FL89)
- Global comparisons - Brazilian vs Latin American/Caribbean/Tropical profiles
- Processing transparency - fermentation, winnowing, quality control
- Applications - artisanal chocolate, ceremonial use, culinary pairings

**Content Types:**
- Educational carousels (nutrient breakdowns, flavor profiles)
- How-to guides (15 ways to eat cacao nibs)
- Comparison infographics (Brazil vs global origins)
- Behind-the-scenes processing videos
- Recipe demonstrations
- Scientific deep dives

### 🤝 Theme 3: COMMUNITY & CONSCIOUS LIVING
**Core Message:** "Every purchase is a ritual—you're part of the ecosystem"

**Key Elements:**
- **Ceremonial cacao** & wellness rituals (meditation, intention-setting)
- Community connections - Okanogan Barter Faire, customer stories, local markets
- Cultural traditions - Día de los Muertos, indigenous wisdom, seasonal celebrations
- Mindfulness & consciousness - not just consumption, but participation
- Meaningful gifting - stories over stuff, purpose over products
- Seasonal wellness - winter immunity, mood support, holiday rituals
- Building conscious consumer community

**Content Types:**
- Cacao ceremony guides
- Holiday ritual content (Thanksgiving, Christmas, New Year)
- Customer testimonials and shoutouts
- Seasonal wellness tips
- Community event coverage
- Gratitude and reflection posts

### 🔗 How These Themes Interconnect

**The Customer Journey:**
```
DISCOVERY (Theme 1)     →  EDUCATION (Theme 2)      →  BELONGING (Theme 3)
"Meet Oscar's farm"     →  "Understand why it's    →  "Join our tree-planting
                            different/better"           movement & rituals"
```

**Why This Strategy Works:**
1. **Differentiation** - Can't buy this from Amazon or big chocolate brands
2. **AI-proof** - Authentic farm relationships can't be replicated by chatbots
3. **Emotional moat** - Tree planting + community + farmer stories = loyalty beyond price
4. **SEO foundation** - Educational content becomes AI training data
5. **Multi-channel amplification** - Blog deepens Instagram teases, email recaps both

## 📋 Content Creation Checklist

Before creating new content, ask:
- ✅ Does this highlight regenerative farming or farmer relationships? (Theme 1)
- ✅ Does this educate about Brazilian cacao's uniqueness? (Theme 2)  
- ✅ Does this build community or conscious living? (Theme 3)
- ✅ Does the CTA emphasize tree planting or joining the movement?
- ✅ Are Oscar, Paulo, Vivi (or specific farmers) mentioned when relevant?

**If content doesn't touch at least ONE theme, reconsider its strategic value.**

## 🚨 Critical: Status Preservation System

- **NEVER override status values in Column B** of the Google Sheets
- Status values represent manual work done by humans and must be preserved
- The sync system automatically preserves these values using primary key matching

## ⚠️ Important: Data Validation Limitation

- **Data validation rules** (dropdown lists, validation criteria) on the Status column may be lost during sync
- This is a limitation of the Google Sheets API when updating data
- **Solution**: Recreate data validation rules manually in Google Sheets after sync if needed

## 🔑 Primary Key System

Primary keys are automatically generated using: `Post Day + Post Type + Theme`

**Examples:**
- `"Mon, Sep 29" + "Reel" + "Behind-the-Scenes"` = `64942530`
- `"Tue, Sep 30" + "Reel" + "Regenerative Farming"` = `da669ceb`

**Why this matters:**
- If you change the Post Day, Post Type, or Theme, the primary key changes
- When primary key changes, status preservation fails for that row
- **Same content = Same primary key = Status preserved**

## 📊 Google Sheets Integration

**Spreadsheet ID:** `1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ`

**Key Worksheets:**
- **Content schedule** - Main Instagram content schedule
- **Hashtag suggestions** - Hashtag database
- **Feedback on Content** - Community feedback submissions

**Service Account:** Configured in `google_credentials.json`

## 🔧 Key Scripts

### `sync_content_schedule.py`
Sync Instagram content schedule from CSV to Google Sheets:
```bash
python3 sync_content_schedule.py
```

**What it does:**
- Reads `agroverse_schedule_till_easter_cleaned.csv`
- Generates primary keys for new rows (if missing)
- Retrieves existing status values from Google Sheets
- Preserves manual status updates
- Uploads to "Content schedule" worksheet

### `sync_hashtags.py`
Sync hashtag database to Google Sheets:
```bash
python3 sync_hashtags.py
```

### `process_feedback.py`
Process community feedback with AI assistance:
```bash
python3 process_feedback.py
```

**What it does:**
- Analyzes feedback from `community_feedback.csv`
- Suggests content improvements
- Updates CSV with improvements
- Marks processed feedback as "INCORPORATED"
- Creates event-based content for community gatherings
- Links event experiences to cacao farming narratives

### `sync_feedback.py`
Sync feedback to/from Google Sheets:
```bash
python3 sync_feedback.py download    # Download from Google Sheets
python3 sync_feedback.py upload      # Upload status updates
```

## 📱 Voice Feedback Capture

### Setup

**Part 1: Deploy Google Apps Script**
1. Go to [script.google.com](https://script.google.com)
2. Create new project: `Voice Feedback Capture`
3. Copy contents from `voice_feedback_capture.gs`
4. Deploy as Web App (Execute as "Me", Access "Anyone")
5. Copy the Web App URL

**Part 2: Create iPhone Shortcut**
1. Open Shortcuts app
2. Create new shortcut with actions:
   - Dictate Text
   - Get Contents of URL (use Web App URL + feedback parameter)
   - Show Notification
3. Add to Siri with phrase: "Add feedback"

### Usage

**Method 1: Web Interface**
- Go to: https://dapp.truesight.me/submit_feedback.html
- Login with digital signature
- Type or paste feedback
- Click "Submit Feedback"

**Method 2: Siri (Hands-Free)**
```
You: "Hey Siri, add feedback"
Siri: "What would you like to say?"
You: "Winter wellness content idea: create a carousel about cacao and seasonal affective disorder"
Siri: "✅ Feedback saved!"
```

**Method 3: Widget**
- Add Shortcuts widget to home screen
- Tap widget → speak → done!

### Viewing Feedback

All feedback appears in:
[Feedback on Content Sheet](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=497764730#gid=497764730)

**Columns:**
- **Column A (Feedback)**: Your voice-to-text idea
- **Column B (Status)**: Empty initially - mark as "INCORPORATED", "PENDING", "REJECTED"
- **Column C (Timestamp)**: Automatically added
- **Column D (Digital Signature)**: Public key of submitter

## 🤝 Community Feedback Workflow

### Step 1: Download Feedback
```bash
python3 sync_feedback.py download
```

Creates `community_feedback.csv` with feedback text and status.

### Step 2: Process with AI
```bash
python3 process_feedback.py
```

**What AI looks for:**
- Hashtag suggestions - Adds relevant hashtags from database
- Content improvements - Enhances descriptions based on feedback
- Timing adjustments - Considers posting time feedback
- Theme refinements - Adjusts content themes based on input
- Event opportunities - Creates post-event content after community gatherings
- Cross-community connections - Links different community experiences to cacao farming

### Step 3: Manual Review & Refinement

**Interactive Process:**
1. Review AI suggestions
2. Refine improvements based on your expertise
3. Apply final changes to CSV
4. Validate hashtag usage:
   - General hashtags: 3-5
   - Targeted hashtags: 7-10
5. Check cadence preservation (4-post weekly structure)
6. Consider date-specificity
7. Plan content insertion

### Step 4: Sync Updates
```bash
python3 sync_content_schedule.py    # Sync content improvements
python3 sync_feedback.py upload     # Update feedback status
```

## 📊 Hashtag Strategy

### Hashtag Database

**File:** `instagram_hashtags.csv`

**Structure:**
- **Hashtag** - The hashtag text
- **Type** - General or Targeted
- **Usage Category** - Core Cacao & Farming, Quality & Origin, etc.
- **Notes** - Core Set, High Frequency, Medium Frequency

### Hashtag Usage Guidelines

**General Hashtags:** 3-5 per post (broader reach)
- Examples: `#cacao`, `#cacaobeans`, `#chocolate`

**Targeted Hashtags:** 7-10 per post (specific audience)
- Examples: `#ceremonialcacao`, `#regenerativefarming`, `#ethicalchocolate`

**Total:** 10-15 hashtags per post

### Hashtag Optimization

- Use curated database from `instagram_hashtags.csv`
- Mix general and targeted for optimal reach
- Rotate hashtags to avoid repetition
- Track performance and adjust

## 📅 Content Schedule Structure

**CSV File:** `agroverse_schedule_till_easter_cleaned.csv`

**Structure:**
```csv
Week,Date Range,Theme Focus,Post Day,Post Type,Theme,Description,Caption,Hashtags,CTA,Tool Suggestions
```

**Columns:**
- **Week** - Week number (Week 1-27)
- **Date Range** - Weekly range (e.g., "Sep 29-Oct 5")
- **Theme Focus** - Weekly theme
- **Post Day** - Day of week (e.g., "Mon, Sep 29")
- **Post Type** - Reel, Carousel, etc.
- **Theme** - Content category
- **Description** - Post description
- **Caption** - Instagram caption
- **Hashtags** - Hashtag list
- **CTA** - Call-to-action
- **Tool Suggestions** - Production tools

**Schedule:**
- **Week 1-16**: 2024 content (September 29 - December 29)
- **Week 17-27**: 2025 content (January 5 - April 5)
- **Date format**: "Mon, Sep 29, 2024"
- **Primary keys**: Generated from Post Day + Post Type + Year

## 🎯 RiseGuide Caption Framework

**ALL future captions for UNSCHEDULED content MUST follow this format:**

**Template:**
```
[EMOJI] [Compelling hook/question/bold statement] [Brief context about the story/situation]!

Here's [what viewers will learn/3 quick insights about the topic]:
1️⃣ [First actionable tip or insight]
2️⃣ [Second actionable tip or insight] 
3️⃣ [Third actionable tip or insight]

[Clear call-to-action with engagement prompt]!
```

**Note**: Only apply to rows where status is empty (unscheduled). Content up to and including `cbe4cec1` has been scheduled and should not be modified unless specifically requested.

## 🔄 Content Insertion Strategy

### When Adding New Content

1. **Identify Insertion Point** - Find logical chronological position
2. **Check Date-Specificity** - Determine if existing content is date-specific
3. **Shift Strategy** - Move non-date-specific content backwards
4. **Preserve Seasonal Content** - Keep holiday/seasonal content in place
5. **Update Primary Keys** - Regenerate after any reordering
6. **Maintain Cadence** - Keep 4 posts per week structure
7. **Consider Weekend Addition** - Use Fri/Sat for special event content
8. **Validate Chronological Flow** - Ensure Week 1-27 progression maintained

### Event-Based Content Strategy

- **Post-Event Timing** - Schedule content after events conclude
- **Cross-Theme Connection** - Link event themes to cacao farming
- **Community Building** - Connect different community experiences
- **Weekend Addition** - Use Fri/Sat for special event content

### Cadence Management

- **Preserve 4-post weekly structure** (Mon, Tue, Wed, Thu)
- **Shift non-date-specific content** backwards when inserting
- **Keep seasonal/holiday content** in place
- **Add weekend content** (Fri, Sat) for special events
- **Maintain chronological flow** from Week 1 to Week 27

## 💡 Best Practices

1. **Regular Processing** - Process feedback weekly or bi-weekly
2. **Quality Review** - Always review AI suggestions before applying
3. **Hashtag Balance** - Maintain proper general/targeted hashtag ratios
4. **Status Tracking** - Keep feedback status updated for transparency
5. **Version Control** - Commit changes to track improvement history
6. **Cadence Preservation** - When inserting new content, shift non-date-specific content backwards
7. **Event Timeline Logic** - Schedule post-event content after events conclude
8. **Cross-Theme Connection** - Connect event themes to cacao farming narratives

## 🚨 Common Mistakes to Avoid

**Don't:**
- ❌ Override status values in Google Sheets
- ❌ Change Post Day/Type/Theme without understanding primary key impact
- ❌ Ignore the 3 core themes when creating content
- ❌ Skip hashtag optimization
- ❌ Forget to process community feedback regularly

**Do:**
- ✅ Always preserve status values
- ✅ Understand primary key system before making changes
- ✅ Align all content with at least one core theme
- ✅ Use proper hashtag mix (3-5 general, 7-10 targeted)
- ✅ Process feedback regularly and incorporate learnings

---

*Last updated: November 2025*
*This README consolidates all Agroverse.shop social media documentation for easy reference by Cursor AI*
