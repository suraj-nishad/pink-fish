"""
Backfill missing hours of data to eliminate gaps
Run this to fill gaps in the data timeline
"""

import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# Import the data generation logic from data_updater
sys.path.insert(0, os.path.dirname(__file__))
from data_updater import ZONES, generate_zone_data, determine_shift, DATA_DIR, PLANT_DATA_FILE, CURRENT_STATUS_FILE

def backfill_missing_hours():
    """Fill in missing hours in the data timeline"""
    
    print("🔍 Analyzing data for gaps...")
    
    # Read current data
    if not os.path.exists(PLANT_DATA_FILE):
        print("❌ No data file found. Run generate_month_data.py first.")
        return
    
    df = pd.read_csv(PLANT_DATA_FILE, parse_dates=['timestamp'])
    
    # Check for gaps in the data
    df_sorted = df.sort_values('timestamp')
    timestamps = pd.Series(df_sorted['timestamp'].unique()).sort_values().reset_index(drop=True)
    
    # Find gaps larger than 2 hours
    gaps = []
    for i in range(len(timestamps) - 1):
        time_diff = (timestamps[i+1] - timestamps[i]).total_seconds() / 3600
        if time_diff > 2:  # Gap larger than 2 hours
            gaps.append({
                'start': timestamps[i],
                'end': timestamps[i+1],
                'hours': int(time_diff) - 1  # Subtract 1 because we fill the hours between
            })
    
    if not gaps:
        print(f"✅ No significant gaps found. Data is continuous.")
        return
    
    print(f"⚠️  Found {len(gaps)} gap(s) in the data:")
    total_hours_missing = 0
    for idx, gap in enumerate(gaps, 1):
        print(f"   Gap {idx}: {gap['start']} → {gap['end']} ({gap['hours']} hours missing)")
        total_hours_missing += gap['hours']
    
    print(f"\n📊 Total missing: {total_hours_missing} hours")
    
    confirm = input(f"\n🔧 Backfill all {total_hours_missing} hours? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Backfill cancelled")
        return
    
    print(f"\n🚀 Backfilling {total_hours_missing} hours of data...")
    
    # Generate data for each gap
    new_records = []
    
    for gap_idx, gap in enumerate(gaps, 1):
        print(f"\n📝 Filling gap {gap_idx}/{len(gaps)}...")
        current_time = gap['start'] + timedelta(hours=1)
        
        while current_time < gap['end']:
            timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            shift = determine_shift(current_time.hour)
            
            # Generate data for all zones for this hour
            for zone in ZONES:
                record = generate_zone_data(zone, timestamp_str, shift, force_anomaly=False)
                new_records.append(record)
            
            current_time += timedelta(hours=1)
        
        hours_filled = (gap['end'] - gap['start']).total_seconds() / 3600 - 1
        print(f"   ✅ Filled {int(hours_filled)} hours for gap {gap_idx}")
    
    # Convert to DataFrame and merge
    df_new = pd.DataFrame(new_records)
    
    # Backup current file
    backup_file = PLANT_DATA_FILE + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    df.to_csv(backup_file, index=False)
    print(f"\n💾 Backup saved: {backup_file}")
    
    # Append new data
    df_combined = pd.concat([df, df_new], ignore_index=True)
    df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'])  # Ensure datetime type
    df_combined = df_combined.sort_values('timestamp')
    
    # Trim to keep only last 2000 records (auto-cleanup)
    if len(df_combined) > 2000:
        df_combined = df_combined.tail(2000)
        print(f"🗑️  Auto-trimmed to last 2000 records")
    
    df_combined.to_csv(PLANT_DATA_FILE, index=False)
    
    print(f"\n✅ Backfill complete!")
    print(f"   Added {len(new_records)} records ({total_hours_missing} hours × {len(ZONES)} zones)")
    print(f"   New date range: {df_combined['timestamp'].min()} to {df_combined['timestamp'].max()}")
    
    # Update current_status.csv with last 10 hours
    df_latest = df_combined.tail(70)  # 10 hours × 7 zones
    df_latest.to_csv(CURRENT_STATUS_FILE, index=False)
    print(f"✅ Updated current_status.csv with last 10 hours")

if __name__ == "__main__":
    backfill_missing_hours()
