# Digital Twin Simulation Documentation

## Overview

The Digital Twin Simulation feature allows users to experiment with plant configurations in a virtual environment before implementing changes in the real plant. Users can add production lines, modify zone parameters, and predict the operational and financial impact of their decisions.

## Key Capabilities

1. **Add/Remove Production Lines** - Test capacity expansion scenarios
2. **Modify Zone Parameters** - Adjust temperature, efficiency, energy usage
3. **What-If Analysis** - Quick impact predictions for single parameters
4. **Compare Scenarios** - Baseline vs. modified configuration comparison
5. **Financial Impact** - Cost, energy, CO₂, and production forecasts

---

## API Endpoints

### 1. Run Full Simulation

**Endpoint**: `POST /api/simulation/run`

**Purpose**: Run a complete digital twin simulation with multiple modifications

**Request Body**:
```json
{
  "simulation_name": "Add Paint Shop Line 2",
  "modifications": [
    {
      "zone_name": "Paint Shop",
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

**Response**:
```json
{
  "simulation_id": "SIM-20251122143000",
  "simulation_name": "Add Paint Shop Line 2",
  "status": "completed",
  "zones_modified": 1,
  "comparison": {
    "baseline": {
      "total_energy_kwh": 142800,
      "total_cost_usd": 17136.0,
      "total_co2_kg": 33272.4,
      "avg_efficiency_pct": 88.86,
      "total_production_units": 178416
    },
    "modified": {
      "total_energy_kwh": 184800,
      "total_cost_usd": 22176.0,
      "total_co2_kg": 43038.4,
      "avg_efficiency_pct": 87.29,
      "total_production_units": 186816
    },
    "delta": {
      "energy_kwh": 42000.0,
      "cost_usd": 5040.0,
      "co2_kg": 9766.0,
      "efficiency_pct": -1.57,
      "production_units": 8400
    },
    "percent_change": {
      "energy_kwh": 29.41,
      "cost_usd": 29.41,
      "co2_kg": 29.35,
      "efficiency_pct": -1.77,
      "production_units": 4.71
    }
  },
  "zone_details": [...],
  "recommendations": [
    "⚠️ Energy increase: 42000.00 kWh (29.4% increase)",
    "📈 Production increase: 8400 units (4.7% improvement)"
  ],
  "timestamp": "2025-11-22T14:30:00Z"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/simulation/run" \
  -H "Content-Type: application/json" \
  -d @simulation_request.json
```

---

### 2. What-If Analysis

**Endpoint**: `POST /api/simulation/what-if`

**Purpose**: Quick analysis of a single parameter change without full simulation

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
  "scenario": {
    "scenario_name": "Reduce Paint Temperature",
    "description": "Test reducing oven temperature by 10°C",
    "zone": "Paint Shop",
    "parameter": "temperature",
    "value_change": -10
  },
  "predicted_impact": {
    "energy_change_kwh_per_hour": -20.0,
    "cost_change_usd_per_hour": -2.4,
    "co2_change_kg_per_hour": -4.66
  },
  "feasibility": "feasible",
  "risk_level": "low",
  "recommendation": "Safe temperature adjustment - proceed with gradual implementation"
}
```

**Supported Parameters**:
- `temperature` - Temperature offset in °C
- `efficiency` - Efficiency percentage change
- `add_production_line` - Simulate adding a new line

---

### 3. Get Simulation Templates

**Endpoint**: `GET /api/simulation/templates`

**Purpose**: Get pre-configured simulation scenarios for common use cases

**Response**:
```json
{
  "templates": [
    {
      "name": "Add Paint Shop Production Line",
      "description": "Simulate adding a second production line to Paint Shop",
      "modifications": [...]
    },
    {
      "name": "Reduce Paint Shop Temperature",
      "description": "Reduce oven temperature by 10°C for energy savings",
      "modifications": [...]
    },
    {
      "name": "Optimize Assembly Line",
      "description": "Improve assembly efficiency through automation",
      "modifications": [...]
    }
  ]
}
```

**Usage**:
1. Get templates
2. Select desired template
3. Modify parameters if needed
4. Run simulation with template modifications

---

### 4. List Simulations

**Endpoint**: `GET /api/simulation/simulations`

**Purpose**: List all stored simulation results

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

### 5. Get Simulation Details

**Endpoint**: `GET /api/simulation/simulations/{simulation_id}`

**Purpose**: Retrieve detailed results of a specific simulation

**Response**: Complete simulation result with all metrics and comparisons

---

### 6. Get Zone Configurations

**Endpoint**: `GET /api/simulation/zone-config`

**Purpose**: Get base configuration parameters for all plant zones

**Response**:
```json
{
  "zones": {
    "Paint Shop": {
      "base_energy": 1200,
      "base_temp": 185,
      "base_efficiency": 85,
      "production_capacity": 60,
      "co2_factor": 0.233
    },
    ...
  },
  "total_zones": 7
}
```

---

## Modification Types

### 1. Temperature Offset

Adjust zone operating temperature:

```json
{
  "zone_name": "Paint Shop",
  "temperature_offset": -10
}
```

**Effects**:
- Energy consumption changes (especially for temperature-sensitive zones)
- Efficiency may be affected
- Product quality considerations (not modeled)

**Use Cases**:
- Energy optimization
- Seasonal adjustments
- Equipment testing

---

### 2. Efficiency Modifier

Change operational efficiency:

```json
{
  "zone_name": "General Assembly",
  "efficiency_modifier": 5.0
}
```

**Effects**:
- Production output changes
- Energy per unit may improve
- Reflects automation, training, or process improvements

**Use Cases**:
- Lean manufacturing initiatives
- Automation ROI analysis
- Workforce training impact

---

### 3. Energy Multiplier

Scale energy consumption:

```json
{
  "zone_name": "Body Shop (BIW)",
  "energy_multiplier": 1.2
}
```

**Effects**:
- Direct energy usage scaling
- Cost and CO₂ scale proportionally
- Reflects equipment upgrades or degradation

**Use Cases**:
- Equipment replacement scenarios
- Energy audit predictions
- Capacity stress testing

---

### 4. Add Production Line

Add new production capacity:

```json
{
  "zone_name": "Paint Shop",
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
```

**Effects**:
- Increased production capacity
- Higher energy consumption
- May have efficiency trade-offs (ramp-up period)

**Use Cases**:
- Capacity expansion planning
- Capital investment ROI
- Production scaling analysis

---

### 5. Remove Production Line

Remove existing production line:

```json
{
  "zone_name": "Body Shop (BIW)",
  "remove_line_ids": ["robotic_welding_1"]
}
```

**Effects**:
- Reduced capacity
- Lower energy consumption
- Efficiency may improve (focusing resources)

**Use Cases**:
- Decommissioning old equipment
- Maintenance shutdown planning
- Cost reduction scenarios

---

## Example Use Cases

### Use Case 1: Capacity Expansion

**Scenario**: Company wants to increase paint shop production by 30%

**Steps**:
1. Get current paint shop configuration
2. Calculate required additional capacity
3. Design new production line
4. Run simulation with new line
5. Analyze cost, energy, and production impact
6. Make informed investment decision

**Code**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/simulation/run",
    json={
        "simulation_name": "Paint Shop Expansion 30%",
        "modifications": [
            {
                "zone_name": "Paint Shop",
                "add_production_lines": [
                    {
                        "line_id": "paint_expansion_1",
                        "name": "Expansion Line 1",
                        "energy_multiplier": 1.3,
                        "efficiency_modifier": 0,
                        "production_capacity": 20
                    }
                ]
            }
        ],
        "duration_hours": 720  # 30 days
    }
)

