/**
 * File: google_apps_scripts/market_research/find_nearby_stores.gs
 * Repository: https://github.com/TrueSightDAO/market_research
 * 
 * Description: REST API endpoint for finding nearby stores from the holistic wellness hit list.
 * Provides distance-based queries to find the top N stores nearest to a given location.
 * Filters stores by status (default: "Contacted") and returns results ordered by distance.
 * Supports status updates with digital signature tracking for audit trails.
 */

/**
 * Web app to find nearby stores from the holistic wellness hit list spreadsheet.
 * 
 * Deployment URL: https://script.google.com/macros/s/AKfycbwB2zqNV9nMCMWs2hSa8FecjA36Oh-mSVuz3pk8TpXrXcy9dvqOqgbWIirNka2LmacgPw/exec
 * 
 * Query parameters (for search):
 *   lat=<number>          : User's latitude (required)
 *   lng=<number>          : User's longitude (required)
 *   limit=<number>        : Maximum number of results (optional, default: 10, max: 50)
 *   status=<string>       : Filter by store status (optional, default: "Contacted")
 *                           Valid values: "Contacted", "Research", "Partnered", "Rejected", or any status value
 *                           Use empty string "" or omit parameter to show all statuses
 * 
 * Query parameters (for status update):
 *   action=update_status     : Action to update store status
 *   shop_name=<string>       : Name of the shop to update (required)
 *   new_status=<string>      : New status value (required)
 *                              Valid values: "Contacted", "Research", "Partnered", "Rejected", or any status value
 *   digital_signature=<string> : Digital signature (public key) of the person making the change (optional but recommended for audit trail)
 * 
 * Response format:
 *   {
 *     "success": true,
 *     "location": { "latitude": <number>, "longitude": <number> },
 *     "status_filter": "<string>",
 *     "count": <number>,
 *     "stores": [
 *       {
 *         "name": "<string>",
 *         "address": "<string>",
 *         "city": "<string>",
 *         "state": "<string>",
 *         "phone": "<string>",
 *         "website": "<string>",
 *         "email": "<string>",
 *         "instagram": "<string>",
 *         "shop_type": "<string>",
 *         "priority": "<string>",
 *         "status": "<string>",
 *         "notes": "<string>",
 *         "contact_date": "<string>",
 *         "contact_method": "<string>",
 *         "latitude": <number>,
 *         "longitude": <number>",
 *         "distance": <number>  // Distance in miles
 *       },
 *       ...
 *     ]
 *   }
 * 
 * Error response:
 *   {
 *     "success": false,
 *     "error": "<error message>"
 *   }
 * 
 * Instructions to call this endpoint:
 * 1. Deploy this script as a web app:
 *    - Click Deploy > New deployment > Web app.
 *    - Set "Execute as" to "Me" and "Who has access" to "Anyone" (or restrict as needed).
 *    - Click Deploy and copy the web app URL.
 * 2. Make an HTTP GET request with latitude and longitude:
 *    - URL format: <web_app_url>?lat=37.7749&lng=-122.4194&limit=10&status=Contacted
 *    - Example: https://script.google.com/macros/s/<ID>/exec?lat=37.7749&lng=-122.4194&limit=10
 * 3. Use a tool like curl, Postman, or JavaScript fetch to test:
 *    - curl: curl "<web_app_url>?lat=37.7749&lng=-122.4194&limit=10"
 *    - JavaScript: fetch("<web_app_url>?lat=37.7749&lng=-122.4194&limit=10").then(res => res.json())
 * 4. To test the function directly:
 *    - Open the script editor and run the testFindNearbyStores() function.
 *    - Check the Logs (View > Logs) for the result.
 * 
 * Note: Ensure the spreadsheet ID and sheet name defined in constants below match your setup.
 */

// Constants for spreadsheet ID and sheet name
const SPREADSHEET_ID = '1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc';
const SHEET_NAME = 'Hit List';

