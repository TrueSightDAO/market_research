# iPhone Shortcuts Template for Voice Feedback

## Quick Setup Instructions

Since iPhone Shortcuts can't be exported as text files easily, follow these exact steps to recreate the shortcut:

---

## 📱 Create "Add Feedback" Shortcut

### Actions to Add (in order):

#### 1. **Dictate Text**
- Search: "Dictate Text"
- Tap to add
- Settings:
  - Language: English
  - Stop Listening: "After Pause"

#### 2. **Set Variable**
- Search: "Set Variable"
- Tap to add
- Name: `FeedbackText`
- Value: (leave as "Dictated Text")

#### 3. **Get Contents of URL**
- Search: "URL"
- Tap to add
- Configure:
  ```
  URL: YOUR_DEPLOYMENT_URL?feedback=FeedbackText&signature=YourPublicKey
  ```
  - Replace `YOUR_DEPLOYMENT_URL` with your actual Web App URL from Google Apps Script
  - The `FeedbackText` should be inserted as a variable (blue bubble)
  - For `YourPublicKey`: You can either:
    - **Option A** (Recommended): Manually paste your public key from create_signature.html
    - **Option B**: Leave empty if you don't need signature tracking for voice feedback
  - Method: **GET**
  - Headers: (none)

**Note**: If using Option A, you'll need to update the shortcut URL with your actual public key after creating your digital signature. For most voice feedback use cases, Option B (without signature) works fine since you'll manually review in Google Sheets anyway.

#### 4. **Get Dictionary from Input**
- Search: "Get Dictionary"
- Tap to add
- (No configuration needed - it parses the JSON response)

#### 5. **Get Dictionary Value**
- Search: "Get Dictionary Value"
- Tap to add
- Configure:
  - Get: `message`
  - From: Dictionary

#### 6. **Show Notification**
- Search: "Show Notification"
- Tap to add
- Configure:
  - Text: Insert "Dictionary Value" variable
  - Play Sound: On (optional)

---

## 🎙️ Add to Siri

1. Tap the shortcut's **⋮** menu (three dots)
2. Tap **ℹ️** (Settings)
3. Tap **"Add to Siri"**
4. Record your phrase:
   - Simple option: *"Add feedback"*
   - Alternative: *"Content idea"*
   - Alternative: *"Save this thought"*
5. Tap **Done**

---

## 🧪 Test Your Shortcut

### Test 1: From Shortcuts App
1. Open Shortcuts app
2. Tap "Add Feedback" shortcut
3. Speak: "This is a test from iPhone"
4. Should see notification: "✅ Feedback saved!"

### Test 2: With Siri
1. Say: *"Hey Siri, add feedback"*
2. Wait for listening prompt
3. Speak: "Test via Siri voice activation"
4. Should see notification and hear confirmation

### Test 3: Check Google Sheet
1. Open [Feedback sheet](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=497764730)
2. Look for your test entries in Column A
3. Verify timestamp in Column C

---

## 📋 Shortcut Configuration Visual Guide

```
┌──────────────────────────────────────────────────────────┐
│  Dictate Text                                            │
│  ↓ (Dictated Text)                                       │
├──────────────────────────────────────────────────────────┤
│  Set Variable: FeedbackText                              │
│  ↓ (FeedbackText)                                        │
├──────────────────────────────────────────────────────────┤
│  Get Contents of URL                                     │
│  URL: YOUR_URL?feedback=FeedbackText&signature=YOUR_KEY  │
│  Method: GET                                             │
│  ↓ (Contents of URL)                                     │
├──────────────────────────────────────────────────────────┤
│  Get Dictionary from Input                               │
│  ↓ (Dictionary)                                          │
├──────────────────────────────────────────────────────────┤
│  Get Dictionary Value                                    │
│  Get: "message"                                          │
│  ↓ (Dictionary Value)                                    │
├──────────────────────────────────────────────────────────┤
│  Show Notification                                       │
│  Text: Dictionary Value                                  │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Usage Examples

### Scenario 1: Watching Instagram
```
You: "Hey Siri, add feedback"
Siri: [Listening...]
You: "Competitor posted great carousel about cacao processing steps. 
      Could we do similar but focus on regenerative soil benefits?"
Siri: "✅ Feedback saved!"
```
→ Immediately appears in Google Sheet

### Scenario 2: Customer Conversation
```
You: "Hey Siri, add feedback"
Siri: [Listening...]
You: "Customer asked about cacao and gut health. 
      Possible blog post idea for February?"
Siri: "✅ Feedback saved!"
```
→ Captured without interrupting conversation

### Scenario 3: Farm Visit
```
You: "Hey Siri, add feedback"
Siri: [Listening...]
You: "Oscar mentioned new fermentation technique. 
      Could be great behind-the-scenes reel."
Siri: "✅ Feedback saved!"
```
→ Captured while hands are dirty!

---

## 🔧 Troubleshooting

### Issue: Siri says "I can't do that"
**Fix**: 
- Re-add shortcut to Siri with simpler phrase
- Try: "Hey Siri, run Add Feedback" (more explicit)

### Issue: No notification appears
**Fix**:
- Check Settings → Shortcuts → Allow Notifications
- Verify URL in shortcut is correct (must end with `/exec`)

### Issue: "Get Dictionary" fails
**Fix**:
- Your Apps Script might not be returning JSON
- Test the URL directly in Safari to see response
- Verify deployment is set to "Anyone can access"

---

## 💡 Pro Tips

1. **Widget Access**: Add shortcut to home screen widget for one-tap access
2. **Lock Screen**: Add to Lock Screen widgets (iOS 16+)
3. **Batch Ideas**: Speak multiple ideas in one recording - just separate with "and also..."
4. **Voice Quality**: Speak clearly but don't over-enunciate - Siri adapts to your voice
5. **Review Later**: Set a reminder to review feedback sheet weekly and update statuses

---

## 🔗 Resources

- **Setup Guide**: [VOICE_FEEDBACK_SETUP.md](../VOICE_FEEDBACK_SETUP.md)
- **Google Apps Script**: [voice_feedback_capture.gs](./voice_feedback_capture.gs)
- **Feedback Sheet**: [View Sheet](https://docs.google.com/spreadsheets/d/1ghZXeMqFq97Vl6yLKrtDmMQdQkd-4EN5yQs34NA_sBQ/edit?gid=497764730)

---

**Last Updated**: October 21, 2025  
**Version**: 1.0

