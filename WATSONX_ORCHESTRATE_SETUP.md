# IBM watsonx Orchestrate Integration Guide

## 🎯 Overview

This guide explains how to integrate your Digital Twin Dashboard APIs with IBM watsonx Orchestrate to create intelligent AI agents that automate plant operations monitoring, energy optimization, and predictive maintenance.

---

## 📋 Prerequisites

1. **IBM watsonx Orchestrate account** (trial or enterprise)
2. **Your deployed API**: `https://pink-fish-production.up.railway.app`
3. **OpenAPI specification file**: `openapi.json` (in project root)

---

## 🚀 Quick Start: Import APIs as Skills

### Step 1: Access watsonx Orchestrate

1. Log into [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate)
2. Navigate to **Skills** → **Import Skills**

### Step 2: Import OpenAPI Specification

**Option A: Direct URL Import**
```
https://raw.githubusercontent.com/suraj-nishad/pink-fish/main/openapi.json
```

**Option B: File Upload**
- Download `openapi.json` from your repository
- Click **Upload OpenAPI File**
- Select `openapi.json`

### Step 3: Verify API Connection

watsonx Orchestrate will automatically:
- Parse your 18 API endpoints
- Detect the production server URL: `https://pink-fish-production.up.railway.app`
- Create skills for each endpoint
- Validate schemas and examples

---

## 🤖 Agent Architecture

### **Hierarchical Agent Structure**

```
👤 USER
  ↓
🤖 PlantOps Orchestrator (Main Agent)
  ↓
├─→ Status Monitoring Agent
├─→ Anomaly Detection Agent
├─→ Energy Intelligence Agent
├─→ Maintenance Agent
└─→ Simulation Agent
```

---

## 🔧 Agent Configuration

### **1. PlantOps Orchestrator (Main Agent)**

**Role**: Primary conversational interface for users

**Skills to Connect**:
- `chatops_query` - Natural language understanding
- `get_zones_status` - Status overview
- `health_check` - System health

**Behavior Configuration**:
```yaml
name: "PlantOps Orchestrator"
type: conversational_ai
description: "I'm your Digital Twin assistant. Ask me about plant status, energy usage, maintenance needs, or run what-if simulations."

intent_routing:
  - intent: "status_check"
    keywords: ["status", "how is", "show me", "overview"]
    delegate_to: "Status Monitoring Agent"
  
  - intent: "troubleshooting"
    keywords: ["why", "problem", "red", "critical", "anomaly"]
    delegate_to: "Anomaly Detection Agent"
  
  - intent: "optimization"
    keywords: ["energy", "optimize", "reduce cost", "savings"]
    delegate_to: "Energy Intelligence Agent"
  
  - intent: "maintenance"
    keywords: ["maintenance", "schedule", "fix", "repair"]
    delegate_to: "Maintenance Agent"
  
  - intent: "simulation"
    keywords: ["what if", "simulate", "add line", "test scenario"]
    delegate_to: "Simulation Agent"

conversational_memory: true
context_retention_hours: 24
```

**Sample Queries**:
- "How is Paint Shop doing?"
- "Why is Paint Shop showing red status?"
- "What zones need maintenance?"
- "What if we add a second production line in Paint Shop?"

---

### **2. Status Monitoring Agent**

**Skills Required**:
- `get_zones_status` (Primary)
- `health_check` (Validation)
- `get_plant_kpis` (Aggregation)

**Configuration**:
```yaml
name: "Status Monitoring Agent"
description: "Provides real-time zone health, metrics, and alerts"
parent: "PlantOps Orchestrator"

triggers:
  - parent_query_contains: ["status", "how is", "overview"]
  - scheduled: "every 30 minutes"

response_format:
  - include: ["zone_name", "status", "energy_kwh", "efficiency_pct"]
  - highlight_critical: true
  - suggest_actions: true
```

**Example Response**:
```
🔴 Paint Shop: CRITICAL
  Energy: 1,250 kWh (25% above normal)
  Efficiency: 78%
  Alert: Temperature anomaly detected
  
🟢 Assembly: NORMAL
  Energy: 680 kWh
  Efficiency: 88%
```

