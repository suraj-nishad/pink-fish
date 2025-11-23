"""
PlantOps Digital Twin Dashboard - FastAPI Backend
Automotive manufacturing plant monitoring with IBM watsonx Orchestrate integration
"""

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Union
import pandas as pd
import os
import json
from datetime import datetime, timedelta
import random

# Import ML and simulation routes
try:
    from backend.routes.ml_routes import router as ml_router
    from backend.routes.simulation_routes import router as simulation_router
    ML_ROUTES_AVAILABLE = True
except Exception as e:
    print(f"⚠️ ML routes not available: {e}")
    ML_ROUTES_AVAILABLE = False

# Import scheduler for automatic data updates
try:
    from backend.scheduler import start_scheduler, stop_scheduler, get_scheduler_status
    SCHEDULER_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Scheduler not available: {e}")
    SCHEDULER_AVAILABLE = False

# Note: This API is designed to be CALLED BY watsonx Orchestrate
# No need to import watsonx client - watsonx will import our OpenAPI spec
# and call our endpoints as tools/skills in workflows

app = FastAPI(
    title="PlantOps Digital Twin Dashboard APIs",
    version="1.0.0",
    description="Automotive plant digital twin APIs with IBM watsonx Orchestrate integration for energy analysis and predictive maintenance",
    servers=[
        {"url": "https://pink-fish-production.up.railway.app", "description": "Production Server"},
        {"url": "http://127.0.0.1:8000", "description": "Local Development Server"}
    ],
)

# Add CORS middleware to allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Startup event: Start the background scheduler
@app.on_event("startup")
async def startup_event():
    """Start background tasks when FastAPI starts"""
    print("🚀 Starting PlantOps Digital Twin API...")
    
    if SCHEDULER_AVAILABLE:
        start_scheduler()
        print("✅ Background data updater initialized")
    else:
        print("⚠️ Background scheduler not available - data updates must be run manually")

