import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.scss'
import PinkFishLogo from './components/pink-fish logo.png';

// Set Carbon theme to g100 (dark theme)
document.documentElement.setAttribute('data-carbon-theme', 'g100');

// Dynamically set favicon to Pink Fish logo (ensures hashed asset path after build).
try {
  const existing = document.querySelector("link[rel~='icon']");
  if (existing) {
    existing.href = PinkFishLogo;
    existing.type = 'image/png';
  } else {
    const link = document.createElement('link');
    link.rel = 'icon';
    link.type = 'image/png';
    link.href = PinkFishLogo;
    document.head.appendChild(link);
  }
} catch (e) {
  // Non-fatal; favicon update failure shouldn't block app render.
  console.warn('Failed to set favicon:', e);
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