---

### **3. Anomaly Detection Agent**

**Skills Required**:
- `detect_anomalies_endpoint` (Primary)
- `predictive_maintenance_endpoint` (Auto-trigger)
- `get_zones_status` (Context)

**Configuration**:
```yaml
name: "Anomaly Detection Agent"
description: "ML-powered anomaly detection and root cause analysis"
parent: "PlantOps Orchestrator"

triggers:
  - parent_query_contains: ["why", "problem", "anomaly"]
  - auto_trigger_when:
      - zone_status == "red"
      - energy_deviation > 20%

ml_model: "Isolation Forest"
confidence_threshold: 0.85

auto_escalation:
  - if_severity: "high"
    then_call: "Maintenance Agent"
    params:
      priority: "high"
      issue: "{{anomaly_description}}"
```

**API Call Example**:
```json
POST /api/ml/anomaly-detection
{
  "zone": "Paint Shop",
  "hours": 24
}
```

**Agent Actions**:
1. Detects anomalies using ML model
2. If anomaly_rate > 10% → Escalate to Maintenance Agent
3. Send Slack notification
4. Log to monitoring system

---

### **4. Energy Intelligence Agent**

**Skills Required**:
- `analyze_energy` (Primary)
- `forecast_energy_endpoint` (Forecasting)
- `what_if_analysis` (Validation)

**Configuration**:
```yaml
name: "Energy Intelligence Agent"
description: "Energy optimization and cost reduction recommendations"
parent: "PlantOps Orchestrator"

triggers:
  - parent_query_contains: ["energy", "cost", "optimize", "savings"]
  - scheduled: "every 6 hours"

analysis_parameters:
  timeframe: "last_24h"
  zones: "all"
  forecast_hours: 48

auto_simulation:
  enabled: true
  trigger_threshold_usd: 500  # If savings > $500/day, auto-validate
  delegate_to: "Simulation Agent"
```

**Workflow**:
1. User asks: "How can we reduce energy costs?"
2. Agent calls: `POST /api/analyze-energy`
3. Receives recommendation: "Reduce Paint Shop temp by 10°C → Save $28/day"
4. Auto-triggers: Simulation Agent to validate
5. If simulation confirms → Present recommendation to user

---

### **5. Maintenance Agent**

**Skills Required**:
- `predictive_maintenance_endpoint` (Primary)
- `schedule_maintenance` (Action)
- `get_zones_status` (Context)

**Configuration**:
```yaml
name: "Maintenance Agent"
description: "Predictive maintenance scheduling and coordination"
parent: "PlantOps Orchestrator"

triggers:
  - parent_query_contains: ["maintenance", "schedule", "fix"]
  - called_by: "Anomaly Detection Agent"
  - scheduled: "daily at 8 AM"

priority_rules:
  high:
    - anomaly_count >= 3
    - zone_status == "red"
    - efficiency < 75%
  medium:
    - anomaly_count >= 2
    - efficiency < 85%
  low:
    - anomaly_count == 1

integrations:
  - jira:
      enabled: true
      project: "PLANT-MAINTENANCE"
      assignee: "maintenance_team"
  - slack:
      channel: "#plant-alerts"
      mention: "@maintenance-team"
```

**Maintenance Workflow**:
```
1. Receive high-priority anomaly from Anomaly Agent
   ↓
2. Call: GET /api/ml/predictive-maintenance
   ↓
3. Evaluate: Priority = HIGH (12 anomalies detected)
   ↓
4. Call: POST /api/maintenance/schedule
   {
     "zone": "Paint Shop",
     "issue": "Oven temperature anomaly - 3 occurrences",
     "priority": "high"
   }
   ↓
5. Create Jira ticket: MAINT-1234
   ↓
6. Send Slack alert: "@maintenance-team Urgent: Paint Shop needs maintenance"
   ↓
7. Respond to user: "Maintenance ticket MAINT-1234 created and scheduled for tomorrow 8 AM"
```