# Shutdown event: Stop the scheduler gracefully
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background tasks when FastAPI shuts down"""
    print("🛑 Shutting down PlantOps Digital Twin API...")
    
    if SCHEDULER_AVAILABLE:
        stop_scheduler()
        print("✅ Background scheduler stopped")

# Include ML and simulation routers
if ML_ROUTES_AVAILABLE:
    app.include_router(ml_router)
    app.include_router(simulation_router)
    print("✅ ML and simulation routes loaded")

# Configuration
CONFIG = {
    "ENERGY_THRESHOLD_AMBER": 0.10,  # 10% above baseline
    "ENERGY_THRESHOLD_RED": 0.20,    # 20% above baseline
    "EFFICIENCY_THRESHOLD_AMBER": 0.05,  # 5% below baseline
    "EFFICIENCY_THRESHOLD_RED": 0.10,    # 10% below baseline
    "CO2_FACTOR": 0.4,  # kg CO2 per kWh
    "COST_PER_KWH": 0.12,  # $ per kWh
}

# Load CSV data at startup
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "plant_data_30days.csv")
CURRENT_STATUS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "current_status.csv")

try:
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    print(f"✅ Loaded {len(df)} records from {DATA_PATH}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    df = pd.DataFrame()

# Pydantic Models for API responses
class AlertModel(BaseModel):
    type: str
    message: str
    timestamp: str

class ZoneMetricsModel(BaseModel):
    energy_kwh: float
    temperature_c: float
    efficiency_pct: float
    co2_kg: float
    cost_usd: float
    production_units: Optional[int] = None

class ZoneStatusModel(BaseModel):
    zone_id: str
    zone_name: str
    status: str  # green, amber, red
    metrics: ZoneMetricsModel
    alerts: List[AlertModel] = []

class PlantStatusResponse(BaseModel):
    zones: List[ZoneStatusModel]
    last_updated: str
    plant_status: str = "operational"
    total_zones: int
    zones_normal: int
    zones_warning: int
    zones_critical: int

class RecommendationModel(BaseModel):
    zone: str
    action: str
    priority: str
    estimated_savings: float
    implementation: str

class EnergyAnalysisResponse(BaseModel):
    hotspots: List[str]
    recommendations: List[RecommendationModel]
    impact: Dict[str, float]
    timestamp: str

class ChatOpsRequest(BaseModel):
    query: str = Field(..., description="Natural language query about plant operations", 
                       examples=["Why is Paint Shop red?", "What zones need maintenance?", "Show me energy consumption trends"])
    user: Optional[str] = Field("operator", description="User identifier")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Why is Paint Shop showing red status?",
                    "user": "operator_123"
                }
            ]
        }
    }

class ChatOpsResponse(BaseModel):
    query: str
    response: str
    related_actions: List[str]
    confidence: float

class MaintenanceRequest(BaseModel):
    zone_name: str = Field(..., description="Zone name requiring maintenance. Valid zones: 'Stamping Shop', 'Body Shop (BIW)', 'Paint Shop', 'General Assembly', 'Powertrain Assembly', 'Quality Control', 'Logistics'", 
                      examples=["Paint Shop", "Body Shop (BIW)", "Assembly"])
    issue: str = Field(..., description="Description of the maintenance issue", 
                       examples=["Oven temperature anomaly", "Equipment efficiency below threshold"])
    priority: str = Field(..., description="Maintenance priority level", 
                          examples=["low", "medium", "high"])
    
    @field_validator('zone_name', mode='before')
    @classmethod
    def normalize_zone_name(cls, v):
        """
        Normalize zone name - handle watsonx sending JSON strings or non-standard formats
        """
        if v is None:
            raise ValueError("zone_name is required for maintenance requests - please specify which zone needs maintenance")
        
        # Handle JSON string format from watsonx
        if isinstance(v, str):
            v = v.strip()
            # Try to parse as JSON if it looks like a JSON structure
            if v.startswith('"') or v.startswith('['):
                try:
                    import json
                    v = json.loads(v)
                except:
                    pass
        
        # Reject "all" keyword for maintenance - must specify specific zone
        if isinstance(v, str) and v.lower() in ['all', 'all zones', '*']:
            raise ValueError("Maintenance requests require a specific zone - cannot schedule maintenance for 'all zones'")
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "zone_name": "Paint Shop",
                    "issue": "Oven temperature anomaly detected - 3 occurrences in 24h",
                    "priority": "high"
                }
            ]
        }
    }

class MaintenanceResponse(BaseModel):
    ticket_id: str
    status: str
    assigned_to: str
    due_date: str

class ConfigModel(BaseModel):
    ENERGY_THRESHOLD_AMBER: float
    ENERGY_THRESHOLD_RED: float
    EFFICIENCY_THRESHOLD_AMBER: float
    EFFICIENCY_THRESHOLD_RED: float
    CO2_FACTOR: float
    COST_PER_KWH: float

# Helper Functions

def load_current_status():
    """Load current status from CSV file - returns only the latest status for each zone"""
    try:
        df = pd.read_csv(CURRENT_STATUS_PATH)
        
        # Convert timestamp to datetime for proper sorting
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get only the latest entry for each zone
        latest_df = df.sort_values('timestamp').groupby('zone_id').tail(1)
        
        zones = []
        for _, row in latest_df.iterrows():
            zones.append({
                "id": row["zone_id"],
                "name": row["zone"],  # Column is "zone" not "zone_name"
                "status": row["status"],
                "energy_usage": float(row["energy_kwh"]),
                "efficiency": float(row["efficiency_pct"]),
                "temperature": float(row["temperature_c"]),
                "co2_emissions": float(row["co2_kg"]),
                "cost": float(row["cost_usd"]),
                "alerts": []  # Add empty alerts array
            })
        return {"zones": zones, "last_updated": datetime.now().isoformat()}
    except Exception as e:
        print(f"❌ Error loading current status: {e}")
        import traceback
        traceback.print_exc()
        return None

def determine_status(energy_kwh, base_energy, efficiency, base_efficiency):
    """Determine zone status based on metrics"""
    energy_deviation = (energy_kwh - base_energy) / base_energy if base_energy > 0 else 0
    efficiency_deviation = (base_efficiency - efficiency) / base_efficiency if base_efficiency > 0 else 0
    
    if energy_deviation > CONFIG["ENERGY_THRESHOLD_RED"] or efficiency_deviation > CONFIG["EFFICIENCY_THRESHOLD_RED"]:
        return "red"
    elif energy_deviation > CONFIG["ENERGY_THRESHOLD_AMBER"] or efficiency_deviation > CONFIG["EFFICIENCY_THRESHOLD_AMBER"]:
        return "amber"
    else:
        return "green"

def detect_anomalies(data_df):
    """Detect anomalies in zone data"""
    anomalies = []
    
    # Group by zone and check for anomalies
    for zone_id in data_df['zone_id'].unique():
        zone_data = data_df[data_df['zone_id'] == zone_id]
        
        # Calculate baseline (median when status is green)
        baseline_energy = zone_data[zone_data['status'] == 'green']['energy_kwh'].median()
        current_energy = zone_data['energy_kwh'].iloc[-1] if len(zone_data) > 0 else 0
        
        if baseline_energy and current_energy > baseline_energy * (1 + CONFIG["ENERGY_THRESHOLD_RED"]):
            anomalies.append({
                "zone": zone_data['zone'].iloc[0],  # CSV column is 'zone' not 'zone_name'
                "type": "energy_spike",
                "severity": "high",
                "current_value": float(current_energy),
                "baseline_value": float(baseline_energy),
                "deviation_percent": float(((current_energy - baseline_energy) / baseline_energy) * 100)
            })
    
    return anomalies

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """API health check"""
    return {
        "status": "online",
        "service": "PlantOps Digital Twin Dashboard",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check"""
    health_data = {
        "status": "healthy",
        "database": "connected" if len(df) > 0 else "disconnected",
        "records_loaded": len(df),
        "deployment": "vercel_ready",
        "api_mode": "tools_for_orchestrate",  # This API provides tools FOR watsonx to call
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Add scheduler status if available
    if SCHEDULER_AVAILABLE:
        scheduler_status = get_scheduler_status()
        health_data["scheduler"] = scheduler_status
    
    return health_data

@app.get("/api/zones/status", response_model=PlantStatusResponse, tags=["Plant Monitoring"])
def get_zones_status():
    """
    Get current status of all manufacturing zones
    Returns real-time metrics, alerts, and overall plant health
    """
    try:
        # Load current status from file
        status_data = load_current_status()
        
        if not status_data:
            raise HTTPException(status_code=500, detail="Unable to load current status")
        
        # Transform to API response format
        zones_response = []
        for zone in status_data['zones']:
            zones_response.append(ZoneStatusModel(
                zone_id=zone['id'],  # Changed from zone['zone_id']
                zone_name=zone['name'],  # Changed from zone['zone_name']
                status=zone['status'],
                metrics=ZoneMetricsModel(
                    energy_kwh=zone['energy_usage'],  # Changed from zone['energy_kwh']
                    temperature_c=zone['temperature'],  # Changed from zone['temperature_c']
                    efficiency_pct=zone['efficiency'],  # Changed from zone['efficiency_pct']
                    co2_kg=zone['co2_emissions'],  # Changed from zone['co2_kg']
                    cost_usd=zone['cost'],  # Changed from zone['cost_usd']
                    production_units=zone.get('production_units')
                ),
                alerts=[AlertModel(**alert) for alert in zone.get('alerts', [])]
            ))
        
        # Calculate zone counts
        zones_green = sum(1 for z in status_data['zones'] if z['status'] == 'green')
        zones_amber = sum(1 for z in status_data['zones'] if z['status'] == 'amber')
        zones_critical = sum(1 for z in status_data['zones'] if z['status'] == 'red')
        total_zones = len(status_data['zones'])
        
        return PlantStatusResponse(
            zones=zones_response,
            last_updated=status_data['last_updated'],
            plant_status='operational' if zones_critical == 0 else 'critical',
            total_zones=total_zones,
            zones_normal=zones_green,
            zones_warning=zones_amber,
            zones_critical=zones_critical
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching zone status: {str(e)}")

class EnergyAnalysisRequest(BaseModel):
    """Request model for energy analysis"""
    zones: Optional[Union[List[str], str]] = Field(
        default=None,
        description=(
            "Array of zone names to analyze. Must be a JSON array of strings. "
            "Valid zone names: 'Stamping Shop', 'Body Shop (BIW)', 'Paint Shop', "
            "'General Assembly', 'Powertrain Assembly', 'Quality Control', 'Logistics'. "
            "To analyze ALL zones: omit this field entirely or set to null. "
            "DO NOT use the string 'all' - use null or omit the field."
        ),
        json_schema_extra={
            "examples": [
                ["Paint Shop"],
                ["Paint Shop", "Body Shop (BIW)"],
                ["Stamping Shop", "Paint Shop", "General Assembly"],
                None
            ]
        }
    )
    timeframe: str = Field(
        default="last_24h",
        description="Analysis timeframe: 'last_24h', 'last_7d', or 'last_30d'",
        json_schema_extra={
            "examples": ["last_24h", "last_7d", "last_30d"]
        }
    )
    
    @field_validator('zones', mode='before')
    @classmethod
    def normalize_zones(cls, v):
        """
        Temporary workaround for watsonx agent sending "all" instead of null.
        This allows the API to work while agent configuration is being fixed.
        TODO: Remove this workaround once agent is properly trained.
        """
        if isinstance(v, str):
            # Handle special "all zones" keywords
            if v.lower() in ["all", "*", "all zones", "all_zones"]:
                return None  # Convert to None to analyze all zones
            else:
                # Single zone sent as string - wrap in array
                # This handles cases where agent sends: "zones": "Paint Shop"
                return [v]
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "zones": ["Paint Shop"],
                    "timeframe": "last_24h"
                },
                {
                    "zones": ["Paint Shop", "Body Shop (BIW)", "General Assembly"],
                    "timeframe": "last_7d"
                },
                {
                    "timeframe": "last_24h"
                }
            ]
        }
    }

