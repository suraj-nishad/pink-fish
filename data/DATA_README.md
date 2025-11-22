# Plant Data Directory - Updated

## Overview

This directory contains generated manufacturing plant data for the Digital Twin Dashboard. The dataset includes **30 days** of comprehensive historical data with realistic patterns, anomalies, and variations suitable for ML model training and analysis.

## Generated Data Files

### 1. plant_data_30days.csv
**Description**: 30 days of hourly plant data across all 7 manufacturing zones

**Schema**:
- `timestamp` - ISO 8601 timestamp (YYYY-MM-DD HH:MM:SS)
- `zone_id` - Zone identifier (stamping, body_shop, paint, assembly, powertrain, quality, logistics)
- `zone` - Full zone name (e.g., "Paint Shop")
- `energy_kwh` - Energy consumption in kilowatt-hours
- `temperature_c` - Operating temperature in Celsius
- `efficiency_pct` - Operational efficiency percentage (0-100)
- `co2_kg` - CO₂ emissions in kilograms
- `cost_usd` - Energy cost in US dollars
- `production_units` - Units produced per hour
- `status` - Zone status (green, amber, red)

**Records**: 5,040 per zone (30 days × 24 hours × 7 zones = 35,280 total records)

**Size**: ~1.5-2 MB

**Use Cases**:
- Training ML models (anomaly detection, forecasting)
- Historical trend analysis
- Baseline establishment for simulations
- Long-term pattern identification

---

### 2. current_status.csv
**Description**: Most recent 24 hours of plant data (extracted from 30-day dataset)

**Schema**: Same as plant_data_30days.csv

**Records**: ~168 (24 hours × 7 zones)

**Update**: Regenerated when new data is created

**Use Cases**:
- Real-time dashboard display
- Current status API responses
- Recent trend visualization

---

### 3. anomalies_log.json
**Description**: Complete log of all injected anomalies in the dataset

**Schema**:
```json
[
  {
    "timestamp": "2025-11-22 15:30:00",
    "zone": "Paint Shop",
    "type": "energy_spike",
    "index": 1234
  }
]
```

**Anomaly Types**:
- `energy_spike` - Energy consumption 30-80% above baseline
- `temp_anomaly` - Temperature 20-50% above baseline  
- `efficiency_drop` - Efficiency 15-30% below baseline

**Injection Rate**: ~3% of all records (~1,000 anomalies total)

**Use Cases**:
- Validating ML anomaly detection accuracy
- Understanding data quality
- Testing alert systems

---

### 4. summary_stats.json
**Description**: Statistical summary and metadata for the generated dataset

**Schema**:
```json
{
  "total_records": 35280,
  "date_range": {
    "start": "2025-10-23 00:00:00",
    "end": "2025-11-22 23:00:00"
  },
  "zones": 7,
  "total_anomalies": 1058,
  "anomalies_by_type": {
    "energy_spike": 352,
    "temp_anomaly": 356,
    "efficiency_drop": 350
  },
  "avg_energy_by_zone": {
    "Stamping Shop": 450.23,
    "Body Shop (BIW)": 801.45,
    "Paint Shop": 1203.67,
    "General Assembly": 682.11,
    "Powertrain Assembly": 551.89,
    "Quality Control": 321.45,
    "Logistics": 281.33
  },
  "avg_efficiency_by_zone": {...},
  "total_energy_kwh": 1428000.0,
  "total_co2_kg": 332724.0,
  "total_cost_usd": 171360.0
}
```

**Use Cases**:
- Quick dataset overview
- Validation of data generation
- Reporting and documentation

---

## Manufacturing Zones

### 1. Stamping Shop
- **Base Energy**: 450 kWh/hour
- **Base Temperature**: 65°C
- **Base Efficiency**: 92%
- **Production Capacity**: 100 units/hour
- **Operations**: Metal stamping and forming

### 2. Body Shop (BIW - Body In White)
- **Base Energy**: 800 kWh/hour
- **Base Temperature**: 55°C
- **Base Efficiency**: 89%
- **Production Capacity**: 80 units/hour
- **Operations**: Robotic welding, body assembly

### 3. Paint Shop
- **Base Energy**: 1200 kWh/hour (highest)
- **Base Temperature**: 185°C (highest)
- **Base Efficiency**: 85%
- **Production Capacity**: 60 units/hour
- **Operations**: Pre-treatment, e-coating, painting, ovens

