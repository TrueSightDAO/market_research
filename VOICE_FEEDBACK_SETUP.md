# 🎤 Voice Feedback Capture Setup Guide

## Overview
Capture content ideas and feedback using your iPhone + Siri, automatically saved to Google Sheets without touching your phone!

**Flow**: Siri → Shortcuts → Google Apps Script → Google Sheets

---

## 📋 Part 1: Deploy Google Apps Script (5 minutes)

### Step 1: Open Google Apps Script
1. Go to [script.google.com](https://script.google.com)
2. Click **"New Project"**
3. Name it: `Voice Feedback Capture`

### Step 2: Copy the Script
1. Delete the default `myFunction()` code
2. Copy ALL contents from: `google_apps_scripts/voice_feedback_capture.gs`
3. Paste into the script editor
4. Click **Save** (💾 icon)

### Step 3: Initialize the Feedback Sheet (Optional)
1. In the script editor, select function: `initializeFeedbackSheet`
2. Click **Run** (▶️ icon)
3. Authorize the script when prompted
4. Check execution log - should say "✅ Sheet initialized successfully!"

### Step 4: Deploy as Web App
1. Click **Deploy** → **New deployment**
2. Click gear icon ⚙️ → Select **"Web app"**
3. Settings:
   - **Description**: "Voice Feedback API"
   - **Execute as**: "Me"
   - **Who has access**: "Anyone" (needed for Shortcuts to access)
4. Click **Deploy**
5. **IMPORTANT**: Copy the **Web app URL** (looks like: `https://script.google.com/macros/s/AKfycby.../exec`)

---

## 📱 Part 2: Create iPhone Shortcut (3 minutes)

### Step 1: Open Shortcuts App
1. Open **Shortcuts** app on iPhone
2. Tap **"+"** to create new shortcut
3. Tap **"Add Action"**

### Step 2: Add Actions

**Action 1: Dictate Text**
1. Search for: "Dictate Text"
2. Add it
3. Configure:
   - Tap "Show More"
   - Set "Stop Listening" to: "After Pause"
   - Language: English (or your preference)

**Action 2: Get Contents of URL**
1. Search for: "Get Contents of URL"
2. Add it
3. Configure:
   - **URL**: `YOUR_WEB_APP_URL?feedback=` (paste your deployment URL from Step 4 above)
   - Tap **"Dictated Text"** variable at the end of URL (it should appear blue)
   - **Method**: GET
   - **Headers**: None needed

**Action 3: Get Dictionary from Input** (Optional but helpful)
1. Search for: "Get Dictionary from Input"
2. Add it
3. Leave default settings

**Action 4: Show Notification**
1. Search for: "Show Notification"
2. Add it
3. Configure:
   - Tap in text field
   - Add: **Dictionary Value** for "message" key
   - Fallback text: "✅ Feedback saved!"

### Step 3: Name Your Shortcut
1. Tap shortcut name at top
2. Rename to: **"Add Feedback"** or **"Content Idea"**
3. Tap **Done**

### Step 4: Add to Siri (Make it Voice-Activated!)
1. Tap the shortcut's ⋮ menu (three dots)
2. Tap ℹ️ (info icon)
3. Tap **"Add to Siri"**
4. Record phrase: *"Add feedback"* or *"Content idea"*
5. Tap **Done**

---

## 🎯 Usage Examples

### Method 1: Siri (Hands-Free)
```
You: "Hey Siri, add feedback"
Siri: "What would you like to say?"
You: "Winter wellness content idea: create a carousel about cacao and seasonal affective disorder"
Siri: [Shows notification] "✅ Feedback saved!"
```

### Method 2: Widget (One Tap)
1. Long-press home screen → Add Widget
2. Find **Shortcuts** widget
3. Add your "Add Feedback" shortcut
4. Now just tap widget → speak → done!

### Method 3: From Shortcuts App
1. Open Shortcuts app
2. Tap "Add Feedback"
3. Speak your idea
4. Done!

---

## 📊 Viewing Your Feedback

All feedback appears in:
🔗 [Feedback on Content Sheet](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=497764730#gid=497764730)

**Columns**:
- **Column A (Feedback)**: Your voice-to-text idea
- **Column B (Status)**: Empty initially - mark as "INCORPORATED", "PENDING", "REJECTED"
- **Column C (Timestamp)**: Automatically added

---

## 🧪 Testing

### Test 1: From Script Editor
1. Go to your Apps Script project
2. Select function: `testAddFeedback`
3. Click **Run** (▶️)
4. Check your Google Sheet - should see test feedback

### Test 2: From Browser
1. Copy your Web App URL
2. Add: `?feedback=Test from browser`
3. Paste in browser and press Enter
4. Should see JSON response: `{"status":"success"...}`
5. Check Google Sheet for the test entry

### Test 3: From iPhone
1. Run your Shortcut
2. Say: "This is a test"
3. Check for notification
4. Verify in Google Sheet

---

## 🔧 Troubleshooting

### Problem: "Script not authorized"
**Solution**: Run `testAddFeedback` in script editor first to authorize

### Problem: No notification on iPhone
**Solution**: 
- Check iPhone Settings → Shortcuts → Allow Notifications
- Verify URL is correct (must end with `/exec`)

### Problem: Feedback not appearing in sheet
**Solution**:
- Check script execution logs (View → Executions in Apps Script)
- Verify sheet name is exactly: "Feedback on Content"
- Run `initializeFeedbackSheet` function

### Problem: Siri says "I can't do that"
**Solution**:
- Re-record Siri phrase (simpler is better)
- Try: "Hey Siri, run Add Feedback"

---

## 🎨 Advanced Customization

### Add Category/Priority
Modify the script to ask for category:

```javascript
// In iPhone Shortcut, add before "Get Contents of URL":
// 1. "Choose from Menu" action with categories
// 2. Append category to feedback text
```

### Email Notifications
Add to script after `sheet.appendRow()`:

```javascript
MailApp.sendEmail({
  to: 'your@email.com',
  subject: '🎤 New Voice Feedback',
  body: feedback
});
```

### Integration with Existing Workflows
The feedback sheet can be:
- Pulled by Python scripts (using `pull_from_sheets.py`)
- Synced with content schedule
- Processed by AI for categorization

---

## 📁 Files in Repository

- **`google_apps_scripts/voice_feedback_capture.gs`**: The Google Apps Script code
- **`VOICE_FEEDBACK_SETUP.md`**: This setup guide (you are here!)
- **`sync_feedback.py`**: Python script to sync feedback to local CSV

---

## 🚀 Next Steps

1. Deploy the script ✅
2. Create iPhone Shortcut ✅
3. Test with Siri ✅
4. Start capturing ideas effortlessly! 🎉

**Pro Tip**: Keep a note of your Web App URL somewhere safe. If you redeploy the script, the URL changes!

---

## 📞 Support

Having issues? Check:
1. Script execution logs in Apps Script
2. iPhone Shortcuts debug mode (tap ⓘ on shortcut)
3. Google Sheet permissions

**Repository**: [market_research](https://github.com/TrueSightDAO/market_research)  
**Spreadsheet**: [Content Marketing Schedule](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ)

