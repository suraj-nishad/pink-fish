# PlantOps Digital Twin - UI Visual Design

## 🎨 Visual Style Guide

### Design Philosophy
**IBM Carbon Design System + Manufacturing Operations**

- Professional, enterprise-grade interface
- Dark theme (G100) optimized for extended monitoring
- Clear visual hierarchy with color-coded status indicators
- Data-dense but scannable layout
- Responsive and accessible

---

## 📱 Page Layouts

### 1. Dashboard Page (`/`)

```
┌─────────────────────────────────────────────────────────────────┐
│ IBM PlantOps Digital Twin    [Dashboard] [Simulation] [Analytics] │
│                                               🔔 ⚙️ 👤            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📊 Manufacturing Plant Overview                                 │
│  Real-time monitoring of all production zones                    │
│                                                                   │
│  [🟢 5 Normal]  [🟡 1 Warning]  [🔴 1 Critical]                  │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ 🗄️  Total Zones  │  │ ⚙️  Plant Status│  │ 🕐  Last Updated│ │
│  │      7           │  │   Critical      │  │   2:45:32 PM    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                   │
│  Zone Cards Grid:                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────┐│
│  │ ✅ Stamping  │  │ ✅ Body Shop │  │ ⚠️ Paint Shop│  │ ✅ As│
│  │              │  │              │  │              │  │      │
│  │ ⚡ 450 kWh   │  │ ⚡ 800 kWh   │  │ ⚡ 1250 kWh  │  │ ⚡ 68│
│  │ 🌡️ 65°C      │  │ 🌡️ 55°C      │  │ 🌡️ 195°C     │  │ 🌡️ 2│
│  │ 💡 92%       │  │ 💡 89%       │  │ 💡 78%       │  │ 💡 88│
│  │              │  │              │  │ 🔴 High Temp │  │      │
│  │ $54.00/hr    │  │ $96.00/hr    │  │ $150.00/hr   │  │ $81.│
│  │ 110 kg CO₂   │  │ 186 kg CO₂   │  │ 291 kg CO₂   │  │ 158 │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────┘│
│                                                                   │
│  [Continue with remaining zones...]                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Key Visual Elements**:
- **Header**: IBM branding, dark background, white text
- **Status Badges**: Color-coded pills (Green/Amber/Red) with counts
- **KPI Tiles**: Large numbers, icon + label layout, subtle background
- **Zone Cards**: 
  - Border-left color indicates status (green/amber/red)
  - Icon-based metrics for quick scanning
  - Hover effect: slight elevation + shadow
  - Alert tags appear when issues detected

**Color Scheme**:
```
Background:    #161616 (Carbon G100 background)
Cards:         #262626 (Carbon layer-01)
Text Primary:  #F4F4F4 (white)
Text Secondary: #C6C6C6 (light gray)
Success:       #24A148 (green)
Warning:       #FFC200 (amber)
Error:         #DA1E28 (red)
Interactive:   #0F62FE (IBM blue)
```

---

### 2. Simulation Page (`/simulation`)

```
┌─────────────────────────────────────────────────────────────────┐
│ IBM PlantOps Digital Twin    [Dashboard] [Simulation] [Analytics] │
│                                               🔔 ⚙️ 👤            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  🔬 Digital Twin Simulation                                      │
│  Test "what-if" scenarios and predict impact before implementation│
│                                                                   │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │ Configure Simulation    │  │  Simulation Results          │  │
│  │                         │  │                              │  │
│  │ Simulation Name:        │  │  ✅ Simulation Complete      │  │
│  │ [________________]      │  │  ID: SIM-20251123134512      │  │
│  │                         │  │                              │  │
│  │ Select Zone:            │  │  ┌────────────────────────┐  │  │
│  │ [Paint Shop      ▼]     │  │  │ Energy Impact          │  │  │
│  │                         │  │  │ +28,800 kWh            │  │  │
│  │ Modification Type:      │  │  │ +28.0%                 │  │  │
│  │ [Add Production Lines▼] │  │  └────────────────────────┘  │  │
│  │                         │  │                              │  │
│  │ Value:                  │  │  ┌────────────────────────┐  │  │
│  │ [1              ]       │  │  │ Cost Impact            │  │  │
│  │                         │  │  │ +$3,456.00             │  │  │
│  │ Duration (hours):       │  │  │ +28.0%                 │  │  │
│  │ [24             ]       │  │  └────────────────────────┘  │  │
│  │                         │  │                              │  │
│  │ [▶️ Run Simulation]     │  │  ┌────────────────────────┐  │  │
│  │ [🔄 Reset]              │  │  │ Production Impact      │  │  │
│  │                         │  │  │ +1,080 units           │  │  │
│  └─────────────────────────┘  │  │ +6.2%                  │  │  │
│                                │  └────────────────────────┘  │  │
│                                │                              │  │
│                                │  ┌────────────────────────┐  │  │
│                                │  │ Efficiency Impact      │  │  │
│                                │  │ -0.7%                  │  │  │
│                                │  └────────────────────────┘  │  │
│                                │                              │  │
│                                │  Recommendations:            │  │
│                                │  • ⚠️ Energy increase: 28.8K │
│                                │  • 📈 Production +1,080 units│
│                                └──────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Key Visual Elements**:
- **Two-column layout**: Form (left) + Results (right)
- **Form styling**: Carbon input components, dropdowns, number inputs
- **Primary button**: IBM blue with icon
- **Results cards**: Large numbers, percentage changes, color-coded
- **Impact indicators**: Positive values in white, negative in subtle red/green

