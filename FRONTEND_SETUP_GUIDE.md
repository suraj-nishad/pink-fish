# PlantOps Digital Twin Dashboard - Complete Setup Guide

## 🎯 What You Have Now

A complete, IBM-styled Digital Twin Dashboard with:

### ✅ **Frontend** (React + IBM Carbon)
- 📊 **Dashboard Page**: Real-time zone monitoring with status cards
- 🔬 **Simulation Page**: Interactive what-if scenario testing
- 📈 **Analytics Page**: Placeholder for future features
- 🎨 **IBM Design**: Professional Carbon Design System theme (G100 dark)

### ✅ **Backend** (FastAPI + Python)
- 🔌 **REST API**: All endpoints working
- 🤖 **Simulation Engine**: Production line modifications fixed
- 🧠 **ML Models**: Anomaly detection & forecasting
- 📊 **Data**: 30 days of plant data

---

## 🚀 Quick Start

### Option 1: Run Everything Locally

#### Step 1: Start the Backend
```bash
cd /Users/suraj/digital-twin

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Backend will run on: `http://localhost:8000`

#### Step 2: Start the Frontend
Open a **new terminal**:

```bash
cd /Users/suraj/digital-twin/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

#### Step 3: Open in Browser
Visit: **http://localhost:3000**

---

## 📁 Project Structure Overview

```
digital-twin/
├── backend/                    # FastAPI Backend
│   ├── app.py                  # Main API server
│   ├── routes/
│   │   ├── ml_routes.py        # ML predictions
│   │   └── simulation_routes.py # Simulations (FIXED!)
│   └── models/                 # ML models
│
├── frontend/                   # React Frontend (NEW!)
│   ├── src/
│   │   ├── components/         # UI components
│   │   │   ├── AppHeader.jsx   # Navigation
│   │   │   └── ZoneCard.jsx    # Zone cards
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx   # Main dashboard
│   │   │   ├── Simulation.jsx  # Simulation tool
│   │   │   └── Analytics.jsx   # Coming soon
│   │   ├── App.jsx             # Root component
│   │   └── main.jsx            # Entry point
│   └── package.json
│
├── data/                       # Plant data
└── test_production_line.py     # Test script
```

---

## 🎨 UI Pages Breakdown

### 1. Dashboard (`/`)
**Real-time plant monitoring**

Features:
- ✅ Live zone status cards (Green/Amber/Red indicators)
- ✅ KPI tiles showing:
  - Total zones
  - Plant status (Operational/Critical)
  - Last update time
- ✅ Auto-refresh every 30 seconds
- ✅ Each zone shows:
  - Energy consumption (kWh)
  - Temperature (°C)
  - Efficiency (%)
  - Cost ($/hr)
  - CO₂ emissions (kg)
- ✅ Alert tags for critical issues

### 2. Simulation (`/simulation`)
**What-if scenario testing**

Features:
- ✅ Interactive form to configure simulations
- ✅ Select zone from dropdown
- ✅ Choose modification type:
  - Add production lines (integer - FIXED!)
  - Temperature offset
  - Efficiency modifier
  - Energy multiplier
- ✅ Set duration (1-720 hours)
- ✅ Real-time results showing:
  - Energy impact (+/- kWh and %)
  - Cost impact ($)
  - Production impact (units)
  - Efficiency changes
- ✅ AI-powered recommendations

### 3. Analytics (`/analytics`)
**Coming soon!**

Planned:
- Historical trends with charts
- ML anomaly visualizations
- Energy forecasting
- Predictive maintenance

---

## 🎨 Design Highlights

### IBM Carbon Design System
The UI uses IBM's professional design language:

**Theme**: Carbon G100 (Dark)
- Optimized for manufacturing/operations
- Reduces eye strain for extended monitoring
- Professional enterprise look

**Colors**:
- 🟢 **Green** (#24A148): Normal operations
- 🟡 **Amber** (#FFC200): Warning state
- 🔴 **Red** (#DA1E28): Critical state
- 🔵 **Blue**: Interactive elements

**Typography**: IBM Plex Sans (professional, readable)

**Components**: Enterprise-grade Carbon React components
- Tiles, Grids, Forms
- Buttons, Notifications
- Tags, Loading states

---

## 🔧 Development Workflow

### Running Both Servers

**Terminal 1** - Backend:
```bash
cd /Users/suraj/digital-twin
source venv/bin/activate
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2** - Frontend:
```bash
cd /Users/suraj/digital-twin/frontend
npm run dev
```

