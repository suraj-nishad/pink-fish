"""
Digital Twin Simulation API Routes
Allows users to experiment with plant configurations
- Add/remove production lines
- Modify zone parameters
- Simulate "what-if" scenarios
- Predict impact of changes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Union
import json
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import copy

router = APIRouter(prefix="/api/simulation", tags=["Digital Twin Simulation"])

# Base zone configurations
BASE_ZONES = {
    "Stamping Shop": {
        "base_energy": 450,
        "base_temp": 65,
        "base_efficiency": 92,
        "production_capacity": 100,
        "co2_factor": 0.233
    },
    "Body Shop (BIW)": {
        "base_energy": 800,
        "base_temp": 55,
        "base_efficiency": 89,
        "production_capacity": 80,
        "co2_factor": 0.233
    },
    "Paint Shop": {
        "base_energy": 1200,
        "base_temp": 185,
        "base_efficiency": 85,
        "production_capacity": 60,
        "co2_factor": 0.233
    },
    "General Assembly": {
        "base_energy": 680,
        "base_temp": 25,
        "base_efficiency": 88,
        "production_capacity": 120,
        "co2_factor": 0.233
    },
    "Powertrain Assembly": {
        "base_energy": 550,
        "base_temp": 35,
        "base_efficiency": 90,
        "production_capacity": 90,
        "co2_factor": 0.233
    },
    "Quality Control": {
        "base_energy": 320,
        "base_temp": 22,
        "base_efficiency": 95,
        "production_capacity": 150,
        "co2_factor": 0.233
    },
    "Logistics": {
        "base_energy": 280,
        "base_temp": 20,
        "base_efficiency": 93,
        "production_capacity": 200,
        "co2_factor": 0.233
    }
}

# Store simulation states
simulation_store = {}

# Pydantic Models

class ProductionLine(BaseModel):
    line_id: str = Field(..., description="Unique identifier for the production line", examples=["line-002", "paint-line-2"])
    name: str = Field(..., description="Descriptive name for the production line", examples=["Paint Line 2", "Assembly Line B"])
    energy_multiplier: float = Field(1.0, description="Energy usage multiplier (e.g., 1.5 = 50% more energy)")
    efficiency_modifier: float = Field(0.0, description="Efficiency percentage modifier (e.g., -5 = -5% efficiency)")
    production_capacity: int = Field(100, description="Production capacity in units per hour")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "line_id": "paint-line-2",
                    "name": "Paint Shop Line 2",
                    "energy_multiplier": 1.0,
                    "efficiency_modifier": -5.0,
                    "production_capacity": 60
                }
            ]
        }
    }

class ZoneModification(BaseModel):
    zone_name: str = Field(..., description="Name of the manufacturing zone to modify. Valid zones: 'Stamping Shop', 'Body Shop (BIW)', 'Paint Shop', 'General Assembly', 'Powertrain Assembly', 'Quality Control', 'Logistics'",
                          examples=["Paint Shop", "Body Shop (BIW)", "General Assembly"])
    temperature_offset: Optional[float] = Field(None, description="Temperature change in °C (e.g., -10 to reduce by 10°C, +5 to increase by 5°C)")
    efficiency_modifier: Optional[float] = Field(None, description="Efficiency percentage change (e.g., -5 for -5% efficiency, +3 for +3% efficiency)")
    energy_multiplier: Optional[float] = Field(None, description="Energy usage multiplier as decimal (e.g., 1.5 for 50% increase, 0.8 for 20% reduction)")
    capacity_increase: Optional[float] = Field(None, description="Production capacity increase as percentage (e.g., 50 for 50% increase when adding production lines, 100 for doubling capacity)")
    add_production_lines: Optional[Union[List[ProductionLine], int]] = Field(None, description="Array of production lines to add to the zone, OR an integer count of lines to add (will auto-generate line details)")
    remove_line_ids: Optional[List[str]] = Field(None, description="Array of line IDs to remove from the zone")
    
    @field_validator('add_production_lines', mode='before')
    @classmethod
    def normalize_production_lines(cls, v, info):
        """
        Handle watsonx agent sending integer instead of array:
        - Integer (e.g., 1, 2) → auto-generate ProductionLine objects
        - List of dicts/ProductionLine → use as-is
        - None → no lines to add
        """
        if v is None:
            return None
        
        # If integer, auto-generate production line objects
        if isinstance(v, int):
            # Get zone_name from the validation context
            zone_name = info.data.get('zone_name', 'Unknown Zone')
            
            # Get base config for the zone
            base_config = BASE_ZONES.get(zone_name, {
                'base_energy': 500,
                'production_capacity': 100
            })
            
            lines = []
            for i in range(abs(v)):
                line_num = i + 2  # Line 1 is the base, so start from 2
                line_id = f"{zone_name.lower().replace(' ', '_').replace('(', '').replace(')', '')}_line_{line_num}"
                lines.append({
                    'line_id': line_id,
                    'name': f"{zone_name} Line {line_num}",
                    'energy_multiplier': 1.0,  # Same energy as base line
                    'efficiency_modifier': -5.0,  # Each additional line reduces efficiency by 5%
                    'production_capacity': base_config.get('production_capacity', 100)
                })
            
            return lines
        
        # If already a list, return as-is
        if isinstance(v, list):
            return v
        
        # If single dict, wrap in list
        if isinstance(v, dict):
            return [v]
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "zone_name": "Paint Shop",
                    "capacity_increase": 50,
                    "efficiency_modifier": -10,
                    "energy_multiplier": 1.5
                },
                {
                    "zone_name": "Body Shop (BIW)",
                    "temperature_offset": -5,
                    "efficiency_modifier": 3
                },
                {
                    "zone_name": "Paint Shop",
                    "add_production_lines": 1
                },
                {
                    "zone_name": "Assembly",
                    "add_production_lines": [
                        {
                            "line_id": "assembly-line-c",
                            "name": "Assembly Line C",
                            "energy_multiplier": 1.0,
                            "efficiency_modifier": -5,
                            "production_capacity": 120
                        }
                    ]
                }
            ]
        }
    }

class SimulationRequest(BaseModel):
    simulation_name: str = Field(..., description="Descriptive name for this simulation scenario", 
                                  examples=["Add second Paint Shop line", "Reduce assembly temperature", "Q1 2026 capacity increase"])
    modifications: Union[List[ZoneModification], str] = Field(..., description="Array of zone modifications to simulate. Must be a JSON array. Each modification must include 'zone_name' and at least one parameter change (capacity_increase, temperature_offset, efficiency_modifier, energy_multiplier, or add_production_lines).")
    duration_hours: int = Field(24, ge=1, le=168, description="Number of hours to simulate (1-168). Use 720 for 30-day simulation, 168 for 1-week simulation.")
    
    @field_validator('modifications', mode='before')
    @classmethod
    def normalize_modifications(cls, v):
        """
        Temporary workaround for watsonx agent sending modifications as JSON string.
        Converts string to proper array and handles parameter/value format.
        TODO: Remove once agent is properly trained.
        """
        # If it's a string, try to parse it as JSON
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                v = parsed if isinstance(parsed, list) else [parsed]
            except json.JSONDecodeError:
                raise ValueError("modifications must be a valid JSON array")
        
        # Ensure it's a list
        if not isinstance(v, list):
            v = [v]
        
        # Normalize each modification
        normalized = []
        for mod in v:
            if isinstance(mod, dict):
                # Handle watsonx sending "production_lines" instead of "add_production_lines"
                if 'production_lines' in mod and 'add_production_lines' not in mod:
                    value = mod['production_lines']
                    zone_name = mod.get('zone_name', '')
                    
                    # Convert production_lines to proper format
                    normalized_mod = {'zone_name': zone_name}
                    
                    if isinstance(value, int):
                        if value > 0:
                            # Positive = add lines
                            # Each line adds ~100% capacity (double, triple, etc.)
                            capacity_pct = value * 100
                            normalized_mod['capacity_increase'] = capacity_pct
                            # Energy increases proportionally
                            normalized_mod['energy_multiplier'] = 1.0 + value
                            # Efficiency drops slightly with more lines (5% per line)
                            normalized_mod['efficiency_modifier'] = -(value * 5.0)
                        elif value < 0:
                            # Negative = remove lines
                            # Reduce capacity proportionally
                            capacity_pct = value * 100  # e.g., -1 = -100%
                            normalized_mod['capacity_increase'] = capacity_pct
                            # Energy decreases proportionally
                            normalized_mod['energy_multiplier'] = 1.0 + value  # e.g., -1 = 0.0 (no energy)
                            # Efficiency might improve with fewer lines
                            normalized_mod['efficiency_modifier'] = -(value * 5.0)  # e.g., -1 gives +5%
                    
                    normalized.append(normalized_mod)
                    continue
                
                # Handle generic parameter/value format
                if 'parameter' in mod and 'value' in mod:
                    param = mod['parameter'].lower()
                    value = mod['value']
                    zone_name = mod.get('zone_name', mod.get('zone', ''))
                    
                    # Convert generic parameters to specific fields
                    normalized_mod = {'zone_name': zone_name}
                    
                    if param in ['production_lines', 'capacity', 'lines']:
                        # Adding production lines - use capacity_increase
                        # If value is 2, that means double capacity (100% increase)
                        if isinstance(value, (int, float)) and value > 0:
                            capacity_pct = (value - 1) * 100 if value < 10 else value
                            normalized_mod['capacity_increase'] = capacity_pct
                            # Adding capacity typically increases energy and reduces efficiency
                            normalized_mod['energy_multiplier'] = 1.0 + (capacity_pct / 100.0)
                            normalized_mod['efficiency_modifier'] = -(capacity_pct / 10.0)
                    elif param in ['temperature', 'temp']:
                        normalized_mod['temperature_offset'] = value
                    elif param == 'efficiency':
                        normalized_mod['efficiency_modifier'] = value
                    elif param in ['energy', 'power']:
                        # If value is percentage, convert to multiplier
                        if abs(value) < 1:
                            normalized_mod['energy_multiplier'] = 1.0 + value
                        else:
                            normalized_mod['energy_multiplier'] = value
                    else:
                        # Unknown parameter, pass through original
                        normalized_mod = mod
                    
                    normalized.append(normalized_mod)
                else:
                    # Already in correct format
                    normalized.append(mod)
            else:
                normalized.append(mod)
        
        return normalized
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "simulation_name": "Add second production line to Paint Shop",
                    "modifications": [
                        {
                            "zone_name": "Paint Shop",
                            "capacity_increase": 100,
                            "efficiency_modifier": -10,
                            "energy_multiplier": 2.0
                        }
                    ],
                    "duration_hours": 720
                },
                {
                    "simulation_name": "Reduce energy consumption in Body Shop",
                    "modifications": [
                        {
                            "zone_name": "Body Shop (BIW)",
                            "temperature_offset": -10,
                            "energy_multiplier": 0.9
                        }
                    ],
                    "duration_hours": 168
                }
            ]
        }
    }

class SimulationMetrics(BaseModel):
    total_energy_kwh: float
    total_cost_usd: float
    total_co2_kg: float
    avg_efficiency_pct: float
    total_production_units: int

class SimulationComparison(BaseModel):
    baseline: SimulationMetrics
    modified: SimulationMetrics
    delta: Dict[str, float]
    percent_change: Dict[str, float]

class SimulationResult(BaseModel):
    simulation_id: str
    simulation_name: str
    status: str
    zones_modified: int
    comparison: SimulationComparison
    zone_details: List[Dict]
    recommendations: List[str]
    timestamp: str

class WhatIfScenario(BaseModel):
    scenario_name: str = Field(..., description="Name for this what-if scenario", 
                               examples=["Reduce Paint Shop Temperature", "Increase Assembly Efficiency"])
    description: str = Field(..., description="Detailed description of the scenario", 
                            examples=["Test impact of reducing oven temperature by 10°C", "Improve efficiency through automation"])
    zone_name: str = Field(..., description="Zone name to test. Valid zones: 'Stamping Shop', 'Body Shop (BIW)', 'Paint Shop', 'General Assembly', 'Powertrain Assembly', 'Quality Control', 'Logistics'",
                     examples=["Paint Shop", "Body Shop (BIW)", "General Assembly"])
    parameter: str = Field(..., description="Parameter to modify. Valid parameters: 'temperature', 'energy', 'efficiency', 'capacity', 'production_rate'",
                          examples=["temperature", "energy", "efficiency"])
    value_change: float = Field(..., description="Amount to change the parameter by (positive or negative). For temperature: degrees Celsius, For efficiency: percentage points, For energy: multiplier (e.g., -0.2 = 20% reduction)")
    
    @field_validator('zone_name', mode='before')
    @classmethod
    def normalize_zone_name(cls, v):
        """
        Normalize zone name - handle watsonx sending JSON strings
        What-if scenarios require a specific zone
        """
        if v is None:
            raise ValueError("zone_name is required for what-if scenarios - please specify which zone to analyze")
        
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
        
        # Reject "all" keyword - what-if scenarios need specific zones
        if isinstance(v, str) and v.lower() in ['all', 'all zones', '*']:
            raise ValueError("What-if scenarios require a specific zone - cannot simulate 'all zones' at once")
        
        return v
    
    @field_validator('parameter', mode='before')
    @classmethod
    def normalize_parameter(cls, v):
        """
        Normalize parameter name - handle watsonx sending JSON strings or variations
        """
        if v is None:
            raise ValueError("parameter is required - specify what to modify (temperature, energy, efficiency, capacity, production_rate)")
        
        # Handle JSON string format
        if isinstance(v, str):
            v = v.strip()
            if v.startswith('"'):
                try:
                    import json
                    v = json.loads(v)
                except:
                    pass
            
            # Normalize common variations
            v_lower = v.lower().replace(' ', '_').replace('-', '_')
            param_map = {
                'temp': 'temperature',
                'temps': 'temperature',
                'oven_temp': 'temperature',
                'power': 'energy',
                'consumption': 'energy',
                'eff': 'efficiency',
                'cap': 'capacity',
                'production': 'production_rate',
                'prod_rate': 'production_rate',
                'output': 'production_rate'
            }
            
            if v_lower in param_map:
                return param_map[v_lower]
        
        return v
    
    @field_validator('value_change', mode='before')
    @classmethod
    def parse_value_change(cls, v):
        """
        Parse value_change - handle watsonx sending strings or various formats
        """
        if v is None:
            raise ValueError("value_change is required - specify how much to change the parameter")
        
        # Handle JSON string format
        if isinstance(v, str):
            v = v.strip()
            if v.startswith('"'):
                try:
                    import json
                    v = json.loads(v)
                except:
                    pass
            
            # Try to convert to float
            try:
                return float(v)
            except ValueError:
                raise ValueError(f"value_change must be a number, got: {v}")
        
        return float(v)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "scenario_name": "Reduce Paint Shop Temperature",
                    "description": "Test impact of reducing oven temperature by 10°C to save energy",
                    "zone_name": "Paint Shop",
                    "parameter": "temperature",
                    "value_change": -10
                },
                {
                    "scenario_name": "Improve Assembly Efficiency",
                    "description": "Test impact of 5% efficiency improvement through automation",
                    "zone_name": "General Assembly",
                    "parameter": "efficiency",
                    "value_change": 5
                }
            ]
        }
    }

class WhatIfResult(BaseModel):
    scenario: WhatIfScenario
    predicted_impact: Dict[str, float]
    feasibility: str
    risk_level: str
    recommendation: str

# Helper Functions

def calculate_zone_metrics(zone_config, hours, production_lines=None):
    """Calculate metrics for a zone configuration"""
    metrics = {
        'energy_kwh': 0,
        'cost_usd': 0,
        'co2_kg': 0,
        'efficiency_pct': zone_config['base_efficiency'],
        'production_units': 0
    }
    
    # Base energy calculation
    base_energy_per_hour = zone_config['base_energy']
    
    # Calculate impact of additional production lines
    # Base assumption: 1 baseline production line already exists
    total_energy_multiplier = 1.0  # Baseline
    efficiency_total_modifier = 0.0
    capacity_total = zone_config['production_capacity']
    
    if production_lines and len(production_lines) > 0:
        # Each additional production line adds energy and capacity
        for line in production_lines:
            # Each line adds proportional energy (line_energy_multiplier is the energy for THAT line)
            # If a line has energy_multiplier=1.0, it consumes same energy as base line
            total_energy_multiplier += line['energy_multiplier']
            efficiency_total_modifier += line['efficiency_modifier']
            capacity_total += line['production_capacity']
    
    # Calculate total metrics
    hourly_energy = base_energy_per_hour * total_energy_multiplier
    metrics['energy_kwh'] = hourly_energy * hours
    metrics['cost_usd'] = metrics['energy_kwh'] * 0.12
    metrics['co2_kg'] = metrics['energy_kwh'] * zone_config['co2_factor']
    metrics['efficiency_pct'] = min(100, max(50, zone_config['base_efficiency'] + efficiency_total_modifier))
    metrics['production_units'] = int(capacity_total * hours * (metrics['efficiency_pct'] / 100))
    
    return metrics

def apply_modifications(base_config, modifications):
    """Apply modifications to base configuration"""
    modified_config = copy.deepcopy(base_config)
    
    for mod in modifications:
        zone = mod.zone_name
        if zone not in modified_config:
            continue
        
        # Apply temperature offset
        if mod.temperature_offset is not None:
            modified_config[zone]['base_temp'] += mod.temperature_offset
            # Temperature affects energy (rough approximation)
            if 'Paint' in zone:
                energy_impact = mod.temperature_offset * 2.0  # Paint shop is temp-sensitive
                modified_config[zone]['base_energy'] += energy_impact
        
        # Apply efficiency modifier
        if mod.efficiency_modifier is not None:
            modified_config[zone]['base_efficiency'] += mod.efficiency_modifier
            # Clamp between 50 and 100
            modified_config[zone]['base_efficiency'] = max(50, min(100, modified_config[zone]['base_efficiency']))
        
        # Apply energy multiplier
        if mod.energy_multiplier is not None:
            modified_config[zone]['base_energy'] *= mod.energy_multiplier
        
        # Apply capacity increase (simplified way to add production capacity)
        if mod.capacity_increase is not None:
            # Increase production capacity
            capacity_multiplier = 1.0 + (mod.capacity_increase / 100.0)
            modified_config[zone]['production_capacity'] = int(
                modified_config[zone]['production_capacity'] * capacity_multiplier
            )
            
            # Adding capacity typically increases energy consumption
            if mod.energy_multiplier is None:  # Only auto-adjust if not explicitly set
                modified_config[zone]['base_energy'] *= capacity_multiplier
            
            # Adding capacity with untrained staff may reduce efficiency slightly
            if mod.efficiency_modifier is None:  # Only auto-adjust if not explicitly set
                efficiency_impact = -(mod.capacity_increase / 10.0)  # 50% capacity = -5% efficiency
                modified_config[zone]['base_efficiency'] += efficiency_impact
                modified_config[zone]['base_efficiency'] = max(50, min(100, modified_config[zone]['base_efficiency']))
        
        # Add production lines
        if mod.add_production_lines:
            if 'production_lines' not in modified_config[zone]:
                modified_config[zone]['production_lines'] = []
            for line in mod.add_production_lines:
                modified_config[zone]['production_lines'].append(line.dict())
        
        # Remove production lines
        if mod.remove_line_ids and 'production_lines' in modified_config[zone]:
            modified_config[zone]['production_lines'] = [
                line for line in modified_config[zone]['production_lines']
                if line['line_id'] not in mod.remove_line_ids
            ]
    
    return modified_config

# API Endpoints

@router.post("/run", response_model=SimulationResult)
def run_simulation(request: SimulationRequest):
    """
    Run a digital twin simulation with specified modifications
    Compares baseline vs modified configuration
    """
    try:
        # Generate simulation ID
        sim_id = f"SIM-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate baseline metrics
        baseline_metrics = {
            'total_energy_kwh': 0,
            'total_cost_usd': 0,
            'total_co2_kg': 0,
            'avg_efficiency_pct': 0,
            'total_production_units': 0
        }
        
        zone_count = 0
        for zone_name, zone_config in BASE_ZONES.items():
            metrics = calculate_zone_metrics(zone_config, request.duration_hours)
            baseline_metrics['total_energy_kwh'] += metrics['energy_kwh']
            baseline_metrics['total_cost_usd'] += metrics['cost_usd']
            baseline_metrics['total_co2_kg'] += metrics['co2_kg']
            baseline_metrics['avg_efficiency_pct'] += metrics['efficiency_pct']
            baseline_metrics['total_production_units'] += metrics['production_units']
            zone_count += 1
        
        baseline_metrics['avg_efficiency_pct'] /= zone_count
        
        # Apply modifications
        modified_config = apply_modifications(BASE_ZONES, request.modifications)
        
        # Calculate modified metrics
        modified_metrics = {
            'total_energy_kwh': 0,
            'total_cost_usd': 0,
            'total_co2_kg': 0,
            'avg_efficiency_pct': 0,
            'total_production_units': 0
        }
        
        zone_details = []
        for zone_name, zone_config in modified_config.items():
            production_lines = zone_config.get('production_lines', None)
            metrics = calculate_zone_metrics(zone_config, request.duration_hours, production_lines)
            
            modified_metrics['total_energy_kwh'] += metrics['energy_kwh']
            modified_metrics['total_cost_usd'] += metrics['cost_usd']
            modified_metrics['total_co2_kg'] += metrics['co2_kg']
            modified_metrics['avg_efficiency_pct'] += metrics['efficiency_pct']
            modified_metrics['total_production_units'] += metrics['production_units']
            
            zone_details.append({
                'zone': zone_name,
                'energy_kwh': round(metrics['energy_kwh'], 2),
                'cost_usd': round(metrics['cost_usd'], 2),
                'efficiency_pct': round(metrics['efficiency_pct'], 2),
                'production_units': metrics['production_units'],
                'production_lines': len(production_lines) if production_lines else 0
            })
        
        modified_metrics['avg_efficiency_pct'] /= zone_count
        
        # Calculate deltas
        delta = {
            'energy_kwh': modified_metrics['total_energy_kwh'] - baseline_metrics['total_energy_kwh'],
            'cost_usd': modified_metrics['total_cost_usd'] - baseline_metrics['total_cost_usd'],
            'co2_kg': modified_metrics['total_co2_kg'] - baseline_metrics['total_co2_kg'],
            'efficiency_pct': modified_metrics['avg_efficiency_pct'] - baseline_metrics['avg_efficiency_pct'],
            'production_units': modified_metrics['total_production_units'] - baseline_metrics['total_production_units']
        }
        
        # Calculate percent changes
        percent_change = {}
        for key in delta.keys():
            if baseline_metrics['total_' + key if key != 'efficiency_pct' and key != 'production_units' else 'avg_' + key if key == 'efficiency_pct' else 'total_' + key] != 0:
                base_val = baseline_metrics['total_' + key if key != 'efficiency_pct' and key != 'production_units' else 'avg_' + key if key == 'efficiency_pct' else 'total_' + key]
                percent_change[key] = round((delta[key] / base_val) * 100, 2)
            else:
                percent_change[key] = 0
        
        # Generate recommendations
        recommendations = []
        if delta['energy_kwh'] < 0:
            recommendations.append(f"✅ Energy savings: {abs(delta['energy_kwh']):.2f} kWh ({abs(percent_change['energy_kwh']):.1f}% reduction)")
        elif delta['energy_kwh'] > 0:
            recommendations.append(f"⚠️ Energy increase: {delta['energy_kwh']:.2f} kWh ({percent_change['energy_kwh']:.1f}% increase)")
        
        if delta['production_units'] > 0:
            recommendations.append(f"📈 Production increase: {delta['production_units']} units ({percent_change['production_units']:.1f}% improvement)")
        
        if delta['efficiency_pct'] > 0:
            recommendations.append(f"⚡ Efficiency improvement: {delta['efficiency_pct']:.2f}%")
        
        if delta['cost_usd'] < -1000:
            recommendations.append(f"💰 Significant cost savings: ${abs(delta['cost_usd']):.2f} over {request.duration_hours} hours")
        
        # Store simulation
        simulation_store[sim_id] = {
            'name': request.simulation_name,
            'baseline': baseline_metrics,
            'modified': modified_metrics,
            'delta': delta,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return SimulationResult(
            simulation_id=sim_id,
            simulation_name=request.simulation_name,
            status="completed",
            zones_modified=len(request.modifications),
            comparison=SimulationComparison(
                baseline=SimulationMetrics(**baseline_metrics),
                modified=SimulationMetrics(**modified_metrics),
                delta=delta,
                percent_change=percent_change
            ),
            zone_details=zone_details,
            recommendations=recommendations,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@router.post("/what-if", response_model=WhatIfResult)
def what_if_analysis(scenario: WhatIfScenario):
    """
    Quick what-if analysis for a single parameter change
    Predicts impact without running full simulation
    """
    try:
        if scenario.zone_name not in BASE_ZONES:
            raise HTTPException(status_code=404, detail=f"Zone '{scenario.zone_name}' not found")
        
        zone_config = BASE_ZONES[scenario.zone_name]
        impact = {}
        feasibility = "feasible"
        risk_level = "low"
        recommendation = ""
        
        # Analyze based on parameter
        if scenario.parameter == "temperature":
            # Temperature change impact
            energy_impact = scenario.value_change * 2.0 if 'Paint' in scenario.zone_name else scenario.value_change * 0.5
            impact['energy_change_kwh_per_hour'] = round(energy_impact, 2)
            impact['cost_change_usd_per_hour'] = round(energy_impact * 0.12, 2)
            impact['co2_change_kg_per_hour'] = round(energy_impact * 0.233, 2)
            
            if abs(scenario.value_change) > 20:
                feasibility = "challenging"
                risk_level = "high"
                recommendation = "Large temperature changes may affect product quality and require equipment modifications"
            elif abs(scenario.value_change) > 10:
                risk_level = "medium"
                recommendation = "Moderate temperature change - monitor quality metrics closely"
            else:
                recommendation = "Safe temperature adjustment - proceed with gradual implementation"
        
        elif scenario.parameter == "efficiency":
            # Efficiency improvement impact
            current_efficiency = zone_config['base_efficiency']
            new_efficiency = current_efficiency + scenario.value_change
            
            if new_efficiency > 100:
                feasibility = "not_feasible"
                risk_level = "high"
                recommendation = "Target efficiency exceeds 100% - not achievable"
            elif new_efficiency < 50:
                feasibility = "not_feasible"
                risk_level = "high"
                recommendation = "Target efficiency too low - indicates equipment failure"
            else:
                production_impact = scenario.value_change * zone_config['production_capacity'] * 0.01
                impact['production_change_units_per_hour'] = round(production_impact, 1)
                impact['efficiency_new_pct'] = round(new_efficiency, 2)
                
                if scenario.value_change > 0:
                    recommendation = f"Efficiency improvement achievable through maintenance, training, or equipment upgrades"
                else:
                    recommendation = f"Efficiency decrease indicates potential issues - investigate root cause"
        
        elif scenario.parameter == "add_production_line":
            # Adding production line impact
            line_energy = zone_config['base_energy'] * 0.7  # New line is 70% of base
            impact['energy_increase_kwh_per_hour'] = round(line_energy, 2)
            impact['cost_increase_usd_per_hour'] = round(line_energy * 0.12, 2)
            impact['production_increase_units_per_hour'] = round(zone_config['production_capacity'] * 0.8, 1)
            
            recommendation = "Adding production line increases capacity but requires space, capital investment, and workforce"
            risk_level = "medium"
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown parameter: {scenario.parameter}")
        
        return WhatIfResult(
            scenario=scenario,
            predicted_impact=impact,
            feasibility=feasibility,
            risk_level=risk_level,
            recommendation=recommendation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"What-if analysis failed: {str(e)}")

@router.get("/templates")
def get_simulation_templates():
    """Get pre-configured simulation templates"""
    return {
        "templates": [
            {
                "name": "Add Paint Shop Production Line",
                "description": "Simulate adding a second production line to Paint Shop",
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
                ]
            },
            {
                "name": "Reduce Paint Shop Temperature",
                "description": "Reduce oven temperature by 10°C for energy savings",
                "modifications": [
                    {
                        "zone_name": "Paint Shop",
                        "temperature_offset": -10,
                        "efficiency_modifier": -1.5
                    }
                ]
            },
            {
                "name": "Optimize Assembly Line",
                "description": "Improve assembly efficiency through automation",
                "modifications": [
                    {
                        "zone_name": "General Assembly",
                        "efficiency_modifier": 5.0,
                        "energy_multiplier": 1.1
                    }
                ]
            },
            {
                "name": "Expand Body Shop Capacity",
                "description": "Add robotic welding line to Body Shop",
                "modifications": [
                    {
                        "zone_name": "Body Shop (BIW)",
                        "add_production_lines": [
                            {
                                "line_id": "robotic_welding_3",
                                "name": "Robotic Welding Line 3",
                                "energy_multiplier": 1.5,
                                "efficiency_modifier": 3.0,
                                "production_capacity": 70
                            }
                        ]
                    }
                ]
            }
        ]
    }

@router.get("/simulations")
def list_simulations():
    """List all stored simulations"""
    return {
        "simulations": [
            {
                "simulation_id": sim_id,
                "name": data['name'],
                "timestamp": data['timestamp'],
                "energy_delta_kwh": round(data['delta']['energy_kwh'], 2),
                "cost_delta_usd": round(data['delta']['cost_usd'], 2)
            }
            for sim_id, data in simulation_store.items()
        ],
        "total_count": len(simulation_store)
    }

@router.get("/simulations/{simulation_id}")
def get_simulation(simulation_id: str):
    """Get details of a specific simulation"""
    if simulation_id not in simulation_store:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return simulation_store[simulation_id]

@router.get("/zone-config")
def get_zone_configurations():
    """Get base zone configurations"""
    return {
        "zones": BASE_ZONES,
        "total_zones": len(BASE_ZONES)
    }
