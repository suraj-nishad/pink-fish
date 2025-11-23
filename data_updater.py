"""
Real-time Data Updater for PlantOps Digital Twin
Generates new plant data every ho    # Calculate derived metrics
    co2_kg = energy_kwh * CO2_FACTOR
    cost_usd = energy_kwh * COST_PER_KWH
    
    # Determine status based on thresholds
    # Adjust baseline for shift (peak shift naturally uses more energy)
    adjusted_baseline = base_energy
    if shift == "peak":
        adjusted_baseline = base_energy * 1.35  # Adjust threshold for peak shift
    elif shift == "night":
        adjusted_baseline = base_energy * 0.75  # Adjust threshold for night shift
    
    energy_deviation = (energy_kwh - adjusted_baseline) / adjusted_baseline if adjusted_baseline > 0 else 0
    efficiency_deviation = (zone["base_efficiency"] - efficiency_pct) / zone["base_efficiency"] if zone["base_efficiency"] > 0 else 0
    
    if energy_deviation > 0.20 or efficiency_deviation > 0.10:
        status = "red"
    elif energy_deviation > 0.10 or efficiency_deviation > 0.05:
        status = "amber"
    else:
        status = "green" to CSV files
Run this script in the background to simulate real-time monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import random

# Path to data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PLANT_DATA_FILE = os.path.join(DATA_DIR, "plant_data_30days.csv")
CURRENT_STATUS_FILE = os.path.join(DATA_DIR, "current_status.csv")

# Zone definitions
ZONES = [
    {"id": "stamping", "name": "Stamping Shop", "base_energy": 300, "base_temp": 65, "base_efficiency": 90},
    {"id": "body_shop", "name": "Body Shop (BIW)", "base_energy": 500, "base_temp": 55, "base_efficiency": 88},
    {"id": "paint", "name": "Paint Shop", "base_energy": 800, "base_temp": 180, "base_efficiency": 85},
    {"id": "assembly", "name": "General Assembly", "base_energy": 450, "base_temp": 25, "base_efficiency": 87},
    {"id": "powertrain", "name": "Powertrain Assembly", "base_energy": 350, "base_temp": 35, "base_efficiency": 89},
    {"id": "quality", "name": "Quality Control", "base_energy": 200, "base_temp": 22, "base_efficiency": 93},
    {"id": "logistics", "name": "Logistics", "base_energy": 180, "base_temp": 20, "base_efficiency": 91}
]

# Configuration
CO2_FACTOR = 0.4  # kg CO2 per kWh
COST_PER_KWH = 0.12  # $ per kWh
UPDATE_INTERVAL = 3600  # seconds (1 hour)
MAX_RECORDS_TO_KEEP = 2000  # Keep only last ~12 days of data (7 zones * 24 hours * 12 days)
ANOMALY_PROBABILITY = 0.08  # 8% chance of anomaly per zone (more realistic)
CRITICAL_ANOMALY_PROBABILITY = 0.08  # 8% chance it's critical when anomaly occurs

def generate_zone_data(zone, timestamp, shift="day", force_anomaly=False):
    """
    Generate realistic data for a zone with higher anomaly probability for demo
    - shift: "day" (normal), "peak" (high production), "night" (low activity)
    - force_anomaly: If True, guarantee at least some issues for demo
    """
    # Base values with some randomness
    base_energy = zone["base_energy"]
    
    # Adjust for shift
    if shift == "peak":
        energy_multiplier = random.uniform(1.2, 1.5)  # Reduced from 1.5-2.0 to avoid all-red status
        production_units = random.randint(800, 1200)
    elif shift == "night":
        energy_multiplier = random.uniform(0.6, 0.9)
        production_units = random.randint(400, 600)
    else:  # day shift
        energy_multiplier = random.uniform(0.9, 1.3)
        production_units = random.randint(450, 550)
    
    # Enhanced anomaly generation (8% chance for realistic mix)
    anomaly_occurred = False
    anomaly_multiplier = 1.0
    
    if force_anomaly or random.random() < ANOMALY_PROBABILITY:
        anomaly_occurred = True
        # Critical anomaly (red status)
        if random.random() < CRITICAL_ANOMALY_PROBABILITY:
            anomaly_multiplier = random.uniform(1.25, 1.45)  # 25-45% spike for critical
        else:
            # Warning anomaly (amber status)
            anomaly_multiplier = random.uniform(1.12, 1.22)  # 12-22% spike for warning
    
    # Apply BOTH shift and anomaly multipliers
    energy_kwh = base_energy * energy_multiplier * anomaly_multiplier
    
    # Temperature with variation
    temperature_c = zone["base_temp"] + random.uniform(-10, 10)
    if anomaly_occurred:
        # Temperature correlates with energy issues
        temperature_c += random.uniform(5, 20)
    
    # Efficiency (inversely related to energy spikes ONLY during anomalies)
    efficiency_pct = zone["base_efficiency"] + random.uniform(-3, 3)  # Smaller variation
    
    if anomaly_occurred:
        efficiency_pct -= random.uniform(3, 8)  # Only reduce efficiency during actual anomalies
    
    efficiency_pct = max(75, min(98, efficiency_pct))  # Raised floor from 70 to 75%
    
    # Calculate derived metrics
    co2_kg = energy_kwh * CO2_FACTOR
    cost_usd = energy_kwh * COST_PER_KWH
    
    # Determine status based on thresholds
    # Adjust baseline for shift (peak shift naturally uses more energy)
    adjusted_baseline = base_energy
    if shift == "peak":
        adjusted_baseline = base_energy * 1.35  # Adjust threshold for peak shift
    elif shift == "night":
        adjusted_baseline = base_energy * 0.75  # Adjust threshold for night shift
    
    energy_deviation = (energy_kwh - adjusted_baseline) / adjusted_baseline  # USE ADJUSTED BASELINE!
    efficiency_deviation = (zone["base_efficiency"] - efficiency_pct) / zone["base_efficiency"]
    
    if energy_deviation > 0.20 or efficiency_deviation > 0.10:
        status = "red"
    elif energy_deviation > 0.10 or efficiency_deviation > 0.05:
        status = "amber"
    else:
        status = "green"
    
    return {
        "timestamp": timestamp,
        "zone_id": zone["id"],
        "zone": zone["name"],
        "energy_kwh": round(energy_kwh, 2),
        "temperature_c": round(temperature_c, 2),
        "efficiency_pct": round(efficiency_pct, 2),
        "co2_kg": round(co2_kg, 2),
        "cost_usd": round(cost_usd, 2),
        "production_units": production_units,
        "status": status
    }

def determine_shift(hour):
    """Determine shift based on hour of day"""
    if 7 <= hour < 15:
        return "day"
    elif 15 <= hour < 23:
        return "peak"  # Evening peak production
    else:
        return "night"

def update_data_files():
    """Generate new data and append to CSV files with automatic cleanup"""
    try:
        # Get current timestamp
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine shift
        shift = determine_shift(now.hour)
        
        print(f"\n{'='*60}")
        print(f"🔄 Updating plant data: {timestamp_str} (Shift: {shift})")
        print(f"{'='*60}")
        
        # Generate data for all zones (let natural anomaly probability handle issues)
        new_records = []
        for idx, zone in enumerate(ZONES):
            record = generate_zone_data(zone, timestamp_str, shift, force_anomaly=False)
            new_records.append(record)
            
            # Print status
            status_emoji = {"green": "🟢", "amber": "🟡", "red": "🔴"}
            print(f"{status_emoji[record['status']]} {record['zone']}: "
                  f"{record['energy_kwh']} kWh | "
                  f"{record['efficiency_pct']}% eff | "
                  f"Status: {record['status']}")
        
        # Convert to DataFrame
        df_new = pd.DataFrame(new_records)
        
        # Append to plant_data_30days.csv
        if os.path.exists(PLANT_DATA_FILE):
            df_new.to_csv(PLANT_DATA_FILE, mode='a', header=False, index=False)
            print(f"✅ Appended {len(new_records)} records to plant_data_30days.csv")
        else:
            df_new.to_csv(PLANT_DATA_FILE, mode='w', header=True, index=False)
            print(f"✅ Created plant_data_30days.csv with {len(new_records)} records")
        
        # AUTOMATIC CLEANUP: Trim plant_data_30days.csv to prevent unlimited growth
        df_all = pd.read_csv(PLANT_DATA_FILE, parse_dates=['timestamp'])
        original_count = len(df_all)
        
        if len(df_all) > MAX_RECORDS_TO_KEEP:
            # Keep only the most recent records
            df_all = df_all.sort_values('timestamp', ascending=False).head(MAX_RECORDS_TO_KEEP)
            df_all = df_all.sort_values('timestamp', ascending=True)  # Re-sort chronologically
            df_all.to_csv(PLANT_DATA_FILE, index=False)
            deleted_count = original_count - len(df_all)
            print(f"🗑️  Auto-cleanup: Deleted {deleted_count} oldest records (kept {MAX_RECORDS_TO_KEEP} most recent)")
            print(f"   File size kept manageable: {len(df_all)} total records")
        else:
            print(f"📊 Current data size: {len(df_all)} records (limit: {MAX_RECORDS_TO_KEEP})")
        
        # Update current_status.csv (replace with latest)
        # Keep last 10 entries per zone (last 10 hours) for better trend visibility
        if os.path.exists(CURRENT_STATUS_FILE):
            df_existing = pd.read_csv(CURRENT_STATUS_FILE)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            
            # Keep only last 10 entries per zone
            df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'])
            df_latest = df_combined.sort_values('timestamp').groupby('zone_id').tail(10)
            
            df_latest.to_csv(CURRENT_STATUS_FILE, index=False)
            print(f"✅ Updated current_status.csv (kept last 10 hours per zone)")
        else:
            df_new.to_csv(CURRENT_STATUS_FILE, mode='w', header=True, index=False)
            print(f"✅ Created current_status.csv")
        
        # Print summary statistics
        status_counts = df_new['status'].value_counts().to_dict()
        print(f"\n📊 Status Summary:")
        print(f"   🟢 Green: {status_counts.get('green', 0)} zones")
        print(f"   🟡 Amber: {status_counts.get('amber', 0)} zones")
        print(f"   � Red: {status_counts.get('red', 0)} zones")
        
        print(f"\n✅ Update complete at {timestamp_str}")
        
    except Exception as e:
        print(f"❌ Error updating data: {e}")
        import traceback
        traceback.print_exc()

def run_continuous_updates():
    """Run continuous updates every hour"""
    print("🚀 PlantOps Real-Time Data Updater Started")
    print(f"⏰ Update interval: {UPDATE_INTERVAL} seconds ({UPDATE_INTERVAL/3600} hours)")
    print(f"📁 Data directory: {DATA_DIR}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            update_data_files()
            
            # Calculate next update time
            next_update = datetime.now() + timedelta(seconds=UPDATE_INTERVAL)
            print(f"\n⏳ Next update at: {next_update.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"💤 Sleeping for {UPDATE_INTERVAL} seconds...\n")
            
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Data updater stopped by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run once for testing
        print("🧪 Running single update (test mode)")
        update_data_files()
    elif len(sys.argv) > 1 and sys.argv[1] == "--interval":
        # Custom interval (in minutes)
        interval_minutes = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        UPDATE_INTERVAL = interval_minutes * 60
        print(f"⚙️  Custom interval: {interval_minutes} minutes")
        run_continuous_updates()
    else:
        # Run continuous updates
        run_continuous_updates()
