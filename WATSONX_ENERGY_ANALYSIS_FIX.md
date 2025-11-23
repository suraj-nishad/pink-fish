# watsonx Orchestrate Energy Analysis Fix

## Issue Summary

**Problem**: When watsonx Orchestrate called `/api/analyze-energy`, it was sending the `zones` parameter as a **string representation of a Python list** instead of a proper JSON array:

```json
❌ WRONG:
{
  "zones": "['Stamping Shop', 'Body Shop (BIW)', 'Paint Shop', ...]"
}
```

This caused the API to return a 500 error:
```
Error while executing Tool http error: status code 500, body: 
{"detail":"Energy analysis failed: 404: No data found for specified zones"}
```

## Root Cause

The endpoint was using FastAPI **Query parameters** instead of a **request body**:

```python
# ❌ OLD (Query parameters - causes watsonx to send as string)
@app.post("/api/analyze-energy")
def analyze_energy(
    zones: List[str] = Query(..., description="Zones to analyze"),
    timeframe: str = Query("last_24h", description="Timeframe")
):
```

When using Query parameters with complex types like `List[str]`, watsonx Orchestrate agents convert them to strings because query parameters are URL-based and can't properly represent nested structures.

## Solution

Changed the endpoint to use a **Pydantic request body model**:

```python
# ✅ NEW (Request body with Pydantic model)
class EnergyAnalysisRequest(BaseModel):
    zones: Optional[List[str]] = Field(
        default=None,
        description="List of zone names to analyze. Leave empty or null to analyze all zones."
    )
    timeframe: str = Field(default="last_24h")

@app.post("/api/analyze-energy")
def analyze_energy(request: EnergyAnalysisRequest):
    zones_to_analyze = request.zones if request.zones else df['zone'].unique().tolist()
    # ... rest of logic
```

## OpenAPI Schema Change

### Before (Query Parameters)
```json
{
  "paths": {
    "/api/analyze-energy": {
      "post": {
        "parameters": [
          {
            "name": "zones",
            "in": "query",
            "required": true,
            "schema": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        ]
      }
    }
  }
}
```

### After (Request Body)
```json
{
  "paths": {
    "/api/analyze-energy": {
      "post": {
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/EnergyAnalysisRequest"
              }
            }
          },
          "required": true
        }
      }
    }
  },
  "components": {
    "schemas": {
      "EnergyAnalysisRequest": {
        "type": "object",
        "properties": {
          "zones": {
            "anyOf": [
              {
                "type": "array",
                "items": {"type": "string"}
              },
              {"type": "null"}
            ],
            "description": "List of zone names to analyze. Leave empty or null to analyze all zones.",
            "examples": [
              ["Paint Shop"],
              ["Paint Shop", "Body Shop (BIW)"],
              null
            ]
          },
          "timeframe": {
            "type": "string",
            "default": "last_24h",
            "examples": ["last_24h", "last_7d", "last_30d"]
          }
        }
      }
    }
  }
}
```

## Testing

### ✅ Correct Usage (JSON Body)
```bash
curl -X POST https://pink-fish-production.up.railway.app/api/analyze-energy \
  -H "Content-Type: application/json" \
  -d '{
    "zones": ["Paint Shop", "Body Shop (BIW)"],
    "timeframe": "last_24h"
  }'
```

**Response:**
```json
{
  "hotspots": ["Paint Shop", "Body Shop (BIW)"],
  "recommendations": [
    {
      "zone": "Paint Shop",
      "action": "Reduce oven temperature by 5°C",
      "priority": "high",
      "estimated_savings": 1200.0,
      "implementation": "Update PLC temperature setpoint"
    }
  ],
  "impact": {
    "cost": 1200.0,
    "co2": 300.0,
    "energy_kwh": 10000.0
  },
  "timestamp": "2025-11-23T09:30:00Z"
}
```

### 🔧 Analyze All Zones (null/omit zones)
```bash
curl -X POST https://pink-fish-production.up.railway.app/api/analyze-energy \
  -H "Content-Type: application/json" \
  -d '{
    "timeframe": "last_24h"
  }'
```

## watsonx Orchestrate Agent Prompt

Update your energy intelligence agent with this guidance:

```
When calling the analyze_energy tool:
- Use JSON body format, not query parameters
- The zones field should be a JSON array: ["Paint Shop", "Body Shop (BIW)"]
- To analyze all zones, omit the zones field or set it to null
- Valid zone names: "Stamping Shop", "Body Shop (BIW)", "Paint Shop", "General Assembly", "Powertrain Assembly", "Quality Control", "Logistics"

Example valid requests:
1. Single zone: {"zones": ["Paint Shop"], "timeframe": "last_24h"}
2. Multiple zones: {"zones": ["Paint Shop", "Body Shop (BIW)"], "timeframe": "last_7d"}
3. All zones: {"timeframe": "last_24h"}
```

## Impact on Test Cases

Update `test-cases-template.csv` test case #8:

**Old Expected Behavior** (Query params):
```
Prompt: "Analyze energy consumption in Paint Shop and Body Shop"
API Call: POST /api/analyze-energy?zones=["Paint Shop", "Body Shop (BIW)"]&timeframe=last_24h
```

**New Expected Behavior** (Request body):
```
Prompt: "Analyze energy consumption in Paint Shop and Body Shop"
API Call: POST /api/analyze-energy
Body: {"zones": ["Paint Shop", "Body Shop (BIW)"], "timeframe": "last_24h"}
```

## Deployment Status

- ✅ **Code Fixed**: `backend/app.py` updated (commit: 739b1de)
- ✅ **OpenAPI Updated**: `openapi.json` regenerated with request body schema
- ✅ **Local Testing**: Verified with curl commands
- ✅ **Production Deploy**: Changes pushed to GitHub (Railway auto-deploy)
- ⏳ **watsonx Update**: Re-import `openapi.json` to watsonx Orchestrate

## Next Steps

1. **Re-import OpenAPI Spec** to watsonx Orchestrate
   - Download updated `openapi.json` from GitHub
   - Go to watsonx Orchestrate → Apps → Your API
   - Re-import the OpenAPI specification
   - This will update the tool schemas automatically

2. **Test in watsonx Orchestrate**
   - Run test case: "Show me energy consumption trends"
   - Run test case: "Analyze energy consumption in Paint Shop"
   - Verify agent sends proper JSON array: `{"zones": ["Paint Shop"]}`

3. **Verify Agent Routing**
   - Check that `energy_intelligence_agent` correctly calls `analyze_energy`
   - Ensure no 424/500 errors
   - Confirm response includes hotspots and recommendations

## Related Documentation

- [WATSONX_ORCHESTRATE_SETUP.md](./WATSONX_ORCHESTRATE_SETUP.md) - Agent configuration
- [WATSONX_FIELD_REFERENCE.md](./WATSONX_FIELD_REFERENCE.md) - API field reference
- [TEST_CASES_README.md](./TEST_CASES_README.md) - Test case guide
- [OPENAPI_ENHANCEMENTS_SUMMARY.md](./OPENAPI_ENHANCEMENTS_SUMMARY.md) - All enhancements

---

**Issue Resolved**: ✅ Commit 739b1de  
**Production URL**: https://pink-fish-production.up.railway.app  
**Fixed Date**: November 23, 2025
