"""
Generate 30 days of manufacturing plant data with realistic patterns
Includes daily/weekly cycles, seasonal variations, and anomalies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Plant zones configuration
ZONES = [
    {"id": "stamping", "name": "Stamping Shop", "base_energy": 450, "base_temp": 65, "base_efficiency": 92},
    {"id": "body_shop", "name": "Body Shop (BIW)", "base_energy": 800, "base_temp": 55, "base_efficiency": 89},
    {"id": "paint", "name": "Paint Shop", "base_energy": 1200, "base_temp": 185, "base_efficiency": 85},
    {"id": "assembly", "name": "General Assembly", "base_energy": 680, "base_temp": 25, "base_efficiency": 88},
    {"id": "powertrain", "name": "Powertrain Assembly", "base_energy": 550, "base_temp": 35, "base_efficiency": 90},
    {"id": "quality", "name": "Quality Control", "base_energy": 320, "base_temp": 22, "base_efficiency": 95},
    {"id": "logistics", "name": "Logistics", "base_energy": 280, "base_temp": 20, "base_efficiency": 93}
]

def calculate_time_factors(hour, day_of_week):
    """Calculate multipliers based on time of day and week"""
    # Daily cycle: higher usage during production hours (6 AM - 10 PM)
    if 6 <= hour < 22:
        daily_factor = 1.0 + 0.3 * np.sin((hour - 6) * np.pi / 16)
    else:
        daily_factor = 0.5 + 0.2 * np.random.random()
    
    # Weekly cycle: lower on weekends
    if day_of_week >= 5:  # Saturday, Sunday
        weekly_factor = 0.6
    else:
        weekly_factor = 1.0
    
    return daily_factor * weekly_factor

def inject_anomalies(data, anomaly_probability=0.05):
    """Inject realistic anomalies into the dataset"""
    anomalies = []
    
    for idx in range(len(data)):
        if np.random.random() < anomaly_probability:
            zone = data.loc[idx, 'zone']
            anomaly_type = np.random.choice(['energy_spike', 'temp_anomaly', 'efficiency_drop'])
            
            if anomaly_type == 'energy_spike':
                data.loc[idx, 'energy_kwh'] *= np.random.uniform(1.3, 1.8)
                data.loc[idx, 'co2_kg'] *= np.random.uniform(1.3, 1.8)
            elif anomaly_type == 'temp_anomaly':
                data.loc[idx, 'temperature_c'] *= np.random.uniform(1.2, 1.5)
            elif anomaly_type == 'efficiency_drop':
                data.loc[idx, 'efficiency_pct'] *= np.random.uniform(0.7, 0.85)
            
            anomalies.append({
                'timestamp': data.loc[idx, 'timestamp'],
                'zone': zone,
                'type': anomaly_type,
                'index': idx
            })
    
    return data, anomalies

def determine_status(row, zone_config):
    """Determine zone status based on metrics"""
    energy_ratio = row['energy_kwh'] / zone_config['base_energy']
    efficiency_ratio = row['efficiency_pct'] / zone_config['base_efficiency']
    
    # Red: Critical conditions
    if energy_ratio > 1.25 or efficiency_ratio < 0.80:
        return 'red'
    # Amber: Warning conditions
    elif energy_ratio > 1.15 or efficiency_ratio < 0.90:
        return 'amber'
    # Green: Normal operations
    else:
        return 'green'

def generate_month_data():
    """Generate 30 days of plant data"""
    start_date = datetime.now() - timedelta(days=30)
    
    all_data = []
    
    # Generate data for each hour of each day
    for day in range(30):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.weekday()
        
        for hour in range(24):
            timestamp = current_date + timedelta(hours=hour)
            time_factor = calculate_time_factors(hour, day_of_week)
            
            for zone in ZONES:
                # Base values with time-based variation
                energy = zone['base_energy'] * time_factor
                temperature = zone['base_temp'] * (0.95 + 0.1 * np.random.random())
                efficiency = zone['base_efficiency'] * (0.95 + 0.05 * np.random.random())
                
                # Add random noise
                energy *= (1 + np.random.normal(0, 0.05))
                temperature *= (1 + np.random.normal(0, 0.03))
                efficiency *= (1 + np.random.normal(0, 0.02))
                
                # Calculate derived metrics
                co2 = energy * 0.233  # kg CO2 per kWh (average grid emissions)
                cost = energy * 0.12  # $ per kWh
                production_units = int(efficiency * time_factor * 10)
                
                all_data.append({
                    'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'zone_id': zone['id'],
                    'zone': zone['name'],
                    'energy_kwh': round(energy, 2),
                    'temperature_c': round(temperature, 2),
                    'efficiency_pct': round(efficiency, 2),
                    'co2_kg': round(co2, 2),
                    'cost_usd': round(cost, 2),
                    'production_units': production_units,
                    'status': 'green'  # Will be updated later
                })
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Inject anomalies
    df, anomalies = inject_anomalies(df, anomaly_probability=0.03)
    
    # Update status based on final metrics
    zone_config_dict = {z['name']: z for z in ZONES}
    df['status'] = df.apply(lambda row: determine_status(row, zone_config_dict[row['zone']]), axis=1)
    
    return df, anomalies

def save_data(df, anomalies):
    """Save generated data to files"""
    # Save full dataset
    df.to_csv('/Users/suraj/digital-twin/data/plant_data_30days.csv', index=False)
    
    # Save current status (last 24 hours)
    df_recent = df.tail(24 * len(ZONES))
    df_recent.to_csv('/Users/suraj/digital-twin/data/current_status.csv', index=False)
    
    # Save anomalies log
    with open('/Users/suraj/digital-twin/data/anomalies_log.json', 'w') as f:
        json.dump(anomalies, f, indent=2)
    
    # Save summary statistics
    summary = {
        'total_records': len(df),
        'date_range': {
            'start': df['timestamp'].min(),
            'end': df['timestamp'].max()
        },
        'zones': len(ZONES),
        'total_anomalies': len(anomalies),
        'anomalies_by_type': {
            'energy_spike': sum(1 for a in anomalies if a['type'] == 'energy_spike'),
            'temp_anomaly': sum(1 for a in anomalies if a['type'] == 'temp_anomaly'),
            'efficiency_drop': sum(1 for a in anomalies if a['type'] == 'efficiency_drop')
        },
        'avg_energy_by_zone': df.groupby('zone')['energy_kwh'].mean().round(2).to_dict(),
        'avg_efficiency_by_zone': df.groupby('zone')['efficiency_pct'].mean().round(2).to_dict(),
        'total_energy_kwh': round(df['energy_kwh'].sum(), 2),
        'total_co2_kg': round(df['co2_kg'].sum(), 2),
        'total_cost_usd': round(df['cost_usd'].sum(), 2)
    }
    
    with open('/Users/suraj/digital-twin/data/summary_stats.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

if __name__ == '__main__':
    df, anomalies = generate_month_data()
    summary = save_data(df, anomalies)
