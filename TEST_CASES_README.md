# watsonx Orchestrate Test Cases Guide

## 📋 Overview

This file (`test-cases-template.csv`) contains **50 comprehensive test cases** for testing your PlantOps Digital Twin Dashboard integrated with IBM watsonx Orchestrate.

---

## 🎯 Test Case Categories

### **1. Zone Status Queries (7 test cases)**
- Current status checks
- Critical zone identification
- Plant-wide status overview
- Efficiency checks

**Examples**:
- "What is the current status of Paint Shop?"
- "Show me zones in critical status"
- "What is the efficiency of Body Shop?"

---

### **2. Anomaly Detection (6 test cases)**
- Detect anomalies in specific zones
- Plant-wide anomaly detection
- Temperature anomaly checks
- Efficiency drop analysis

**Examples**:
- "Detect anomalies in Paint Shop"
- "Why is Paint Shop showing red status?"
- "Check for temperature anomalies in Paint Shop"

---

### **3. Energy Forecasting (5 test cases)**
- Zone-specific forecasts
- Multi-day forecasts
- Cost predictions
- Consumption trends

**Examples**:
- "Forecast energy consumption for Paint Shop"
- "How much energy will Paint Shop use tomorrow?"
- "Forecast energy for the next 48 hours"

---

### **4. Digital Twin Simulations (10 test cases)**
- Add production lines
- Temperature modifications
- Capacity changes
- Multi-zone simulations
- Peak production scenarios

**Examples**:
- "What if we add a second production line in Paint Shop?"
- "What happens if we reduce Paint Shop temperature by 10 degrees?"
- "Simulate adding production capacity to Paint Shop"
- "What happens if we increase Assembly production capacity by 30%?"

---

### **5. Maintenance Management (7 test cases)**
- Predictive maintenance
- Ticket creation
- Urgent maintenance
- Overdue tasks
- Maintenance predictions

**Examples**:
- "What zones need maintenance?"
- "Schedule maintenance for Paint Shop"
- "What are the predictive maintenance recommendations?"
- "Can you predict when Paint Shop will need maintenance?"

---

### **6. Energy Optimization (6 test cases)**
- Cost reduction recommendations
- Energy analysis
- Hotspot identification
- Plant-wide optimization
- Zone comparisons

**Examples**:
- "How can we reduce energy costs in Paint Shop?"
- "What is the most energy-intensive zone?"
- "Help me optimize energy consumption plant-wide"
- "Run energy analysis for last 24 hours"

---

### **7. General Capabilities (9 test cases)**
- System capabilities
- Available zones
- Configuration queries
- Comparisons
- Summaries

**Examples**:
- "Describe your capabilities"
- "What zones are available for monitoring?"
- "What is the plant-wide energy consumption?"
- "Show me a summary of all zones"

---

## 🔧 How to Use with watsonx Orchestrate

### **Step 1: Upload Test Cases**
1. Open IBM watsonx Orchestrate
2. Go to your PlantOps Orchestrator agent
3. Navigate to **Test** or **Validation** section
4. Upload `test-cases-template.csv`

### **Step 2: Run Tests**
watsonx Orchestrate will automatically:
- Send each prompt to your configured agent
- Call the appropriate API endpoints
- Compare actual responses with expected patterns
- Generate a test report

### **Step 3: Review Results**
Check for:
- ✅ **Pass**: Response matches expected pattern
- ⚠️ **Partial**: Response contains key information but format differs
- ❌ **Fail**: Wrong endpoint called or incorrect response

---

## 📊 Expected Response Format

### **Response Patterns Use Placeholders**
Responses use placeholders like `[X]`, `[Y]`, `[zone]` to represent dynamic values:

**Example**:
```
Expected: "Paint Shop status: [GREEN/AMBER/RED], Energy: [X] kWh"
Actual:   "Paint Shop status: RED, Energy: 1250 kWh"
Result:   ✅ PASS
```

### **Key Response Elements**
Responses should include:
1. **Status indicators**: GREEN/AMBER/RED
2. **Numerical values**: Energy (kWh), Cost ($), CO₂ (kg)
3. **Recommendations**: Specific actions to take
4. **Context**: Zone names, timestamps, priorities

---

## 🎯 Test Coverage

| Category | Test Cases | Coverage |
|----------|-----------|----------|
| Zone Status | 7 | Status checks, efficiency, health |
| Anomaly Detection | 6 | ML-powered detection, root cause |
| Energy Forecasting | 5 | Predictions, costs, trends |
| Simulations | 10 | What-if scenarios, capacity planning |
| Maintenance | 7 | Predictive, scheduling, tickets |
| Energy Optimization | 6 | Cost reduction, analysis |
| General | 9 | Capabilities, config, summaries |
| **TOTAL** | **50** | **Comprehensive coverage** |

