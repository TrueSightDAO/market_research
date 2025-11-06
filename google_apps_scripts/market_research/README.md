# Market Research Google Apps Scripts

This directory contains Google Apps Script files for market research and store location services.

## 📁 Scripts

### `find_nearby_stores.gs`

**Purpose**: Find the top N stores (filtered by status) nearest to a given location from the holistic wellness hit list spreadsheet.

**Spreadsheet**: [20251104 - holistic wellness hit list](https://docs.google.com/spreadsheets/d/1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc/edit)  
**Sheet Name**: "Hit List"

**Features**:
- ✅ Distance calculation using Haversine formula (returns miles)
- ✅ Filters stores by status (default: "Contacted")
- ✅ Returns top N stores ordered by distance (default: 10, max: 50)
- ✅ Web API (GET) for easy integration
- ✅ Test functions included for debugging

**Setup**:
1. Copy the script to Google Apps Script editor
2. Deploy as Web App (Anyone can access)
3. Copy deployment URL
4. Update the placeholder URL in the DApp module (`stores_nearby.html`)

**API Endpoint**:
```
GET <deployment_url>?lat=<latitude>&lng=<longitude>&limit=<number>&status=<status>
```

**Parameters**:
- `lat` (required): User's latitude
- `lng` (required): User's longitude
- `limit` (optional): Maximum number of results (default: 10, max: 50)
- `status` (optional): Filter by store status (default: "Contacted")

**Response Format**:
```json
{
  "success": true,
  "location": { "latitude": 37.7749, "longitude": -122.4194 },
  "status_filter": "Contacted",
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
      "instagram": "https://instagram.com/store",
      "shop_type": "Metaphysical/Spiritual",
      "priority": "High",
      "status": "Contacted",
      "notes": "Store notes...",
      "contact_date": "2025-11-05",
      "contact_method": "Email",
      "latitude": 37.7849,
      "longitude": -122.4094,
      "distance": 1.2
    }
  ]
}
```

**Testing**:
- Run `testFindNearbyStores()` to test the core function
- Run `testDoGet()` to test the full web app flow
- Check View > Logs for output

**DApp Integration**:
The script is integrated with the TrueSight DAO DApp at `stores_nearby.html`. After deployment, update the `API_URL` constant in the HTML file with your deployment URL.

---

**Repository**: [market_research](https://github.com/TrueSightDAO/market_research)

