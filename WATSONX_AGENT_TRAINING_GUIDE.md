# watsonx Orchestrate Agent Training Guide

## Current Issues & Solutions

### Issue 1: Agent Sending "all" Instead of null ❌

**Error:**
```json
{
  "zones": "all",  // ❌ WRONG - causes validation error
  "timeframe": "today_vs_yesterday"
}
```

**Expected:**
```json
{
  "timeframe": "last_24h"  // ✅ CORRECT - zones omitted = analyze all
}
```

**Root Cause**: Agent is interpreting natural language "all zones" as the literal string `"all"`.

---

## Agent Configuration Instructions

### 1. Energy Intelligence Agent - Training Instructions

Add these **explicit instructions** to your `energy_intelligence_agent` configuration:

```
CRITICAL FIELD MAPPING RULES for analyze_energy tool:

1. ZONES FIELD:
   - Type: JSON array of strings OR null OR omit entirely
   - Valid values: ["Paint Shop"], ["Body Shop (BIW)"], etc.
   - To analyze ALL zones: OMIT the zones field entirely
   - NEVER use: "all", "all zones", "*", or any string value
   
   Examples:
   ✅ CORRECT: {"timeframe": "last_24h"}
   ✅ CORRECT: {"zones": ["Paint Shop"], "timeframe": "last_24h"}
   ✅ CORRECT: {"zones": null, "timeframe": "last_24h"}
   ❌ WRONG: {"zones": "all", "timeframe": "last_24h"}
   ❌ WRONG: {"zones": "Paint Shop", "timeframe": "last_24h"}

2. TIMEFRAME FIELD:
   - Type: string
   - Valid values: "last_24h", "last_7d", "last_30d"
   - If user says "today vs yesterday": use "last_24h"
   - If user says "this week": use "last_7d"
   - If user says "this month": use "last_30d"
   
3. USER INTENT TRANSLATION:
   Query: "Show me energy consumption trends"
   → Call: analyze_energy with {"timeframe": "last_24h"}
   
   Query: "Compare energy usage today vs yesterday"
   → Call: analyze_energy with {"timeframe": "last_24h"}
   
   Query: "Analyze Paint Shop energy"
   → Call: analyze_energy with {"zones": ["Paint Shop"], "timeframe": "last_24h"}
   
   Query: "Check all zones for anomalies"
   → Call: analyze_energy with {"timeframe": "last_24h"}
   
   Query: "Energy consumption in Paint Shop and Body Shop"
   → Call: analyze_energy with {"zones": ["Paint Shop", "Body Shop (BIW)"], "timeframe": "last_24h"}
```

---

## Valid Zone Names (Exact Match Required)

Copy these exact strings when calling APIs:

```
"Stamping Shop"
"Body Shop (BIW)"
"Paint Shop"
"General Assembly"
"Powertrain Assembly"
"Quality Control"
"Logistics"
```

**Important**: Zone names are case-sensitive and must match exactly, including parentheses.

---

## Agent Skill Configuration

### Energy Intelligence Agent

```yaml
Agent Name: energy_intelligence_agent
Description: Analyzes plant energy consumption and provides optimization recommendations

Skills/Tools:
  - analyze_energy
  - get_zones_status (for current status)
  - detect_anomalies (ML-powered)
  - forecast_energy (ML-powered)

Routing Logic:
  - User mentions "energy", "consumption", "trends" → analyze_energy
  - User says "all zones" or "entire plant" → analyze_energy WITHOUT zones field
  - User mentions specific zone name → analyze_energy WITH zones: ["Zone Name"]
  - User asks about "status" or "current" → get_zones_status
  - User asks "why is [zone] red?" → chatops tool
  
Field Mapping Rules:
  zones field:
    - If user says "all", "entire plant", "whole facility": OMIT zones field
    - If user names 1+ specific zones: zones = ["Zone1", "Zone2"]
    - If zones field is included, it MUST be a JSON array, never a string
  
  timeframe field:
    - "today", "current", "now" → "last_24h"
    - "this week", "past week" → "last_7d"
    - "this month", "past month" → "last_30d"
```

---

## Testing Prompts with Expected API Calls

### Test Case 1: General Energy Trends
**User Prompt:** "Show me energy consumption trends"

**Expected Agent Behavior:**
```
1. Route to: energy_intelligence_agent
2. Select tool: analyze_energy
3. Parameters: {"timeframe": "last_24h"}
4. DO NOT include zones field
```

**Expected API Call:**
```json
POST /api/analyze-energy
{
  "timeframe": "last_24h"
}
```

---

### Test Case 2: Compare Today vs Yesterday
**User Prompt:** "Compare energy usage today vs yesterday"

**Expected Agent Behavior:**
```
1. Route to: energy_intelligence_agent
2. Select tool: analyze_energy
3. Map "today vs yesterday" → "last_24h"
4. Parameters: {"timeframe": "last_24h"}
```

**Expected API Call:**
```json
POST /api/analyze-energy
{
  "timeframe": "last_24h"
}
```

---

### Test Case 3: Specific Zone Analysis
**User Prompt:** "Analyze energy consumption in Paint Shop"

**Expected Agent Behavior:**
```
1. Route to: energy_intelligence_agent
2. Select tool: analyze_energy
3. Extract zone: "Paint Shop"
4. Parameters: {"zones": ["Paint Shop"], "timeframe": "last_24h"}
```

**Expected API Call:**
```json
POST /api/analyze-energy
{
  "zones": ["Paint Shop"],
  "timeframe": "last_24h"
}
```

---

### Test Case 4: Multiple Zones
**User Prompt:** "Compare energy in Paint Shop and Body Shop"

