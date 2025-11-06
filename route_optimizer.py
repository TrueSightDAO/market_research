#!/usr/bin/env python3
"""
Route Optimizer for Market Research Store Visits
Enhances the itinerary with route optimization suggestions and travel time estimates
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
from generate_shop_list import (
    get_google_sheets_client,
    SPREADSHEET_ID,
    SHOPS
)

# Approximate driving times between major cities (in minutes)
# Based on typical traffic conditions
CITY_DRIVE_TIMES = {
    # Bay Area
    ("San Francisco", "Oakland"): 20,
    ("San Francisco", "Berkeley"): 25,
    ("San Francisco", "San Jose"): 60,
    ("San Francisco", "Palo Alto"): 45,
    ("Oakland", "Berkeley"): 10,
    ("Oakland", "San Jose"): 50,
    ("Berkeley", "San Jose"): 55,
    ("Palo Alto", "San Jose"): 20,
    
    # Central California
    ("San Jose", "Stockton"): 75,
    ("Stockton", "Modesto"): 30,
    ("Modesto", "Fresno"): 90,
    ("Fresno", "Bakersfield"): 110,
    ("Bakersfield", "Mojave"): 60,
    ("Mojave", "Barstow"): 60,
    ("Barstow", "Palm Springs"): 90,
    
    # Coastal California
    ("San Jose", "Monterey"): 60,
    ("Monterey", "Big Sur"): 45,
    ("Big Sur", "San Luis Obispo"): 90,
    ("San Luis Obispo", "Paso Robles"): 30,
    ("Paso Robles", "Santa Barbara"): 120,
    ("Santa Barbara", "Ventura"): 30,
    ("Ventura", "Los Angeles"): 60,
    
    # Southern California
    ("Los Angeles", "Palm Springs"): 120,
    ("Palm Springs", "Indio"): 20,
    ("Indio", "Niland"): 60,
    ("Niland", "Blythe"): 45,
    ("Blythe", "Needles"): 60,
    
    # Arizona
    ("Needles", "Kingman"): 90,
    ("Kingman", "Lake Havasu City"): 60,
    ("Lake Havasu City", "Parker"): 45,
    ("Parker", "Quartzsite"): 30,
}

def get_drive_time(city1, city2):
    """Get estimated drive time between two cities"""
    # Try direct lookup
    key1 = (city1, city2)
    key2 = (city2, city1)
    
    if key1 in CITY_DRIVE_TIMES:
        return CITY_DRIVE_TIMES[key1]
    elif key2 in CITY_DRIVE_TIMES:
        return CITY_DRIVE_TIMES[key2]
    else:
        # Estimate based on distance (rough: 1 mile ≈ 1 minute in city, 0.75 min on highway)
        return None  # Could implement distance-based estimation

def calculate_optimal_route_segment(cities):
    """
    Calculate optimal visit order for a segment of cities
    Uses simple heuristics: prioritize high-priority cities, minimize backtracking
    """
    # This is a simplified version - full TSP would require more complex algorithm
    # For now, we'll use the existing route order but suggest improvements
    
    if len(cities) <= 2:
        return cities
    
    # Group by priority (if we had priority data)
    # For now, return cities in order
    return cities

def enhance_itinerary_with_routing(client):
    """Add route optimization columns to the Itinerary sheet"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet("Itinerary")
    except Exception as e:
        print(f"Error accessing itinerary sheet: {e}")
        return
    
    # Get existing data
    try:
        existing_data = worksheet.get_all_values()
        if not existing_data or len(existing_data) < 2:
            print("No data in itinerary sheet")
            return
        
        headers = existing_data[0]
        
        # Check if routing columns already exist
        if "Drive Time from Prev" in headers:
            print("✅ Routing columns already exist")
            return
        
        # Add new columns
        new_headers = headers + ["Drive Time from Prev", "Est. Total Time", "Visit Order"]
        
        # Update headers
        worksheet.update('A1', [new_headers])
        
        # Calculate drive times and visit order
        rows_to_update = []
        prev_city = None
        prev_region = None
        
        for i, row in enumerate(existing_data[1:], start=2):  # Start from row 2 (after header)
            if len(row) < 3:
                continue
            
            region = row[0] if len(row) > 0 else ""
            city = row[1] if len(row) > 1 else ""
            
            # Calculate drive time from previous city
            drive_time = ""
            if prev_city and prev_region == region:  # Only calculate if same region
                time = get_drive_time(prev_city, city)
                if time:
                    drive_time = f"{time} min"
            
            # Estimate total time (visit + travel)
            # Rough estimate: 30 min per shop + drive time
            shop_count = row[3] if len(row) > 3 else "0"
            try:
                shop_count_int = int(shop_count) if shop_count.isdigit() else 0
            except:
                shop_count_int = 0
            
            visit_time = shop_count_int * 30  # 30 min per shop
            total_time = visit_time + (int(drive_time.split()[0]) if drive_time else 0)
            est_total = f"{total_time} min" if total_time > 0 else "30 min"
            
            # Visit order (simple: 1, 2, 3... within each region)
            visit_order = ""
            if city and region:
                # This is simplified - would need more logic for optimal ordering
                visit_order = "1"  # Placeholder
            
            # Extend row with new data
            new_row = row + [drive_time, est_total, visit_order]
            
            # Update the row
            range_name = f"A{i}:{chr(ord('A') + len(new_row) - 1)}{i}"
            worksheet.update(range_name, [new_row])
            
            prev_city = city if city else prev_city
            prev_region = region if region else prev_region
        
        print("✅ Enhanced itinerary with routing information")
        print("📝 Note: Drive times are estimates. Use Google Maps for actual routing.")
        
    except Exception as e:
        print(f"Error enhancing itinerary: {e}")

