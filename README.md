# Market Research Repository

This repository contains tools and data for managing **multi-channel content marketing** for Agroverse.shop, including Instagram, blog content, and hashtag research.

## 📁 Repository Structure

```
market_research/
├── .github/
│   └── workflows/
│       └── sync-to-sheets.yml              # GitHub Actions workflow
├── venv/                                    # Python virtual environment
├── requirements.txt                         # Python dependencies
├── .gitignore                              # Git ignore file
├── README.md                               # This file
├── GITHUB_ACTIONS_SETUP.md                 # GitHub Actions setup guide
├── CURSOR_AI_GUIDE.md                      # Instagram content management guide
├── BLOG_SCHEDULE_GUIDE.md                  # Blog content management guide ⭐ NEW
├── FEEDBACK_WORKFLOW.md                    # Manual feedback integration guide
├── env.example                             # Environment variables template
├── google_credentials.json                 # Google Sheets API credentials (not in repo)
│
├── instagram_hashtags.csv                  # Comprehensive hashtag database
├── agroverse_schedule_till_easter_cleaned.csv  # Instagram content schedule
├── sync_content_schedule.py                # Sync Instagram schedule to Sheets
│
├── blog_schedule.csv                       # Blog content schedule ⭐ NEW
├── blog_schedule_template.csv              # Blog schedule template/example ⭐ NEW
├── blog_posts/                             # Markdown blog post content ⭐ NEW
│   └── okanogan_journey.md                 # First blog post
├── sync_blog_schedule.py                   # Sync blog schedule to Sheets ⭐ NEW
├── create_blog_drafts.py                   # Create Wix drafts from schedule ⭐ NEW
├── update_blog_draft.py                    # Update Wix drafts by primary key ⭐ NEW
├── wix_blog_publisher.py                   # Wix API integration library ⭐ NEW
│
├── sync_hashtags.py                        # Script to sync hashtags
├── sync_feedback.py                        # Script to sync community feedback
└── process_feedback.py                     # AI feedback processor
```

## 🚀 Quick Start

### Option 1: Manual Setup (Local Development)

#### 1. Setup Virtual Environment

```bash
# Navigate to the repository
cd market_research

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

#### 2. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create a Service Account
5. Download the JSON credentials file
6. Rename it to `google_credentials.json` and place it in this directory
7. Share your Google Sheets document with the service account email

#### 3. Run Sync Scripts

```bash
# Sync Instagram content schedule to Google Sheets
python sync_content_schedule.py

# Sync blog content schedule to Google Sheets
python sync_blog_schedule.py