---

### 3. Analytics Page (`/analytics`)

```
┌─────────────────────────────────────────────────────────────────┐
│ IBM PlantOps Digital Twin    [Dashboard] [Simulation] [Analytics] │
│                                               🔔 ⚙️ 👤            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📈 Analytics & Insights                                         │
│  Historical trends and AI-powered recommendations                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                            │   │
│  │                    🚧 Coming Soon                          │   │
│  │                                                            │   │
│  │  Advanced analytics features including:                   │   │
│  │                                                            │   │
│  │  • Historical trend analysis with interactive charts      │   │
│  │  • ML-powered anomaly detection visualizations            │   │
│  │  • Energy consumption forecasting                         │   │
│  │  • Predictive maintenance scheduling                      │   │
│  │  • Cost optimization recommendations                      │   │
│  │                                                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Component Specifications

### Zone Card Anatomy

```
┌────────────────────────────────────┐
│ ✅ Zone Name          [Normal] ────┤ Status border (green)
│                                    │
│ ⚡ Energy                          │
│    Energy Usage                    │
│    450 kWh                         │
│                                    │
│ 🌡️ Temperature                     │
│    Temperature                     │
│    65.0°C                          │
│                                    │
│ 💡 Efficiency                      │
│    Efficiency                      │
│    92.0%                           │
│                                    │
│ [🔴 High Temperature Alert]        │ ← Only if alerts exist
│                                    │
│ ────────────────────────────────── │
│ $54.00/hr         110 kg CO₂       │
└────────────────────────────────────┘
     ↑                    ↑
   Cost              CO₂ emissions
```

**Status Border Colors**:
- 🟢 Green (`4px solid #24A148`): Normal
- 🟡 Amber (`4px solid #FFC200`): Warning  
- 🔴 Red (`4px solid #DA1E28`): Critical

**Hover State**:
- Transform: `translateY(-2px)`
- Box shadow: `0 4px 12px rgba(0,0,0,0.3)`

---

### Button Styles

**Primary Button** (Run Simulation):
```
┌─────────────────────────┐
│ ▶️ Run Simulation       │ ← IBM Blue background (#0F62FE)
└─────────────────────────┘   White text, icon left-aligned
```