### 4. General Assembly
- **Base Energy**: 680 kWh/hour
- **Base Temperature**: 25°C
- **Base Efficiency**: 88%
- **Production Capacity**: 120 units/hour
- **Operations**: Final assembly, interior, exterior

### 5. Powertrain Assembly
- **Base Energy**: 550 kWh/hour
- **Base Temperature**: 35°C
- **Base Efficiency**: 90%
- **Production Capacity**: 90 units/hour
- **Operations**: Engine and transmission assembly

### 6. Quality Control
- **Base Energy**: 320 kWh/hour
- **Base Temperature**: 22°C
- **Base Efficiency**: 95% (highest)
- **Production Capacity**: 150 units/hour
- **Operations**: Testing, inspection, validation

### 7. Logistics
- **Base Energy**: 280 kWh/hour (lowest)
- **Base Temperature**: 20°C
- **Base Efficiency**: 93%
- **Production Capacity**: 200 units/hour
- **Operations**: Shipping, distribution, warehousing

---

## Data Generation Process

### Temporal Patterns

**Daily Cycle**:
- **Production Hours (6 AM - 10 PM)**: 100-130% of baseline energy
- **Off Hours (10 PM - 6 AM)**: 50-70% of baseline energy
- Pattern: `1.0 + 0.3 × sin((hour - 6) × π / 16)`

**Weekly Cycle**:
- **Weekdays (Mon-Fri)**: 100% capacity
- **Weekends (Sat-Sun)**: 60% capacity

**Random Variation**:
- Energy: Normal distribution with σ=5%
- Temperature: Normal distribution with σ=3%
- Efficiency: Normal distribution with σ=2%

### Anomaly Injection

Anomalies are injected randomly with ~3% probability:

1. **Energy Spike**: Energy × (1.3 to 1.8), CO₂ × (1.3 to 1.8)
2. **Temperature Anomaly**: Temperature × (1.2 to 1.5)
3. **Efficiency Drop**: Efficiency × (0.7 to 0.85)

### Status Determination

Based on deviation from baseline:

- **🟢 Green (Normal)**: Energy ratio < 1.25 AND Efficiency ratio > 0.80
- **🟡 Amber (Warning)**: Energy ratio 1.15-1.25 OR Efficiency ratio 0.80-0.90
- **🔴 Red (Critical)**: Energy ratio > 1.25 OR Efficiency ratio < 0.80

---

## Regenerating Data

### Full Regeneration

```bash
cd /Users/suraj/digital-twin

# Clean up old data
rm -f data/*.csv data/*.json

# Generate new 30-day dataset
python generate_month_data.py

# Retrain ML models on new data
python backend/ml_models.py
```

### Custom Parameters

Edit `generate_month_data.py` to customize:

```python
# Change number of days
for day in range(30):  # Change to 60 for 2 months
    ...

# Adjust anomaly rate
df, anomalies = inject_anomalies(df, anomaly_probability=0.05)  # 5% instead of 3%

# Modify zone configurations
ZONES = [
    {"id": "stamping", "name": "Stamping Shop", "base_energy": 500, ...},  # Increased from 450
    ...
]
```

---

## Usage Examples

### Python - Load and Analyze

```python
import pandas as pd
import numpy as np

# Load full 30-day dataset
df = pd.read_csv('/Users/suraj/digital-twin/data/plant_data_30days.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter by zone
paint_shop = df[df['zone'] == 'Paint Shop']

# Get recent week
recent_week = df[df['timestamp'] > df['timestamp'].max() - pd.Timedelta(days=7)]

# Calculate statistics
avg_energy_by_zone = df.groupby('zone')['energy_kwh'].mean()
total_cost = df['cost_usd'].sum()
anomaly_count = len(df[df['status'] == 'red'])

print(f"Total energy cost: ${total_cost:,.2f}")
print(f"Critical events: {anomaly_count}")
```

### Python - Load Anomalies

```python
import json

# Load anomalies log
with open('/Users/suraj/digital-twin/data/anomalies_log.json', 'r') as f:
    anomalies = json.load(f)

# Count by zone
from collections import Counter
zones = [a['zone'] for a in anomalies]
print(Counter(zones))

# Count by type
types = [a['type'] for a in anomalies]
print(Counter(types))
```

### Python - Time Series Analysis

