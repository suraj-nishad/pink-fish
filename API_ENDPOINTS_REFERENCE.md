# API Endpoints Complete Reference

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-deployment-url.com`

## Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Quick Reference

| Category | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| **Health** | `/` | GET | API health check |
| **Health** | `/health` | GET | Detailed health status |
| **Monitoring** | `/api/zones/status` | GET | Current plant status |
| **Monitoring** | `/api/zones/{zone_id}/history` | GET | Zone historical data |
| **Analytics** | `/api/kpis` | GET | Plant-wide KPIs |
| **Analysis** | `/api/analyze-energy` | POST | Energy analysis |
| **ChatOps** | `/api/chatops` | POST | Natural language queries |
| **Maintenance** | `/api/maintenance/schedule` | POST | Schedule maintenance |
| **Configuration** | `/api/config` | GET/PUT | Analysis thresholds |
| **ML** | `/api/ml/anomaly-detection` | POST | Detect anomalies |
| **ML** | `/api/ml/energy-forecast` | POST | Forecast energy |
| **ML** | `/api/ml/predictive-maintenance` | GET | Maintenance predictions |
| **ML** | `/api/ml/model-info` | GET | Model information |
| **Simulation** | `/api/simulation/run` | POST | Run full simulation |
| **Simulation** | `/api/simulation/what-if` | POST | What-if analysis |
| **Simulation** | `/api/simulation/templates` | GET | Simulation templates |
| **Simulation** | `/api/simulation/simulations` | GET | List simulations |
| **Simulation** | `/api/simulation/simulations/{id}` | GET | Get simulation details |
| **Simulation** | `/api/simulation/zone-config` | GET | Zone configurations |

---

## Core Plant Monitoring

### GET / - Health Check

**Response**:
```json
{
  "status": "online",
  "service": "PlantOps Digital Twin Dashboard",
  "version": "1.0.0",
  "timestamp": "2025-11-22T15:30:00.000Z"
}
```

---

### GET /api/zones/status - Current Plant Status

**Description**: Get real-time status of all manufacturing zones

**Response**:
```json
{
  "zones": [
    {
      "zone_id": "stamping",
      "zone_name": "Stamping Shop",
      "status": "green",
      "metrics": {
        "energy_kwh": 450.5,
        "temperature_c": 65.2,
        "efficiency_pct": 92.3,
        "co2_kg": 105.0,
        "cost_usd": 54.06,
        "production_units": 95
      },
      "alerts": []
    }
  ],
  "last_updated": "2025-11-22T15:30:00Z",
  "plant_status": "operational",
  "total_zones": 7,
  "zones_normal": 5,
  "zones_warning": 1,
  "zones_critical": 1
}
```

**Status Codes**:
- `200` - Success
- `500` - Internal error

---

### GET /api/zones/{zone_id}/history - Zone History

**Description**: Get historical data for a specific zone

**Parameters**:
- `zone_id` (path) - Zone identifier (e.g., "paint", "assembly")
- `hours` (query, optional) - Hours of history (1-168, default: 24)

**Example**: `/api/zones/paint/history?hours=48`

**Response**:
```json
{
  "zone_id": "paint",
  "zone_name": "Paint Shop",
  "hours": 48,
  "data_points": 576,
  "history": [
    {
      "timestamp": "2025-11-22T15:30:00Z",
      "energy_kwh": 1250.5,
      "temperature_c": 185.0,
      "efficiency_pct": 85.5,
      "co2_kg": 291.37,
      "cost_usd": 150.06,
      "status": "amber"
    }
  ]
}
```

---

### GET /api/kpis - Plant-wide KPIs

**Description**: Get aggregated plant metrics

**Parameters**:
- `hours` (query, optional) - Analysis period (default: 24)

**Response**:
```json
{
  "timeframe_hours": 24,
  "kpis": {
    "total_energy_kwh": 142800.0,
    "total_co2_kg": 33272.4,
    "total_cost_usd": 17136.0,
    "avg_efficiency_pct": 88.9,
    "total_production_units": 178416
  },
  "zone_breakdown": {
    "Paint Shop": {
      "energy_kwh": 28800.0,
      "co2_kg": 6710.4,
      "cost_usd": 3456.0
    }
  },
  "timestamp": "2025-11-22T15:30:00Z"
}
```

---

## AI-Powered Analysis

### POST /api/analyze-energy - Energy Analysis

**Description**: Analyze energy consumption and get AI recommendations

**Request Body**:
```json
{
  "zones": ["Paint Shop", "General Assembly"],
  "timeframe": "last_24h"
}
```

**Response**:
```json
{
  "hotspots": ["Paint Shop"],
  "recommendations": [
    {
      "zone": "Paint Shop",
      "action": "Reduce oven temperature by 5°C",
      "priority": "high",
      "estimated_savings": 3600.0,
      "implementation": "Update PLC temperature setpoint"
    }
  ],
  "impact": {
    "cost": 3600.0,
    "co2": 900.0,
    "energy_kwh": 30000.0
  },
  "timestamp": "2025-11-22T15:30:00Z"
}
```

---

### POST /api/chatops - Natural Language Queries

**Description**: Ask questions about plant status in natural language

**Request Body**:
```json
{
  "query": "Why is Paint Shop red?",
  "user": "operator_123"
}
```

**Response**:
```json
{
  "query": "Why is Paint Shop red?",
  "response": "Paint Shop is in critical state due to elevated energy consumption (25% above normal) and oven temperature anomaly detected at 15:30. Recommended action: Reduce oven temperature by 5°C and schedule maintenance.",
  "related_actions": ["schedule_maintenance", "adjust_temperature"],
  "confidence": 0.92
}
```

**Example Queries**:
- "Why is Paint Shop red?"
- "What is the plant status?"
- "Show me Assembly line efficiency"
- "Which zones need maintenance?"

---

### POST /api/maintenance/schedule - Schedule Maintenance

**Description**: Create maintenance ticket

**Request Body**:
```json
{
  "zone": "Paint Shop",
  "issue": "Oven temperature anomaly",
  "priority": "high"
}
```

**Response**:
```json
{
  "ticket_id": "MAINT-1234",
  "status": "created",
  "assigned_to": "Maintenance Team",
  "due_date": "2025-11-23T08:00:00Z"
}
```

---

## Machine Learning Endpoints

### POST /api/ml/anomaly-detection - Detect Anomalies

**Description**: Use ML to detect operational anomalies

**Request Body**:
```json
{
  "zone": "Paint Shop",
  "hours": 48
}
```

**Response**:
```json
{
  "total_records": 576,
  "anomalies_detected": 18,
  "anomaly_rate": 0.0312,
  "results": [
    {
      "timestamp": "2025-11-22T15:30:00Z",
      "zone": "Paint Shop",
      "is_anomaly": true,
      "anomaly_score": -0.234,
      "confidence": 0.87,
      "metrics": {
        "energy_kwh": 1450.0,
        "temperature_c": 195.0,
        "efficiency_pct": 78.0
      }
    }
  ],
  "timestamp": "2025-11-22T15:30:00Z"
}
```

---

### POST /api/ml/energy-forecast - Forecast Energy

**Description**: Predict future energy consumption

**Request Body**:
```json
{
  "zone": "Paint Shop",
  "hours_ahead": 24,
  "current_temp": 185.0,
  "current_efficiency": 85.0
}
```

**Response**:
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
  "confidence_level": "high",
  "timestamp": "2025-11-22T15:30:00Z"
}
```