---

### **6. Simulation Agent**

**Skills Required**:
- `run_simulation` (Primary)
- `what_if_analysis` (Quick scenarios)
- `get_simulation_templates` (Pre-built scenarios)

**Configuration**:
```yaml
name: "Simulation Agent"
description: "Digital twin what-if scenario testing"
parent: "PlantOps Orchestrator"

triggers:
  - parent_query_contains: ["what if", "simulate", "test", "add line"]
  - called_by: "Energy Intelligence Agent"

simulation_defaults:
  duration_hours: 720  # 30 days
  baseline: "30-day historical average"

scenario_templates:
  - name: "Add Production Line"
    modifications:
      - capacity_increase: 50
      - efficiency_modifier: -10
      - energy_multiplier: 1.5
  
  - name: "Temperature Reduction"
    modifications:
      - temperature_offset: -10
      - energy_multiplier: 0.8
  
  - name: "Efficiency Improvement"
    modifications:
      - efficiency_modifier: 5
      - energy_multiplier: 0.95
```

**Simulation Request Format** (IMPORTANT for watsonx):
```json
POST /api/simulation/run
{
  "simulation_name": "Add second production line to Paint Shop",
  "modifications": [
    {
      "zone_name": "Paint Shop",
      "capacity_increase": 50,
      "efficiency_modifier": -10,
      "energy_multiplier": 1.5
    }
  ],
  "duration_hours": 720
}
```

**Key Points**:
- ✅ Use `zone_name` (NOT `zone`)
- ✅ Use `capacity_increase` for adding production capacity (percentage)
- ✅ Use `energy_multiplier` for energy changes (1.5 = 50% increase)
- ✅ Use `efficiency_modifier` for efficiency changes (-10 = -10% efficiency)

---

## 🔄 Multi-Agent Workflow Examples

### **Example 1: Proactive Anomaly Response**

```
USER: "Why is Paint Shop red?"

PlantOps Orchestrator:
  ├─ Identifies intent: Troubleshooting
  ├─ Delegates to: Status Monitoring Agent
  │   └─ Calls: GET /api/zones/status
  │   └─ Returns: "Paint Shop RED, energy spike"
  │
  ├─ Delegates to: Anomaly Detection Agent
  │   └─ Calls: POST /api/ml/anomaly-detection {"zone": "Paint Shop"}
  │   └─ Returns: "3 anomalies, oven temp issue, HIGH severity"
  │   │
  │   └─ Auto-triggers: Maintenance Agent
  │       └─ Calls: POST /api/maintenance/schedule
  │       └─ Creates: Ticket MAINT-1234
  │
  └─ Responds to user:
      "🔴 Paint Shop has oven temperature anomalies (3 occurrences).
       High-priority maintenance ticket MAINT-1234 created.
       Scheduled for tomorrow 8 AM.
       
       Would you like me to simulate temperature reduction in the meantime?"
```

---

### **Example 2: Energy Optimization with Validation**

```
USER: "How can we save energy in Paint Shop?"

PlantOps Orchestrator:
  ├─ Identifies intent: Optimization
  ├─ Delegates to: Energy Intelligence Agent
  │   └─ Calls: POST /api/analyze-energy {"zones": ["Paint Shop"]}
  │   └─ Returns: "Reduce temp by 10°C → Save $28.80/day"
  │   │
  │   └─ Auto-triggers: Simulation Agent (savings > threshold)
  │       └─ Calls: POST /api/simulation/what-if
  │       └─ Returns: "-240 kWh/day, -$28.80/day, 87% confidence"
  │
  └─ Responds to user:
      "💡 Optimization Opportunity:
       
       Recommendation: Reduce oven temp by 10°C
       
       Validated Impact:
       • Energy: -240 kWh/day (-20%)
       • Cost: -$28.80/day ($864/month)
       • CO₂: -60 kg/day
       • Efficiency: -2% (minimal)
       • Confidence: 87%
       
       ✅ PROCEED recommended
       
       Should I implement this change? (Reply 'yes' to approve)"
```

