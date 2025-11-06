#!/usr/bin/env python3
"""
Generate shop list for SF → LA → Slab City → Quartzite route
Adds shops to Google Sheet "LA Route"
"""

import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials

# Google Sheets configuration
SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
SERVICE_ACCOUNT_EMAIL = "agroverse-market-research@get-data-io.iam.gserviceaccount.com"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Shops along SF → LA → Slab City → Quartzite route
# Ordered by driving route
SHOPS_LA_ROUTE = [
    # ==== SAN FRANCISCO ====
    {
        "name": "The Love of Ganesha",
        "address": "1700 Haight St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "ACCEPTED - Bought outright (no consignment). Existing partner.",
        "priority": "Existing Partner",
        "status": "Partnered",
        "outcome": "Accepted - outright purchase"
    },
    {
        "name": "Kiki's Cocoa",
        "address": "Boutique chocolatier location",
        "city": "San Francisco",
        "state": "CA",
        "type": "Boutique Chocolate",
        "notes": "Already a partner - ethically-sourced, single-origin",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    {
        "name": "Infinity Coven",
        "address": "2827 25th St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Witchy boutique with spells, herbs, books, community workshops. Focus on magic and empowerment. Good fit for cacao.",
        "priority": "High",
        "status": "Research"
    },
    
    # ==== SAN JOSE / GILROY AREA ====
    {
        "name": "Ancient Ways",
        "address": "2980 Meridian Ave",
        "city": "San Jose",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Pagan and metaphysical store with herbs, candles, books, ritual supplies. Community-oriented events.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Gilroy Metaphysical Shop",
        "address": "[TBD]",
        "city": "Gilroy",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Gilroy metaphysical shop' or 'Gilroy spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    
    # ==== MONTEREY / SALINAS / BIG SUR ====
    {
        "name": "[Research Needed] Salinas Metaphysical Shop",
        "address": "[TBD]",
        "city": "Salinas",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Salinas metaphysical shop' or 'Salinas wellness center'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Monterey Metaphysical Shop",
        "address": "[TBD]",
        "city": "Monterey",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Monterey metaphysical shop' or 'Monterey spiritual store'. Tourist area may have wellness shops.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Big Sur Wellness/Retail",
        "address": "[TBD]",
        "city": "Big Sur",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Big Sur has spiritual retreats and wellness centers. Search: 'Big Sur wellness' or 'Big Sur retreat center retail'",
        "priority": "Low",
        "status": "Research"
    },
    
    # ==== SAN LUIS OBISPO AREA ====
    {
        "name": "[Research Needed] San Luis Obispo Metaphysical Shop",
        "address": "[TBD]",
        "city": "San Luis Obispo",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "College town - search: 'SLO metaphysical shop' or 'San Luis Obispo spiritual store'. Check downtown area.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Paso Robles Wellness Shop",
        "address": "[TBD]",
        "city": "Paso Robles",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Wine country area - search: 'Paso Robles wellness center' or 'Paso Robles health food store'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Morro Bay Spiritual Shop",
        "address": "[TBD]",
        "city": "Morro Bay",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Coastal town - search: 'Morro Bay metaphysical' or 'Morro Bay spiritual store'",
        "priority": "Low",
        "status": "Research"
    },
    
    # ==== SANTA BARBARA ====
    {
        "name": "[Research Needed] Santa Barbara Metaphysical Shop",
        "address": "[TBD]",
        "city": "Santa Barbara",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Upscale coastal city - search: 'Santa Barbara metaphysical shop' or 'Santa Barbara spiritual store'. Check State Street area.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Santa Barbara Wellness Center",
        "address": "[TBD]",
        "city": "Santa Barbara",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Search: 'Santa Barbara wellness center' or 'Santa Barbara yoga studio retail'",
        "priority": "Medium",
        "status": "Research"
    },
    
    # ==== VENTURA ====
    {
        "name": "[Research Needed] Ventura Metaphysical Shop",
        "address": "[TBD]",
        "city": "Ventura",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Ventura metaphysical shop' or 'Ventura spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    
    # ==== LOS ANGELES ====
    {
        "name": "[Research Needed] LA Melrose/Fairfax Metaphysical",
        "address": "[TBD]",
        "city": "Los Angeles",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Melrose/Fairfax area has many metaphysical shops. Search: 'Melrose metaphysical' or 'Fairfax spiritual store'. Check The Crystal Cave, Sage Goddess, etc.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] LA Venice/Santa Monica Metaphysical",
        "address": "[TBD]",
        "city": "Los Angeles",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Venice and Santa Monica have wellness/spiritual shops. Search: 'Venice metaphysical' or 'Santa Monica spiritual store'",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] LA Silver Lake/Echo Park Metaphysical",
        "address": "[TBD]",
        "city": "Los Angeles",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Hipster area with conscious retail. Search: 'Silver Lake metaphysical' or 'Echo Park spiritual store'",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] LA Boutique Chocolate Shop",
        "address": "[TBD]",
        "city": "Los Angeles",
        "state": "CA",
        "type": "Boutique Chocolate",
        "notes": "Search: 'Los Angeles boutique chocolate' or 'LA ethical chocolate'. Check areas like Beverly Hills, West Hollywood, Pasadena.",
        "priority": "High",
        "status": "Research"
    },
    
    # ==== PALM SPRINGS / INDIO ====
    {
        "name": "[Research Needed] Palm Springs Metaphysical Shop",
        "address": "[TBD]",
        "city": "Palm Springs",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Desert resort town - search: 'Palm Springs metaphysical shop' or 'Palm Springs spiritual store'. Check downtown area.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Indio Metaphysical Shop",
        "address": "[TBD]",
        "city": "Indio",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Coachella Valley - search: 'Indio metaphysical shop' or 'Coachella Valley spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    
    # ==== NILAND / SLAB CITY ====
    {
        "name": "[Research Needed] Niland Area Shop",
        "address": "[TBD]",
        "city": "Niland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Small town near Slab City - search: 'Niland shop' or check if there are any stores serving Slab City community",
        "priority": "Low",
        "status": "Research"
    },
    {
        "name": "The Ponderosa",
        "address": "Slab City",
        "city": "Niland",
        "state": "CA",
        "type": "Unique/Lifestyle",
        "notes": "Already a partner - off-grid, sustainability focus. Check if they want additional products.",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    
    # ==== BLYTHE / QUARTZSITE ====
    {
        "name": "[Research Needed] Blythe Metaphysical Shop",
        "address": "[TBD]",
        "city": "Blythe",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Gateway to Arizona - search: 'Blythe metaphysical shop' or 'Blythe spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Quartzsite Metaphysical Shop",
        "address": "[TBD]",
        "city": "Quartzsite",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "Famous for gem shows - many vendors during show season. Search: 'Quartzsite crystals' or 'Quartzsite metaphysical'. Target permanent retail spaces, not just show vendors.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Quartzsite Mineral/Crystal Shop",
        "address": "[TBD]",
        "city": "Quartzsite",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "During gem show season (Jan-Feb), many vendors. Focus on permanent shops that stay year-round. Verify product mix - not just crystals/stones.",
        "priority": "High",
        "status": "Research"
    },
]

def get_google_sheets_client():
    """Authenticate and return Google Sheets client"""
    creds_path = Path(__file__).parent / "google_credentials.json"
    
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Google credentials not found at {creds_path}. "
            "Please add google_credentials.json with service account credentials."
        )
    
    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=SCOPES
    )
    
    client = gspread.authorize(creds)
    return client

def create_shop_list_sheet(client, sheet_name="LA Route"):
    """Create or get shop list worksheet"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
    except Exception as e:
        raise Exception(f"Could not access spreadsheet. Make sure it's shared with {SERVICE_ACCOUNT_EMAIL}. Error: {e}")
    
    # Try to get existing worksheet
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"Found existing worksheet: {sheet_name}")
    except gspread.WorksheetNotFound:
        # Create new worksheet
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=100,
            cols=14
        )
        print(f"Created new worksheet: {sheet_name}")
    
    return worksheet

def add_shops_to_sheet(worksheet, shops):
    """Add shops to Google Sheet"""
    # Headers
    headers = [
        "Shop Name",
        "Address",
        "City",
        "State",
        "Shop Type",
        "Phone",
        "Website",
        "Notes",
        "Priority",
        "Status",
        "Contact Date",
        "Visit Date",
        "Outcome",
        "Sales Process Notes"
    ]
    
    # Clear existing data and add headers
    try:
        worksheet.clear()
        worksheet.append_row(headers)
    except Exception as e:
        print(f"Error clearing/adding headers: {e}")
        # If headers don't exist, add them
        if not worksheet.row_values(1):
            worksheet.append_row(headers)
    
    # Prepare all rows at once for batch update
    rows = []
    for shop in shops:
        row = [
            shop.get("name", ""),
            shop.get("address", ""),
            shop.get("city", ""),
            shop.get("state", ""),
            shop.get("type", ""),
            shop.get("phone", ""),
            shop.get("website", ""),
            shop.get("notes", ""),
            shop.get("priority", ""),
            shop.get("status", "Research"),
            shop.get("contact_date", ""),
            shop.get("visit_date", ""),
            shop.get("outcome", ""),
            shop.get("sales_notes", ""),
        ]
        rows.append(row)
    
    # Batch update for efficiency
    if rows:
        try:
            # Use batch_update for better performance
            range_name = f"A2:N{len(rows) + 1}"
            worksheet.update(values=rows, range_name=range_name)
            print(f"✅ Added {len(shops)} shops to worksheet")
        except Exception as e:
            print(f"Error in batch update: {e}")
            # Fallback to individual row updates
            for row in rows:
                try:
                    worksheet.append_row(row)
                except Exception as e:
                    print(f"Error adding row: {e}")
                    continue

def main():
    print("Generating shop list for SF → LA → Slab City → Quartzite route...")
    print(f"Target spreadsheet: {SPREADSHEET_ID}")
    
    client = get_google_sheets_client()
    worksheet = create_shop_list_sheet(client, "LA Route")
    add_shops_to_sheet(worksheet, SHOPS_LA_ROUTE)
    
    print(f"\n📊 Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={worksheet.id}")
    print("\n✅ Success! Shop list added to Google Sheet")
    print("\n📝 Next Steps:")
    print("1. Research actual shops in each city")
    print("2. Update the Google Sheet with real shop names and addresses")
    print("3. Use the search queries from PARTNER_TARGETING_GUIDE.md")
    print("4. Verify each shop's alignment with our values")

if __name__ == "__main__":
    main()