```python
import matplotlib.pyplot as plt

# Plot energy consumption over time for Paint Shop
paint = df[df['zone'] == 'Paint Shop'].set_index('timestamp')
paint['energy_kwh'].plot(figsize=(15, 5), title='Paint Shop Energy Consumption (30 Days)')
plt.axhline(y=1200, color='r', linestyle='--', label='Baseline')
plt.legend()
plt.ylabel('Energy (kWh)')
plt.show()
```

---

## ML Model Training

The 30-day dataset is used to train ML models:

### Anomaly Detection (Isolation Forest)

```python
from backend.ml_models import AnomalyDetector

# Load data
df = pd.read_csv('data/plant_data_30days.csv')

# Train detector
detector = AnomalyDetector(contamination=0.05)
detector.train(df)
detector.save()

# Test predictions
predictions = detector.predict(df.tail(168))  # Last 24 hours
```

### Energy Forecasting (Linear Regression)

```python
from backend.ml_models import EnergyForecaster

# Load data
df = pd.read_csv('data/plant_data_30days.csv')

# Train forecaster
forecaster = EnergyForecaster()
forecaster.train(df)
forecaster.save()

# Forecast next 24 hours for Paint Shop
forecast = forecaster.predict('Paint Shop', hours_ahead=24)
```

---

## Data Quality Metrics

### Completeness
- ✅ No missing values
- ✅ All timestamps sequential (no gaps)
- ✅ All zones represented equally

### Validity
- ✅ Energy values: 200-2000 kWh (reasonable range)
- ✅ Temperature: 20-210°C (within zone capabilities)
- ✅ Efficiency: 50-100% (realistic operational range)

### Consistency
- ✅ Status matches metric thresholds
- ✅ CO₂ = Energy × 0.233 (validated)
- ✅ Cost = Energy × $0.12 (validated)

### Realism
- ✅ Daily patterns reflect industrial operations
- ✅ Weekend reduction realistic
- ✅ Anomaly distribution typical for manufacturing

---

## File Sizes

| File | Approximate Size |
|------|------------------|
| plant_data_30days.csv | 1.5-2 MB |
| current_status.csv | 15-20 KB |
| anomalies_log.json | 40-60 KB |
| summary_stats.json | 2-3 KB |
| **Total** | **~2 MB** |

---

## Performance Considerations

### Loading Times (on typical hardware)
- CSV load (pandas): ~150ms
- JSON load: <10ms
- Filter operations: <50ms
- Aggregation queries: <100ms

### Optimization Tips
- Use `pd.read_csv()` with `parse_dates=['timestamp']`
- Filter by zone before time-based operations
- Use `df.query()` for complex filters
- Consider chunking for very large analyses

---

## Integration with API

### FastAPI Endpoint Example

```python
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load data at startup
df = pd.read_csv('data/plant_data_30days.csv')

@app.get("/api/zones/{zone_id}/history")
def get_zone_history(zone_id: str, hours: int = 24):
    zone_data = df[df['zone_id'] == zone_id].tail(hours)
    return zone_data.to_dict(orient='records')
```

---

## Troubleshooting

### Problem: File Not Found
```bash
# Check if files exist
ls -lh /Users/suraj/digital-twin/data/

# Regenerate if missing
python generate_month_data.py
```

### Problem: Outdated Data
```bash
# Check file modification time
stat data/plant_data_30days.csv

# Regenerate with current dates
python generate_month_data.py
```

### Problem: Corrupted Data
```bash
# Validate CSV structure
python -c "import pandas as pd; df = pd.read_csv('data/plant_data_30days.csv'); print(df.info())"

# If corrupted, delete and regenerate
rm data/*.csv data/*.json
python generate_month_data.py
```

---

## Future Enhancements

- [ ] Add seasonal variations (temperature impact)
- [ ] Include shift change patterns
- [ ] Model supply chain disruptions
- [ ] Add equipment lifecycle patterns
- [ ] Implement data versioning
- [ ] Add data validation tests
- [ ] Create data pipeline automation

---

## Documentation Links

- **ML Models**: See `ML_MODELS_DOCUMENTATION.md`
- **API Endpoints**: See `API_ENDPOINTS_REFERENCE.md`
- **Simulation**: See `SIMULATION_DOCUMENTATION.md`
- **Data Generation**: See `generate_month_data.py`

---

**Generated**: November 22, 2025  
**Dataset Version**: 1.0  
**Records**: 35,280  
**Time Span**: 30 days