---

### **Example 3: Complex Simulation**

```
USER: "What if we add a second paint line?"

PlantOps Orchestrator:
  ├─ Identifies intent: Simulation (complex)
  ├─ Delegates to: Simulation Agent
  │   └─ Calls: POST /api/simulation/run
  │       Request:
  │       {
  │         "simulation_name": "Add Paint Shop Line 2",
  │         "modifications": [{
  │           "zone_name": "Paint Shop",
  │           "capacity_increase": 50,
  │           "efficiency_modifier": -10,
  │           "energy_multiplier": 1.5
  │         }],
  │         "duration_hours": 720
  │       }
  │   └─ Returns: Detailed 30-day projection
  │
  └─ Responds to user:
      "🔬 Simulation: Add Paint Shop Line 2
       
       30-Day Impact:
       • Production: +50% capacity
       • Energy: +1,800 kWh/day (+50%)
       • Cost: +$216/day ($6,480/month)
       • Efficiency: -10% (initial ramp-up)
       
       ⚠️ Cost per additional unit: $4.32
       Break-even: 1,500 units/month
       
       Would you like me to:
       1. Simulate optimization to reduce energy impact?
       2. Schedule maintenance prep?
       3. Generate business case report?"
```

---

## 📊 Endpoint-to-Agent Mapping

| Endpoint | Primary Agent | Secondary Agents | Auto-Trigger Conditions |
|----------|---------------|------------------|-------------------------|
| `/api/zones/status` | Status Monitoring | All agents | Every 30 min |
| `/api/ml/anomaly-detection` | Anomaly Detection | - | zone_status == "red" |
| `/api/ml/energy-forecast` | Energy Intelligence | - | Every 6 hours |
| `/api/ml/predictive-maintenance` | Maintenance | Anomaly Detection | anomaly_rate > 10% |
| `/api/analyze-energy` | Energy Intelligence | Simulation | User query |
| `/api/simulation/run` | Simulation | - | savings > $500/day |
| `/api/simulation/what-if` | Simulation | Energy Intelligence | Validation needed |
| `/api/maintenance/schedule` | Maintenance | - | severity == "high" |
| `/api/chatops` | PlantOps Orchestrator | - | All user messages |

---

## 🎯 watsonx Orchestrate Setup Checklist

### ✅ Phase 1: Import Skills (15 minutes)

- [ ] Import `openapi.json` into watsonx Orchestrate
- [ ] Verify production URL: `https://pink-fish-production.up.railway.app`
- [ ] Test individual skills:
  - [ ] `get_zones_status`
  - [ ] `detect_anomalies_endpoint`
  - [ ] `run_simulation`
  - [ ] `chatops_query`

### ✅ Phase 2: Create Main Agent (30 minutes)

- [ ] Create "PlantOps Orchestrator" conversational AI agent
- [ ] Configure intent routing (status, troubleshooting, optimization, maintenance, simulation)
- [ ] Connect to `chatops_query` skill
- [ ] Enable conversation memory (24-hour retention)
- [ ] Test sample queries:
  - [ ] "How is the plant?"
  - [ ] "Show me Paint Shop status"

### ✅ Phase 3: Create Sub-Agents (1 hour)

- [ ] **Status Monitoring Agent**
  - [ ] Connect skills: `get_zones_status`, `health_check`
  - [ ] Configure scheduled trigger (every 30 min)
  
- [ ] **Anomaly Detection Agent**
  - [ ] Connect skills: `detect_anomalies_endpoint`, `predictive_maintenance_endpoint`
  - [ ] Configure auto-escalation to Maintenance Agent
  - [ ] Set severity threshold: anomaly_rate > 10%
  
- [ ] **Energy Intelligence Agent**
  - [ ] Connect skills: `analyze_energy`, `forecast_energy_endpoint`
  - [ ] Configure scheduled trigger (every 6 hours)
  - [ ] Enable auto-simulation for high-impact recommendations
  
