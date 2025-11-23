import { useState, useEffect } from 'react';
import {
  Grid,
  Column,
  Loading,
  InlineNotification,
  Tile,
  SkeletonText,
} from '@carbon/react';
import { Dashboard as DashboardIcon, DataBase, Activity } from '@carbon/icons-react';
import ZoneCard from '../components/ZoneCard';
import axios from 'axios';
import './Dashboard.scss';

const Dashboard = () => {
  const [zones, setZones] = useState([]);
  const [plantStatus, setPlantStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchZoneStatus();
    const interval = setInterval(fetchZoneStatus, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchZoneStatus = async () => {
    try {
      const response = await axios.get('/api/zones/status');
      setZones(response.data.zones);
      setPlantStatus({
        total: response.data.total_zones,
        normal: response.data.zones_normal,
        warning: response.data.zones_warning,
        critical: response.data.zones_critical,
        lastUpdated: response.data.last_updated,
      });
      setError(null);
    } catch (err) {
      setError('Failed to fetch zone status. Please check if the backend is running.');
      console.error('Error fetching zones:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <Loading description="Loading plant status..." withOverlay={false} />
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      {/* Page Header */}
      <div className="dashboard-header">
        <div className="dashboard-header__title">
          <DashboardIcon size={32} />
          <div>
            <h1>Manufacturing Plant Overview</h1>
            <p>Real-time monitoring of all production zones</p>
          </div>
        </div>
        {plantStatus && (
          <div className="dashboard-header__status">
            <span className="status-badge status-badge--green">
              {plantStatus.normal} Normal
            </span>
            <span className="status-badge status-badge--amber">
              {plantStatus.warning} Warning
            </span>
            <span className="status-badge status-badge--red">
              {plantStatus.critical} Critical
            </span>
          </div>
        )}
      </div>

      {/* Error Notification */}
      {error && (
        <InlineNotification
          kind="error"
          title="Connection Error"
          subtitle={error}
          onClose={() => setError(null)}
          style={{ marginBottom: '2rem' }}
        />
      )}

      {/* KPI Summary */}
      {plantStatus && (
        <Grid className="kpi-grid" narrow>
          <Column lg={4} md={4} sm={4}>
            <Tile className="kpi-tile">
              <div className="kpi-tile__icon">
                <DataBase size={24} />
              </div>
              <div className="kpi-tile__content">
                <span className="kpi-tile__label">Total Zones</span>
                <span className="kpi-tile__value">{plantStatus.total}</span>
              </div>
            </Tile>
          </Column>
          <Column lg={4} md={4} sm={4}>
            <Tile className="kpi-tile">
              <div className="kpi-tile__icon">
                <Activity size={24} />
              </div>
              <div className="kpi-tile__content">
                <span className="kpi-tile__label">Plant Status</span>
                <span className={`kpi-tile__value kpi-tile__value--${plantStatus.critical > 0 ? 'critical' : 'normal'}`}>
                  {plantStatus.critical > 0 ? 'Critical' : 'Operational'}
                </span>
              </div>
            </Tile>
          </Column>
          <Column lg={4} md={4} sm={4}>
            <Tile className="kpi-tile">
              <div className="kpi-tile__icon">
                <DashboardIcon size={24} />
              </div>
              <div className="kpi-tile__content">
                <span className="kpi-tile__label">Last Updated</span>
                <span className="kpi-tile__value kpi-tile__value--small">
                  {new Date(plantStatus.lastUpdated).toLocaleTimeString()}
                </span>
              </div>
            </Tile>
          </Column>
        </Grid>
      )}

      {/* Zone Cards Grid */}
      <Grid className="zones-grid">
        {zones.length === 0 && !loading ? (
          <Column lg={16}>
            <InlineNotification
              kind="info"
              title="No Data"
              subtitle="No zones found. Please check your backend connection."
              hideCloseButton
            />
          </Column>
        ) : (
          zones.map((zone) => (
            <Column key={zone.zone_id} lg={4} md={4} sm={4}>
              <ZoneCard zone={zone} />
            </Column>
          ))
        )}
      </Grid>
    </div>
  );
};

export default Dashboard;