**Secondary Button** (Reset):
```
┌─────────────────────────┐
│ 🔄 Reset                │ ← Transparent background
└─────────────────────────┘   Blue border, blue text
```

---

### Navigation Header

```
┌──────────────────────────────────────────────────────────────┐
│ IBM   PlantOps Digital Twin  │ Dashboard  Simulation  Analytics │  🔔  ⚙️  👤 │
└──────────────────────────────────────────────────────────────┘
  ↑              ↑                        ↑                          ↑
Logo       Product Name            Navigation Menu          Global Actions
```

**Header Specs**:
- Height: `48px`
- Background: `#161616` (Carbon header background)
- IBM logo: White on blue square
- Text: White (`#F4F4F4`)
- Active nav item: White text with bottom border

---

## 📐 Grid & Spacing

### Carbon Grid System
- **Columns**: 16 columns (responsive)
- **Gutter**: 32px (desktop), 16px (mobile)
- **Margins**: 32px (desktop), 16px (mobile)

### Zone Card Grid
- **Desktop (lg)**: 4 columns per card = 4 cards per row
- **Tablet (md)**: 4 columns per card = 2 cards per row
- **Mobile (sm)**: 4 columns per card = 1 card per row

### Spacing Scale (Carbon)
```
0.25rem = 4px   (micro spacing)
0.5rem  = 8px   (small gaps)
1rem    = 16px  (standard spacing)
1.5rem  = 24px  (medium spacing)
2rem    = 32px  (large spacing)
```

---

## 🎨 Typography

### IBM Plex Sans
- **Headings**: 600 weight (Semi-bold)
- **Body**: 400 weight (Regular)
- **Labels**: 400 weight, uppercase, letter-spacing: 0.5px

### Font Sizes
```
h1:  2rem    (32px) - Page titles
h2:  1.5rem  (24px) - Section headings
h3:  1.125rem (18px) - Card titles
Body: 1rem   (16px) - Standard text
Small: 0.875rem (14px) - Labels, metadata
```

---

## 💫 Animations & Interactions

### Card Hover
```css
transition: all 0.2s ease;
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0,0,0,0.3);
```

### Button Click
- Ripple effect (Carbon built-in)
- Slight scale down on click

### Loading States
- Carbon spinner component
- Skeleton text for placeholders

### Notifications
- Slide in from top-right
- Auto-dismiss after 5 seconds (optional)
- Toast-style inline notifications

---

## 📱 Responsive Breakpoints

```
sm:  320px - 671px   (Mobile)
md:  672px - 1055px  (Tablet)
lg:  1056px - 1311px (Desktop)
xlg: 1312px - 1583px (Large Desktop)
max: 1584px+         (Extra Large)
```

### Responsive Behavior
- **Mobile**: Single column, stacked cards
- **Tablet**: 2-column grid
- **Desktop**: 4-column grid
- **Navigation**: Hamburger menu on mobile (future)

---

## 🎭 Visual Hierarchy

### Information Priority
1. **Status Indicators** (Green/Amber/Red) - Immediate attention
2. **Large Metrics** (Energy, Cost) - Primary data
3. **Zone Names** - Context
4. **Secondary Metrics** (Temperature, Efficiency) - Supporting data
5. **Timestamps, IDs** - Metadata

### Color Usage
- **Status colors**: Only for status indicators and alerts
- **IBM Blue**: Interactive elements (buttons, links)
- **White/Gray**: Text (primary/secondary)
- **Black**: Backgrounds
- **Avoid**: Pure black (#000) - use Carbon grays

---

## ♿ Accessibility

### Carbon Built-in Features
- ✅ WCAG 2.1 AA compliant
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Focus indicators
- ✅ Color contrast ratios

### Additional Considerations
- Avoid color-only indicators (use icons too)
- Provide text alternatives for icons
- Maintain 4.5:1 contrast ratio minimum
- Support reduced motion preferences

---

**This design creates a professional, enterprise-grade manufacturing operations dashboard that looks like it belongs in the IBM product family! 🎨**