- [ ] **Maintenance Agent**
  - [ ] Connect skills: `predictive_maintenance_endpoint`, `schedule_maintenance`
  - [ ] Configure Jira integration (optional)
  - [ ] Configure Slack notifications (optional)
  
- [ ] **Simulation Agent**
  - [ ] Connect skills: `run_simulation`, `what_if_analysis`, `get_simulation_templates`
  - [ ] Load scenario templates

### ✅ Phase 4: Agent Connections (30 minutes)

- [ ] Link Main Agent → All Sub-Agents
- [ ] Link Anomaly Agent → Maintenance Agent (auto-escalation)
- [ ] Link Energy Agent → Simulation Agent (validation)
- [ ] Link Simulation Agent → Energy Agent (optimization feedback)

### ✅ Phase 5: Testing (1 hour)

- [ ] Test status queries
- [ ] Test anomaly detection workflow
- [ ] Test energy optimization with simulation
- [ ] Test maintenance scheduling
- [ ] Test complex multi-agent scenarios

### ✅ Phase 6: Production Readiness (30 minutes)

- [ ] Configure notification channels (Slack/Teams)
- [ ] Set up scheduled jobs (status checks, energy analysis)
- [ ] Enable audit logging
- [ ] Configure human-in-the-loop approvals for:
  - [ ] High-cost decisions (> $500 impact)
  - [ ] Critical zone changes
  - [ ] Maintenance scheduling

---

## 🔐 Authentication (Optional)

If you need to secure your APIs:

1. **Add API Key Authentication**:
```python
# backend/app.py
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY", "your-secure-key")
api_key_header = APIKeyHeader(name="X-API-Key")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            return JSONResponse(status_code=403, content={"detail": "Invalid API key"})
    return await call_next(request)
```

2. **Configure in watsonx Orchestrate**:
   - Go to Skill Settings → Authentication
   - Select "API Key (Header)"
   - Header name: `X-API-Key`
   - Value: Your API key

---

## 📚 Additional Resources

- **Live API**: https://pink-fish-production.up.railway.app
- **API Documentation**: https://pink-fish-production.up.railway.app/docs
- **OpenAPI Spec**: https://pink-fish-production.up.railway.app/openapi.json
- **GitHub Repository**: https://github.com/suraj-nishad/pink-fish

---

## 🐛 Troubleshooting

### Issue: "Connection refused to 127.0.0.1:8000"

**Solution**: OpenAPI spec has wrong server URL

1. Verify `openapi.json` has production URL first:
```json
"servers": [
  {"url": "https://pink-fish-production.up.railway.app", "description": "Production"},
  {"url": "http://127.0.0.1:8000", "description": "Local"}
]
```

2. Re-import OpenAPI spec in watsonx Orchestrate

### Issue: "Field required: zone_name"

**Solution**: Agent using wrong field names

Make sure simulation requests use:
- ✅ `zone_name` (NOT `zone`)
- ✅ `capacity_increase` (percentage)
- ✅ `energy_multiplier` (decimal)
- ✅ `efficiency_modifier` (percentage)

### Issue: "422 Validation Error"

**Solution**: Check request body format

Use OpenAPI examples as templates:
```json
{
  "simulation_name": "Test",
  "modifications": [{
    "zone_name": "Paint Shop",
    "capacity_increase": 50
  }],
  "duration_hours": 720
}
```

---

## 🎉 Success Criteria

Your watsonx Orchestrate integration is successful when:

✅ Users can ask natural language questions and get accurate responses  
✅ Agents autonomously detect and respond to anomalies  
✅ Energy optimization recommendations are validated via simulation  
✅ Maintenance tickets are auto-created for high-priority issues  
✅ Complex scenarios can be simulated with confidence predictions  
✅ Multi-agent workflows execute seamlessly  
✅ Notifications are sent to appropriate channels (Slack/Teams)  

---

**🚀 Your Digital Twin Dashboard is now powered by AI agents!**