**Expected Agent Behavior:**
```
1. Route to: energy_intelligence_agent
2. Select tool: analyze_energy
3. Extract zones: "Paint Shop", "Body Shop (BIW)"
4. Parameters: {"zones": ["Paint Shop", "Body Shop (BIW)"], "timeframe": "last_24h"}
```

**Expected API Call:**
```json
POST /api/analyze-energy
{
  "zones": ["Paint Shop", "Body Shop (BIW)"],
  "timeframe": "last_24h"
}
```

---

### Test Case 5: All Zones Explicitly
**User Prompt:** "Check all zones for energy issues"

**Expected Agent Behavior:**
```
1. Route to: energy_intelligence_agent
2. Select tool: analyze_energy
3. Recognize "all zones" → OMIT zones field
4. Parameters: {"timeframe": "last_24h"}
```

**Expected API Call:**
```json
POST /api/analyze-energy
{
  "timeframe": "last_24h"
}
```

---

## Debugging Agent Issues

### Issue: Validation Error - "Input should be a valid list"

**Symptoms:**
```
1 validation error for DynamicModel
zones
  Input should be a valid list [type=list_type, input_value='all', input_type=str]
```

**Cause:** Agent is sending `"zones": "all"` (string) instead of omitting the field or sending an array.

**Fix Options:**

**Option 1: Improve Agent Instructions** (Recommended)
Add explicit rules to agent configuration:
```
When user says "all zones", "entire plant", or similar:
DO NOT include the zones field in the API call.
Simply call: {"timeframe": "last_24h"}
```

**Option 2: Add Custom Validation in API** (Fallback)
Modify the API to accept `"all"` as a special case and convert to `None`:

```python
class EnergyAnalysisRequest(BaseModel):
    zones: Optional[Union[List[str], str]] = Field(default=None)
    
    @field_validator('zones')
    @classmethod
    def validate_zones(cls, v):
        if v == "all" or v == "*":
            return None  # Convert "all" to None
        if isinstance(v, str):
            raise ValueError("zones must be an array of strings, not a single string")
        return v
```

**Option 3: Pre-process in Agent** (Most Flexible)
Add a pre-processing step in watsonx that normalizes the zones field before calling the API.

---

## Recommended Approach: Agent-Level Fix

### Why Fix at Agent Level?
1. ✅ **Cleaner API**: API schema remains strict and well-defined
2. ✅ **Better Training**: Agent learns correct patterns for future
3. ✅ **Reusability**: Other agents can learn from proper examples
4. ✅ **Standards**: Follows OpenAPI and JSON schema best practices

### Why NOT Fix at API Level?
1. ❌ **Loose Validation**: Accepting `"all"` as a string weakens type safety
2. ❌ **Ambiguity**: What if there's a zone actually named "all"?
3. ❌ **Bad Precedent**: Other endpoints would need similar workarounds
4. ❌ **Maintenance**: More complex validation logic to maintain

---

## Implementation Steps

### Step 1: Update Agent Configuration
1. Go to watsonx Orchestrate → Agents → `energy_intelligence_agent`
2. Add the **CRITICAL FIELD MAPPING RULES** from above to agent instructions
3. Save and test

### Step 2: Re-import Updated OpenAPI Spec
1. Download latest `openapi.json` from GitHub
2. Go to watsonx Orchestrate → Apps → Your API
3. Re-import the OpenAPI specification
4. The improved descriptions will guide the agent better

### Step 3: Test with Prompts
Run these test prompts in sequence:
1. "Show me energy consumption trends" → Should omit zones field
2. "Analyze Paint Shop energy" → Should send zones: ["Paint Shop"]
3. "Compare all zones this week" → Should send timeframe: "last_7d" with no zones

### Step 4: Monitor and Iterate
- Check watsonx logs for actual API calls
- If agent still sends "all", add more explicit examples
- Consider adding negative examples: "DO NOT send zones: 'all'"

---

## Alternative: API-Level Workaround (If Needed)

If agent training proves difficult, we can add a temporary workaround in the API:

```python
# In backend/app.py - EnergyAnalysisRequest
from pydantic import field_validator

class EnergyAnalysisRequest(BaseModel):
    zones: Optional[Union[List[str], str]] = Field(default=None)
    timeframe: str = Field(default="last_24h")
    
    @field_validator('zones', mode='before')
    @classmethod
    def normalize_zones(cls, v):
        """
        Temporary workaround for watsonx agent sending "all" instead of null.
        TODO: Remove once agent is properly trained.
        """
        if isinstance(v, str):
            if v.lower() in ["all", "*", "all zones"]:
                return None  # Convert to None to analyze all zones
            else:
                # Single zone sent as string - wrap in array
                return [v]
        return v
```

This is a **temporary fix** and should be removed once the agent is properly configured.

---

## Success Criteria

✅ Agent successfully handles: "Show me energy consumption trends"  
✅ Agent successfully handles: "Compare energy usage today vs yesterday"  
✅ Agent successfully handles: "Analyze Paint Shop energy"  
✅ Agent successfully handles: "Check all zones for energy issues"  
✅ No validation errors in watsonx logs  
✅ API receives properly formatted JSON arrays  

---

## Related Documentation

- [WATSONX_ENERGY_ANALYSIS_FIX.md](./WATSONX_ENERGY_ANALYSIS_FIX.md) - Previous fix for query params issue
- [WATSONX_FIELD_REFERENCE.md](./WATSONX_FIELD_REFERENCE.md) - Complete API field reference
- [TEST_CASES_README.md](./TEST_CASES_README.md) - All test cases
- [WATSONX_ORCHESTRATE_SETUP.md](./WATSONX_ORCHESTRATE_SETUP.md) - Initial setup guide

---

**Last Updated**: November 23, 2025  
**Issue**: watsonx agent sending `"zones": "all"` instead of omitting field  
**Recommended Fix**: Agent configuration (not API change)