/**
 * Calculate distance between two points using Haversine formula
 * Returns distance in miles
 * @param {number} lat1 - Latitude of first point
 * @param {number} lon1 - Longitude of first point
 * @param {number} lat2 - Latitude of second point
 * @param {number} lon2 - Longitude of second point
 * @return {number} Distance in miles
 */
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 3959; // Earth's radius in miles
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  
  return distance;
}

/**
 * Convert degrees to radians
 * @param {number} degrees - Angle in degrees
 * @return {number} Angle in radians
 */
function toRad(degrees) {
  return degrees * (Math.PI / 180);
}

/**
 * Find nearby stores from the spreadsheet
 * @param {number} userLat - User's latitude
 * @param {number} userLng - User's longitude
 * @param {number} limit - Maximum number of results (default: 10)
 * @param {string|null} statusFilter - Filter by store status (default: "Contacted"). Use null to show all statuses
 * @return {Array} Array of store objects with distance
 */
function findNearbyStores(userLat, userLng, limit, statusFilter) {
  // Default statusFilter to "Contacted" if not provided
  if (statusFilter === undefined) {
    statusFilter = "Contacted";
  }
  try {
    // Open the spreadsheet
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error(`Sheet "${SHEET_NAME}" not found`);
    }
    
    // Get all data
    const data = sheet.getDataRange().getValues();
    if (data.length < 2) {
      return []; // No data rows
    }
    
    // Find column indices
    const headers = data[0];
    const shopNameIdx = headers.indexOf("Shop Name");
    const statusIdx = headers.indexOf("Status");
    const addressIdx = headers.indexOf("Address");
    const cityIdx = headers.indexOf("City");
    const stateIdx = headers.indexOf("State");
    const phoneIdx = headers.indexOf("Phone");
    const websiteIdx = headers.indexOf("Website");
    const emailIdx = headers.indexOf("Email");
    const instagramIdx = headers.indexOf("Instagram");
    const shopTypeIdx = headers.indexOf("Shop Type");
    const priorityIdx = headers.indexOf("Priority");
    const notesIdx = headers.indexOf("Notes");
    const contactDateIdx = headers.indexOf("Contact Date");
    const contactMethodIdx = headers.indexOf("Contact Method");
    const latIdx = headers.indexOf("Latitude");
    const lngIdx = headers.indexOf("Longitude");
    
    if (shopNameIdx === -1 || statusIdx === -1 || latIdx === -1 || lngIdx === -1) {
      throw new Error("Required columns not found in sheet");
    }
    
    // Process rows and filter by status
    const stores = [];
    
    // Log filtering info for debugging
    Logger.log("Filtering stores with statusFilter: " + statusFilter + " (type: " + typeof statusFilter + ")");
    
    for (let i = 1; i < data.length; i++) {
      const row = data[i];
      
      // Get status from row and normalize it
      const status = row[statusIdx];
      const rowStatus = status ? String(status).trim() : "";
      
      // Apply status filter (if statusFilter is null, show all stores regardless of status)
      if (statusFilter !== null && statusFilter !== undefined) {
        // We have a filter, so only include stores that match
        const filterStatus = String(statusFilter).trim();
        if (rowStatus !== filterStatus) {
          continue; // Skip this store - it doesn't match the filter
        }
      }
      // If statusFilter is null, we show all stores (no filtering)
      
      // Get coordinates
      const latStr = row[latIdx];
      const lngStr = row[lngIdx];
      
      // Skip if no coordinates
      if (!latStr || !lngStr || latStr === "" || lngStr === "") {
        continue;
      }
      
      // Parse coordinates
      let storeLat, storeLng;
      try {
        storeLat = parseFloat(latStr);
        storeLng = parseFloat(lngStr);
        
        if (isNaN(storeLat) || isNaN(storeLng)) {
          continue;
        }
      } catch (e) {
        continue;
      }
      
      // Calculate distance
      const distance = calculateDistance(userLat, userLng, storeLat, storeLng);
      
      // Build store object with all available fields
      const store = {
        name: row[shopNameIdx] || "",
        address: addressIdx >= 0 ? (row[addressIdx] || "") : "",
        city: cityIdx >= 0 ? (row[cityIdx] || "") : "",
        state: stateIdx >= 0 ? (row[stateIdx] || "") : "",
        phone: phoneIdx >= 0 ? (row[phoneIdx] || "") : "",
        website: websiteIdx >= 0 ? (row[websiteIdx] || "") : "",
        email: emailIdx >= 0 ? (row[emailIdx] || "") : "",
        instagram: instagramIdx >= 0 ? (row[instagramIdx] || "") : "",
        shop_type: shopTypeIdx >= 0 ? (row[shopTypeIdx] || "") : "",
        priority: priorityIdx >= 0 ? (row[priorityIdx] || "") : "",
        status: rowStatus, // Use the trimmed status
        notes: notesIdx >= 0 ? (row[notesIdx] || "") : "",
        contact_date: contactDateIdx >= 0 ? (row[contactDateIdx] || "") : "",
        contact_method: contactMethodIdx >= 0 ? (row[contactMethodIdx] || "") : "",
        latitude: storeLat,
        longitude: storeLng,
        distance: Math.round(distance * 10) / 10 // Round to 1 decimal place
      };
      
      stores.push(store);
    }
    
    // Sort by distance
    stores.sort((a, b) => a.distance - b.distance);
    
    // Return top N stores
    return stores.slice(0, limit);
    
  } catch (error) {
    Logger.log("Error in findNearbyStores: " + error.toString());
    throw error;
  }
}

