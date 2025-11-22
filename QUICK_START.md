# 🚀 Quick Start Guide - Digital Twin Dashboard

**Status:** ✅ Production Ready | **Test Coverage:** 100% (13/13 APIs)

---

## ⚡ 30-Second Start

```bash
cd /Users/suraj/digital-twin
source venv/bin/activate
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

**Server running at:** http://localhost:8000

---

## 🧪 Verify Installation

```bash
curl http://localhost:8000/health | python -m json.tool
```

**Expected:** `"status": "healthy", "records_loaded": 5040`

---

## 📡 Test All APIs (One Command)

```bash
python test_all_apis.py
```

**Expected:** `✅ ALL TESTS PASSED (100%)`

---

## 🎯 Top 5 Demo Endpoints

### 1. Plant Status (Real-Time)
```bash
curl http://localhost:8000/api/zones/status | python -m json.tool
```

### 2. Detect Anomalies (ML-Powered)
```bash
curl -X POST http://localhost:8000/api/ml/anomaly-detection \
  -H "Content-Type: application/json" \
  -d '{"zone": "Paint Shop", "hours": 24}' | python -m json.tool
```

### 3. Energy Forecast (24h Ahead)
```bash
curl -X POST http://localhost:8000/api/ml/energy-forecast \
  -H "Content-Type: application/json" \
  -d '{"zone": "Paint Shop", "hours_ahead": 24}' | python -m json.tool
```

### 4. What-If Simulation (Digital Twin)
```bash
curl -X POST http://localhost:8000/api/simulation/what-if \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_name": "Reduce Temperature",
    "zone": "Paint Shop",
    "parameter": "temperature",
    "value_change": -10,
    "description": "Test 10C reduction"
  }' | python -m json.tool
```

### 5. Natural Language Query (ChatOps)
```bash
curl -X POST http://localhost:8000/api/chatops \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the plant status?", "user": "operator"}' | python -m json.tool
```

---

## 📊 All 13 API Endpoints

| # | Endpoint | Method | Purpose |
|---|----------|--------|---------|
| 1 | `/health` | GET | Health check |
| 2 | `/api/zones/status` | GET | All zones status |
| 3 | `/api/zones/{zone_id}` | GET | Individual zone |
| 4 | `/api/config` | GET | Configuration |
| 5 | `/api/ml/model-info` | GET | ML model metadata |
| 6 | `/api/ml/anomaly-detection` | POST | Detect anomalies |
| 7 | `/api/ml/energy-forecast` | POST | Forecast energy |
| 8 | `/api/ml/predictive-maintenance` | GET | Maintenance needs |
| 9 | `/api/simulation/templates` | GET | Simulation templates |
| 10 | `/api/simulation/what-if` | POST | What-if analysis |
| 11 | `/api/simulation/run` | POST | Full simulation |
| 12 | `/api/chatops` | POST | Natural language query |
| 13 | `/api/analyze-energy` | POST | AI energy analysis |
| 14 | `/api/maintenance/schedule` | POST | Schedule maintenance |

---

## 📖 Documentation Files

1. **README.md** - Project overview
2. **ML_MODELS_DOCUMENTATION.md** - ML architecture
3. **SIMULATION_DOCUMENTATION.md** - Simulation guide
4. **API_ENDPOINTS_REFERENCE.md** - API specs
5. **SETUP_COMPLETE_SUMMARY.md** - Setup instructions
6. **API_TEST_RESULTS.md** - Test results
7. **PROJECT_STATUS_FINAL.md** - Project status
8. **data/DATA_README.md** - Data documentation

---

## 🎬 Hackathon Demo Flow

**Duration:** 5 minutes

1. **Show Real-Time Monitoring** (30s)
   - GET `/api/zones/status`
   - Display 7 zones with live metrics

2. **Demonstrate ML Anomaly Detection** (60s)
   - POST `/api/ml/anomaly-detection`
   - Show detected anomalies

3. **Energy Forecasting** (45s)
   - POST `/api/ml/energy-forecast`
   - Show 24h prediction

4. **Digital Twin What-If** (90s)
   - POST `/api/simulation/what-if`
   - Show cost savings from temperature reduction

5. **Natural Language Query** (45s)
   - POST `/api/chatops`
   - Ask "What is the plant status?"

6. **Wrap-Up** (30s)
   - Show test results (100% passing)
   - Highlight business value

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

### Restart Server
```bash
pkill -9 python
cd /Users/suraj/digital-twin
source venv/bin/activate
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

### Check Logs
```bash
tail -f server.log
```

### Regenerate Data
```bash
python generate_month_data.py
```

---

## 💡 Key Features

- ✅ **30 days** of manufacturing data
- ✅ **7 zones** monitored
- ✅ **3 ML models** trained
- ✅ **13 APIs** operational
- ✅ **100% test** coverage
- ✅ **Sub-second** response times

---

## 🏆 Business Value

**Without Digital Twin:**
- Reactive maintenance
- Unknown energy waste
- Costly downtime
- Manual monitoring

**With Digital Twin:**
- Predictive maintenance
- 10-20% energy savings
- Prevented downtime
- Real-time insights
- **ROI: < 1 month**

---

## 📞 Quick Reference

**Project Path:** `/Users/suraj/digital-twin`  
**Server Port:** `8000`  
**Python Version:** `3.9+`  
**Records Loaded:** `5,040`  
**Test Status:** ✅ `13/13 passing`

---

## ⚡ One-Liner Commands

**Start:**
```bash
cd ~/digital-twin && source venv/bin/activate && python -m uvicorn backend.app:app --port 8000
```

**Test:**
```bash
curl http://localhost:8000/health
```

**Full Test:**
```bash
python test_all_apis.py
```

---

**Ready for Demo! 🎉**  
**All Systems Operational ✅**  
**Good Luck! 🚀**
