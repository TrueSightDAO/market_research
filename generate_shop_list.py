#!/usr/bin/env python3
"""
Generate shop target list for SF to Quartzite route and add to Google Sheet
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from pathlib import Path

# Google Sheets configuration
SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
SERVICE_ACCOUNT_EMAIL = "agroverse-market-research@get-data-io.iam.gserviceaccount.com"

# Scope for Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Route: San Francisco → Quartzite, Arizona
# Cities along the route (ordered by driving sequence)
ROUTE_CITIES = [
    # California
    ("San Francisco", "CA"),
    ("Oakland", "CA"),
    ("Stockton", "CA"),
    ("Modesto", "CA"),
    ("Fresno", "CA"),
    ("Bakersfield", "CA"),
    ("Mojave", "CA"),
    ("Barstow", "CA"),
    # Arizona
    ("Needles", "CA"),  # Note: Needles is actually in CA, near AZ border
    ("Kingman", "AZ"),
    ("Lake Havasu City", "AZ"),
    ("Parker", "AZ"),
    ("Quartzsite", "AZ"),
]

# Shops from Grok research + existing partners + route research
SHOPS = [
    # Existing Partners
    {
        "name": "The Love of Ganesha",
        "address": "1700 Haight St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "ACCEPTED - Bought outright (no consignment). Successful model - prefer outright purchase over consignment.",
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
    # South Bay (Mountain View, Palo Alto, San Jose)
    {
        "name": "East West Bookshop",
        "address": "324 Castro St",
        "city": "Mountain View",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "REJECTED - Doesn't like consignment + needs 100% markup. Issue is pricing structure, not venue fit. Need to offer outright purchase + calculate wholesale price that allows 100% markup.",
        "priority": "High",
        "status": "Rejected",
        "outcome": "Rejected - pricing/markup issue"
    },
    {
        "name": "7 Rays Holistic Center",
        "address": "3035 El Camino Real",
        "city": "Palo Alto",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Offers reiki, crystal healing, metaphysical products (tarot, sacred geometry). Focus on energy work and personal growth. Suitable for cacao as ceremonial enhancement.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "Ancient Ways",
        "address": "2980 Meridian Ave",
        "city": "San Jose",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Pagan and metaphysical store with herbs, candles, books, ritual supplies. Community-oriented events and ancient traditions. Fosters courage through sacred practices.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "The Universal Connection",
        "address": "1261 Lincoln Ave #104",
        "city": "San Jose",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Features crystals, incense, oracle decks, healing sessions. Serene spot for spiritual seekers. Cacao could complement smudging and intention-setting tools.",
        "priority": "High",
        "status": "Research"
    },
    # San Francisco
    {
        "name": "Paxton Gate",
        "address": "824 Valencia St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Curiosity Shop",
        "notes": "Curiosity shop blending natural history with metaphysical items (minerals, taxidermy, oddities). Eclectic bohemian vibe. Potential for cacao as unique regenerative addition.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Infinity Coven",
        "address": "2827 25th St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Witchy boutique with spells, herbs, books, community workshops. Focus on magic and empowerment. Good fit for cacao in consignment for group rituals.",
        "priority": "High",
        "status": "Research"
    },
    # East Bay (Oakland, Berkeley)
    {
        "name": "The Sacred Well",
        "address": "536 Grand Ave",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Magical emporium with crystals, herbs, tarot, classes on spirituality. Community-driven approach. Cacao fitting as life-force enhancer.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "Ancient Future",
        "address": "2903 College Ave",
        "city": "Berkeley",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Global spiritual artifacts, books, wellness products. Nomadic horizon-shifting vibe supports consignment for cacao in settings that evoke impermanence.",
        "priority": "High",
        "status": "Research"
    },
    # Route cities (to be researched)
    {
        "name": "[Research Needed] Stockton Spiritual Shop",
        "address": "[TBD]",
        "city": "Stockton",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Stockton metaphysical' or 'Stockton spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Modesto Health Food",
        "address": "[TBD]",
        "city": "Modesto",
        "state": "CA",
        "type": "Health Food Store",
        "notes": "Search: 'Modesto health food store' or 'Modesto natural foods'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Fresno Metaphysical",
        "address": "[TBD]",
        "city": "Fresno",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Fresno metaphysical shop' or 'Fresno crystal shop'",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Fresno Wellness Center",
        "address": "[TBD]",
        "city": "Fresno",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Search: 'Fresno wellness center' or 'Fresno yoga studio'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Bakersfield Spiritual Shop",
        "address": "[TBD]",
        "city": "Bakersfield",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Bakersfield metaphysical' or 'Bakersfield spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Bakersfield Health Food",
        "address": "[TBD]",
        "city": "Bakersfield",
        "state": "CA",
        "type": "Health Food Store",
        "notes": "Search: 'Bakersfield health food store' or 'Bakersfield natural foods'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Mojave Spiritual Shop",
        "address": "[TBD]",
        "city": "Mojave",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Smaller town - may need to search broader area",
        "priority": "Low",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Barstow Metaphysical",
        "address": "[TBD]",
        "city": "Barstow",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Barstow spiritual store' or check nearby cities",
        "priority": "Low",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Needles Area Shops",
        "address": "[TBD]",
        "city": "Needles",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Near AZ border - check for spiritual/wellness shops",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Kingman Metaphysical",
        "address": "[TBD]",
        "city": "Kingman",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Kingman crystals' or 'Kingman metaphysical shop'",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Kingman Wellness Center",
        "address": "[TBD]",
        "city": "Kingman",
        "state": "AZ",
        "type": "Wellness Center",
        "notes": "Search: 'Kingman yoga studio' or 'Kingman wellness center'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Lake Havasu Metaphysical",
        "address": "[TBD]",
        "city": "Lake Havasu City",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Lake Havasu crystals' or 'Lake Havasu spiritual store'",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Lake Havasu Wellness",
        "address": "[TBD]",
        "city": "Lake Havasu City",
        "state": "AZ",
        "type": "Wellness Center",
        "notes": "Search: 'Lake Havasu yoga studio' or 'Lake Havasu wellness center'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Parker Spiritual Shop",
        "address": "[TBD]",
        "city": "Parker",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Parker AZ metaphysical' or 'Parker spiritual store'",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Quartzsite Gem Show Vendors",
        "address": "Various locations during shows",
        "city": "Quartzsite",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "Famous for gem/mineral shows - target vendors with permanent retail spaces",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "[Research Needed] Quartzsite Metaphysical Shop",
        "address": "[TBD]",
        "city": "Quartzsite",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "notes": "Search: 'Quartzsite crystals' or 'Quartzsite metaphysical' - many shops during show season",
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

def create_shop_list_sheet(client, sheet_name="Hit List"):
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
            cols=13
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
        print("Cleared existing data and added headers")
    except Exception as e:
        print(f"Warning: Could not clear sheet: {e}")
        # Try to add headers if they don't exist
        try:
            existing_headers = worksheet.row_values(1)
            if not existing_headers or len(existing_headers) == 0:
                worksheet.append_row(headers)
        except:
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
            worksheet.append_rows(rows)
            print(f"✅ Added {len(rows)} shops to worksheet")
        except Exception as e:
            print(f"Error in batch update: {e}")
            # Fallback to individual row updates
            for i, row in enumerate(rows):
                try:
                    worksheet.append_row(row)
                except Exception as e2:
                    print(f"Error adding row {i+1}: {e2}")
                    continue
    
    print(f"\n📊 Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={worksheet.id}")

def main():
    """Main execution"""
    print("Generating shop list for SF → Quartzite route...")
    print(f"Target spreadsheet: {SPREADSHEET_ID}")
    
    try:
        # Get Google Sheets client
        client = get_google_sheets_client()
        
        # Create or get worksheet
        worksheet = create_shop_list_sheet(client)
        
        # Add shops
        add_shops_to_sheet(worksheet, SHOPS)
        
        print("\n✅ Success! Shop list added to Google Sheet")
        print("\n📝 Next Steps:")
        print("1. Research actual shops in each city")
        print("2. Update the Google Sheet with real shop names and addresses")
        print("3. Use the search queries from PARTNER_TARGETING_GUIDE.md")
        print("4. Verify each shop's alignment with our values")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure google_credentials.json exists")
        print(f"2. Verify spreadsheet is shared with {SERVICE_ACCOUNT_EMAIL}")
        print(f"3. Check that spreadsheet ID is correct: {SPREADSHEET_ID}")

if __name__ == "__main__":
    main()

