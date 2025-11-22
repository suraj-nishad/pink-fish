# watsonx Orchestrate API Field Reference Guide

## 🎯 Purpose
This guide ensures watsonx Orchestrate agents use the **exact correct field names** when calling your Digital Twin Dashboard APIs. All field names, types, and examples are documented here.

---

## ✅ **CRITICAL: Always Use These Exact Field Names**

### **❌ Common Mistakes to Avoid**
- ❌ Using `zone` instead of `zone_name` in SimulationRequest
- ❌ Using `value change` instead of specific fields like `capacity_increase`
- ❌ Using `value_change` instead of `value_change` (underscore, not space)
- ❌ Misspelling zone names ("Paint shop" vs "Paint Shop")
- ❌ Wrong capitalization ("paint shop" vs "Paint Shop")

---

## 📋 **API Endpoint Reference**

### **1. POST /api/ml/anomaly-detection**

**Purpose**: Detect energy, temperature, and efficiency anomalies using ML

**Request Body**:
```json
{
  "zone": "Paint Shop",          // Optional: specific zone or null for all
  "hours": 24                    // Required: 1-168 hours of data to analyze
}
```

**Field Details**:
| Field | Type | Required | Description | Examples |
|-------|------|----------|-------------|----------|
| `zone` | string \| null | No | Zone name or null for all zones | `"Paint Shop"`, `"Body Shop (BIW)"`, `null` |
| `hours` | integer | No | Hours of data (1-168) | `24`, `48`, `72` |

**Valid Zone Names**:
- ✅ `"Paint Shop"`
- ✅ `"Body Shop (BIW)"`
- ✅ `"Stamping Shop"`
- ✅ `"General Assembly"`
- ✅ `"Powertrain Assembly"`
- ✅ `"Quality Control"`
- ✅ `"Logistics"`

**Response**: Returns anomaly detection results with confidence scores

---

### **2. POST /api/ml/energy-forecast**

**Purpose**: Forecast future energy consumption for a zone

**Request Body**:
```json
{
  "zone": "Paint Shop",          // Required: zone name
  "hours_ahead": 24,             // Required: hours to forecast (1-168)
  "current_temp": 185.0,         // Optional: current temperature °C
  "current_efficiency": 85.0     // Optional: current efficiency %
}
```

**Field Details**:
| Field | Type | Required | Description | Examples |
|-------|------|----------|-------------|----------|
| `zone` | string | **YES** | Zone name to forecast | `"Paint Shop"`, `"Assembly"` |
| `hours_ahead` | integer | No (default: 24) | Hours to forecast (1-168) | `24`, `48`, `168` |
| `current_temp` | float \| null | No | Current temperature in °C | `185.0`, `65.0`, `null` |
| `current_efficiency` | float \| null | No | Current efficiency % | `85.0`, `92.0`, `null` |

**Response**: Returns hourly forecast with energy, cost, and CO₂ predictions

---

### **3. GET /api/ml/predictive-maintenance**

**Purpose**: Get maintenance recommendations for all zones

**Request**: No body (GET request)

**Response**: Returns prioritized maintenance recommendations

---

### **4. POST /api/simulation/run** ⚠️ **MOST COMPLEX**

**Purpose**: Run full digital twin simulation with zone modifications

**Request Body**:
```json
{
  "simulation_name": "Add second Paint Shop line",  // Required: descriptive name
  "modifications": [                                 // Required: array of modifications
    {
      "zone_name": "Paint Shop",                    // ✅ Required: USE "zone_name" NOT "zone"
      "capacity_increase": 50,                      // Optional: percentage (50 = 50% increase)
      "efficiency_modifier": -10,                   // Optional: percentage points (-10 = -10%)
      "energy_multiplier": 1.5,                     // Optional: decimal (1.5 = 50% increase)
      "temperature_offset": -10                     // Optional: degrees Celsius
    }
  ],
  "duration_hours": 720                             // Optional: hours to simulate (default: 24)
}
```

**Field Details for `modifications` array**:
| Field | Type | Required | Description | Examples |
|-------|------|----------|-------------|----------|
| `zone_name` | string | **YES** | ✅ Zone name (exact spelling required) | `"Paint Shop"`, `"Body Shop (BIW)"` |
| `capacity_increase` | float \| null | No | Percentage increase (simple way to add capacity) | `50` (=50%), `100` (=double) |
| `temperature_offset` | float \| null | No | Temperature change in °C (+ or -) | `-10` (reduce 10°C), `5` (increase 5°C) |
| `efficiency_modifier` | float \| null | No | Efficiency change in percentage points | `-10` (=-10%), `5` (=+5%) |
| `energy_multiplier` | float \| null | No | Energy multiplier as decimal | `1.5` (=+50%), `0.8` (=-20%) |
| `add_production_lines` | array \| null | No | Array of ProductionLine objects | See below |
| `remove_line_ids` | array \| null | No | Array of line IDs to remove | `["line-001", "line-002"]` |

**Example Scenarios**:

