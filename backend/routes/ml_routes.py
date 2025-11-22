"""
ML-Powered API Routes for Digital Twin
- Anomaly Detection
- Energy Forecasting
- Predictive Maintenance
- Digital Twin Simulation
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

# Import ML models
from backend.ml_models import AnomalyDetector, EnergyForecaster, PredictiveMaintenanceModel

# Create router
router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

# Load trained models - auto-train if not found
try:
    anomaly_detector = AnomalyDetector.load()
    energy_forecaster = EnergyForecaster.load()
    maintenance_model = PredictiveMaintenanceModel()
    print("✅ ML models loaded from disk")
except Exception as e:
    print(f"⚠️  Could not load ML models: {e}")
    print("🔄 Training models from scratch (this may take 30 seconds)...")
    
    try:
        # Load training data
        data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "plant_data_30days.csv")
        df_train = pd.read_csv(data_path, parse_dates=["timestamp"])
        
        # Train anomaly detector
        anomaly_detector = AnomalyDetector()
        anomaly_detector.train(df_train)
        anomaly_detector.save()
        print("✅ Anomaly detector trained and saved")
        
        # Train energy forecaster
        energy_forecaster = EnergyForecaster()
        energy_forecaster.train(df_train)
        energy_forecaster.save()
        print("✅ Energy forecaster trained and saved")
        
        # Predictive maintenance doesn't need training
        maintenance_model = PredictiveMaintenanceModel()
        print("✅ All ML models ready")
        
    except Exception as train_error:
        print(f"❌ Error training models: {train_error}")
        anomaly_detector = None
        energy_forecaster = None
        maintenance_model = None

# Pydantic Models

class AnomalyDetectionRequest(BaseModel):
    zone: Optional[str] = Field(None, description="Specific zone to analyze (e.g., 'Paint Shop'), or None for all zones", 
                                 examples=["Paint Shop", "Body Shop (BIW)", "Assembly"])
    hours: int = Field(24, ge=1, le=168, description="Hours of historical data to analyze (1-168)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "zone": "Paint Shop",
                    "hours": 24
                },
                {
                    "zone": None,
                    "hours": 48
                }
            ]
        }
    }

class AnomalyResult(BaseModel):
    timestamp: str
    zone: str
    is_anomaly: bool
    anomaly_score: float
    confidence: float
    metrics: Dict[str, float]

class AnomalyDetectionResponse(BaseModel):
    total_records: int
    anomalies_detected: int
    anomaly_rate: float
    results: List[AnomalyResult]
    timestamp: str

class EnergyForecastRequest(BaseModel):
    zone: str = Field(..., description="Zone name to forecast energy consumption", 
                      examples=["Paint Shop", "Body Shop (BIW)", "General Assembly"])
    hours_ahead: int = Field(24, ge=1, le=168, description="Number of hours to forecast ahead (1-168)")
    current_temp: Optional[float] = Field(None, description="Current temperature in °C (optional, uses latest if not provided)")
    current_efficiency: Optional[float] = Field(None, description="Current efficiency percentage (optional, uses latest if not provided)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "zone": "Paint Shop",
                    "hours_ahead": 24,
                    "current_temp": 185.0,
                    "current_efficiency": 85.0
                },
                {
                    "zone": "Assembly",
                    "hours_ahead": 48
                }
            ]
        }
    }

class ForecastPoint(BaseModel):
    timestamp: str
    hour: int
    predicted_energy_kwh: float
    predicted_cost_usd: float
    predicted_co2_kg: float

class EnergyForecastResponse(BaseModel):
    zone: str
    forecast_hours: int
    forecast: List[ForecastPoint]
    total_predicted_energy: float
    total_predicted_cost: float
    total_predicted_co2: float
    confidence_level: str
    timestamp: str

class MaintenanceRecommendation(BaseModel):
    zone: str
    priority: str
    anomaly_count: int
    issue: str
    recommended_action: str
    current_avg_energy: float
    current_avg_efficiency: float
    estimated_downtime_hours: int

class PredictiveMaintenanceResponse(BaseModel):
    recommendations: List[MaintenanceRecommendation]
    total_zones_needing_maintenance: int
    high_priority_count: int
    estimated_total_downtime: int
    timestamp: str

# Helper functions

def load_plant_data():
    """Load plant data from CSV"""
    # Use relative path that works in any environment
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "plant_data_30days.csv")
    try:
        return pd.read_csv(data_path, parse_dates=["timestamp"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not load plant data: {str(e)}")

# API Endpoints

@router.post("/anomaly-detection", response_model=AnomalyDetectionResponse)
def detect_anomalies_endpoint(request: AnomalyDetectionRequest):
    """
    Detect anomalies in plant zone data using Isolation Forest ML model
    Returns anomaly predictions with confidence scores
    """
    if anomaly_detector is None:
        raise HTTPException(status_code=503, detail="Anomaly detection model not available")
    
    try:
        # Load data
        df = load_plant_data()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter by zone if specified
        if request.zone:
            df = df[df['zone'] == request.zone]
        
        # Get recent data
        cutoff_time = df['timestamp'].max() - timedelta(hours=request.hours)
        df_recent = df[df['timestamp'] >= cutoff_time].copy()
        
        if len(df_recent) == 0:
            raise HTTPException(status_code=404, detail="No data found for specified parameters")
        
        # Predict anomalies
        predictions = anomaly_detector.predict(df_recent)
        
        # Merge predictions with original data
        df_with_predictions = df_recent.merge(
            predictions,
            on=['timestamp', 'zone'],
            how='left'
        )
        
        # Build results
        results = []
        for _, row in df_with_predictions.iterrows():
            results.append(AnomalyResult(
                timestamp=row['timestamp'].isoformat(),
                zone=row['zone'],
                is_anomaly=bool(row['is_anomaly']),
                anomaly_score=float(row['anomaly_score']),
                confidence=float(row['confidence']),
                metrics={
                    'energy_kwh': float(row['energy_kwh']),
                    'temperature_c': float(row['temperature_c']),
                    'efficiency_pct': float(row['efficiency_pct'])
                }
            ))
        
        anomalies_detected = sum(1 for r in results if r.is_anomaly)
        
        return AnomalyDetectionResponse(
            total_records=len(results),
            anomalies_detected=anomalies_detected,
            anomaly_rate=round(anomalies_detected / len(results) if len(results) > 0 else 0, 4),
            results=results,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection failed: {str(e)}")

@router.post("/energy-forecast", response_model=EnergyForecastResponse)
def forecast_energy_endpoint(request: EnergyForecastRequest):
    """
    Forecast energy consumption for a specific zone using trained ML model
    Predicts future energy usage, costs, and CO2 emissions
    """
    if energy_forecaster is None:
        raise HTTPException(status_code=503, detail="Energy forecasting model not available")
    
    try:
        # Get forecast
        forecast_data = energy_forecaster.predict(
            zone=request.zone,
            hours_ahead=request.hours_ahead,
            current_temp=request.current_temp,
            current_efficiency=request.current_efficiency
        )
        
        if forecast_data is None:
            raise HTTPException(status_code=404, detail=f"Zone '{request.zone}' not found in trained models")
        
        # Convert to Pydantic models
        forecast_points = [ForecastPoint(**point) for point in forecast_data]
        
        # Calculate totals
        total_energy = sum(p.predicted_energy_kwh for p in forecast_points)
        total_cost = sum(p.predicted_cost_usd for p in forecast_points)
        total_co2 = sum(p.predicted_co2_kg for p in forecast_points)
        
        # Determine confidence level
        if request.hours_ahead <= 24:
            confidence = "high"
        elif request.hours_ahead <= 72:
            confidence = "medium"
        else:
            confidence = "low"
        
        return EnergyForecastResponse(
            zone=request.zone,
            forecast_hours=request.hours_ahead,
            forecast=forecast_points,
            total_predicted_energy=round(total_energy, 2),
            total_predicted_cost=round(total_cost, 2),
            total_predicted_co2=round(total_co2, 2),
            confidence_level=confidence,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Energy forecasting failed: {str(e)}")

@router.get("/predictive-maintenance", response_model=PredictiveMaintenanceResponse)
def predictive_maintenance_endpoint():
    """
    Analyze plant data to predict maintenance needs
    Uses anomaly patterns to recommend preventive maintenance
    """
    if anomaly_detector is None or maintenance_model is None:
        raise HTTPException(status_code=503, detail="Predictive maintenance models not available")
    
    try:
        # Load data
        df = load_plant_data()
        
        # Get anomaly predictions
        predictions = anomaly_detector.predict(df)
        
        # Analyze maintenance needs
        recommendations_data = maintenance_model.analyze_maintenance_needs(df, predictions)
        
        # Convert to Pydantic models
        recommendations = [MaintenanceRecommendation(**rec) for rec in recommendations_data]
        
        # Calculate statistics
        high_priority = sum(1 for r in recommendations if r.priority == 'high')
        total_downtime = sum(r.estimated_downtime_hours for r in recommendations)
        
        return PredictiveMaintenanceResponse(
            recommendations=recommendations,
            total_zones_needing_maintenance=len(recommendations),
            high_priority_count=high_priority,
            estimated_total_downtime=total_downtime,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Predictive maintenance analysis failed: {str(e)}")

@router.get("/model-info")
def get_model_info():
    """Get information about loaded ML models"""
    return {
        "anomaly_detector": {
            "loaded": anomaly_detector is not None,
            "type": "Isolation Forest",
            "zones_trained": len(anomaly_detector.models) if anomaly_detector else 0
        },
        "energy_forecaster": {
            "loaded": energy_forecaster is not None,
            "type": "Linear Regression",
            "zones_trained": len(energy_forecaster.models) if energy_forecaster else 0
        },
        "maintenance_model": {
            "loaded": maintenance_model is not None,
            "type": "Rule-based + Anomaly Analysis"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