@app.post("/api/analyze-energy", response_model=EnergyAnalysisResponse, tags=["AI Analysis"])
def analyze_energy(request: EnergyAnalysisRequest):
    """
    Trigger energy analysis workflow via IBM watsonx Orchestrate
    Analyzes energy consumption patterns and provides AI-powered recommendations
    
    Args:
        request: Energy analysis request with zones (optional) and timeframe
        
    Returns:
        Energy analysis with hotspots, recommendations, and impact metrics
    """
    try:
        # Use all zones if none specified
        zones_to_analyze = request.zones if request.zones else df['zone'].unique().tolist()
        
        # Filter data for specified zones
        zone_data = df[df['zone'].isin(zones_to_analyze)]
        
        if len(zone_data) == 0:
            raise HTTPException(status_code=404, detail="No data found for specified zones")
        
        # Detect anomalies
        anomalies = detect_anomalies(zone_data)
        hotspots = [a['zone'] for a in anomalies]
        
        # Build recommendations based on detected anomalies
        recommendations = []
        for anomaly in anomalies:
            zone = anomaly['zone']
            
            # Determine action based on anomaly type
            if anomaly['type'] == 'energy_spike':
                if 'Paint' in zone:
                    action = "Reduce oven temperature by 5°C"
                    implementation = "Update PLC temperature setpoint in paint shop oven controls"
                elif 'Assembly' in zone:
                    action = "Schedule compressor maintenance"
                    implementation = "Inspect and service air compressor system for leaks"
                else:
                    action = "Investigate equipment efficiency"
                    implementation = "Conduct energy audit and check for malfunctioning equipment"
            else:
                action = f"Optimize {zone} operations"
                implementation = "Review operational schedules and equipment settings"
            
            recommendations.append(RecommendationModel(
                zone=zone,
                action=action,
                priority="high" if anomaly['severity'] == 'high' else "medium",
                estimated_savings=float(anomaly['current_value'] - anomaly['baseline_value']) * CONFIG['COST_PER_KWH'] * 24 * 30,  # Monthly savings
                implementation=implementation
            ))
        
        # Calculate total impact
        total_energy_savings = sum(
            (a['current_value'] - a['baseline_value']) for a in anomalies
        ) * 24 * 30  # Monthly savings in kWh
        
        impact = {
            "cost": round(total_energy_savings * CONFIG['COST_PER_KWH'], 2) if anomalies else 0.0,
            "co2": round(total_energy_savings * CONFIG['CO2_FACTOR'], 2) if anomalies else 0.0,
            "energy_kwh": round(total_energy_savings, 2) if anomalies else 0.0
        }
        
        # FIXED: If no anomalies detected, provide meaningful trend analysis instead of flagging all zones
        if not hotspots:
            # Calculate trend analysis for zones with normal operations
            trend_analysis = []
            for zone_name in zones_to_analyze:
                zone_df = zone_data[zone_data['zone'] == zone_name].tail(24)  # Last 24 hours
                if len(zone_df) > 0:
                    current_avg = zone_df['energy_kwh'].mean()
                    baseline = zone_df['energy_kwh'].median()
                    trend_analysis.append({
                        'zone': zone_name,
                        'current_avg': current_avg,
                        'baseline': baseline,
                        'trend': 'stable'
                    })
            
            # Create meaningful recommendations for normal operations
            recommendations = [
                RecommendationModel(
                    zone="All Zones",
                    action="All zones operating within normal parameters",
                    priority="low",
                    estimated_savings=0.0,
                    implementation="Continue current monitoring schedule. Review energy efficiency opportunities during planned maintenance windows."
                )
            ]
            
            # Return empty hotspots (not all zones)
            return EnergyAnalysisResponse(
                hotspots=[],
                recommendations=recommendations,
                impact=impact,
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Return anomaly-based analysis
        return EnergyAnalysisResponse(
            hotspots=hotspots,
            recommendations=recommendations,
            impact=impact,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Energy analysis failed: {str(e)}")

@app.post("/api/chatops", response_model=ChatOpsResponse, tags=["ChatOps"])
def chatops_query(request: ChatOpsRequest):
    """
    Handle natural language queries about plant status
    Uses IBM watsonx Orchestrate for intelligent query processing
    """
    try:
        query = request.query.lower()
        
        # Load current status
        status_data = load_current_status()
        
        # Simple query parsing (in production, use watsonx NLP)
        response_text = ""
        related_actions = []
        confidence = 0.85
        
        # Check if query is about a specific zone
        for zone in status_data['zones']:
            zone_name_lower = zone['name'].lower()  # Changed from zone['zone_name']
            
            if zone_name_lower in query or zone['id'] in query:  # Changed from zone['zone_id']
                status = zone['status']
                
                if status == 'red':
                    response_text = f"{zone['name']} is in critical state due to "  # Changed from zone['zone_name']
                    
                    if zone.get('alerts'):
                        alert_msg = zone['alerts'][0]['message']
                        response_text += f"{alert_msg}. "
                    else:
                        response_text += f"elevated energy consumption ({zone['energy_usage']} kWh, {((zone['energy_usage'] / 600) - 1) * 100:.0f}% above normal). "  # Changed from zone['energy_kwh']
                    
                    # Add recommendations
                    if 'paint' in zone_name_lower:
                        response_text += "Recommended action: Reduce oven temperature by 5°C and schedule maintenance inspection."
                        related_actions = ["reduce_temperature", "schedule_maintenance"]
                    elif 'assembly' in zone_name_lower:
                        response_text += "Recommended action: Inspect air compressor for leaks and schedule maintenance."
                        related_actions = ["inspect_compressor", "schedule_maintenance"]
                    else:
                        response_text += "Recommended action: Conduct energy audit and review equipment efficiency."
                        related_actions = ["energy_audit", "equipment_check"]
                    
                    confidence = 0.92
                    
                elif status == 'amber':
                    response_text = f"{zone['name']} is in warning state. Energy consumption is approaching threshold. Monitor closely and consider preventive maintenance."
                    related_actions = ["monitor", "preventive_maintenance"]
                    confidence = 0.88
                    
                else:
                    response_text = f"{zone['name']} is operating normally. Energy consumption: {zone['energy_usage']} kWh, Efficiency: {zone['efficiency']}%."
                    related_actions = ["continue_monitoring"]
                    confidence = 0.95
                
                break
        
        # If no specific zone found, provide general status
        if not response_text:
            if "status" in query or "how" in query:
                # Calculate zone counts
                zones_critical = sum(1 for z in status_data['zones'] if z['status'] == 'red')
                zones_warning = sum(1 for z in status_data['zones'] if z['status'] == 'amber')
                zones_normal = sum(1 for z in status_data['zones'] if z['status'] == 'green')
                
                response_text = f"Plant status: {zones_critical} zones critical, {zones_warning} zones warning, {zones_normal} zones normal. "
                
                if zones_critical > 0:
                    critical_zones = [z['name'] for z in status_data['zones'] if z['status'] == 'red']
                    response_text += f"Critical zones: {', '.join(critical_zones)}."
                    related_actions = ["view_details", "schedule_maintenance"]
                else:
                    response_text += "All critical systems operating within normal parameters."
                    related_actions = ["continue_monitoring"]
                
                confidence = 0.90
            else:
                # For complex queries, return a helpful response
                # In production, watsonx Orchestrate can enhance this with its NLP capabilities
                response_text = "I can help you with plant status queries. Try asking about specific zones (e.g., 'Paint Shop status') or overall plant health."
                related_actions = ["ask_differently", "view_status"]
                confidence = 0.75
        
        return ChatOpsResponse(
            query=request.query,
            response=response_text,
            related_actions=related_actions,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ChatOps query failed: {str(e)}")

@app.post("/api/maintenance/schedule", response_model=MaintenanceResponse, tags=["Maintenance"])
def schedule_maintenance(request: MaintenanceRequest):
    """
    Create maintenance ticket
    This endpoint can be called by watsonx Orchestrate workflows
    which can then trigger Jira/ServiceNow integrations
    """
    try:
        # Generate ticket ID
        ticket_id = f"MAINT-{random.randint(1000, 9999)}"
        
        # This endpoint returns ticket info
        # watsonx Orchestrate can take this response and:
        # 1. Create actual Jira ticket using Jira skill
        # 2. Send Slack notification using Slack skill
        # 3. Update internal tracking system
        
        # Determine due date based on priority
        if request.priority.lower() == "high":
            due_date = datetime.utcnow() + timedelta(hours=4)
        elif request.priority.lower() == "medium":
            due_date = datetime.utcnow() + timedelta(hours=24)
        else:
            due_date = datetime.utcnow() + timedelta(hours=72)
        
        return MaintenanceResponse(
            ticket_id=ticket_id,
            status="created",
            assigned_to="Maintenance Team",
            due_date=due_date.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Maintenance scheduling failed: {str(e)}")

@app.get("/api/zones/{zone_id}/history", tags=["Plant Monitoring"])
def get_zone_history(
    zone_id: str = Path(..., description="Zone identifier. Valid values: 'stamping', 'body_shop', 'paint', 'assembly', 'powertrain', 'quality', 'logistics'", example="paint"),
    hours: int = Query(24, ge=1, le=168, description="Hours of history to retrieve")
):
    """
    Get historical data for a specific zone
    Useful for trend analysis and visualization
    
    Valid zone_id values:
    - stamping (Stamping Shop)
    - body_shop (Body Shop / BIW)
    - paint (Paint Shop)
    - assembly (General Assembly)
    - powertrain (Powertrain Assembly)
    - quality (Quality Control)
    - logistics (Logistics)
    """
    try:
        # Filter data for zone
        zone_data = df[df['zone_id'] == zone_id].tail(hours * 12)  # 12 points per hour (5-min intervals)
        
        if len(zone_data) == 0:
            raise HTTPException(status_code=404, detail=f"Zone {zone_id} not found")
        
        # Convert to records
        history = zone_data[[
            'timestamp', 'energy_kwh', 'temperature_c', 'efficiency_pct', 
            'co2_kg', 'cost_usd', 'status'
        ]].to_dict(orient='records')
        
        # Convert timestamps to strings
        for record in history:
            record['timestamp'] = record['timestamp'].isoformat()
        
        return JSONResponse(content={
            "zone_id": zone_id,
            "zone_name": zone_data['zone'].iloc[0],  # CSV column is 'zone' not 'zone_name'
            "hours": hours,
            "data_points": len(history),
            "history": history
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

@app.get("/api/config", response_model=ConfigModel, tags=["Configuration"])
def get_config():
    """Get current analysis configuration thresholds"""
    return ConfigModel(**CONFIG)

@app.put("/api/config", response_model=ConfigModel, tags=["Configuration"])
def update_config(config_update: ConfigModel):
    """Update analysis configuration thresholds"""
    global CONFIG
    try:
        CONFIG.update(config_update.dict())
        return ConfigModel(**CONFIG)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Config update failed: {str(e)}")

@app.get("/api/kpis", tags=["Analytics"])
def get_plant_kpis(
    hours: int = Query(24, description="Hours to analyze")
):
    """
    Get plant-wide KPIs and metrics
    Aggregated statistics for dashboard display
    """
    try:
        # Get recent data
        recent_data = df.tail(hours * 12 * 7)  # 7 zones, 12 points/hour
        
        # Calculate KPIs
        total_energy = recent_data['energy_kwh'].sum()
        total_co2 = recent_data['co2_kg'].sum()
        total_cost = recent_data['cost_usd'].sum()
        avg_efficiency = recent_data['efficiency_pct'].mean()
        
        # Production units (only for assembly zones)
        production_data = recent_data[recent_data['production_units'].notna()]
        total_production = production_data['production_units'].sum() if len(production_data) > 0 else 0
        
        # Zone breakdown
        zone_breakdown = recent_data.groupby('zone').agg({  # CSV column is 'zone' not 'zone_name'
            'energy_kwh': 'sum',
            'co2_kg': 'sum',
            'cost_usd': 'sum'
        }).to_dict(orient='index')
        
        return JSONResponse(content={
            "timeframe_hours": hours,
            "kpis": {
                "total_energy_kwh": round(total_energy, 2),
                "total_co2_kg": round(total_co2, 2),
                "total_cost_usd": round(total_cost, 2),
                "avg_efficiency_pct": round(avg_efficiency, 1),
                "total_production_units": int(total_production)
            },
            "zone_breakdown": zone_breakdown,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"KPI calculation failed: {str(e)}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    import os
    # Use Railway's PORT environment variable, or default to 8000 for local dev
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
