# GitHub Actions Setup Guide

This guide explains how to set up automated syncing to Google Sheets using GitHub Actions.

## 🚀 Overview

The GitHub Actions workflow automatically syncs your CSV files to Google Sheets whenever you commit changes to:
- `agroverse_schedule_till_easter.csv`
- `instagram_hashtags.csv`
- `sync_content_schedule.py`
- `sync_hashtags.py`

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Google Service Account**: You need a Google Cloud service account with Sheets API access
3. **Google Sheets Access**: The service account must have edit access to your target Google Sheet

## 🔧 Setup Steps

### Step 1: Prepare Google Credentials

1. **Download your service account JSON file** (the same one you use locally)
2. **Convert to single line**: The JSON needs to be on a single line for GitHub Secrets
   ```bash
   # On Mac/Linux:
   cat google_credentials.json | tr -d '\n' | tr -d ' '
   
   # Or use jq to format it properly:
   jq -c . google_credentials.json
   ```

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:

   **Name**: `GOOGLE_CREDENTIALS_JSON`
   
   **Value**: Paste the entire JSON content (single line) from your service account file
   
   Example:
   ```
   {"type":"service_account","project_id":"your-project","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"your-service-account@your-project.iam.gserviceaccount.com","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"}
   ```

### Step 3: Verify Workflow File

The workflow file is already created at `.github/workflows/sync-to-sheets.yml`. It includes:

- **Triggers**: Runs on pushes to main/master branch when relevant files change
- **Two Jobs**: 
  - `sync-content-schedule`: Syncs content schedule CSV
  - `sync-hashtags`: Syncs hashtags CSV
- **Dependencies**: Installs Python 3.11 and required packages
- **Security**: Uses GitHub Secrets for credentials
- **Logging**: Uploads logs as artifacts for debugging

## 🔄 How It Works

### Trigger Conditions

The workflow runs when you push changes to:
- `agroverse_schedule_till_easter.csv` → Triggers content schedule sync
- `instagram_hashtags.csv` → Triggers hashtags sync
- `sync_content_schedule.py` → Triggers content schedule sync
- `sync_hashtags.py` → Triggers hashtags sync

### Workflow Steps

1. **Checkout Code**: Downloads your repository
2. **Setup Python**: Installs Python 3.11
3. **Install Dependencies**: Installs packages from `requirements.txt`
4. **Create Credentials**: Creates `google_credentials.json` from GitHub Secret
5. **Run Sync**: Executes the appropriate sync script
6. **Upload Logs**: Saves logs for debugging

## 📊 Monitoring

### View Workflow Runs

1. Go to your GitHub repository
2. Click the **Actions** tab
3. Select **Sync Content to Google Sheets** from the left sidebar
4. Click on any run to see detailed logs

### Check Results

- ✅ **Green checkmark**: Sync completed successfully
- ❌ **Red X**: Sync failed (check logs for details)
- ⚪ **Gray circle**: Workflow was skipped (no relevant files changed)

### Debugging Failed Runs

1. Click on a failed workflow run
2. Expand the failed step to see error messages
3. Download logs from the **Artifacts** section
4. Common issues:
   - Invalid JSON in GitHub Secret
   - Missing Google Sheets permissions
   - Network connectivity issues
   - CSV file format problems

## 🔒 Security Considerations

### GitHub Secrets

- ✅ **Secure**: Credentials are encrypted and only accessible during workflow runs
- ✅ **Environment**: Secrets are injected as environment variables
- ✅ **Scope**: Only accessible to workflows in this repository

### Google Service Account

- ✅ **Limited Scope**: Only has access to specific Google Sheets
- ✅ **Audit Trail**: All API calls are logged in Google Cloud Console
- ✅ **Rotation**: Can be rotated/regenerated if compromised

## 🛠️ Customization

### Modify Trigger Paths

Edit `.github/workflows/sync-to-sheets.yml` to change which files trigger the sync:

```yaml
paths:
  - 'your-custom-file.csv'
  - 'another-script.py'
```

### Add Environment Variables

Add custom environment variables to the workflow:

```yaml
- name: Run Content Schedule Sync
  env:
    CUSTOM_VAR: "value"
  run: |
    python sync_content_schedule.py
```

### Schedule-Based Runs

Add a schedule trigger to run syncs at specific times:

```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
  push:
    # ... existing triggers
```

## 🚨 Troubleshooting

### Common Issues

1. **"Google credentials not found"**
   - Check that `GOOGLE_CREDENTIALS_JSON` secret is properly set
   - Verify JSON format (must be single line)

2. **"Permission denied to Google Sheet"**
   - Ensure service account has edit access to the target sheet
   - Check sheet ID in sync scripts

3. **"Python dependencies not found"**
   - Verify `requirements.txt` is up to date
   - Check Python version compatibility

4. **"Workflow not triggering"**
   - Ensure you're pushing to the correct branch (main/master)
   - Check that file paths match the trigger conditions

### Getting Help

1. Check workflow logs in GitHub Actions tab
2. Download and examine log artifacts
3. Test scripts locally first
4. Verify Google Sheets API quotas and permissions

## 📈 Benefits

- ✅ **Automated**: No manual intervention required
- ✅ **Consistent**: Same sync process every time
- ✅ **Trackable**: Full audit trail in GitHub
- ✅ **Reliable**: Runs in isolated, consistent environment
- ✅ **Scalable**: Can handle multiple files and sheets
- ✅ **Secure**: Credentials stored safely in GitHub Secrets

---

**Next Steps**: After setting up GitHub Actions, your CSV files will automatically sync to Google Sheets whenever you commit changes! 🎉