def create_route_suggestions(client):
    """Create a new sheet with suggested multi-day routes"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
    except Exception as e:
        print(f"Error accessing spreadsheet: {e}")
        return
    
    sheet_name = "Route Suggestions"
    
    # Try to get existing worksheet or create new
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"Found existing worksheet: {sheet_name}")
        worksheet.clear()
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=100,
            cols=8
        )
        print(f"Created new worksheet: {sheet_name}")
    
    headers = [
        "Trip",
        "Day",
        "Cities",
        "Total Shops",
        "High Priority",
        "Est. Drive Time",
        "Est. Visit Time",
        "Total Time"
    ]
    
    # Define suggested trips
    trips = [
        {
            "trip": "Trip 1: Bay Area Loop",
            "days": [
                {
                    "day": "Day 1",
                    "cities": ["San Francisco", "Oakland", "Berkeley"],
                    "description": "Start in SF, hit East Bay, end in Berkeley"
                },
                {
                    "day": "Day 2",
                    "cities": ["Berkeley", "Palo Alto", "San Jose"],
                    "description": "South Bay route"
                }
            ]
        },
        {
            "trip": "Trip 2: Central Valley + Desert",
            "days": [
                {
                    "day": "Day 1",
                    "cities": ["Stockton", "Modesto", "Fresno"],
                    "description": "I-5 South"
                },
                {
                    "day": "Day 2",
                    "cities": ["Fresno", "Bakersfield", "Mojave"],
                    "description": "Continue south"
                },
                {
                    "day": "Day 3",
                    "cities": ["Mojave", "Barstow", "Palm Springs", "Indio"],
                    "description": "Desert route"
                }
            ]
        },
        {
            "trip": "Trip 3: Coastal Route",
            "days": [
                {
                    "day": "Day 1",
                    "cities": ["Monterey", "Big Sur", "San Luis Obispo"],
                    "description": "Coastal Highway 1"
                },
                {
                    "day": "Day 2",
                    "cities": ["San Luis Obispo", "Paso Robles", "Santa Barbara", "Ventura"],
                    "description": "Continue south"
                }
            ]
        },
        {
            "trip": "Trip 4: LA + Arizona",
            "days": [
                {
                    "day": "Day 1",
                    "cities": ["Los Angeles"],
                    "description": "LA metro area"
                },
                {
                    "day": "Day 2",
                    "cities": ["Los Angeles", "Palm Springs", "Indio"],
                    "description": "Desert transition"
                },
                {
                    "day": "Day 3",
                    "cities": ["Indio", "Niland", "Blythe", "Needles"],
                    "description": "Arizona border"
                },
                {
                    "day": "Day 4",
                    "cities": ["Needles", "Kingman", "Lake Havasu City"],
                    "description": "Arizona route"
                },
                {
                    "day": "Day 5",
                    "cities": ["Lake Havasu City", "Parker", "Quartzsite"],
                    "description": "Final Arizona stops"
                }
            ]
        }
    ]
    
    rows = []
    for trip_data in trips:
        trip_name = trip_data["trip"]
        for day_data in trip_data["days"]:
            cities_str = " → ".join(day_data["cities"])
            # Count shops in these cities (simplified)
            total_shops = 0
            high_priority = 0
            
            for city in day_data["cities"]:
                for shop in SHOPS:
                    if shop.get("city", "").lower() == city.lower():
                        if shop.get("status") not in ["Partnered", "Rejected"]:
                            total_shops += 1
                            if shop.get("priority") == "High":
                                high_priority += 1
            
            # Estimate drive time (simplified)
            est_drive = len(day_data["cities"]) * 45  # Rough estimate
            est_visit = total_shops * 30
            total_time = est_drive + est_visit
            
            rows.append([
                trip_name,
                day_data["day"],
                cities_str,
                total_shops,
                high_priority,
                f"{est_drive} min",
                f"{est_visit} min",
                f"{total_time} min ({total_time // 60}h {total_time % 60}m)"
            ])
    
    # Update sheet
    try:
        worksheet.append_row(headers)
        if rows:
            worksheet.append_rows(rows)
        
        # Format headers
        worksheet.format('A1:H1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        print(f"✅ Created route suggestions")
        print(f"📋 Route suggestions URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={worksheet.id}")
        
    except Exception as e:
        print(f"Error creating route suggestions: {e}")

def main():
    """Main execution"""
    print("🛣️  Route Optimizer for Market Research")
    print("=" * 50)
    
    try:
        client = get_google_sheets_client()
        
        print("\n1️⃣  Enhancing itinerary with routing information...")
        enhance_itinerary_with_routing(client)
        
        print("\n2️⃣  Creating route suggestions...")
        create_route_suggestions(client)
        
        print("\n✅ Route optimization complete!")
        print("\n📝 Next Steps:")
        print("1. Review the 'Route Suggestions' sheet")
        print("2. Use Google Maps to verify actual drive times")
        print("3. Adjust visit order based on store hours and availability")
        print("4. Export to Google My Maps for mobile navigation")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()


