"""
Data Cleanup Utility for PlantOps Digital Twin
Manually clean up old data and manage file sizes
"""

import pandas as pd
import os
from datetime import datetime, timedelta

# Path to data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PLANT_DATA_FILE = os.path.join(DATA_DIR, "plant_data_30days.csv")
CURRENT_STATUS_FILE = os.path.join(DATA_DIR, "current_status.csv")

def analyze_data():
    """Analyze current data files"""
    print("📊 Data Analysis")
    print("=" * 60)
    
    if os.path.exists(PLANT_DATA_FILE):
        df = pd.read_csv(PLANT_DATA_FILE, parse_dates=['timestamp'])
        print(f"\n📁 plant_data_30days.csv:")
        print(f"   Total records: {len(df)}")
        print(f"   File size: {os.path.getsize(PLANT_DATA_FILE) / 1024 / 1024:.2f} MB")
        print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print(f"   Zones: {df['zone'].nunique()}")
        
        # Status distribution
        status_counts = df['status'].value_counts()
        print(f"\n   Status Distribution:")
        for status, count in status_counts.items():
            print(f"      {status}: {count} ({count/len(df)*100:.1f}%)")
    else:
        print(f"\n❌ {PLANT_DATA_FILE} not found")
    
    if os.path.exists(CURRENT_STATUS_FILE):
        df_current = pd.read_csv(CURRENT_STATUS_FILE, parse_dates=['timestamp'])
        print(f"\n📁 current_status.csv:")
        print(f"   Total records: {len(df_current)}")
        print(f"   File size: {os.path.getsize(CURRENT_STATUS_FILE) / 1024:.2f} KB")
        print(f"   Date range: {df_current['timestamp'].min()} to {df_current['timestamp'].max()}")
    else:
        print(f"\n❌ {CURRENT_STATUS_FILE} not found")
    
    print("\n" + "=" * 60)

def cleanup_by_record_limit(keep_records=2000):
    """Keep only the most recent N records"""
    print(f"\n🗑️  Cleaning up to keep last {keep_records} records...")
    
    if not os.path.exists(PLANT_DATA_FILE):
        print("❌ Data file not found")
        return
    
    df = pd.read_csv(PLANT_DATA_FILE, parse_dates=['timestamp'])
    original_count = len(df)
    
    if original_count <= keep_records:
        print(f"✅ No cleanup needed. Current: {original_count} records, Limit: {keep_records}")
        return
    
    # Keep most recent records
    df_sorted = df.sort_values('timestamp', ascending=False).head(keep_records)
    df_sorted = df_sorted.sort_values('timestamp', ascending=True)  # Re-sort chronologically
    
    # Backup old file
    backup_file = PLANT_DATA_FILE + ".backup"
    df.to_csv(backup_file, index=False)
    print(f"💾 Backup saved to: {backup_file}")
    
    # Save cleaned data
    df_sorted.to_csv(PLANT_DATA_FILE, index=False)
    
    deleted_count = original_count - len(df_sorted)
    print(f"✅ Deleted {deleted_count} old records")
    print(f"✅ Kept {len(df_sorted)} most recent records")
    
    # Calculate size reduction
    old_size = os.path.getsize(backup_file) / 1024 / 1024
    new_size = os.path.getsize(PLANT_DATA_FILE) / 1024 / 1024
    saved = old_size - new_size
    print(f"💾 File size: {old_size:.2f} MB → {new_size:.2f} MB (saved {saved:.2f} MB)")

def cleanup_by_days(keep_days=7):
    """Keep only data from the last N days"""
    print(f"\n🗑️  Cleaning up to keep last {keep_days} days...")
    
    if not os.path.exists(PLANT_DATA_FILE):
        print("❌ Data file not found")
        return
    
    df = pd.read_csv(PLANT_DATA_FILE, parse_dates=['timestamp'])
    original_count = len(df)
    
    cutoff_date = datetime.now() - timedelta(days=keep_days)
    df_recent = df[df['timestamp'] >= cutoff_date]
    
    if len(df_recent) == original_count:
        print(f"✅ No cleanup needed. All data is within {keep_days} days")
        return
    
    # Backup old file
    backup_file = PLANT_DATA_FILE + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    df.to_csv(backup_file, index=False)
    print(f"💾 Backup saved to: {backup_file}")
    
    # Save cleaned data
    df_recent.to_csv(PLANT_DATA_FILE, index=False)
    
    deleted_count = original_count - len(df_recent)
    print(f"✅ Deleted {deleted_count} records older than {cutoff_date.strftime('%Y-%m-%d')}")
    print(f"✅ Kept {len(df_recent)} records from last {keep_days} days")

def reset_to_fresh_data():
    """Reset and regenerate fresh demo data"""
    print("\n🔄 Resetting to fresh data...")
    
    # Backup existing data
    if os.path.exists(PLANT_DATA_FILE):
        backup_file = PLANT_DATA_FILE + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy(PLANT_DATA_FILE, backup_file)
        print(f"💾 Backup saved to: {backup_file}")
    
    # Run the data generator
    print("\n🎲 Generating fresh 30-day dataset...")
    os.system(f"python {os.path.join(os.path.dirname(__file__), 'generate_month_data.py')}")
    print("\n✅ Fresh data generated")

if __name__ == "__main__":
    import sys
    
    # Show current state
    analyze_data()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--cleanup-records":
            # Keep only last N records (default 2000)
            keep = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
            cleanup_by_record_limit(keep)
            print("\n" + "=" * 60)
            analyze_data()
            
        elif command == "--cleanup-days":
            # Keep only last N days (default 7)
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            cleanup_by_days(days)
            print("\n" + "=" * 60)
            analyze_data()
            
        elif command == "--reset":
            # Reset to fresh data
            confirm = input("\n⚠️  This will replace all data. Continue? (yes/no): ")
            if confirm.lower() == 'yes':
                reset_to_fresh_data()
                analyze_data()
            else:
                print("❌ Reset cancelled")
                
        elif command == "--help":
            print("\n📖 Usage:")
            print("  python cleanup_old_data.py                    # Show analysis")
            print("  python cleanup_old_data.py --cleanup-records [N]  # Keep last N records (default: 2000)")
            print("  python cleanup_old_data.py --cleanup-days [N]     # Keep last N days (default: 7)")
            print("  python cleanup_old_data.py --reset                # Reset to fresh 30-day data")
            print("  python cleanup_old_data.py --help                 # Show this help")
        else:
            print(f"\n❌ Unknown command: {command}")
            print("   Run with --help to see available commands")
    else:
        print("\n💡 Tip: Run with --help to see cleanup options")
