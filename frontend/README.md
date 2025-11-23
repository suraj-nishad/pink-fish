# PlantOps Digital Twin Dashboard - Frontend

Modern React-based UI for the Digital Twin Dashboard, built with IBM Carbon Design System.

## 🎨 Design System

- **Framework**: React 18 + Vite
- **UI Library**: IBM Carbon Design System (Carbon React)
- **Styling**: SCSS with Carbon themes
- **Icons**: Carbon Icons React
- **Theme**: Carbon G100 (Dark theme optimized for manufacturing/operations)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── AppHeader.jsx    # Main navigation header
│   │   └── ZoneCard.jsx     # Zone status card component
│   ├── pages/               # Main application pages
│   │   ├── Dashboard.jsx    # Real-time zone monitoring
│   │   ├── Simulation.jsx   # What-if scenario simulation
│   │   └── Analytics.jsx    # Analytics & insights (coming soon)
│   ├── App.jsx              # Main app component with routing
│   ├── App.scss             # App-level styles
│   ├── main.jsx             # Application entry point
│   └── index.scss           # Global styles & Carbon theme setup
├── index.html               # HTML template
├── package.json             # Dependencies & scripts
└── vite.config.js           # Vite configuration
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Production files will be in the `dist/` directory.

## 📄 Pages

### 1. Dashboard (`/`)
- **Purpose**: Real-time monitoring of all manufacturing zones
- **Features**:
  - Live zone status cards with color-coded indicators (Green/Amber/Red)
  - KPI summary tiles (Total Zones, Plant Status, Last Updated)
  - Auto-refresh every 30 seconds
  - Energy, temperature, efficiency metrics per zone
  - Alert notifications for critical zones

### 2. Simulation (`/simulation`)
- **Purpose**: Run "what-if" scenarios before implementing changes
- **Features**:
  - Configure simulations with zone selection
  - Multiple modification types:
    - Add/remove production lines
    - Temperature adjustments
    - Efficiency modifiers
    - Energy multipliers
  - Real-time simulation results showing:
    - Energy impact (kWh & %)
    - Cost impact ($)
    - Production impact (units)
    - Efficiency changes
  - AI-powered recommendations

### 3. Analytics (`/analytics`)
- **Status**: Coming Soon
- **Planned Features**:
  - Historical trend analysis
  - ML-powered anomaly detection visualizations
  - Energy consumption forecasting
  - Predictive maintenance scheduling
  - Cost optimization recommendations

## 🎨 UI Components

### AppHeader
- IBM-style navigation header
- Global actions (Notifications, App Switcher, User Profile)
- Responsive navigation menu

### ZoneCard
- Status indicator (Green/Amber/Red) with visual feedback
- Key metrics display:
  - Energy consumption (kWh)
  - Temperature (°C)
  - Efficiency (%)
  - Cost ($/hr)
  - CO₂ emissions (kg)
- Alert tags for critical issues
- Hover effects for better UX

## 🌈 IBM Carbon Theme

The UI uses IBM Carbon's **G100 theme** (dark theme), optimized for:
- Manufacturing/operations dashboards
- Extended monitoring sessions
- Reduced eye strain
- Professional, enterprise look

### Color Palette
- **Success (Green)**: `#24A148` - Normal operations
- **Warning (Amber)**: `#FFC200` - Warning state
- **Error (Red)**: `#DA1E28` - Critical state
- **Primary**: IBM Blue - Interactive elements
- **Background**: Dark gray - Main background
- **Text**: White/Light gray - Text content

## 🔌 API Integration

The frontend connects to the FastAPI backend via axios:

```javascript
// Proxy configuration in vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

### API Endpoints Used

1. **GET `/api/zones/status`**
   - Fetches real-time status of all zones
   - Auto-refreshes every 30 seconds

2. **POST `/api/simulation/run`**
   - Runs digital twin simulations
   - Returns impact analysis and recommendations

## 📱 Responsive Design

- **Desktop**: Full-width layout with grid system
- **Tablet**: Responsive columns with Carbon Grid
- **Mobile**: Single-column stacked layout (coming soon)

## 🎯 Key Features

### Real-time Monitoring
- Live zone status updates
- Color-coded status indicators
- Auto-refresh capabilities
- Error handling with inline notifications

### Interactive Simulations
- Form-based simulation configuration
- Instant results visualization
- Impact analysis across multiple metrics
- AI-powered recommendations

### IBM Design Language
- Professional, enterprise-grade UI
- Consistent with IBM product ecosystem
- Accessibility built-in (Carbon components)
- Dark theme optimized for operations

## 🛠️ Technologies

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **IBM Carbon React**: Enterprise UI component library
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing
- **SCSS**: Enhanced CSS with variables and nesting

## 🚧 Future Enhancements

1. **Analytics Page**
   - Historical charts (Recharts integration)
   - Trend analysis
   - Predictive visualizations

2. **ChatOps Integration**
   - Natural language queries
   - Conversational interface
   - watsonx Assistant integration

3. **Advanced Simulations**
   - Multi-zone simulations
   - Scenario comparison
   - Save/load simulation configurations

4. **Mobile Optimization**
   - Responsive layouts for mobile devices
   - Touch-optimized controls
   - Progressive Web App (PWA)

## 📝 Development Guidelines

### Component Structure
```jsx
import { Component } from '@carbon/react';
import './ComponentName.scss';

const ComponentName = ({ prop1, prop2 }) => {
  // Component logic
  return (
    <div className="component-name">
      {/* JSX */}
    </div>
  );
};

export default ComponentName;
```

### Styling Convention
- Use BEM methodology for class names
- Scope styles with component-specific classes
- Leverage Carbon design tokens
- Keep SCSS modular (one file per component)

### State Management
- React hooks (useState, useEffect) for component state
- No global state management needed yet
- Consider Context API or Redux for larger scale

## 🤝 Contributing

1. Follow IBM Carbon design guidelines
2. Maintain consistent component structure
3. Write clean, commented code
4. Test API integrations thoroughly
5. Ensure responsive design

## 📄 License

Part of the PlantOps Digital Twin Dashboard project.

---

**Built with ❤️ using IBM Carbon Design System**
