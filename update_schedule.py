#!/usr/bin/env python3
import pandas as pd
import hashlib
from datetime import datetime, timedelta

# Load the current schedule
df = pd.read_csv('agroverse_schedule_till_easter.csv')

print('🔧 ADJUSTING START DATE TO 20250928')
print('=' * 60)

# Calculate new start date
new_start_date = datetime(2025, 9, 28)  # September 28th, 2025
print(f'New start date: {new_start_date.strftime("%B %d, %Y")} (20250928)')

# Get current start date for reference
current_start = df['Post Day'].iloc[0]
print(f'Current start: {current_start}')

# Calculate the offset from current start to new start
current_start_date = datetime(2025, 9, 26)  # Current start
days_offset = (new_start_date - current_start_date).days

print(f'Days offset: {days_offset} days')

# Update all dates
for idx, row in df.iterrows():
    current_date_str = row['Post Day']
    
    try:
        current_date = datetime.strptime(str(current_date_str), '%Y%m%d')
        new_date = current_date + timedelta(days=days_offset)
        new_date_str = new_date.strftime('%Y%m%d')
        df.loc[idx, 'Post Day'] = new_date_str
        
        # Update Date Range
        week_num = int(row['Week'].replace('Week ', ''))
        week_start = new_start_date + timedelta(weeks=week_num-1)
        week_end = week_start + timedelta(days=6)
        df.loc[idx, 'Date Range'] = f'{week_start.strftime("%b %d")}-{week_end.strftime("%b %d, %Y")}'
        
    except ValueError as e:
        print(f'Error parsing date {current_date_str}: {e}')
        continue

print(f'\n📱 INTEGRATING EXISTING INSTAGRAM REELS')
print('=' * 60)

# Define the 3 existing reels with enhanced captions and hashtags
existing_reels = [
    {
        'Post Day': '20250928',
        'Post Type': 'Reel',
        'Theme': 'Behind-the-Scenes',
        'Description': 'Vivi takes us on a walk through the cacao farm to show daily farm management. A lot of walking involved!',
        'Caption': 'Vivi took me on a walk through the #cacao farm to show how it is like managing a #cacao farm on a daily basis. It is a lot of walking 🤣\n\n🌱 Experience the daily rhythm of regenerative farming with us! From dawn to dusk, our farmers walk miles to tend each cacao tree with care.\n\n💬 What questions do you have about farm life? Drop them below!\n\n🔗 Discover our sustainable cacao journey at Agroverse.shop',
        'Hashtags': '#cacao #cacaofarm #cacaolife #cacaolove #cacaolovers #beantobar #cacaobeans #sustainablecacao #regenerativefarming #cacaocommunity #farmlife #dailyfarm #cacaofarmer #sustainableagriculture #cacaotree #cacaopod #cacaonatural #cacaoorganico #cacaofino #singleorigin #cacaotraceability #agroverse #cacaocoastbrazil #ilheus #bahia #brazil',
        'CTA': 'What questions do you have about farm life? Drop them below!',
        'Tool Suggestions': 'Instagram Native for scheduling',
        'status': 'SCHEDULED'
    },
    {
        'Post Day': '20250930',
        'Post Type': 'Reel',
        'Theme': 'Behind-the-Scenes',
        'Description': 'Observing the road scale contraption at the local cacao collection center in Ilhéus for accurate measurement of cacao deliveries.',
        'Caption': 'Observed this very interesting contraption where at the local #cacao collection center in #ilheus. The road weighs used helps them quickly and accurately measure the bags of cacao that are being delivered by the local #cacao farmers along the #cacaocoastbrazil\n\n⚖️ Precision meets tradition! This road scale ensures every farmer gets fair compensation for their harvest. Quality control starts right here at the collection center.\n\n💬 Have you ever wondered how cacao gets from farm to your chocolate bar?\n\n🔗 Follow our journey from bean to bar at Agroverse.shop',
        'Hashtags': '#cacao #cacaofarm #cacaolife #cacaolove #cacaolovers #beantobar #cacaobeans #sustainablecacao #regenerativefarming #cacaocommunity #farmlife #cacaofarmer #sustainableagriculture #cacaotree #cacaopod #cacaonatural #cacaoorganico #cacaofino #singleorigin #cacaotraceability #agroverse #cacaocoastbrazil #ilheus #bahia #brazil #qualitycontrol #fairtrade #cacaocollection',
        'CTA': 'Have you ever wondered how cacao gets from farm to your chocolate bar?',
        'Tool Suggestions': 'Instagram Native for scheduling',
        'status': 'SCHEDULED'
    },
    {
        'Post Day': '20251002',
        'Post Type': 'Reel',
        'Theme': 'Behind-the-Scenes',
        'Description': 'Journey to Oscar\'s Farm in Bahia, Brazil, exploring 70-year-old cacao trees and the legacy of fine-flavored cacao selection.',
        'Caption': 'Journey to Oscar\'s Farm in Bahia, Brazil, where cacao is more than a crop—it\'s a legacy! Oscar walked us through his family\'s 70-year-old trees, planted by his grandfather, and shared the art of selecting fine-flavored cacao for Agroverse.shop. From hand-picked pods to premium beans, every step celebrates quality and sustainability. 🍫\n\n🌳 Three generations of wisdom in every tree! Oscar\'s family has been perfecting the art of cacao cultivation for decades.\n\n💬 What\'s your favorite chocolate memory? Share it with us!\n\n🔗 Discover the heart of our cacao at Agroverse.shop and follow us for more stories from the farm!',
        'Hashtags': '#cacao #cacaofarm #cacaolife #cacaolove #cacaolovers #beantobar #cacaobeans #sustainablecacao #regenerativefarming #cacaocommunity #farmlife #cacaofarmer #sustainableagriculture #cacaotree #cacaopod #cacaonatural #cacaoorganico #cacaofino #singleorigin #cacaotraceability #agroverse #cacaocoastbrazil #ilheus #bahia #brazil #oscarsfarm #familylegacy #cacaolegacy #fineflavoredcacao #premiumcacao #handpicked #cacaoselection',
        'CTA': 'What\'s your favorite chocolate memory? Share it with us!',
        'Tool Suggestions': 'Instagram Native for scheduling',
        'status': 'SCHEDULED'
    }
]

