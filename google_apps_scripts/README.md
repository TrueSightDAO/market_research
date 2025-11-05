# Google Apps Scripts for Content Marketing

This directory contains Google Apps Script files that integrate with the content marketing workflow.

## 📁 Scripts

### 1. `voice_feedback_capture.gs`

**Purpose**: Capture voice feedback from iPhone via Siri + Shortcuts and automatically add to Google Sheets.

**Spreadsheet**: [20250924 - Instagram Content Marketing Schedule](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ)  
**Sheet Name**: "Feedback on Content"

**Features**:
- ✅ Voice-to-text via iPhone Siri
- ✅ Hands-free feedback capture
- ✅ Automatic timestamping
- ✅ Works offline (queues until online)
- ✅ Simple GET/POST API
- ✅ Test functions included

**Setup**: See [VOICE_FEEDBACK_SETUP.md](../VOICE_FEEDBACK_SETUP.md)

---

## 🚀 Quick Start

1. **Copy script** to Google Apps Script editor
2. **Deploy** as Web App (Anyone can access)
3. **Copy deployment URL**
4. **Create iPhone Shortcut** with:
   - Dictate Text
   - Get Contents of URL (using your deployment URL)
   - Show Notification
5. **Add to Siri**: "Hey Siri, add feedback"

---

## 🔗 Related Files

- **Setup Guide**: [`VOICE_FEEDBACK_SETUP.md`](../VOICE_FEEDBACK_SETUP.md)
- **Feedback Sync**: [`sync_feedback.py`](../sync_feedback.py)
- **Process Feedback**: [`process_feedback.py`](../process_feedback.py)

---

## 📊 Workflow Integration

```
Voice Idea → Siri → Shortcuts → Apps Script → Google Sheets
                        ↓                              ↓
                  (with signature)          [Feedback, Status, Timestamp, Signature]
                                                     ↓
                                          sync_feedback.py
                                                     ↓
                                          community_feedback.csv
                                                     ↓
                                          process_feedback.py
                                                     ↓
                                     Content Schedule Integration
```

**Sheet Structure** (after v2.0 update):
- Column A: Feedback
- Column B: Status (INCORPORATED, PENDING, REJECTED)
- Column C: Timestamp
- Column D: Digital Signature (for verification & attribution)

---

## 🧪 Testing

Each script includes test functions you can run directly in the Apps Script editor:

```javascript
// voice_feedback_capture.gs
testAddFeedback()           // Test adding feedback
initializeFeedbackSheet()   // Initialize sheet structure
```

---

## 📝 Notes

- Scripts must be deployed as **Web Apps** to be accessible via HTTP
- Use **"Anyone can access"** permission for Shortcuts integration
- Deployment URLs change when you redeploy - save them!
- Check **View → Executions** in Apps Script for debugging

---

## 🔐 Security

- Scripts use OAuth authentication when deployed under "Execute as: Me"
- No sensitive data is exposed via the API
- Only POST/GET parameters are processed
- All data stays within your Google account

---

**Repository**: [market_research](https://github.com/TrueSightDAO/market_research)