### API Proxy
The frontend automatically proxies API requests:
- Frontend request: `http://localhost:3000/api/zones/status`
- Proxied to: `http://localhost:8000/api/zones/status`

Configured in `frontend/vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

---

## 🧪 Testing the UI

### Test Dashboard
1. Go to `http://localhost:3000`
2. You should see 7 zone cards with live data
3. Status indicators should show current state
4. Metrics should update every 30 seconds

### Test Simulation
1. Click "Simulation" in the header
2. Select "Paint Shop" zone
3. Choose "Add Production Lines"
4. Enter value: `1`
5. Duration: `24` hours
6. Click "Run Simulation"
7. Results should show:
   - ✅ +28,800 kWh (+28%)
   - ✅ +$3,456 cost
   - ✅ +1,080 units production

---

## 📦 Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

Output: `frontend/dist/` directory

### Deployment Options

#### Option 1: Serve with Python
```bash
cd frontend/dist
python3 -m http.server 3000
```

#### Option 2: Deploy to Vercel/Netlify
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

#### Option 3: Serve from FastAPI
Add static file serving to `backend/app.py`:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
```

---

## 🎯 Key Features Showcase

### For Demo/Presentation

1. **Dashboard Overview** (30 seconds)
   - Show live monitoring
   - Point out color-coded status
   - Highlight auto-refresh
   - Show KPI tiles

2. **Run Simulation** (1 minute)
   - Navigate to Simulation page
   - Configure: "Add production line to Paint Shop"
   - Run simulation
   - Show results: +28% energy, +$3,456 cost
   - Read AI recommendations

3. **watsonx Integration** (1 minute)
   - Explain how watsonx agent calls same APIs
   - Show that agent can ask: "What if we add a production line?"
   - Backend returns structured data
   - Same as UI but conversational

---

## 🐛 Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API connection errors
- Check backend is running on port 8000
- Check proxy configuration in `vite.config.js`
- Check CORS is enabled in `backend/app.py`

### Blank dashboard
- Check browser console for errors
- Verify `/api/zones/status` returns data:
  ```bash
  curl http://localhost:8000/api/zones/status
  ```

### Simulation errors
- Check backend logs for details
- Verify payload format matches API expectations
- Test with curl first:
  ```bash
  curl -X POST http://localhost:8000/api/simulation/run \
    -H "Content-Type: application/json" \
    -d '{"simulation_name":"Test","modifications":"[{\"zone_name\":\"Paint Shop\",\"add_production_lines\":1}]","duration_hours":24}'
  ```

---

## 📚 Next Steps

### Immediate
1. ✅ Install frontend dependencies
2. ✅ Start both servers
3. ✅ Test dashboard and simulation
4. ✅ Try watsonx agent integration

### Short-term Enhancements
- [ ] Add historical charts to Dashboard
- [ ] Implement ChatOps widget
- [ ] Add dark/light theme toggle
- [ ] Mobile responsive improvements
- [ ] Save simulation results

### Medium-term Features
- [ ] Build Analytics page with Recharts
- [ ] Add user authentication
- [ ] Real-time WebSocket updates
- [ ] Export simulation reports (PDF)
- [ ] Multi-zone comparison view

---

## 🎓 Learning Resources

### IBM Carbon Design
- [Carbon Design System](https://carbondesignsystem.com/)
- [Carbon React Components](https://react.carbondesignsystem.com/)
- [Carbon Icons](https://www.carbondesignsystem.com/guidelines/icons/library/)

### React + Vite
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)

---

## 🤝 Contributing

### Adding a New Page
1. Create `frontend/src/pages/NewPage.jsx`
2. Create `frontend/src/pages/NewPage.scss`
3. Add route in `frontend/src/App.jsx`:
   ```jsx
   <Route path="/newpage" element={<NewPage />} />
   ```
4. Add link in `AppHeader.jsx`:
   ```jsx
   <HeaderMenuItem href="/newpage">New Page</HeaderMenuItem>
   ```

### Adding a New Component
1. Create `frontend/src/components/NewComponent.jsx`
2. Create `frontend/src/components/NewComponent.scss`
3. Import and use in pages

---

## 📞 Support

For issues:
1. Check browser console for errors
2. Check backend logs
3. Verify API endpoints with curl
4. Review CORS settings
5. Check proxy configuration

---

**🎉 You now have a complete, IBM-styled Digital Twin Dashboard!**

Start both servers and visit `http://localhost:3000` to see it in action.