**Scenario 1: Add Production Line (Simple)**
```json
{
  "simulation_name": "Add second production line to Paint Shop",
  "modifications": [{
    "zone_name": "Paint Shop",
    "capacity_increase": 50
  }],
  "duration_hours": 720
}
```

**Scenario 2: Temperature Reduction**
```json
{
  "simulation_name": "Reduce Paint Shop temperature",
  "modifications": [{
    "zone_name": "Paint Shop",
    "temperature_offset": -10
  }],
  "duration_hours": 168
}
```

**Scenario 3: Multiple Zones**
```json
{
  "simulation_name": "Plant-wide optimization",
  "modifications": [
    {
      "zone_name": "Paint Shop",
      "temperature_offset": -10,
      "energy_multiplier": 0.9
    },
    {
      "zone_name": "Body Shop (BIW)",
      "efficiency_modifier": 5
    }
  ],
  "duration_hours": 720
}
```

**Response**: Returns baseline vs modified comparison with recommendations

---

### **5. POST /api/simulation/what-if**

**Purpose**: Quick what-if analysis for single parameter change

**Request Body**:
```json
{
  "scenario_name": "Reduce Paint Shop Temperature",     // Required: scenario name
  "description": "Test 10°C reduction impact",          // Required: description
  "zone": "Paint Shop",                                  // Required: zone name
  "parameter": "temperature",                            // Required: parameter name
  "value_change": -10                                    // Required: change amount
}
```

**Field Details**:
| Field | Type | Required | Description | Examples |
|-------|------|----------|-------------|----------|
| `scenario_name` | string | **YES** | Name for scenario | `"Reduce Paint Shop Temperature"` |
| `description` | string | **YES** | Detailed description | `"Test impact of reducing oven temperature by 10°C"` |
| `zone` | string | **YES** | Zone name | `"Paint Shop"`, `"Assembly"` |
| `parameter` | string | **YES** | Parameter to change | `"temperature"`, `"energy"`, `"efficiency"` |
| `value_change` | float | **YES** | Amount to change | `-10`, `5`, `-0.2` |

**Valid Parameters**:
- ✅ `"temperature"` - Change in °C
- ✅ `"energy"` - Energy multiplier
- ✅ `"efficiency"` - Efficiency percentage points
- ✅ `"capacity"` - Capacity percentage
- ✅ `"production_rate"` - Production rate change

**Response**: Returns predicted impact, feasibility, risk level, recommendation

---

### **6. POST /api/chatops**

**Purpose**: Natural language query interface

**Request Body**:
```json
{
  "query": "Why is Paint Shop showing red status?",   // Required: natural language query
  "user": "operator_123"                              // Optional: user identifier
}
```

**Field Details**:
| Field | Type | Required | Description | Examples |
|-------|------|----------|-------------|----------|
| `query` | string | **YES** | Natural language question | `"Why is Paint Shop red?"`, `"What zones need maintenance?"` |
| `user` | string | No (default: "operator") | User identifier | `"operator_123"`, `"manager_456"` |

**Example Queries**:
- `"Why is Paint Shop showing red status?"`
- `"What zones need maintenance today?"`
- `"How can we reduce energy costs?"`
- `"Show me energy consumption trends"`
- `"What is the current plant status?"`

**Response**: Returns answer, related actions, confidence score

---

### **7. POST /api/maintenance/schedule**

**Purpose**: Create maintenance ticket

**Request Body**:
```json
{
  "zone": "Paint Shop",                              // Required: zone name
  "issue": "Oven temperature anomaly detected",      // Required: issue description
  "priority": "high"                                 // Required: priority level
}
```

**Field Details**:
| Field | Type | Required | Description | Examples |
|-------|------|----------|-------------|----------|
| `zone` | string | **YES** | Zone requiring maintenance | `"Paint Shop"`, `"Assembly"` |
| `issue` | string | **YES** | Issue description | `"Oven temperature anomaly detected - 3 occurrences"` |
| `priority` | string | **YES** | Priority level | `"low"`, `"medium"`, `"high"` |

**Valid Priority Values**:
- ✅ `"low"` - Minor issues, schedule during regular maintenance
- ✅ `"medium"` - Important issues, schedule within 1 week
- ✅ `"high"` - Critical issues, schedule within 24 hours

**Response**: Returns ticket ID, status, assigned team, due date

---

### **8. POST /api/analyze-energy**

**Purpose**: Analyze energy consumption and get recommendations

**Query Parameters** (not body):
- `zones` - Array of zone names (required)
- `timeframe` - Analysis timeframe (optional, default: "last_24h")

**Example**:
```
POST /api/analyze-energy?zones=Paint%20Shop&zones=Assembly&timeframe=last_24h
```

**Response**: Returns hotspots, recommendations, impact analysis

---

### **9. GET /api/zones/status**

**Purpose**: Get current status of all zones

**Request**: No body (GET request)

**Response**: Returns status, metrics, alerts for all zones

---

## 🎯 **Quick Reference: Required Fields**

