# 🤖 Cursor.AI Guide for Content Schedule Management

## 🎯 **Your Mission**
You are taking over the management of Instagram content scheduling for Agroverse.shop. Your primary responsibility is to update the content schedule when marketing priorities change or new opportunities arise.

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
3. **Run sync** - new content will get empty status (ready for manual status updates)

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
5. **When in doubt, ask the user** before making changes

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

---

**Remember**: Your job is to help the user update content while preserving the valuable status tracking work that's already been done in Google Sheets. When in doubt, explain the implications to the user before proceeding.