/**
 * Update store status in the spreadsheet
 * @param {string} shopName - Name of the shop to update
 * @param {string} newStatus - New status value
 * @param {string} digitalSignature - Digital signature (public key) of the person making the change
 * @return {Object} Result object with success/error
 */
function updateStoreStatus(shopName, newStatus, digitalSignature) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      throw new Error(`Sheet "${SHEET_NAME}" not found`);
    }
    
    // Get all data
    const data = sheet.getDataRange().getValues();
    if (data.length < 2) {
      throw new Error("No data found in sheet");
    }
    
    // Find column indices
    const headers = data[0];
    const shopNameIdx = headers.indexOf("Shop Name");
    const statusIdx = headers.indexOf("Status");
    
    // Find or create "Status Updated By" column
    let statusUpdatedByIdx = headers.indexOf("Status Updated By");
    if (statusUpdatedByIdx === -1) {
      // Column doesn't exist, add it at the end
      const lastCol = headers.length;
      sheet.getRange(1, lastCol + 1).setValue("Status Updated By");
      statusUpdatedByIdx = lastCol;
      Logger.log("Created 'Status Updated By' column");
    }
    
    // Find or create "Status Updated Date" column
    let statusUpdatedDateIdx = headers.indexOf("Status Updated Date");
    if (statusUpdatedDateIdx === -1) {
      // Column doesn't exist, add it after "Status Updated By"
      const lastCol = headers.length + (statusUpdatedByIdx === headers.length ? 1 : 0);
      sheet.getRange(1, lastCol + 1).setValue("Status Updated Date");
      statusUpdatedDateIdx = lastCol;
      Logger.log("Created 'Status Updated Date' column");
    }
    
    if (shopNameIdx === -1 || statusIdx === -1) {
      throw new Error("Required columns not found in sheet");
    }
    
    // Find the shop by name (exact match)
    let found = false;
    for (let i = 1; i < data.length; i++) {
      if (data[i][shopNameIdx] === shopName) {
        const rowNum = i + 1; // Convert to 1-indexed for sheet
        
        // Update status
        sheet.getRange(rowNum, statusIdx + 1).setValue(newStatus);
        
        // Update digital signature (public key)
        if (digitalSignature) {
          sheet.getRange(rowNum, statusUpdatedByIdx + 1).setValue(digitalSignature);
        }
        
        // Update timestamp
        const timestamp = new Date();
        sheet.getRange(rowNum, statusUpdatedDateIdx + 1).setValue(timestamp);
        
        found = true;
        Logger.log(`Updated status for "${shopName}" to "${newStatus}" by ${digitalSignature || "unknown"}`);
        break;
      }
    }
    
    if (!found) {
      throw new Error(`Shop "${shopName}" not found`);
    }
    
    return { success: true, message: `Status updated to "${newStatus}"` };
  } catch (error) {
    Logger.log("Error in updateStoreStatus: " + error.toString());
    throw error;
  }
}