---

### GET /api/ml/predictive-maintenance - Predictive Maintenance

**Description**: Get maintenance recommendations based on ML analysis

**Response**:
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
  "estimated_total_downtime": 6,
  "timestamp": "2025-11-22T15:30:00Z"
}
```

---

### GET /api/ml/model-info - Model Information

**Description**: Get information about loaded ML models

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
  },
  "timestamp": "2025-11-22T15:30:00Z"
}
```

---

## Digital Twin Simulation

### POST /api/simulation/run - Run Simulation

**Description**: Run complete digital twin simulation

**Request Body**:
```json
{
  "simulation_name": "Add Paint Shop Line 2",
  "modifications": [
    {
      "zone_name": "Paint Shop",
      "temperature_offset": -10,
      "efficiency_modifier": 2.0,
      "energy_multiplier": 1.1,
      "add_production_lines": [
        {
          "line_id": "paint_line_2",
          "name": "Paint Line 2",
          "energy_multiplier": 1.7,
          "efficiency_modifier": -2.0,
          "production_capacity": 50
        }
      ]
    }
  ],
  "duration_hours": 168
}
```

**Response**: See SIMULATION_DOCUMENTATION.md for full response schema

---

### POST /api/simulation/what-if - What-If Analysis

**Description**: Quick analysis of single parameter change

**Request Body**:
```json
{
  "scenario_name": "Reduce Paint Temperature",
  "description": "Test reducing oven temperature by 10°C",
  "zone": "Paint Shop",
  "parameter": "temperature",
  "value_change": -10
}
```