result = response.json()
print(f"Production increase: {result['comparison']['delta']['production_units']} units")
print(f"Monthly cost increase: ${result['comparison']['delta']['cost_usd']:.2f}")
```

---

### Use Case 2: Energy Optimization

**Scenario**: Reduce energy costs by 10% without impacting production

**Steps**:
1. Run what-if analysis for each zone
2. Identify low-risk energy reduction opportunities
3. Test combined modifications
4. Verify production targets are met
5. Calculate ROI and payback period

**Code**:
```python
# Test temperature reduction in Paint Shop
response = requests.post(
    "http://localhost:8000/api/simulation/what-if",
    json={
        "scenario_name": "Paint Energy Reduction",
        "description": "Lower oven temp by 5°C",
        "zone": "Paint Shop",
        "parameter": "temperature",
        "value_change": -5
    }
)

impact = response.json()
hourly_savings = abs(impact['predicted_impact']['cost_change_usd_per_hour'])
annual_savings = hourly_savings * 24 * 365
print(f"Estimated annual savings: ${annual_savings:.2f}")
```

---

### Use Case 3: Maintenance Planning

**Scenario**: Plan production line shutdown for maintenance

**Steps**:
1. Remove line from simulation
2. Check if remaining capacity meets demand
3. Calculate lost production
4. Optimize maintenance schedule
5. Minimize business impact

---

### Use Case 4: Sustainability Goals

**Scenario**: Reduce CO₂ emissions by 15% while maintaining production

**Steps**:
1. Baseline current CO₂ emissions
2. Test efficiency improvements
3. Test temperature reductions
4. Combine multiple modifications
5. Find optimal configuration
6. Calculate sustainability metrics

---

## Integration with ML Models

The simulation engine can be enhanced with ML predictions:

1. **Anomaly Detection**: Simulate configurations that minimize anomalies
2. **Energy Forecasting**: Use forecasts to validate simulation accuracy
3. **Predictive Maintenance**: Factor maintenance schedules into simulations

**Future Enhancement**:
```python
# Simulate configuration and predict anomalies
sim_result = run_simulation(modifications)
ml_predictions = anomaly_detector.predict(sim_result['zone_details'])

