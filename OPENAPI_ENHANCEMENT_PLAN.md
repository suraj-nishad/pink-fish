# OpenAPI Enhancement Plan for watsonx Orchestrate

## 🎯 Goal
Ensure watsonx Orchestrate agents use correct field names by adding detailed examples, descriptions, and constraints to all schemas.

---

## 📊 Current Schema Analysis

### ✅ **GOOD - Already Have Examples/Descriptions:**
1. ✅ `ZoneModification` - Has `capacity_increase` field with description
2. ✅ `AnomalyDetectionRequest` - Has field descriptions
3. ✅ `EnergyForecastRequest` - Has field descriptions
4. ✅ `ProductionLine` - Has field descriptions with defaults

### ⚠️ **NEEDS ENHANCEMENT:**

#### **1. AnomalyDetectionRequest**
- Missing: Example values
- Missing: Zone name enum/examples
- Fix: Add example object

#### **2. EnergyForecastRequest**
- Missing: Example values
- Missing: Zone name enum/examples
- Fix: Add example object

#### **3. ChatOpsRequest**
- Missing: Example queries
- Fix: Add example object with common queries

#### **4. MaintenanceRequest**
- Missing: Example values
- Missing: Priority enum
- Fix: Add example object + enum for priority

#### **5. SimulationRequest** ⚠️ **CRITICAL**
- Missing: Inline request body example
- Fix: Add example in endpoint definition

#### **6. WhatIfScenario**
- Missing: Parameter enum (temperature, efficiency, etc.)
- Missing: Example values
- Fix: Add parameter enum + example

#### **7. ZoneModification** ⚠️ **CRITICAL**
- Has description but missing: 
  - Inline examples
  - Valid zone name enum
  - Parameter interaction rules
- Fix: Add comprehensive example

---

## 🔧 Enhancements to Apply

### **Enhancement 1: Add Zone Name Enum**

Create a reusable enum for valid zone names:
```json
"ZoneName": {
  "type": "string",
  "enum": [
    "Stamping Shop",
    "Body Shop (BIW)",
    "Paint Shop",
    "General Assembly",
    "Powertrain Assembly",
    "Quality Control",
    "Logistics"
  ],
  "description": "Valid manufacturing zone names"
}
```

### **Enhancement 2: Add Priority Enum**

```json
"Priority": {
  "type": "string",
  "enum": ["low", "medium", "high"],
  "description": "Priority level for maintenance requests"
}
```

### **Enhancement 3: Add Parameter Enum**

```json
"SimulationParameter": {
  "type": "string",
  "enum": ["temperature", "energy", "efficiency", "capacity", "production_rate"],
  "description": "Valid parameters for what-if scenarios"
}
```

### **Enhancement 4: Add Examples to All Request Schemas**

#### AnomalyDetectionRequest:
```json
"example": {
  "zone": "Paint Shop",
  "hours": 24
}
```

#### EnergyForecastRequest:
```json
"example": {
  "zone": "Paint Shop",
  "hours_ahead": 24,
  "current_temp": 185.0,
  "current_efficiency": 85.0
}
```

#### ChatOpsRequest:
```json
"example": {
  "query": "Why is Paint Shop showing red status?",
  "user": "operator_123"
}
```

#### MaintenanceRequest:
```json
"example": {
  "zone": "Paint Shop",
  "issue": "Oven temperature anomaly detected",
  "priority": "high"
}
```

#### WhatIfScenario:
```json
"example": {
  "scenario_name": "Reduce Paint Shop Temperature",
  "description": "Test impact of reducing oven temperature by 10 degrees",
  "zone": "Paint Shop",
  "parameter": "temperature",
  "value_change": -10
}
```

#### ZoneModification:
```json
"example": {
  "zone_name": "Paint Shop",
  "capacity_increase": 50,
  "efficiency_modifier": -10,
  "energy_multiplier": 1.5
}
```

### **Enhancement 5: Add Request Body Examples to Endpoints**

All POST/PUT endpoints should have:
```json
"requestBody": {
  "content": {
    "application/json": {
      "schema": { "$ref": "#/components/schemas/SchemaName" },
      "examples": {
        "default": {
          "summary": "Standard request",
          "value": { ... }
        },
        "advanced": {
          "summary": "Complex scenario",
          "value": { ... }
        }
      }
    }
  }
}
```

---

## 📝 Implementation Checklist

### Phase 1: Add Enums
- [ ] ZoneName enum
- [ ] Priority enum  
- [ ] SimulationParameter enum

### Phase 2: Update Request Schemas
- [ ] AnomalyDetectionRequest - Add example
- [ ] EnergyForecastRequest - Add example
- [ ] ChatOpsRequest - Add example + common queries
- [ ] MaintenanceRequest - Add example + priority enum
- [ ] SimulationRequest - Add inline examples
- [ ] WhatIfScenario - Add example + parameter enum
- [ ] ZoneModification - Enhanced example

### Phase 3: Update Endpoints with Examples
- [ ] POST /api/ml/anomaly-detection
- [ ] POST /api/ml/energy-forecast
- [ ] POST /api/simulation/run
- [ ] POST /api/simulation/what-if
- [ ] POST /api/chatops
- [ ] POST /api/maintenance/schedule

### Phase 4: Add Detailed Descriptions
- [ ] All required fields marked clearly
- [ ] Default values documented
- [ ] Min/max constraints explained
- [ ] Field interactions documented

---

## 🎯 Expected Outcome

After enhancements, watsonx Orchestrate agents will:
1. ✅ See valid zone names (no guessing)
2. ✅ Use correct field names (`zone_name` not `zone`)
3. ✅ Understand parameter types and ranges
4. ✅ Follow examples for complex requests
5. ✅ Know which fields are required vs. optional
6. ✅ Understand field interactions (e.g., capacity_increase affects energy)

---

## 🚨 Critical Fields to Highlight

### SimulationRequest
```
REQUIRED: simulation_name (string)
REQUIRED: modifications (array of ZoneModification)
OPTIONAL: duration_hours (integer, 1-168, default: 24)
```

### ZoneModification
```
REQUIRED: zone_name (string) ← USE THIS, NOT "zone"
OPTIONAL: capacity_increase (number) ← Percentage, e.g., 50 = 50% increase
OPTIONAL: temperature_offset (number) ← Degrees Celsius, e.g., -10 = reduce by 10°C
OPTIONAL: efficiency_modifier (number) ← Percentage points, e.g., -5 = -5%
OPTIONAL: energy_multiplier (number) ← Decimal, e.g., 1.5 = 50% increase
```

### Common Mistakes to Prevent
❌ Using `zone` instead of `zone_name`
❌ Using `value change` instead of specific fields
❌ Missing required `zone_name` field
❌ Invalid zone names (typos, wrong capitalization)
❌ Wrong data types (string instead of number)

---

## 📚 Reference: Valid Values

### Zone Names (exact spelling required)
- "Stamping Shop"
- "Body Shop (BIW)"
- "Paint Shop"
- "General Assembly"
- "Powertrain Assembly"
- "Quality Control"
- "Logistics"

### Priority Levels
- "low"
- "medium"
- "high"

### Simulation Parameters
- "temperature" - Temperature in °C
- "energy" - Energy consumption multiplier
- "efficiency" - Efficiency percentage
- "capacity" - Production capacity
- "production_rate" - Units per hour

---

This plan will make the OpenAPI spec self-documenting and AI-agent-friendly! 🚀
