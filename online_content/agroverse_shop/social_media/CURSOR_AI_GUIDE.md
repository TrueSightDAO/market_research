# 🤖 Cursor.AI Guide for Content Schedule Management

## 🎯 **Your Mission**
You are taking over the management of Instagram content scheduling for Agroverse.shop. Your primary responsibility is to update the content schedule when marketing priorities change or new opportunities arise.

### 📆 Google Calendar Follow-Ups (Market Research Hit List)
- The service account in `google_credentials.json` already has access to the Hit List calendar (`GOOGLE_CALENDAR_ID` is set locally).  
- When a shop needs a reminder, update the `Follow Up Date` column with an ISO timestamp like `YYYY-MM-DD HH:MM` (optionally `HH:MM-HH:MM` for a range).  
- Run `source venv/bin/activate && python create_followup_events.py` from `market_research/` to create/update Google Calendar events.  
- Example: `Earth Impact → 2025-11-13 10:00` (call Stephanie at 10 AM) and `Go Ask Alice → 2025-11-14 11:00` (in-store pop-in).  
- The script is idempotent—re-running it simply updates existing events rather than duplicating them.

## 🌟 **AGROVERSE CONTENT MARKETING STRATEGY: THE 3 CORE THEMES**

**CRITICAL**: All content must align with at least one (ideally multiple) of these strategic pillars. These themes create Agroverse's competitive moat in the regenerative cacao market.

### **🌱 Theme 1: REGENERATIVE FARMING & TRACEABILITY**
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

**Sample Captions:**
- "Oscar's 80-year-old trees planted by his grandfather"
- "Your spring purchases funded the relationships we're celebrating today"
- "Plant trees with every purchase! 🌳"

---

### **📚 Theme 2: CACAO EDUCATION & ORIGINS**
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

**Sample Content:**
- "The Heart of Brazilian Cacao: Bahia and Amazon Origins" (blog)
- "What's actually IN regenerative cacao?" (nutrients carousel)
- "How to eat cacao nibs" (8-slide practical guide)

---

### **🤝 Theme 3: COMMUNITY & CONSCIOUS LIVING**
**Core Message:** "Every purchase is a ritual—you're part of the ecosystem"

**Key Elements:**
- **Ceremonial cacao** & wellness rituals (meditation, intention-setting)
- Community connections - Okanogan Barter Faire, customer stories, local markets
- Cultural traditions - Día de los Muertos, indigenous wisdom, seasonal celebrations
- Mindfulness & consciousness - not just consumption, but participation
- Meaningful gifting - stories over stuff, purpose over products
- Seasonal wellness - winter immunity, mood support, holiday rituals
- Building conscious consumer community - "Tag someone who asks where their food comes from"

**Content Types:**
- Cacao ceremony guides
- Holiday ritual content (Thanksgiving, Christmas, New Year)
- Customer testimonials and shoutouts
- Seasonal wellness tips
- Community event coverage
- Gratitude and reflection posts

**Sample Content:**
- "Halloween Cacao Rituals: Ancient Traditions Meet Modern Celebrations"
- "Gifts that tell better stories than flowers"
- "New Year intention-setting with cacao"
- "Elinor and Rune sharing at Okanogan - building bridges from Okanogan to Amazon"

---

### **🔗 How These Themes Interconnect:**

**The Customer Journey:**
```
DISCOVERY (Theme 1)     →  EDUCATION (Theme 2)      →  BELONGING (Theme 3)
"Meet Oscar's farm"     →  "Understand why it's    →  "Join our tree-planting
                            different/better"           movement & rituals"
```

**Example Multi-Theme Post:**
```
🍂 Elinor and Rune are at Okanogan... (Theme 3: Community)
...sharing cacao from Oscar's farm... (Theme 1: Farmer relationship)
These clips show conscious community connecting... (Theme 3: Conscious living)
Direct relationships matter—Oscar, Paulo, Vivi... (Theme 1: Traceability)
Plant trees with every purchase! 🌳 (Theme 1: Impact + Theme 3: Movement)
```

**Why This Strategy Works:**
1. **Differentiation** - Can't buy this from Amazon or big chocolate brands
2. **AI-proof** - Authentic farm relationships can't be replicated by chatbots
3. **Emotional moat** - Tree planting + community + farmer stories = loyalty beyond price
4. **SEO foundation** - Educational content becomes AI training data
5. **Multi-channel amplification** - Blog deepens Instagram teases, email recaps both