### **Always Required**
✅ `zone` in EnergyForecastRequest  
✅ `zone_name` in ZoneModification (NOT "zone")  
✅ `simulation_name` in SimulationRequest  
✅ `modifications` array in SimulationRequest  
✅ `scenario_name`, `description`, `zone`, `parameter`, `value_change` in WhatIfScenario  
✅ `query` in ChatOpsRequest  
✅ `zone`, `issue`, `priority` in MaintenanceRequest  

### **Common Optional Fields**
⚪ `hours` - Default: 24 (1-168)  
⚪ `hours_ahead` - Default: 24 (1-168)  
⚪ `duration_hours` - Default: 24 (1-168)  
⚪ `user` - Default: "operator"  
⚪ `timeframe` - Default: "last_24h"  

---

## 📊 **Valid Values Reference**

### **Zone Names (Exact Spelling)**
```
"Stamping Shop"
"Body Shop (BIW)"          ← Note: includes "(BIW)"
"Paint Shop"
"General Assembly"
"Powertrain Assembly"
"Quality Control"
"Logistics"
```

### **Priority Levels**
```
"low"
"medium"
"high"
```

### **Simulation Parameters**
```
"temperature"      → Temperature in °C
"energy"           → Energy multiplier
"efficiency"       → Efficiency percentage
"capacity"         → Production capacity
"production_rate"  → Units per hour
```

### **Timeframes**
```
"last_1h"
"last_6h"
"last_12h"
"last_24h"         ← Default
"last_48h"
"last_7d"
```

---

## 🔍 **Validation Rules**

### **Hours/Duration**
- Minimum: `1`
- Maximum: `168` (7 days)
- Default: `24`

### **Percentage Values**
- `capacity_increase`: 0-1000 (0% to 1000%)
- `efficiency_modifier`: -50 to +50 (percentage points)

### **Multipliers**
- `energy_multiplier`: 0.1-10.0 (10% to 1000%)

### **Temperature**
- `temperature_offset`: -100 to +100 (°C)

---

## 🚨 **Error Prevention Checklist**

Before making API calls, verify:

✅ Field names exactly match (case-sensitive)  
✅ `zone_name` not `zone` in SimulationRequest  
✅ Zone names have correct spelling and capitalization  
✅ Required fields are present  
✅ Data types are correct (string vs number)  
✅ Values are within valid ranges  
✅ Arrays use square brackets `[]`  
✅ Objects use curly braces `{}`  

---

## 📝 **Example: Full Simulation Request**

```json
{
  "simulation_name": "Q1 2026 Capacity Expansion",
  "modifications": [
    {
      "zone_name": "Paint Shop",
      "capacity_increase": 50,
      "efficiency_modifier": -10,
      "energy_multiplier": 1.5,
      "temperature_offset": 0
    },
    {
      "zone_name": "Body Shop (BIW)",
      "efficiency_modifier": 5,
      "energy_multiplier": 0.95
    },
    {
      "zone_name": "General Assembly",
      "capacity_increase": 30,
      "efficiency_modifier": -5
    }
  ],
  "duration_hours": 720
}
```

**This request**:
- Adds 50% capacity to Paint Shop (reduces efficiency by 10%, increases energy by 50%)
- Improves Body Shop efficiency by 5% (reduces energy by 5%)
- Adds 30% capacity to Assembly (reduces efficiency by 5%)
- Simulates for 30 days (720 hours)

---

## 🎓 **Training Examples for watsonx Orchestrate**

### **User Query**: "What if we add a second paint line?"

**Agent Should Generate**:
```json
{
  "simulation_name": "Add second Paint Shop production line",
  "modifications": [{
    "zone_name": "Paint Shop",
    "capacity_increase": 50
  }],
  "duration_hours": 720
}
```

### **User Query**: "How can we save energy in Paint Shop?"

**Agent Should Call**:
1. `POST /api/analyze-energy?zones=Paint%20Shop`
2. Review recommendations
3. If recommended: `POST /api/simulation/what-if` with temperature reduction

### **User Query**: "Why is Paint Shop red?"

**Agent Should Call**:
1. `POST /api/chatops` with query: `"Why is Paint Shop showing red status?"`
2. OR sequence:
   - `GET /api/zones/status`
   - `POST /api/ml/anomaly-detection` with `{"zone": "Paint Shop"}`

---

## ✅ **Success Criteria**

Your watsonx Orchestrate agent is correctly configured when:

1. ✅ It uses `zone_name` (not `zone`) in SimulationRequest
2. ✅ It uses exact zone name spelling with correct capitalization
3. ✅ It includes all required fields
4. ✅ It uses correct data types (string, number, array)
5. ✅ It provides values within valid ranges
6. ✅ It gets 200 OK responses (not 422 Validation Errors)

---

## 📞 **Support**

- **Live API**: https://pink-fish-production.up.railway.app
- **API Docs**: https://pink-fish-production.up.railway.app/docs
- **OpenAPI Spec**: https://pink-fish-production.up.railway.app/openapi.json
- **GitHub**: https://github.com/suraj-nishad/pink-fish

---

**Last Updated**: 2025-11-22  
**API Version**: 1.0.0  
**Status**: ✅ Production Ready
