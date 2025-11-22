# GitHub Copilot Instructions for Digital Twin Dashboard Project

## Project Context

This is a **hackathon project** building a Digital Twin Dashboard for automotive manufacturing plant operations, integrated with IBM watsonx Orchestrate for AI-powered workflows.

### Project Name
**PlantOps Digital Twin Dashboard**

### Primary Goal
Create a web-based dashboard that visualizes manufacturing plant zones in real-time, analyzes energy consumption, predicts anomalies, and triggers automated maintenance workflows through IBM watsonx Orchestrate integration.

---

## Domain Knowledge

### Automotive Manufacturing Plant Zones
When generating code related to plant zones, use these standard zones:

1. **Stamping/Press Shop** - Metal stamping and forming operations
2. **Body Shop (BIW)** - Welding and body assembly (highly automated)
3. **Paint Shop** - Pre-treatment, e-coating, priming, and painting
4. **General Assembly** - Final assembly line (interior, exterior, chassis)
5. **Powertrain Assembly** - Engine and transmission assembly
6. **Quality Control** - Final inspection and testing
7. **Logistics** - Shipping and distribution

### Zone Status Indicators
- **🟢 Green**: Normal operations, all metrics within acceptable range
- **🟡 Amber/Yellow**: Warning state, approaching thresholds, requires monitoring
- **🔴 Red**: Critical state, immediate action required, anomaly detected

### Key Performance Indicators (KPIs)
- Energy consumption (kWh)
- CO₂ emissions (kg)
- Cost impact ($)
- Equipment efficiency (%)
- Temperature levels (°C)
- Production output (units)

---

## Tech Stack Guidelines

### Frontend
- **Framework**: React.js (preferred) or plain HTML/CSS/JS
- **Styling**: CSS modules, Tailwind CSS, or styled-components
- **State Management**: React hooks (useState, useEffect, useContext)
- **HTTP Client**: Axios or fetch API
- **UI Components**: Modular, reusable components

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI (FastAPI preferred for async operations)
- **API Design**: RESTful architecture
- **Data Processing**: Pandas for CSV/JSON manipulation
- **Response Format**: JSON

### Integration Layer
- **IBM watsonx Orchestrate**: REST API integration
- **Mock Services**: Slack, Jira (simulated for hackathon)
- **Data Format**: JSON for all API communications

---

## Project Architecture

### Frontend Structure
```
src/
├── components/
│   ├── Dashboard.jsx          # Main dashboard container
│   ├── ZoneCard.jsx            # Individual zone display card
│   ├── KPISidebar.jsx          # KPI metrics display
│   ├── ActionPanel.jsx         # Workflow action buttons
│   ├── ChatOpsWidget.jsx       # Chat interface for queries
│   └── AlertBanner.jsx         # Notification/alert display
├── services/
│   └── api.js                  # API client for backend calls
├── utils/
│   └── helpers.js              # Utility functions
└── App.jsx                     # Root component
```

### Backend Structure
```
backend/
├── app.py                      # Main Flask/FastAPI application
├── routes/
│   ├── analyze.py              # Energy analysis endpoints
│   ├── chatops.py              # ChatOps query handling
│   └── maintenance.py          # Maintenance workflow endpoints
├── services/
│   ├── orchestrate_client.py  # IBM watsonx Orchestrate integration
│   ├── data_processor.py      # CSV/JSON data processing
│   └── anomaly_detector.py    # Anomaly prediction logic
├── models/
│   └── schemas.py              # Pydantic models or data schemas
└── data/
    └── plant_data.csv          # Mock energy data
```

---

## API Endpoints

When implementing API routes, follow these specifications:

### 1. POST /api/analyze-energy
**Purpose**: Trigger energy analysis workflow via watsonx Orchestrate

**Request Body**:
```json
{
  "zones": ["Paint Shop", "Assembly"],
  "timeframe": "last_24h"
}
```

**Response**:
```json
{
  "hotspots": ["Paint Shop", "Assembly"],
  "recommendations": [
    {
      "zone": "Paint Shop",
      "action": "Reduce oven temperature by 5°C",
      "priority": "high",
      "estimated_savings": 1200
    }
  ],
  "impact": {
    "cost": 1200,
    "co2": 300
  },
  "timestamp": "2025-11-22T10:30:00Z"
}
```

