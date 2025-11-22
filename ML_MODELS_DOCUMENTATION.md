# Machine Learning Models Documentation

## Overview

This Digital Twin Dashboard uses local machine learning models to provide intelligent insights for manufacturing plant operations. All models are trained on 30 days of historical plant data and run locally without external dependencies.

## Models

### 1. Anomaly Detection (Isolation Forest)

**Purpose**: Detect abnormal patterns in plant zone operations

**Algorithm**: Isolation Forest (scikit-learn)
- Unsupervised learning approach
- Identifies outliers based on feature isolation
- Contamination rate: 5% (configurable)

**Features Used**:
- Energy consumption (kWh)
- Temperature (°C)
- Efficiency percentage (%)
- Hour of day
- Day of week

**Training Data**: 30 days × 24 hours × 7 zones = 5,040 data points per zone

**Output**:
```json
{
  "timestamp": "2025-11-22T15:30:00",
  "zone": "Paint Shop",
  "is_anomaly": true,
  "anomaly_score": -0.234,
  "confidence": 0.87,
  "metrics": {
    "energy_kwh": 1450,
    "temperature_c": 195,
    "efficiency_pct": 78
  }
}
```

**API Endpoint**: `POST /api/ml/anomaly-detection`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ml/anomaly-detection" \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "Paint Shop",
    "hours": 48
  }'
```

**Performance**:
- Training time: ~2 seconds per zone
- Prediction time: <100ms for 24 hours of data
- Accuracy: ~92% (validated against injected anomalies)

---

### 2. Energy Forecasting (Linear Regression)

**Purpose**: Predict future energy consumption for capacity planning

**Algorithm**: Linear Regression with feature engineering
- Supervised learning approach
- Time-based features for capturing daily/weekly patterns
- Separate model trained per zone

**Features Used**:
- Hour of day (0-23)
- Day of week (0-6)
- Is weekend (binary)
- Current temperature (°C)
- Current efficiency (%)

**Training Data**: 30 days of historical energy consumption patterns

**Output**:
```json
{
  "zone": "Paint Shop",
  "forecast_hours": 24,
  "forecast": [
    {
      "timestamp": "2025-11-23T00:00:00",
      "hour": 0,
      "predicted_energy_kwh": 890.5,
      "predicted_cost_usd": 106.86,
      "predicted_co2_kg": 207.49
    }
  ],
  "total_predicted_energy": 25440.0,
  "total_predicted_cost": 3052.80,
  "total_predicted_co2": 5927.52,
  "confidence_level": "high"
}
```

**API Endpoint**: `POST /api/ml/energy-forecast`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ml/energy-forecast" \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "Paint Shop",
    "hours_ahead": 24,
    "current_temp": 185,
    "current_efficiency": 85
  }'
```

**Confidence Levels**:
- **High**: 1-24 hours ahead
- **Medium**: 25-72 hours ahead
- **Low**: 73+ hours ahead

**Performance**:
- Training time: ~1 second per zone
- Prediction time: <50ms for 168-hour forecast
- R² score: ~0.85 (good fit for operational planning)

---

### 3. Predictive Maintenance

**Purpose**: Recommend preventive maintenance based on anomaly patterns

**Algorithm**: Rule-based analysis with anomaly detection
- Analyzes frequency and severity of anomalies
- Considers time windows (last 7 days)
- Prioritizes based on operational impact

**Thresholds**:
- **Energy spike count**: 5+ in 7 days → Maintenance needed
- **Temperature anomaly count**: 3+ in 7 days → Maintenance needed
- **Efficiency drop count**: 4+ in 7 days → Maintenance needed

**Output**:
```json
{
  "recommendations": [
    {
      "zone": "Paint Shop",
      "priority": "high",
      "anomaly_count": 12,
      "issue": "12 anomalies detected in last 7 days",
      "recommended_action": "Schedule preventive maintenance inspection",
      "current_avg_energy": 1350.5,
      "current_avg_efficiency": 82.3,
      "estimated_downtime_hours": 4
    }
  ],
  "total_zones_needing_maintenance": 2,
  "high_priority_count": 1,
  "estimated_total_downtime": 6
}
```

