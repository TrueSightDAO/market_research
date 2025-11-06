# Find Nearby Stores - Google Apps Script

This Google Apps Script finds the top 10 stores (with status "Contacted") that are nearest to a given location.

## 📋 Overview

The script queries the "Hit List" sheet in your Google Spreadsheet, filters for stores with status "Contacted", calculates distances using the Haversine formula, and returns the nearest stores ordered by distance.

## 🚀 Setup

### 1. Copy Script to Google Apps Script

1. Open [Google Apps Script](https://script.google.com/)
2. Create a new project
3. Copy the contents of `find_nearby_stores.gs` into the editor
4. Save the project (e.g., "Find Nearby Stores")

### 2. Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Click the gear icon ⚙️ next to "Select type" and choose **Web app**
3. Configure:
   - **Description**: "Find nearby stores API"
   - **Execute as**: Me (your account)
   - **Who has access**: Anyone (or "Anyone with Google account" if you prefer)
4. Click **Deploy**
5. **Copy the Web App URL** - you'll need this to call the API

### 3. Authorize the Script

- On first run, you'll need to authorize the script to access your Google Sheets
- Click **Review permissions** → Choose your account → **Advanced** → **Go to [Project Name] (unsafe)** → **Allow**

## 📖 Usage

### As a Web API

The script can be called via HTTP GET or POST with these parameters:

- `lat` or `latitude` (required): Your latitude
- `lng` or `longitude` (required): Your longitude  
- `limit` (optional): Maximum number of results (default: 10, max: 50)

#### Example GET Request

```
https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?lat=37.7749&lng=-122.4194&limit=10
```

#### Example POST Request (JavaScript)

```javascript
const url = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
const params = new URLSearchParams({
  lat: 37.7749,
  lng: -122.4194,
  limit: 10
});

fetch(`${url}?${params}`)
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.count} nearby stores:`);
    data.stores.forEach(store => {
      console.log(`${store.name} - ${store.distance} miles away`);
    });
  });
```

#### Example cURL

```bash
curl "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec?lat=37.7749&lng=-122.4194&limit=10"
```

### Response Format

```json
{
  "success": true,
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "count": 10,
  "stores": [
    {
      "name": "Store Name",
      "address": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "phone": "(555) 123-4567",
      "website": "https://example.com",
      "email": "info@example.com",
      "priority": "High",
      "latitude": 37.7849,
      "longitude": -122.4094,
      "distance": 1.2
    },
    ...
  ]
}
```

### Direct Function Call (in Apps Script Editor)

You can also test the function directly in the Apps Script editor:

1. Open the script editor
2. Run the `testFindNearbyStores()` function
3. Check the **Execution log** (View → Logs) for results

Or call it programmatically:

```javascript
const stores = findNearbyStores(37.7749, -122.4194, 10);
Logger.log(stores);
```

## 🔧 Configuration

Edit these constants at the top of the script if needed:

```javascript
const SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc";
const SHEET_NAME = "Hit List";
```

## 📊 How It Works

1. **Opens the spreadsheet** using the configured ID
2. **Reads all data** from the "Hit List" sheet
3. **Filters stores** with status "Contacted"
4. **Calculates distances** using the Haversine formula (returns miles)
5. **Sorts by distance** (nearest first)
6. **Returns top N stores** (default: 10)

## ⚠️ Important Notes

- **Distance is in miles** (to change to kilometers, modify the `R` constant in `calculateDistance()`)
- Only stores with **status = "Contacted"** are included
- Stores without valid **Latitude** and **Longitude** are skipped
- The script requires the sheet to have columns: "Shop Name", "Status", "Latitude", "Longitude"
- Rate limiting: Google Apps Script has execution time limits (6 minutes max)

## 🐛 Troubleshooting

### "Sheet not found" error
- Verify the `SHEET_NAME` constant matches your sheet name exactly
- Check that the sheet exists in your spreadsheet

### "Required columns not found"
- Ensure your sheet has columns: "Shop Name", "Status", "Latitude", "Longitude"
- Column names are case-sensitive

### No results returned
- Check that you have stores with status "Contacted"
- Verify those stores have valid Latitude and Longitude values
- Try running `testFindNearbyStores()` in the editor to see detailed logs

### Authorization errors
- Make sure the script is deployed with "Execute as: Me"
- Re-authorize if you've changed permissions

## 🔗 Related Files

- **Python Script**: `generate_shop_list.py` - Updates the sheet with shop data and geocodes addresses
- **Spreadsheet**: [Holistic Wellness Hit List](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit)

## 📝 Example Use Cases

1. **Mobile App Integration**: Call the API from your mobile app to show nearby stores
2. **Route Planning**: Find stores near your current location for efficient route planning
3. **Sales Visits**: Prioritize store visits based on proximity
4. **Analytics**: Track which stores are closest to key locations

---

**Repository**: [market_research](https://github.com/TrueSightDAO/market_research)