### 2. POST /api/chatops
**Purpose**: Handle natural language queries about plant status

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

### 3. POST /api/maintenance/schedule
**Purpose**: Create maintenance ticket via Orchestrate → Jira integration

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
  "assigned_to": "maintenance_team",
  "due_date": "2025-11-23T08:00:00Z"
}
```

### 4. GET /api/zones/status
**Purpose**: Retrieve current status of all plant zones

**Response**:
```json
{
  "zones": [
    {
      "id": "stamping",
      "name": "Stamping Shop",
      "status": "green",
      "energy_usage": 450,
      "efficiency": 92,
      "alerts": []
    },
    {
      "id": "paint",
      "name": "Paint Shop",
      "status": "red",
      "energy_usage": 1250,
      "efficiency": 78,
      "alerts": [
        {
          "type": "energy_spike",
          "message": "Energy consumption 25% above normal",
          "timestamp": "2025-11-22T15:30:00Z"
        }
      ]
    }
  ],
  "last_updated": "2025-11-22T16:00:00Z"
}
```

---

## IBM watsonx Orchestrate Integration

### Authentication Pattern
```python
# Use environment variables for credentials
ORCHESTRATE_API_KEY = os.getenv("WATSONX_API_KEY")
ORCHESTRATE_ENDPOINT = os.getenv("WATSONX_ENDPOINT")

headers = {
    "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
    "Content-Type": "application/json"
}
```

### Workflow Invocation Pattern
When calling watsonx Orchestrate workflows, use this pattern:

```python
async def call_orchestrate_workflow(workflow_name, input_data):
    """
    Call IBM watsonx Orchestrate workflow
    For hackathon: Can use mock responses if API not available
    """
    url = f"{ORCHESTRATE_ENDPOINT}/workflows/{workflow_name}/execute"
    
    # For demo purposes, include mock fallback
    if MOCK_MODE:
        return generate_mock_response(workflow_name, input_data)
    
    response = await http_client.post(url, json=input_data, headers=headers)
    return response.json()
```

---

## UI/UX Guidelines

### Dashboard Layout
- **Header**: Project title, current time, overall plant status
- **Main Grid**: 3-4 columns of zone cards, responsive layout
- **Sidebar**: Fixed position, displays aggregated KPIs
- **Action Panel**: Floating or bottom panel with primary action buttons
- **Chat Widget**: Collapsible bottom-right corner widget

### Zone Card Design
Each zone card should display:
- Zone name with icon
- Status indicator (large colored circle or border)
- Key metrics (2-3 primary KPIs)
- Mini trend chart (optional, if time permits)
- Quick action button

### Color Scheme
```css
:root {
  --status-green: #10b981;
  --status-amber: #f59e0b;
  --status-red: #ef4444;
  --background: #0f172a;
  --card-bg: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --accent: #3b82f6;
}
```

---

## Data Processing

### Mock Data Format (CSV)
```csv
timestamp,zone,energy_kwh,temperature_c,co2_kg,efficiency_pct,status
2025-11-22 10:00,Paint Shop,1200,185,280,75,amber
2025-11-22 10:00,Stamping,450,65,110,92,green
2025-11-22 10:00,Assembly,680,25,150,88,green
```

### Data Transformation
When processing CSV data:
1. Parse CSV using pandas
2. Calculate rolling averages for anomaly detection
3. Apply threshold rules for status determination
4. Generate insights and recommendations
5. Convert to JSON for API responses

### Anomaly Detection Logic
```python
def detect_anomaly(current_value, historical_avg, threshold=0.20):
    """
    Simple anomaly detection: flag if current value exceeds 
    historical average by threshold percentage
    """
    deviation = (current_value - historical_avg) / historical_avg
    return deviation > threshold