---

## ✅ Success Criteria

### **Agent Should Successfully:**
1. ✅ Route queries to correct endpoints
2. ✅ Use proper field names (`zone_name` not `zone`)
3. ✅ Handle complex simulations with multiple parameters
4. ✅ Provide actionable recommendations
5. ✅ Format responses clearly
6. ✅ Handle edge cases (null zones, invalid inputs)

### **Expected Pass Rate:**
- **Excellent**: 90-100% (45-50 tests passing)
- **Good**: 80-89% (40-44 tests passing)
- **Needs Work**: <80% (review agent configuration)

---

## 🔍 Debugging Failed Tests

### **Common Issues:**

#### **Issue 1: Wrong Endpoint Called**
**Symptom**: Agent calls `/api/chatops` instead of `/api/ml/anomaly-detection`  
**Solution**: Review intent routing in agent configuration

#### **Issue 2: Field Name Errors**
**Symptom**: 422 Validation Error - "Field required: zone_name"  
**Solution**: Check agent is using `zone_name` not `zone` in simulation requests

#### **Issue 3: Invalid Zone Names**
**Symptom**: Error about unknown zone  
**Solution**: Verify agent uses exact spelling:
- ✅ "Paint Shop" ❌ "paint shop"
- ✅ "Body Shop (BIW)" ❌ "Body Shop"

#### **Issue 4: Missing Required Fields**
**Symptom**: 422 Validation Error  
**Solution**: Review `WATSONX_FIELD_REFERENCE.md` for required fields

---

## 📝 Test Case Format

```csv
"Prompt","Expected_Response"
"<user question>","<expected response pattern with [placeholders]>"
```

**Prompt**: Natural language query from user  
**Expected_Response**: Pattern that actual response should match

---

## 🎓 Training Tips for Agents

### **1. Status Queries → Status Monitoring Agent**
Prompts containing: "status", "how is", "show me", "current"

### **2. Anomaly Questions → Anomaly Detection Agent**
Prompts containing: "why", "anomaly", "detect", "problem", "red"

### **3. Energy Questions → Energy Intelligence Agent**
Prompts containing: "energy", "forecast", "cost", "optimize", "consumption"

### **4. Simulation Questions → Simulation Agent**
Prompts containing: "what if", "simulate", "add line", "test", "happens if"

### **5. Maintenance Questions → Maintenance Agent**
Prompts containing: "maintenance", "schedule", "ticket", "fix", "repair"

---

## 📊 Advanced Testing

### **Test Sequences** (Multi-Step Workflows)

#### **Sequence 1: Anomaly → Maintenance**
1. "Why is Paint Shop red?"
2. "Schedule maintenance for Paint Shop"
3. Expected: Agent auto-escalates from anomaly to maintenance

#### **Sequence 2: Optimization → Simulation**
1. "How can we reduce energy costs?"
2. "Simulate reducing Paint Shop temperature"
3. Expected: Agent validates recommendations via simulation

#### **Sequence 3: Status → Forecast → Action**
1. "What is Paint Shop status?"
2. "Forecast Paint Shop energy for tomorrow"
3. "Create maintenance ticket if needed"
4. Expected: Agent sequences actions logically

---

## 🔗 Related Documentation

- **WATSONX_ORCHESTRATE_SETUP.md** - Agent configuration guide
- **WATSONX_FIELD_REFERENCE.md** - API field names and validation
- **API_DOCUMENTATION.md** - Complete API reference
- **ML_MODELS_DOCUMENTATION.md** - ML model details
- **SIMULATION_DOCUMENTATION.md** - Simulation capabilities

---

## 📞 Support

If tests fail consistently:
1. Check agent configuration in watsonx Orchestrate
2. Review endpoint routing logic
3. Verify field names in API calls
4. Check OpenAPI spec is latest version
5. Review agent logs for error details

**Live API**: https://pink-fish-production.up.railway.app  
**API Docs**: https://pink-fish-production.up.railway.app/docs

---

## 🎉 Expected Outcomes

After running all 50 test cases, you should see:

✅ **Agent correctly routes** natural language queries to appropriate endpoints  
✅ **API calls use correct field names** and data types  
✅ **Responses include actionable insights** and recommendations  
✅ **Multi-agent workflows execute** seamlessly  
✅ **Simulations validate** optimization recommendations  
✅ **Maintenance tickets created** automatically for critical issues  

**Your Digital Twin Dashboard is ready for production! 🚀**

---

**Last Updated**: November 23, 2025  
**Test Cases**: 50  
**Categories**: 7  
**Coverage**: Comprehensive (all 18 API endpoints)