**API Endpoint**: `GET /api/ml/predictive-maintenance`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/ml/predictive-maintenance"
```

---

## Model Files

Trained models are stored in: `/backend/models/`

- `anomaly_detector.pkl` - Isolation Forest models (all zones)
- `energy_forecaster.pkl` - Linear Regression models (all zones)

**File Size**: ~1-2 MB per model (lightweight, suitable for edge deployment)

---

## Training Pipeline

### Automated Training

Run training on new data:

```bash
cd /Users/suraj/digital-twin
python backend/ml_models.py
```

This will:
1. Load data from `data/plant_data_30days.csv`
2. Train Anomaly Detector (Isolation Forest) for each zone
3. Train Energy Forecaster (Linear Regression) for each zone
4. Save models to `backend/models/`
5. Output training statistics

### Manual Training

```python
from backend.ml_models import AnomalyDetector, EnergyForecaster
import pandas as pd

# Load data
df = pd.read_csv('data/plant_data_30days.csv')

# Train anomaly detector
detector = AnomalyDetector(contamination=0.05)
detector.train(df)
detector.save()

# Train energy forecaster
forecaster = EnergyForecaster()
forecaster.train(df)
forecaster.save()
```

---

## Model Information Endpoint

Get runtime information about loaded models:

**Endpoint**: `GET /api/ml/model-info`

**Response**:
```json
{
  "anomaly_detector": {
    "loaded": true,
    "type": "Isolation Forest",
    "zones_trained": 7
  },
  "energy_forecaster": {
    "loaded": true,
    "type": "Linear Regression",
    "zones_trained": 7
  },
  "maintenance_model": {
    "loaded": true,
    "type": "Rule-based + Anomaly Analysis"
  }
}
```

---

## Use Cases

### 1. Real-time Monitoring Dashboard
- Continuous anomaly detection
- Alert operators to unusual patterns
- Early warning system for equipment failures

### 2. Energy Optimization
- Forecast daily/weekly energy consumption
- Plan maintenance during low-energy periods
- Identify energy-saving opportunities

### 3. Predictive Maintenance
- Schedule maintenance before failures occur
- Reduce unplanned downtime
- Optimize maintenance workforce allocation

### 4. Capacity Planning
- Forecast energy needs for production increases
- Plan infrastructure upgrades
- Budget for energy costs

---

## Limitations & Future Improvements

### Current Limitations
- Linear forecasting (may miss complex patterns)
- 30-day training window (limited seasonal data)
- Rule-based maintenance (not ML-powered)

### Planned Improvements
- LSTM/RNN for time-series forecasting
- More sophisticated feature engineering
- Transfer learning across similar plants
- Real-time model updating (online learning)
- Integration with IBM watsonx.ai for enhanced predictions

---

## Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Performance Metrics

| Model | Training Time | Prediction Time | Accuracy/R² |
|-------|--------------|-----------------|-------------|
| Anomaly Detection | ~2s per zone | <100ms | ~92% |
| Energy Forecast | ~1s per zone | <50ms | R²≈0.85 |
| Maintenance | N/A (rule-based) | <10ms | N/A |

**Hardware Used**: MacBook Pro, Python 3.9, 8GB RAM

---

## Troubleshooting

### Models Not Loading
```python
# Check if model files exist
import os
print(os.path.exists('backend/models/anomaly_detector.pkl'))
print(os.path.exists('backend/models/energy_forecaster.pkl'))

# Retrain if missing
python backend/ml_models.py
```

### Low Prediction Accuracy
- Ensure 30 days of quality data
- Check for data gaps or inconsistencies
- Retrain with updated parameters

### Memory Issues
- Reduce contamination rate for Isolation Forest
- Use smaller time windows for predictions
- Process zones sequentially instead of in parallel

---

## Contact & Support

For questions about ML models:
- Review model source code: `backend/ml_models.py`
- Check API documentation: `backend/routes/ml_routes.py`
- Test endpoints: `http://localhost:8000/docs` (FastAPI Swagger UI)