```

---

## Mock Integrations (Hackathon Shortcuts)

### Slack Alert Simulation
```javascript
// Frontend simulation
function sendSlackAlert(message) {
  console.log(`📱 SLACK ALERT: ${message}`);
  // Show toast notification in UI
  showToast(`Slack alert sent: ${message}`, 'success');
}
```

### Jira Ticket Creation (Mock)
```python
def create_jira_ticket_mock(zone, issue, priority):
    """Mock Jira ticket creation for demo"""
    ticket_id = f"MAINT-{random.randint(1000, 9999)}"
    return {
        "ticket_id": ticket_id,
        "status": "created",
        "url": f"https://jira.example.com/browse/{ticket_id}",
        "assigned_to": "maintenance_team"
    }
```

---

## Code Generation Preferences

### General
- Write clean, well-commented code suitable for hackathon judging
- Include error handling and logging
- Use async/await for API calls where possible
- Add docstrings to all functions
- Use type hints in Python code

### Frontend (React)
- Use functional components with hooks
- Implement loading states and error boundaries
- Make components reusable and prop-driven
- Add PropTypes or TypeScript types
- Use semantic HTML and accessibility attributes

### Backend (Python)
- Use FastAPI decorators with proper type annotations
- Implement CORS middleware for frontend integration
- Add request validation using Pydantic models
- Include health check endpoint (`/health`)
- Use environment variables for configuration

### API Integration
- Always include timeout configuration
- Implement retry logic for external API calls
- Provide mock/fallback responses for demo reliability
- Log all API requests and responses (sanitized)

---

## Testing & Demo Preparation

### Test Scenarios
1. **Normal Operation**: All zones green
2. **Single Anomaly**: One zone amber, trigger analysis
3. **Critical Alert**: One zone red, trigger maintenance
4. **ChatOps Query**: Ask about zone status
5. **Workflow Execution**: Run full energy analysis

### Demo Script
When generating demo code or documentation, include:
1. Setup instructions (environment variables, dependencies)
2. Sample data loading commands
3. API testing with curl/Postman examples
4. Frontend development server setup
5. Integration testing checklist

---

## Environment Variables

Always reference these environment variables in code:

```bash
# IBM watsonx Orchestrate
WATSONX_API_KEY=your_api_key_here
WATSONX_ENDPOINT=https://api.watsonx.ai/orchestrate

# Application Config
FLASK_ENV=development
PORT=5000
FRONTEND_URL=http://localhost:3000

# Feature Flags
MOCK_MODE=true  # Use mock responses when watsonx unavailable
ENABLE_SLACK=false
ENABLE_JIRA=false
```

---

## Hackathon Success Tips

When generating code, keep in mind:

1. **Prioritize Visual Impact**: Dashboard should look impressive
2. **Reliable Demo**: Mock responses ensure demo never fails
3. **Clear Narrative**: Code should tell the story of digital twin monitoring
4. **Scalability Hints**: Comment on how this could scale in production
5. **Innovation Points**: Highlight watsonx Orchestrate integration benefits
6. **Quick Setup**: Minimize dependencies, easy to run locally

---

## Example Queries You Can Ask Copilot

- "Create a ZoneCard component that displays zone status with color indicators"
- "Implement the /api/analyze-energy endpoint with watsonx Orchestrate integration"
- "Generate mock CSV data for 7 plant zones over 24 hours"
- "Build a ChatOps widget that sends queries to the backend"
- "Create an anomaly detection function using pandas"
- "Add error handling and retry logic to the Orchestrate API client"
- "Design a responsive dashboard layout with zone grid and KPI sidebar"

---

## Additional Context

- **Target Audience**: Manufacturing operations teams, plant managers
- **Key Differentiator**: AI-powered insights via watsonx Orchestrate
- **Business Value**: Reduce energy costs, prevent downtime, optimize operations
- **Hackathon Judges**: Look for innovation, technical execution, business impact
- **Time Constraint**: Build MVP in hackathon timeframe, prioritize core features

---

**Remember**: This is a hackathon project demonstrating the art of the possible. Focus on:
✅ Working demo with impressive visuals
✅ Clear integration story with IBM watsonx
✅ Realistic use case and business value
✅ Clean, presentable code
✅ Reliable execution (use mocks when needed)

Good luck! 🚀