# Recommend configuration with lowest anomaly probability
```

---

## Limitations & Assumptions

### Current Limitations

1. **Static Models**: Does not account for:
   - Market demand fluctuations
   - Raw material availability
   - Workforce constraints
   - Equipment breakdown probabilities

2. **Linear Relationships**: Assumes:
   - Energy scales linearly with production
   - No diminishing returns
   - No economies of scale

3. **No Quality Modeling**: Does not predict:
   - Product quality impact
   - Defect rates
   - Rework requirements

### Assumptions

- All equipment operates independently
- No supply chain constraints
- Maintenance schedules are flexible
- Workforce is available for new lines
- Energy grid has sufficient capacity

---

## Best Practices

### 1. Start Small
- Begin with what-if analysis
- Validate with single-zone modifications
- Gradually increase complexity

### 2. Validate Results
- Compare with historical data
- Cross-check with engineering estimates
- Test multiple scenarios

### 3. Consider Context
- Regulatory requirements
- Safety constraints
- Operational feasibility
- Change management impact

### 4. Document Decisions
- Save simulation IDs
- Record assumptions
- Track recommendation outcomes

---

## API Client Examples

### Python Client

```python
import requests

class DigitalTwinSimulator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def run_simulation(self, name, modifications, hours=168):
        response = requests.post(
            f"{self.base_url}/api/simulation/run",
            json={
                "simulation_name": name,
                "modifications": modifications,
                "duration_hours": hours
            }
        )
        return response.json()
    
    def what_if(self, scenario_name, zone, parameter, value_change):
        response = requests.post(
            f"{self.base_url}/api/simulation/what-if",
            json={
                "scenario_name": scenario_name,
                "description": f"Test {parameter} change",
                "zone": zone,
                "parameter": parameter,
                "value_change": value_change
            }
        )
        return response.json()

# Usage
simulator = DigitalTwinSimulator()
result = simulator.what_if(
    "Test Temperature",
    "Paint Shop",
    "temperature",
    -10
)
```

### JavaScript Client

```javascript
async function runSimulation(name, modifications, hours = 168) {
  const response = await fetch('http://localhost:8000/api/simulation/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      simulation_name: name,
      modifications: modifications,
      duration_hours: hours
    })
  });
  return await response.json();
}

// Usage
const result = await runSimulation(
  'Expand Paint Shop',
  [{
    zone_name: 'Paint Shop',
    add_production_lines: [{
      line_id: 'paint_2',
      name: 'Paint Line 2',
      energy_multiplier: 1.7,
      efficiency_modifier: -2.0,
      production_capacity: 50
    }]
  }]
);
```

---

## Troubleshooting

### Simulation Returns Unexpected Results
- Check zone names (case-sensitive)
- Verify parameter ranges
- Review modification logic
- Validate input data types

### Performance Issues
- Reduce duration_hours for faster results
- Limit number of modifications
- Use what-if for quick checks

### Zone Not Found
- Use `GET /api/simulation/zone-config` to see available zones
- Check spelling and capitalization
- Refer to zone list in documentation

---

## Future Enhancements

- **Machine Learning Integration**: Predict optimal configurations
- **Multi-Objective Optimization**: Balance cost, emissions, production
- **Risk Analysis**: Monte Carlo simulation for uncertainty
- **Visual Dashboard**: Interactive simulation builder
- **Real-Time Sync**: Compare simulation vs. actual performance

---

## Support

- API Documentation: http://localhost:8000/docs
- Source Code: `backend/routes/simulation_routes.py`
- Templates: `GET /api/simulation/templates`