**Response**:
```json
{
  "scenario": {...},
  "predicted_impact": {
    "energy_change_kwh_per_hour": -20.0,
    "cost_change_usd_per_hour": -2.4,
    "co2_change_kg_per_hour": -4.66
  },
  "feasibility": "feasible",
  "risk_level": "low",
  "recommendation": "Safe temperature adjustment"
}
```

---

### GET /api/simulation/templates - Simulation Templates

**Description**: Get pre-configured simulation scenarios

**Response**:
```json
{
  "templates": [
    {
      "name": "Add Paint Shop Production Line",
      "description": "Simulate adding a second production line",
      "modifications": [...]
    }
  ]
}
```

---

### GET /api/simulation/simulations - List Simulations

**Description**: List all stored simulation results

**Response**:
```json
{
  "simulations": [
    {
      "simulation_id": "SIM-20251122143000",
      "name": "Add Paint Shop Line 2",
      "timestamp": "2025-11-22T14:30:00Z",
      "energy_delta_kwh": 42000.0,
      "cost_delta_usd": 5040.0
    }
  ],
  "total_count": 1
}
```

---

### GET /api/simulation/zone-config - Zone Configurations

**Description**: Get base zone parameters

**Response**:
```json
{
  "zones": {
    "Stamping Shop": {
      "base_energy": 450,
      "base_temp": 65,
      "base_efficiency": 92,
      "production_capacity": 100,
      "co2_factor": 0.233
    }
  },
  "total_zones": 7
}
```

---

## Configuration

### GET /api/config - Get Configuration

**Response**:
```json
{
  "ENERGY_THRESHOLD_AMBER": 0.10,
  "ENERGY_THRESHOLD_RED": 0.20,
  "EFFICIENCY_THRESHOLD_AMBER": 0.05,
  "EFFICIENCY_THRESHOLD_RED": 0.10,
  "CO2_FACTOR": 0.4,
  "COST_PER_KWH": 0.12
}
```

---

### PUT /api/config - Update Configuration

**Request Body**: Same as GET response

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes**:
- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Resource not found
- `500` - Internal server error
- `503` - Service unavailable (model not loaded)

---

## Rate Limiting

Currently no rate limiting in development. Production deployment should implement:
- Rate limiting per IP
- API key authentication
- Request throttling

---

## Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Get zone status
curl http://localhost:8000/api/zones/status

# Analyze energy
curl -X POST http://localhost:8000/api/analyze-energy \
  -H "Content-Type: application/json" \
  -d '{"zones": ["Paint Shop"], "timeframe": "last_24h"}'

# Detect anomalies
curl -X POST http://localhost:8000/api/ml/anomaly-detection \
  -H "Content-Type: application/json" \
  -d '{"zone": "Paint Shop", "hours": 24}'

# Forecast energy
curl -X POST http://localhost:8000/api/ml/energy-forecast \
  -H "Content-Type: application/json" \
  -d '{"zone": "Paint Shop", "hours_ahead": 24}'

# What-if analysis
curl -X POST http://localhost:8000/api/simulation/what-if \
  -H "Content-Type: application/json" \
  -d '{"scenario_name": "Test", "zone": "Paint Shop", "parameter": "temperature", "value_change": -10}'
```

---

## Python Client Example

```python
import requests

class PlantOpsClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_zone_status(self):
        return requests.get(f"{self.base_url}/api/zones/status").json()
    
    def detect_anomalies(self, zone, hours=24):
        return requests.post(
            f"{self.base_url}/api/ml/anomaly-detection",
            json={"zone": zone, "hours": hours}
        ).json()
    
    def forecast_energy(self, zone, hours_ahead=24):
        return requests.post(
            f"{self.base_url}/api/ml/energy-forecast",
            json={"zone": zone, "hours_ahead": hours_ahead}
        ).json()

# Usage
client = PlantOpsClient()
status = client.get_zone_status()
print(f"Zones critical: {status['zones_critical']}")
```

---

## WebSocket Support (Future)

Planned for real-time updates:
- `ws://localhost:8000/ws/zones` - Real-time zone status
- `ws://localhost:8000/ws/alerts` - Live alerts stream
- `ws://localhost:8000/ws/kpis` - KPI updates

---

## Authentication (Production)

Recommended for production deployment:
- JWT token authentication
- API key per client
- Role-based access control (RBAC)
- OAuth 2.0 integration

---

## Support

- API Documentation: http://localhost:8000/docs
- GitHub: [Your Repository]
- Email: [Your Contact]
