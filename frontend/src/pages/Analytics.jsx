import { Tile } from '@carbon/react';
import { ChartLine } from '@carbon/icons-react';
import './Analytics.scss';

const Analytics = () => {
  return (
    <div className="analytics-page">
      <div className="page-header">
        <ChartLine size={32} />
        <div>
          <h1>Analytics & Insights</h1>
          <p>Historical trends and AI-powered recommendations</p>
        </div>
      </div>

      <Tile className="coming-soon">
        <h3>🚧 Coming Soon</h3>
        <p>Advanced analytics features including:</p>
        <ul>
          <li>Historical trend analysis with interactive charts</li>
          <li>ML-powered anomaly detection visualizations</li>
          <li>Energy consumption forecasting</li>
          <li>Predictive maintenance scheduling</li>
          <li>Cost optimization recommendations</li>
        </ul>
      </Tile>
    </div>
  );
};

export default Analytics;