# Find and replace the first 3 entries with the existing reels
for i, reel in enumerate(existing_reels):
    if i < len(df):
        df.loc[i, 'Post Day'] = reel['Post Day']
        df.loc[i, 'Post Type'] = reel['Post Type']
        df.loc[i, 'Theme'] = reel['Theme']
        df.loc[i, 'Description'] = reel['Description']
        df.loc[i, 'Caption'] = reel['Caption']
        df.loc[i, 'Hashtags'] = reel['Hashtags']
        df.loc[i, 'CTA'] = reel['CTA']
        df.loc[i, 'Tool Suggestions'] = reel['Tool Suggestions']
        df.loc[i, 'status'] = reel['status']
        print(f'✅ Updated entry {i+1}: {reel["Post Day"]} - {reel["Theme"]}')

# Regenerate primary keys
def generate_primary_key(row):
    date_str = str(row.get('Post Day', ''))
    post_type = str(row.get('Post Type', ''))
    unique_string = f'{date_str}_{post_type}'
    hash_object = hashlib.md5(unique_string.encode())
    return hash_object.hexdigest()[:8]

df['primary_key'] = df.apply(generate_primary_key, axis=1)

# Sort by week number to maintain order
def extract_week_number(week_str):
    try:
        if pd.isna(week_str):
            return 999
        return int(str(week_str).replace('Week ', ''))
    except:
        return 999

df['week_num'] = df['Week'].apply(extract_week_number)
df = df.sort_values(['week_num', 'Post Day']).reset_index(drop=True)
df = df.drop('week_num', axis=1)

# Save the updated schedule
df.to_csv('agroverse_schedule_till_easter.csv', index=False)

print(f'\n✅ Schedule updated successfully!')
print(f'Total entries: {len(df)}')

# Show the first 5 entries
print(f'\n📅 First 5 entries:')
for i, row in df.head(5).iterrows():
    print(f'  {row["Post Day"]} - {row["Post Type"]} - {row["Theme"]} - Status: {row["status"]}')

# Show schedule overview
print(f'\n📊 Schedule Overview:')
print(f'Start: {df["Post Day"].iloc[0]} ({df["Week"].iloc[0]})')
print(f'End: {df["Post Day"].iloc[-1]} ({df["Week"].iloc[-1]})')
print(f'Duration: {len(df.groupby("Week"))} weeks')
