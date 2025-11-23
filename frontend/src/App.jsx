import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Theme } from '@carbon/react';
import AppHeader from './components/AppHeader';
import Dashboard from './pages/Dashboard';
import Simulation from './pages/Simulation';
import Analytics from './pages/Analytics';
import './App.scss';

function App() {
  return (
    <Theme theme="g100">
      <Router>
        <div className="app-container">
          <AppHeader />
          <main className="app-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/simulation" element={<Simulation />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </main>
        </div>
      </Router>
    </Theme>
  );
}

export default App;