---

### **📋 Content Creation Checklist:**

Before creating new content, ask:
- ✅ Does this highlight regenerative farming or farmer relationships? (Theme 1)
- ✅ Does this educate about Brazilian cacao's uniqueness? (Theme 2)  
- ✅ Does this build community or conscious living? (Theme 3)
- ✅ Does the CTA emphasize tree planting or joining the movement?
- ✅ Are Oscar, Paulo, Vivi (or specific farmers) mentioned when relevant?

**If content doesn't touch at least ONE theme, reconsider its strategic value.**

---

## 🚨 **CRITICAL: Status Preservation System**
- **NEVER override status values in Column B** of the Google Sheets
- Status values represent manual work done by humans and must be preserved
- The sync system automatically preserves these values using primary key matching

## ⚠️ **IMPORTANT: Data Validation Limitation**
- **Data validation rules** (dropdown lists, validation criteria) on the Status column may be lost during sync
- This is a limitation of the Google Sheets API when updating data
- **Solution**: Recreate data validation rules manually in Google Sheets after sync if needed
- **Workaround**: Set up data validation rules as a template and reapply them after major updates

## 📁 **Key Files**
- **Repository**: `agroverse_content_schedule`
- **Main CSV**: `agroverse_schedule_till_easter.csv`
- **Google Sheet**: [Content Schedule](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=1682511679#gid=1682511679)
- **Sync Script**: `sync_content_schedule.py`

## 🔑 **Primary Key System (CRITICAL TO UNDERSTAND)**
Primary keys are automatically generated using: `Post Day + Post Type + Theme`

**Examples:**
- `"Mon, Sep 29" + "Reel" + "Behind-the-Scenes"` = `64942530`
- `"Tue, Sep 30" + "Reel" + "Regenerative Farming"` = `da669ceb`

**Why this matters:**
- If you change the Post Day, Post Type, or Theme, the primary key changes
- When primary key changes, status preservation fails for that row
- **Same content = Same primary key = Status preserved**

## 📋 **CSV File Structure**
```csv
Week,Date Range,Theme Focus,Post Day,Post Type,Theme,Description,Caption,Hashtags,CTA,Tool Suggestions
Week 1,Sep 29-Oct 5,Fall Harvest Tease,"Mon, Sep 29",Reel,Behind-the-Scenes,Quick clip...,As fall arrives...,#cacao #cacaobeans...,Tag a friend...,Canva for thumbnail...
```

## 🎯 **CRITICAL: RiseGuide Caption Framework**
**ALL future captions for UNSCHEDULED content MUST follow this format:**
**Note**: Only apply to rows where status is empty (unscheduled). Content up to and including `cbe4cec1` has been scheduled and should not be modified unless specifically requested.

### **Current Scheduling Status (as of latest update):**
- **SCHEDULED**: Primary keys `3e583b71`, `1e33633b`, `c3b9a959`, `4932f5b1`, `25271f57`, `1fb39e1b`, `30874650`, `b1a49285`, `cbe4cec1`
- **UNSCHEDULED**: All content after `cbe4cec1` (status = empty)
- **RiseGuide Framework**: Apply ONLY to unscheduled content

### **Hook + Value (3 Quick Tips) + CTA Structure**

**Template:**
```
[EMOJI] [Compelling hook/question/bold statement] [Brief context about the story/situation]!

Here's [what viewers will learn/3 quick insights about the topic]:
1️⃣ [First actionable tip or insight]
2️⃣ [Second actionable tip or insight] 
3️⃣ [Third actionable tip or insight]

[Clear call-to-action with engagement prompt]!
```

**Example (CORRECT):**
```
🌍 Ever wonder what it takes to get Brazilian cacao to your doorstep? Watch Matheus battle bureaucracy at Correios, only to be blocked by USA tariffs!

Here's the reality of small business shipping:
1️⃣ Tariffs can suddenly block even simple mail packages
2️⃣ International shipping requires navigating complex customs rules
3️⃣ Small businesses like us face extra challenges that big companies don't!

Drop a 🇧🇷 below if you're rooting for us to bring this regenerative goodness to you!
```

**Example (INCORRECT - Generic tips):**
```
🌍 Ever wonder what it takes to get Brazilian cacao to your doorstep? Watch Matheus battle bureaucracy at Correios, only to be blocked by USA tariffs!

Here's how we overcome export challenges:
1️⃣ Partnering with local advocates to navigate regulations
2️⃣ Finding creative shipping solutions to keep costs down
3️⃣ Staying relentless—because sustainable cacao is worth it!

Drop a 🇧🇷 below if you're rooting for us to bring this regenerative goodness to you!
```

### **Key Requirements:**
1. **Hook**: Must be engaging and relevant to the story being told
2. **3 Tips**: Must be directly related to the actual situation/content
3. **Tips should be educational** and provide real value to viewers
4. **CTA**: Must encourage engagement (comments, tags, DMs)
5. **Use numbered emojis** (1️⃣ 2️⃣ 3️⃣) for the tips
6. **Keep authentic to sustainable cacao farming in Brazil**

### **Common Mistakes to Avoid:**
- ❌ Generic tips that don't relate to the actual story
- ❌ Tips about "solutions" when the story is about challenges
- ❌ Tips that contradict the narrative being shown
- ❌ Overly promotional language in the tips section
- ❌ Missing numbered emojis (1️⃣ 2️⃣ 3️⃣)

## ⚡ **Common Scenarios & Solutions**

### **Scenario 1: "Something new came up that's more interesting"**
**User says**: "We need to change the content focus for Week 3 because there's a new sustainability initiative we should highlight instead."

**Your actions:**
1. **Identify the affected rows** in the CSV (Week 3 date range)
2. **Update the content** while keeping Post Day, Post Type, and Theme the same if possible
3. **If you must change Post Day/Type/Theme**: Understand that status values will be lost for those rows
4. **Run sync**: `python sync_content_schedule.py`

**Example update:**
```csv
# BEFORE
Week 3,Oct 13-19,Fall Community Gathering,"Mon, Oct 13",Reel,Community Impact,Tease for Okanogan...

# AFTER (keeping same Post Day/Type/Theme for status preservation)
Week 3,Oct 13-19,Sustainability Initiative,"Mon, Oct 13",Reel,Community Impact,Highlight new sustainability program...
```

### **Scenario 2: "We need to add content for a new date range"**
**Your actions:**
1. **Add new rows** to the CSV with proper date ranges
2. **Follow the existing format** exactly
3. **Apply RiseGuide caption framework** to ALL new captions
4. **Run sync** - new content will get empty status (ready for manual status updates)

**Caption Generation Process:**
1. **Understand the story/theme** being told
2. **Create compelling hook** that relates to the actual content
3. **Develop 3 educational tips** that are directly relevant to the story
4. **Write engaging CTA** that encourages interaction
5. **Review for authenticity** to sustainable cacao farming in Brazil

### **Scenario 3: "We need to remove content for certain dates"**
**Your actions:**
1. **Delete rows** from the CSV
2. **Run sync** - removed content will disappear from Google Sheets
3. **Status values** for removed content will be lost (this is expected)

## 🛠️ **Step-by-Step Process**

### **Step 1: Analyze the Request**
- What date ranges are affected?
- What content needs to change?
- Can you keep Post Day/Type/Theme the same?
- **Check scheduling status**: Are the affected rows SCHEDULED or UNSCHEDULED?
- **If SCHEDULED**: Only modify if specifically requested by user
- **If UNSCHEDULED**: Apply RiseGuide framework to all new captions

### **Step 2: Make Changes**
```bash
# Edit the CSV file
# Make your changes
# Save the file
```

### **Step 3: Test Primary Key Generation**
```bash
# Run this to see what primary keys will be generated
python -c "
import pandas as pd
import hashlib

def generate_primary_key(row):
    date_str = str(row.get('Post Day', ''))
    post_type = str(row.get('Post Type', ''))
    theme = str(row.get('Theme', ''))
    unique_string = f'{date_str}_{post_type}_{theme}'
    hash_object = hashlib.md5(unique_string.encode())
    return hash_object.hexdigest()[:8]

df = pd.read_csv('agroverse_schedule_till_easter.csv')
for i in range(3):
    row = df.iloc[i]
    pk = generate_primary_key(row)
    print(f'Row {i+1}: {row[\"Post Day\"]} + {row[\"Post Type\"]} + {row[\"Theme\"]} = {pk}')
"
```

### **Step 4: Run Sync**
```bash
python sync_content_schedule.py
```

### **Step 5: Verify Results**
- Check the Google Sheet to ensure changes were applied
- Verify that existing status values were preserved
- Confirm new content has empty status (ready for manual updates)

## 🚨 **Critical Rules**

1. **NEVER modify `sync_content_schedule.py`** unless you fully understand the status preservation logic
2. **ALWAYS test with small changes first** (1-2 rows)
3. **Primary keys are immutable** - changing date/type/theme changes the key
4. **Status values are sacred** - they represent human work
5. **ALL NEW/UNSCHEDULED captions MUST follow RiseGuide framework** - Hook + Value (3 Quick Tips) + CTA
6. **DO NOT modify scheduled captions** (status = "SCHEDULED") unless specifically requested
7. **Tips must be relevant to the actual story** - not generic business advice
8. **When in doubt, ask the user** before making changes

## 🛠️ **Troubleshooting**

### **"Status not preserved"**
- **Cause**: Primary key changed due to content modifications
- **Solution**: Check if Post Day, Post Type, or Theme changed
- **Prevention**: Keep these fields the same when possible

### **"JSON error"**
- **Cause**: Data cleaning issue (rare)
- **Solution**: The script handles this automatically, just retry

### **"Permission denied"**
- **Cause**: Google Sheets API credentials issue
- **Solution**: Check `google_credentials.json` file exists and has proper permissions

### **"Data validation rules lost"**
- **Cause**: Google Sheets API limitation when updating data
- **Solution**: Recreate data validation rules manually in Google Sheets
- **Prevention**: Document your data validation rules for easy recreation

### **"Caption doesn't follow RiseGuide format"**
- **Cause**: Missing framework structure or irrelevant tips
- **Solution**: Review and rewrite using Hook + Value (3 Quick Tips) + CTA structure
- **Validation Checklist**:
  - ✅ Has engaging hook related to the story?
  - ✅ Has exactly 3 numbered tips (1️⃣ 2️⃣ 3️⃣)?
  - ✅ Tips are relevant to the actual content shown?
  - ✅ Has clear call-to-action for engagement?
  - ✅ Authentic to sustainable cacao farming in Brazil?

## 💡 **Pro Tips**

1. **Make incremental changes** - easier to track and debug
2. **Keep a backup** of the CSV before major changes
3. **Use descriptive themes** for better primary key uniqueness
4. **Test primary key generation** before running sync
5. **Communicate with the user** about status preservation implications

## 📊 **Status Management**
- **Column A**: Primary key (auto-generated, don't touch)
- **Column B**: Status (manual updates in Google Sheets, preserved during sync)
- **Column C+**: Content data (safe to modify in CSV)

## 🔄 **Understanding the Sync Process**
1. Script reads CSV file
2. Generates deterministic primary keys for each row
3. Retrieves existing status values from Google Sheets
4. Matches rows by primary key
5. Preserves non-empty status values
6. Updates all other content
7. Writes back to Google Sheets

## 📞 **When to Ask for Help**
- When the user wants to change Post Day/Type/Theme (affects status preservation)
- When you're unsure about the impact of changes
- When sync fails with errors you don't understand
- When the user wants to modify the sync script itself

## 🎯 **Success Criteria**
- ✅ Content changes are applied correctly
- ✅ Existing status values are preserved
- ✅ New content is ready for manual status updates
- ✅ Google Sheets reflects all changes
- ✅ User understands any status preservation implications
- ✅ **All NEW/UNSCHEDULED captions follow RiseGuide framework**
- ✅ **SCHEDULED captions remain unchanged** (unless specifically requested)
- ✅ **Tips are relevant to the actual story/content**
- ✅ **Captions are educational and engaging**

---

**Remember**: Your job is to help the user update content while preserving the valuable status tracking work that's already been done in Google Sheets. When in doubt, explain the implications to the user before proceeding.

---

# 📝 **TrueSight DAO Blog Post Generation**

## 🎯 **Mission**
Generate bi-weekly blog posts for TrueSight DAO highlighting community activity from the past 2 weeks, pulled directly from the public Telegram contribution logs.

## 📊 **Data Source**
- **Google Sheet**: [TrueSight DAO Telegram Compilation](https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ)
- **Worksheet**: "Telegram Chat Logs"
- **Data Range**: Last 14 days of contributions

## 🤖 **Understanding Edgar**
- **Edgar is NOT a human contributor**
- Edgar is the **AI bot** that logs submissions from DAO members via Telegram
- When you see "Contributor Name: Edgar" - it means Edgar logged a community member's submission
- **NEVER say**: "Edgar did X" or "Edgar attended Y"
- **ALWAYS say**: "Community members did X (logged by Edgar)" or "A community member attended Y"

## 📁 **File Naming Convention**
```
truesight_blog_posts/YYYYMMDD_highlight_title.md
```

**Examples:**
- `20251013_cacao_sourcing_expansion.md` (26 sourcing activities = main story)
- `20251027_infrastructure_overhaul.md` (if infrastructure is the highlight)
- `20251110_partnership_expansion.md` (if partnerships dominate)

**Key Rule**: Title reflects the **actual highlight** of the 2-week period, NOT generic "fortnight update"

## 🔍 **Analysis Process**

### Step 1: Pull Data from Google Sheets
```python
# Use google.oauth2.service_account to authenticate
# Pull last 100 records from "Telegram Chat Logs" worksheet
# Filter for past 14 days based on "Status date" column
```

### Step 2: Identify the Main Story
Analyze contribution types and count:
- Cacao sourcing activities
- Infrastructure improvements
- Community building
- Business development
- DAO governance

**The category with the most activity becomes the blog post title/focus**

### Step 3: Content Structure
```markdown
# [Highlight Title]: [Key Metric] in Two Weeks

**Meta Description**: Brief summary with key numbers

**SEO Title**: SEO-friendly version

**URL Slug**: url-friendly-slug

## [Opening Section - Lead with the main story]

## 📊 By the Numbers
- Total contributions logged by AI bot
- Key metrics for main story
- Supporting statistics

## 🌱 [Main Story Section]
### [Subsection 1]
### [Subsection 2]

## 🛠️ [Supporting Story 1]

## 🤝 [Supporting Story 2]

## 💡 What This Activity Means
### Transparent Contribution Tracking (explain Edgar's role)
### [Main Story] in Action

## 🔮 Looking Ahead

## 🎯 Key Takeaways
**For Contributors:**
**For Observers:**
**For [relevant stakeholder]:**

## 📢 How to Follow Along
[Link to Telegram]
[Link to public ledger]

## Conclusion
[Tie it back to main story]

---
**Next Update**: [Date] - highlighting the next major milestone
**TDG Airdrop**: Next expected distribution: June 21, 2025
---
*Compiled from [X] contributions logged by Edgar in Telegram between [dates]*
**About TrueSight DAO**: [Description with Telegram link]
```

## ✅ **Content Guidelines**

### DO:
- ✅ Lead with the main story (highest activity category)
- ✅ Use specific numbers (26 sourcing activities, 100 contributions, etc.)
- ✅ Clarify Edgar is the AI tracking bot, not a contributor
- ✅ Link to Telegram (https://t.me/truesightdao) and public ledger
- ✅ Focus on what **community members** did, not what Edgar did
- ✅ Make phrases clickable URLs where appropriate

### DON'T:
- ❌ Use generic titles like "Fortnight Update" or "Bi-Weekly Update"
- ❌ Say "Edgar attended" or "Edgar did [activity]"
- ❌ Claim events happened that didn't (verify from actual data)
- ❌ Include marketing fluff - stick to actual logged activity
- ❌ Forget to link Telegram and public ledger multiple times

## 🔗 **Key Links to Include**
- Telegram: https://t.me/truesightdao
- Bot: https://t.me/truesight_tdg_bot
- Public Ledger: https://docs.google.com/spreadsheets/d/1qbZZhf-_7xzmDTriaJVWj6OZshyQsFkdsAV8-pyzASQ

## 📅 **Publishing Cadence**
- **Every 2 weeks** (bi-weekly)
- Pull data from past 14 days
- Publish within 1-2 days after period ends
- Next update date should be mentioned in each post

## 🎯 **Success Criteria**
- ✅ Title reflects actual highlight, not generic date
- ✅ Edgar correctly described as AI bot throughout
- ✅ All claims are factually correct based on logged data
- ✅ Multiple clickable links to Telegram and ledger
- ✅ File named with YYYYMMDD_highlight_title.md format
- ✅ Specific numbers and metrics throughout
- ✅ Clear separation between what community members did vs what Edgar logged

---

**Remember**: These blog posts demonstrate TrueSight DAO's transparency. Every claim should be verifiable in the public Telegram logs and Google Sheets ledger.