# Sync hashtags to Google Sheets
python sync_hashtags.py
```

### Option 2: Automated Setup (GitHub Actions) ⭐ **RECOMMENDED**

For automated syncing whenever you commit changes, set up GitHub Actions:

1. **Follow the detailed setup guide**: [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md)
2. **Quick setup**:
   - Add your Google credentials as a GitHub Secret: `GOOGLE_CREDENTIALS_JSON`
   - Push changes to trigger automatic syncing
   - View sync status in the Actions tab of your repository

**Benefits**:
- ✅ Automatic syncing on every commit
- ✅ No manual intervention required
- ✅ Consistent, reliable execution
- ✅ Full audit trail and logging

## 📊 Data Files

### Instagram Hashtags (`instagram_hashtags.csv`)

Contains 400+ curated hashtags organized by:
- **Usage Category**: Core Cacao & Farming, Quality & Origin, etc.
- **Type**: General or Targeted
- **Notes**: Core Set, High Frequency, or Medium Frequency

### Content Schedule (`agroverse_schedule_till_easter.csv`)

Contains Instagram content planning data with:
- **Primary Key**: Unique 8-character identifier for each row
- **Status**: Content status (preserved during sync)
- **Weekly content themes**
- **Post schedules**
- **Content types** (Reel, Carousel, etc.)
- **Captions and hashtags**
- **Call-to-action suggestions**

**Important**: The `primary_key` column is automatically generated and used to match rows during sync, preserving manual status updates in Google Sheets.

### Blog Content Schedule (`blog_schedule.csv`) ⭐ NEW

Contains blog publishing schedule data with:
- **Primary Key**: Unique 8-character identifier based on Publish Date + Blog Title
- **Status**: Content status (DRAFT, REVIEW, SCHEDULED, PUBLISHED)
- **SEO Keywords**: Target keywords for each post
- **Content Outline**: Section-by-section structure
- **Instagram Tie-In**: How blog connects to Instagram content
- **Internal Links**: SEO linking strategy
- **Target Word Count**: Article length goals

**Synchronization with Instagram**: Blog posts are strategically timed to support and expand on Instagram content themes, creating a cohesive multi-channel strategy.

**Recommended Cadence**: 
- Start: 1 blog post per week (Weekly Monday publishing)
- Growth: 2 blog posts per week (Monday + Thursday)
- Blog published BEFORE related Instagram series begins

**Wix Draft Integration**: Blog drafts are created via Wix API and tracked in Google Sheets by Wix Draft ID. This allows for easy reference by primary key and collaborative editing workflow.

See **[BLOG_SCHEDULE_GUIDE.md](./BLOG_SCHEDULE_GUIDE.md)** for strategy, **[WIX_DRAFT_WORKFLOW.md](./WIX_DRAFT_WORKFLOW.md)** for the draft creation workflow, **[WIX_BLOG_GUIDE.md](./WIX_BLOG_GUIDE.md)** for manual publishing, and **[WIX_API_AUTOMATION_GUIDE.md](./WIX_API_AUTOMATION_GUIDE.md)** for API details.

## 🔄 Sync Process

### Content Schedule Sync

The `sync_content_schedule.py` script:
1. Reads `agroverse_schedule_till_easter.csv`
2. Generates primary keys for new rows (if missing)
3. Retrieves existing status values from Google Sheets
4. Connects to Google Sheets using API credentials
5. Clears existing content in "Content schedule" tab
6. Uploads new data while preserving existing status values
7. Matches rows by primary key to maintain status integrity
8. Provides confirmation and link to updated sheet

**Status Preservation**: Manual status updates in Column B are preserved during sync using primary key matching.

### Blog Schedule Sync ⭐ NEW

The `sync_blog_schedule.py` script:
1. Reads `blog_schedule.csv`
2. Generates primary keys based on Publish Date + Blog Title
3. Retrieves existing status values from Google Sheets
4. Connects to "Blog Content Schedule" worksheet (same spreadsheet)
5. Clears existing content
6. Uploads new data while preserving status values
7. Maintains status integrity through primary key matching

**Status Preservation**: Like Instagram, blog post statuses (DRAFT, SCHEDULED, PUBLISHED) are preserved during sync.

**Integration**: Blog schedule lives in the same Google Sheets document as Instagram content for easy cross-referencing.

### Hashtags Sync

The `sync_hashtags.py` script:
1. Reads `instagram_hashtags.csv`
2. Connects to Google Sheets using API credentials
3. Clears existing content in "Hashtag suggestions" tab
4. Uploads new data with formatting and auto-resized columns
5. Provides confirmation and link to updated sheet

## 🛠️ Dependencies

- `google-api-python-client`: Google Sheets API integration
- `gspread`: Simplified Google Sheets interface
- `pandas`: CSV data manipulation
- `python-dotenv`: Environment variable management
- `google-auth-oauthlib`: Google authentication

## 📝 How to Refresh CSV Files

### 1. Update Instagram Hashtags

1. Edit `instagram_hashtags.csv` directly
2. Add new hashtags with proper categorization
3. Run sync script:
   ```bash
   python sync_hashtags.py
   ```

### 2. Update Content Schedule

1. Create or edit `agroverse_schedule_till_easter.csv`
2. Ensure proper column headers:
   - Status, Week, Date Range, Theme, etc.
3. Run sync script:
   ```bash
   python sync_content_schedule.py
   ```

## 🤖 **Cursor.AI Instructions for New Users**

### **Quick Start for New Cursor.AI Instances**

When taking over this project, here's what you need to know:

#### **🎯 Primary Task: Content Schedule Management**
- **Main File**: `agroverse_schedule_till_easter.csv` 
- **Google Sheet**: [Content Schedule Tab](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=1682511679#gid=1682511679)
- **Key Constraint**: **NEVER override status values in Column B of Google Sheets**

#### **📋 CSV File Structure**
The CSV must have these columns in this exact order:
```csv
Week,Date Range,Theme Focus,Post Day,Post Type,Theme,Description,Caption,Hashtags,CTA,Tool Suggestions
```

#### **🔑 Primary Key System**
- Primary keys are **automatically generated** based on: `Post Day + Post Type + Theme`
- **Same content = Same primary key** (deterministic)
- **Status preservation** works by matching these primary keys

#### **⚡ Common Workflows**

**Scenario 1: Update Content for Specific Date Ranges**
```bash
# 1. Edit the CSV file
# 2. Update the content for the date range you want to change
# 3. Run sync (status values will be preserved)
python sync_content_schedule.py
```

**Scenario 2: Add New Content**
```bash
# 1. Add new rows to the CSV with proper date ranges
# 2. Run sync (new content gets empty status)
python sync_content_schedule.py
```

**Scenario 3: Check Current Status**
```bash
# View the Google Sheet directly to see current status values
# Link: https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ
```

#### **🚨 Critical Rules**
1. **NEVER modify the sync script** unless you understand the status preservation logic
2. **ALWAYS test changes** on a small subset first
3. **Primary keys are immutable** - changing date/type/theme changes the key
4. **Status values are sacred** - they represent manual work done in Google Sheets

#### **🛠️ Troubleshooting**
- **"Status not preserved"**: Check if primary key changed due to content modifications
- **"JSON error"**: Data cleaning is handled automatically in the script
- **"Permission denied"**: Check Google Sheets API credentials

#### **📊 Status Management**
- **Column A**: Primary key (auto-generated, don't touch)
- **Column B**: Status (manual updates, preserved during sync)
- **Column C+**: Content data (safe to modify)

#### **🔄 Sync Process**
1. Script reads CSV file
2. Generates deterministic primary keys
3. Retrieves existing status values from Google Sheets
4. Matches rows by primary key
5. Preserves non-empty status values
6. Updates all other content
7. Writes back to Google Sheets

#### **💡 Pro Tips**
- **Test changes** by modifying 1-2 rows first
- **Check primary keys** if status preservation fails
- **Use descriptive themes** for better primary key uniqueness
- **Keep status values simple**: "In Progress", "Completed", "Review", etc.

#### **📞 Getting Help**
- Check the sync script logs for detailed information
- Verify primary key generation with small test changes
- Ensure CSV format matches expected structure

### 3. CSV Format Requirements

**Instagram Hashtags CSV:**
```csv
Hashtag,Type,Usage Category,Notes
#cacao,General,Core Cacao & Farming,Core Set
#craftchocolate,General,Quality & Origin,High Frequency
```

**Content Schedule CSV:**
```csv
primary_key,status,week,date_range,theme,date,type,category,description,caption,hashtags,call_to_action,tools
a1b2c3d4,,Week 1,Sep 29-Oct 5,Fall Harvest Tease,Mon Sep 29,Reel,Behind-the-Scenes,Quick clip...,As fall arrives...,#cacao #cacaobeans...,Tag a friend...,Canva for thumbnail...
e5f6g7h8,In Progress,Week 1,Sep 29-Oct 5,Fall Harvest Tease,Tue Sep 30,Reel,Regenerative Farming,Time-lapse...,Building back...,#cacao #cacaofarm...,What's your dream...,CapCut for edit...
```

**Note**: The `primary_key` column is automatically managed by the sync script. The `status` column can be manually updated in Google Sheets and will be preserved during sync.

## 🔐 Security Notes

- `google_credentials.json` is in `.gitignore` and should never be committed
- Keep your Google Sheets API credentials secure
- Only share the Google Sheets document with necessary team members
- The service account should have minimal required permissions

## 🐛 Troubleshooting

### Common Issues

1. **"google_credentials.json not found"**
   - Ensure the credentials file is in the correct directory
   - Check file permissions

2. **"Permission denied" errors**
   - Verify the service account has access to the Google Sheets document
   - Check API permissions in Google Cloud Console

3. **"Worksheet not found"**
   - Ensure worksheet names match exactly: "Content schedule" and "Hashtag suggestions"
   - Check if worksheets exist in the Google Sheets document

### Getting Help

1. Check the console output for detailed error messages
2. Verify your CSV file format matches the expected structure
3. Ensure all dependencies are installed correctly

## 📈 Usage Tips

1. **Regular Syncs**: Run sync scripts after updating CSV files
2. **Backup**: Keep local copies of your CSV files
3. **Version Control**: Commit CSV changes to track updates
4. **Testing**: Test syncs with small data sets first

## 🔗 Links

- [Google Sheets Document](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=1682511679#gid=1682511679)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)

---

*Last updated: January 2025*
