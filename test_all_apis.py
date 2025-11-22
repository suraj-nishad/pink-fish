#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Digital Twin Dashboard
Tests all endpoints including ML models and simulations
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
RESULTS = []

def log_test(name, status, details=""):
    """Log test results"""
    result = {
        "test": name,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    RESULTS.append(result)
    icon = "✅" if status == "PASS" else "❌"
    print(f"{icon} {name}: {status}")
    if details:
        print(f"   {details}")

def test_health_endpoints():
    """Test health check endpoints"""
    print("\n" + "="*60)
    print("TESTING HEALTH ENDPOINTS")
    print("="*60)
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /", "PASS", f"Status: {data.get('status')}")
        else:
            log_test("GET /", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /", "FAIL", str(e))
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /health", "PASS", f"Records: {data.get('records_loaded')}")
        else:
            log_test("GET /health", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /health", "FAIL", str(e))

def test_monitoring_endpoints():
    """Test plant monitoring endpoints"""
    print("\n" + "="*60)
    print("TESTING MONITORING ENDPOINTS")
    print("="*60)
    
    # Test zones status
    try:
        response = requests.get(f"{BASE_URL}/api/zones/status")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/zones/status", "PASS", 
                    f"Zones: {data.get('total_zones')}, Critical: {data.get('zones_critical')}")
        else:
            log_test("GET /api/zones/status", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/zones/status", "FAIL", str(e))
    
    # Test zone history
    try:
        response = requests.get(f"{BASE_URL}/api/zones/paint/history?hours=24")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/zones/paint/history", "PASS", 
                    f"Data points: {data.get('data_points')}")
        else:
            log_test("GET /api/zones/paint/history", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/zones/paint/history", "FAIL", str(e))
    
    # Test KPIs
    try:
        response = requests.get(f"{BASE_URL}/api/kpis?hours=24")
        if response.status_code == 200:
            data = response.json()
            kpis = data.get('kpis', {})
            log_test("GET /api/kpis", "PASS", 
                    f"Energy: {kpis.get('total_energy_kwh'):.0f} kWh, Cost: ${kpis.get('total_cost_usd'):.2f}")
        else:
            log_test("GET /api/kpis", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/kpis", "FAIL", str(e))

def test_analysis_endpoints():
    """Test AI analysis endpoints"""
    print("\n" + "="*60)
    print("TESTING ANALYSIS ENDPOINTS")
    print("="*60)
    
    # Test energy analysis
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-energy",
            params={"zones": ["Paint Shop", "General Assembly"], "timeframe": "last_24h"}
        )
        if response.status_code == 200:
            data = response.json()
            log_test("POST /api/analyze-energy", "PASS", 
                    f"Hotspots: {len(data.get('hotspots', []))}, Recommendations: {len(data.get('recommendations', []))}")
        else:
            log_test("POST /api/analyze-energy", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/analyze-energy", "FAIL", str(e))
    
    # Test ChatOps
    try:
        response = requests.post(
            f"{BASE_URL}/api/chatops",
            json={"query": "What is the plant status?", "user": "test_user"}
        )
        if response.status_code == 200:
            data = response.json()
            log_test("POST /api/chatops", "PASS", 
                    f"Confidence: {data.get('confidence'):.2%}")
        else:
            log_test("POST /api/chatops", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/chatops", "FAIL", str(e))
    
    # Test maintenance scheduling
    try:
        response = requests.post(
            f"{BASE_URL}/api/maintenance/schedule",
            json={"zone": "Paint Shop", "issue": "Test issue", "priority": "high"}
        )
        if response.status_code == 200:
            data = response.json()
            log_test("POST /api/maintenance/schedule", "PASS", 
                    f"Ticket: {data.get('ticket_id')}")
        else:
            log_test("POST /api/maintenance/schedule", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/maintenance/schedule", "FAIL", str(e))

def test_ml_endpoints():
    """Test machine learning endpoints"""
    print("\n" + "="*60)
    print("TESTING ML ENDPOINTS")
    print("="*60)
    
    # Test model info
    try:
        response = requests.get(f"{BASE_URL}/api/ml/model-info")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/ml/model-info", "PASS", 
                    f"Detector loaded: {data.get('anomaly_detector', {}).get('loaded')}, "
                    f"Forecaster loaded: {data.get('energy_forecaster', {}).get('loaded')}")
        else:
            log_test("GET /api/ml/model-info", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/ml/model-info", "FAIL", str(e))
    
    # Test anomaly detection
    try:
        response = requests.post(
            f"{BASE_URL}/api/ml/anomaly-detection",
            json={"zone": "Paint Shop", "hours": 48}
        )
        if response.status_code == 200:
            data = response.json()
            log_test("POST /api/ml/anomaly-detection", "PASS", 
                    f"Records: {data.get('total_records')}, Anomalies: {data.get('anomalies_detected')}, "
                    f"Rate: {data.get('anomaly_rate'):.2%}")
        else:
            log_test("POST /api/ml/anomaly-detection", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/ml/anomaly-detection", "FAIL", str(e))
    
    # Test energy forecast
    try:
        response = requests.post(
            f"{BASE_URL}/api/ml/energy-forecast",
            json={
                "zone": "Paint Shop",
                "hours_ahead": 24,
                "current_temp": 185.0,
                "current_efficiency": 85.0
            }
        )
        if response.status_code == 200:
            data = response.json()
            log_test("POST /api/ml/energy-forecast", "PASS", 
                    f"Forecast hours: {data.get('forecast_hours')}, "
                    f"Total energy: {data.get('total_predicted_energy'):.0f} kWh, "
                    f"Confidence: {data.get('confidence_level')}")
        else:
            log_test("POST /api/ml/energy-forecast", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/ml/energy-forecast", "FAIL", str(e))
    
    # Test predictive maintenance
    try:
        response = requests.get(f"{BASE_URL}/api/ml/predictive-maintenance")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/ml/predictive-maintenance", "PASS", 
                    f"Zones needing maintenance: {data.get('total_zones_needing_maintenance')}, "
                    f"High priority: {data.get('high_priority_count')}")
        else:
            log_test("GET /api/ml/predictive-maintenance", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/ml/predictive-maintenance", "FAIL", str(e))

def test_simulation_endpoints():
    """Test digital twin simulation endpoints"""
    print("\n" + "="*60)
    print("TESTING SIMULATION ENDPOINTS")
    print("="*60)
    
    # Test zone configuration
    try:
        response = requests.get(f"{BASE_URL}/api/simulation/zone-config")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/simulation/zone-config", "PASS", 
                    f"Total zones: {data.get('total_zones')}")
        else:
            log_test("GET /api/simulation/zone-config", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/simulation/zone-config", "FAIL", str(e))
    
    # Test templates
    try:
        response = requests.get(f"{BASE_URL}/api/simulation/templates")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/simulation/templates", "PASS", 
                    f"Templates available: {len(data.get('templates', []))}")
        else:
            log_test("GET /api/simulation/templates", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/simulation/templates", "FAIL", str(e))
    
    # Test what-if analysis
    try:
        response = requests.post(
            f"{BASE_URL}/api/simulation/what-if",
            json={
                "scenario_name": "Test Temperature Reduction",
                "description": "Test reducing temperature",
                "zone": "Paint Shop",
                "parameter": "temperature",
                "value_change": -10
            }
        )
        if response.status_code == 200:
            data = response.json()
            impact = data.get('predicted_impact', {})
            log_test("POST /api/simulation/what-if", "PASS", 
                    f"Feasibility: {data.get('feasibility')}, "
                    f"Risk: {data.get('risk_level')}, "
                    f"Energy impact: {impact.get('energy_change_kwh_per_hour', 0):.2f} kWh/h")
        else:
            log_test("POST /api/simulation/what-if", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/simulation/what-if", "FAIL", str(e))
    
    # Test full simulation
    try:
        response = requests.post(
            f"{BASE_URL}/api/simulation/run",
            json={
                "simulation_name": "Test Simulation",
                "modifications": [
                    {
                        "zone_name": "Paint Shop",
                        "temperature_offset": -5,
                        "efficiency_modifier": 1.0
                    }
                ],
                "duration_hours": 24
            }
        )
        if response.status_code == 200:
            data = response.json()
            comparison = data.get('comparison', {})
            delta = comparison.get('delta', {})
            log_test("POST /api/simulation/run", "PASS", 
                    f"Simulation ID: {data.get('simulation_id')}, "
                    f"Energy delta: {delta.get('energy_kwh', 0):.0f} kWh, "
                    f"Cost delta: ${delta.get('cost_usd', 0):.2f}")
        else:
            log_test("POST /api/simulation/run", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("POST /api/simulation/run", "FAIL", str(e))
    
    # Test simulations list
    try:
        response = requests.get(f"{BASE_URL}/api/simulation/simulations")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/simulation/simulations", "PASS", 
                    f"Total simulations: {data.get('total_count')}")
        else:
            log_test("GET /api/simulation/simulations", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/simulation/simulations", "FAIL", str(e))

def test_config_endpoints():
    """Test configuration endpoints"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION ENDPOINTS")
    print("="*60)
    
    # Test get config
    try:
        response = requests.get(f"{BASE_URL}/api/config")
        if response.status_code == 200:
            data = response.json()
            log_test("GET /api/config", "PASS", 
                    f"Energy threshold red: {data.get('ENERGY_THRESHOLD_RED')}")
        else:
            log_test("GET /api/config", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("GET /api/config", "FAIL", str(e))

def generate_report():
    """Generate test report"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(RESULTS)
    passed = sum(1 for r in RESULTS if r['status'] == 'PASS')
    failed = sum(1 for r in RESULTS if r['status'] == 'FAIL')
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)")
    
    if failed > 0:
        print("\n❌ Failed Tests:")
        for r in RESULTS:
            if r['status'] == 'FAIL':
                print(f"  - {r['test']}: {r['details']}")
    
    # Save report to file
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "success_rate": f"{passed/total*100:.1f}%"
        },
        "results": RESULTS
    }
    
    with open('/Users/suraj/digital-twin/test_results.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📊 Full report saved to: test_results.json")
    
    # Return exit code
    return 0 if failed == 0 else 1

def main():
    """Run all tests"""
    print("="*60)
    print("DIGITAL TWIN API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Wait for server to be ready
    print("\nWaiting for server to be ready...")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=1)
            if response.status_code == 200:
                print("✅ Server is ready!\n")
                break
        except:
            time.sleep(1)
    else:
        print("❌ Server not responding after 10 seconds")
        return 1
    
    # Run all test suites
    test_health_endpoints()
    test_monitoring_endpoints()
    test_analysis_endpoints()
    test_ml_endpoints()
    test_simulation_endpoints()
    test_config_endpoints()
    
    # Generate report
    return generate_report()

if __name__ == "__main__":
    exit(main())
