import { useState, useEffect } from 'react';
import { Tile, Tag, Button } from '@carbon/react';
import {
  Lightning,
  Temperature,
  Power,
  WarningAltFilled,
  CheckmarkFilled,
  Close,
} from '@carbon/icons-react';
import axios from 'axios';
import './ZoneCard.scss';

const ZoneCard = ({ zone, onViewTrends }) => {
  // Card no longer manages trends; handled by external drawer

  // No local effects for history.

  // History fetching removed from card.

  const handleViewTrends = () => {
    // Gracefully handle missing callback
    if (typeof onViewTrends === 'function') {
      onViewTrends(zone);
    } else {
      // Optional: log once to console in dev without throwing
      if (process.env.NODE_ENV !== 'production') {
        // eslint-disable-next-line no-console
        console.warn('[ZoneCard] onViewTrends prop not provided.');
      }
    }
  };

  const handleTimeframeChange = (e) => {
    setTimeframe(e.target.value);
  };

  const getTimeframeLabel = () => {
    switch (timeframe) {
      case '24': return 'Last 24 Hours';
      case '48': return 'Last 48 Hours';
      case '72': return 'Last 3 Days';
      case '168': return 'Last 7 Days';
      default: return 'Last 24 Hours';
    }
  };
  const getStatusIcon = (status) => {
    switch (status) {
      case 'green':
        return <CheckmarkFilled size={20} className="status-icon status-green" />;
      case 'amber':
        return <WarningAltFilled size={20} className="status-icon status-amber" />;
      case 'red':
        return <WarningAltFilled size={20} className="status-icon status-red" />;
      default:
        return null;
    }
  };

  const getStatusTag = (status) => {
    const types = {
      green: 'green',
      amber: 'warm-gray',
      red: 'red',
    };
    const labels = {
      green: 'Normal',
      amber: 'Warning',
      red: 'Critical',
    };
    return <Tag type={types[status]} size="sm">{labels[status]}</Tag>;
  };

  return (
    <div className="zone-card-wrapper">
      <Tile className={`zone-card zone-card--${zone.status}`}>      
        <div className="zone-card__header">
          <div className="zone-card__title">
            {getStatusIcon(zone.status)}
            <h3>{zone.zone_name}</h3>
          </div>
          {getStatusTag(zone.status)}
        </div>

        <div className="zone-card__metrics">
          <div className="metric">
            <Lightning size={20} className="metric-icon" />
            <div className="metric-info">
              <span className="metric-label">Energy</span>
              <span className="metric-value">{zone.metrics.energy_kwh.toFixed(0)} kWh</span>
            </div>
          </div>

          <div className="metric">
            <Temperature size={20} className="metric-icon" />
            <div className="metric-info">
              <span className="metric-label">Temperature</span>
              <span className="metric-value">{zone.metrics.temperature_c.toFixed(1)}°C</span>
            </div>
          </div>

          <div className="metric">
            <Power size={20} className="metric-icon" />
            <div className="metric-info">
              <span className="metric-label">Efficiency</span>
              <span className="metric-value">{zone.metrics.efficiency_pct.toFixed(1)}%</span>
            </div>
          </div>
        </div>

        {zone.alerts && zone.alerts.length > 0 && (
          <div className="zone-card__alerts">
            {zone.alerts.map((alert, idx) => (
              <Tag key={idx} type="red" size="sm">
                {alert.message}
              </Tag>
            ))}
          </div>
        )}

        <div className="zone-card__footer">
          <div className="zone-card__cost">
            <span className="footer-label">Cost</span>
            <span className="footer-value">${zone.metrics.cost_usd.toFixed(2)}/hr</span>
          </div>
          <div className="zone-card__co2">
            <span className="footer-label">CO₂</span>
            <span className="footer-value">{zone.metrics.co2_kg.toFixed(1)} kg</span>
          </div>
        </div>

        <div className="zone-card__actions">
          <Button kind="ghost" size="sm" onClick={handleViewTrends}>View Trends</Button>
        </div>
      </Tile>
    </div>
  );
};

export default ZoneCard;