/**
 * Web app entry point - handles GET requests
 * @param {Object} e - Event object with parameters
 * @return {TextOutput} JSON response
 */
function doGet(e) {
  try {
    // Check if this is a status update request
    if (e.parameter.action === 'update_status') {
      const shopName = e.parameter.shop_name;
      const newStatus = e.parameter.new_status;
      const digitalSignature = e.parameter.digital_signature || e.parameter.signature || e.parameter.public_key;
      
      if (!shopName || !newStatus) {
        return ContentService
          .createTextOutput(JSON.stringify({
            success: false,
            error: "Missing parameters",
            message: "shop_name and new_status are required for status updates"
          }))
          .setMimeType(ContentService.MimeType.JSON);
      }
      
      // Update the status (digitalSignature is optional but recommended)
      const result = updateStoreStatus(shopName, newStatus, digitalSignature);
      
      return ContentService
        .createTextOutput(JSON.stringify({
          success: true,
          message: result.message
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Otherwise, handle as a search request
    // Get parameters
    const lat = parseFloat(e.parameter.lat || e.parameter.latitude);
    const lng = parseFloat(e.parameter.lng || e.parameter.longitude);
    const limit = parseInt(e.parameter.limit || "10");
    // Handle status filter: if not provided, default to "Contacted"; if empty string, show all
    let statusFilter = null;
    if (e.parameter.status !== undefined && e.parameter.status !== null) {
      // If status is empty string, set to null to show all
      if (e.parameter.status === "" || e.parameter.status === "All") {
        statusFilter = null;
      } else {
        statusFilter = e.parameter.status;
      }
    } else {
      statusFilter = "Contacted"; // Default if not provided
    }
    
    Logger.log("Status filter: " + statusFilter + " (type: " + typeof statusFilter + ")");
    
    // Validate parameters
    if (isNaN(lat) || isNaN(lng)) {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: "Invalid parameters",
          message: "lat and lng (or latitude and longitude) are required and must be valid numbers"
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    if (isNaN(limit) || limit < 1 || limit > 50) {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          error: "Invalid limit",
          message: "limit must be a number between 1 and 50"
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Find nearby stores
    const stores = findNearbyStores(lat, lng, limit, statusFilter);
    
    // Return JSON response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        location: { latitude: lat, longitude: lng },
        status_filter: statusFilter || "All",
        count: stores.length,
        stores: stores
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    Logger.log("Error in doGet: " + error.toString());
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Test function for status update
 * Usage: Run this function in the Apps Script editor to test the updateStoreStatus function
 */
function testUpdateStoreStatus() {
  const testShopName = "iChakras Smart Healing Center";
  const testNewStatus = "Partnered";
  
  Logger.log("Testing updateStoreStatus with:");
  Logger.log("  Shop Name: " + testShopName);
  Logger.log("  New Status: " + testNewStatus);
  Logger.log("");
  
  try {
    const result = updateStoreStatus(testShopName, testNewStatus);
    Logger.log("✅ Test successful!");
    Logger.log("Result: " + JSON.stringify(result));
    return result;
  } catch (error) {
    Logger.log("❌ Test failed: " + error.toString());
    throw error;
  }
}

/**
 * Test function - tests the actual method called by doGet
 * Usage: Run this function in the Apps Script editor to test the findNearbyStores function
 * Check View > Logs for the output
 */
function testFindNearbyStores() {
  // Test with San Francisco coordinates
  const lat = 37.7749;
  const lng = -122.4194;
  const limit = 10;
  
  // Test different status filters
  const testCases = [
    { status: "Contacted", description: "Filter by Contacted" },
    { status: "Research", description: "Filter by Research" },
    { status: null, description: "Show all statuses (null)" },
    { status: "", description: "Show all statuses (empty string)" }
  ];
  
  testCases.forEach(testCase => {
    Logger.log("=".repeat(50));
    Logger.log("Testing: " + testCase.description);
    Logger.log("  Latitude: " + lat);
    Logger.log("  Longitude: " + lng);
    Logger.log("  Limit: " + limit);
    Logger.log("  Status Filter: " + testCase.status);
    Logger.log("");
  
    try {
      const stores = findNearbyStores(lat, lng, limit, testCase.status);
    
      Logger.log("✅ Test successful!");
      Logger.log("Found " + stores.length + " stores");
      Logger.log("");
      if (stores.length > 0) {
        stores.forEach((store, index) => {
          Logger.log((index + 1) + ". " + store.name + " (Status: " + store.status + ") - " + store.distance.toFixed(2) + " miles");
        });
      } else {
        Logger.log("No stores found matching the filter.");
      }
      Logger.log("");
    } catch (error) {
      Logger.log("❌ Test failed: " + error.toString());
      Logger.log("");
    }
  });
}

/**
 * Test function - simulates doGet call with test parameters
 * Usage: Run this function in the Apps Script editor to test the full doGet flow
 * Check View > Logs for the output
 */
function testDoGet() {
  // Simulate doGet call with test parameters
  const e = {
    parameter: {
      lat: "37.7749",
      lng: "-122.4194",
      limit: "10",
      status: "Contacted"
    }
  };
  
  Logger.log("Testing doGet with parameters:");
  Logger.log("  lat: " + e.parameter.lat);
  Logger.log("  lng: " + e.parameter.lng);
  Logger.log("  limit: " + e.parameter.limit);
  Logger.log("  status: " + e.parameter.status);
  Logger.log("");
  
  try {
    const output = doGet(e);
    const responseText = output.getContent();
    const response = JSON.parse(responseText);
    
    Logger.log("✅ doGet test successful!");
    Logger.log("Response:");
    Logger.log(responseText);
    
    if (response.success) {
      Logger.log("Found " + response.count + " stores");
    } else {
      Logger.log("Error: " + response.error);
    }
    
    return response;
  } catch (error) {
    Logger.log("❌ doGet test failed: " + error.toString());
    throw error;
  }
}

/**
 * Test function - simulates status update doGet call
 * Usage: Run this function in the Apps Script editor to test the status update functionality
 * Check View > Logs for the output
 */
function testDoGetStatusUpdate() {
  // Simulate doGet call for status update
  const e = {
    parameter: {
      action: "update_status",
      shop_name: "iChakras Smart Healing Center",
      new_status: "Partnered"
    }
  };
  
  Logger.log("Testing doGet status update with parameters:");
  Logger.log("  action: " + e.parameter.action);
  Logger.log("  shop_name: " + e.parameter.shop_name);
  Logger.log("  new_status: " + e.parameter.new_status);
  Logger.log("");
  
  try {
    const output = doGet(e);
    const responseText = output.getContent();
    const response = JSON.parse(responseText);
    
    Logger.log("✅ Status update test successful!");
    Logger.log("Response:");
    Logger.log(responseText);
    
    return response;
  } catch (error) {
    Logger.log("❌ Status update test failed: " + error.toString());
    throw error;
  }
}

