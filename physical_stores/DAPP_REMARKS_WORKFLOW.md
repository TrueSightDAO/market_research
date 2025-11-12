## DApp Remarks Workflow

This repository now supports collecting status updates and free-form remarks from the `stores_nearby.html` DApp. Remarks are stored in the `DApp Remarks` worksheet until they are reviewed and merged into the main Hit List.

### Capturing remarks

1. From the DApp, expand a store card and choose the new **Remarks** textarea.
2. Pick any status (including the new **Shortlisted** option) and optionally enter notes.
3. Click **Update Status**.  
   The DApp calls the Apps Script endpoint, which:
   - Updates the Hit List status immediately.
   - Logs the submission in the `DApp Remarks` sheet with a unique ID and timestamps.

### Resolving remarks into the Hit List

Run the helper script whenever you want to merge the stored remarks into the Hit List:

```bash
cd /Users/garyjob/Applications/market_research
source venv/bin/activate
python3 process_dapp_remarks.py
```

What the script does:
- Reads all rows in `DApp Remarks` where **Processed != "Yes"**.
- Finds the matching shop in the Hit List.
- Updates the status (if present).
- Appends the remark to `Sales Process Notes` with a timestamp and submitter.
- Stamps `Processed = Yes` and sets `Processed At`.

Dry run mode (no updates) is available:

```bash
python3 process_dapp_remarks.py --dry-run
```

### Notes

- Make sure `google_credentials.json` is present before running the script.
- Each status update submission returns a `submission_id` (visible in browser dev tools) for traceability.
- The Hit List still needs to be regenerated and synced via `python3 generate_shop_list.py` when the underlying `generate_shop_list.py` data changes; the remarks script only patches the live sheet.

