import { Button, Select, SelectItem, SkeletonText } from '@carbon/react';
import { Close } from '@carbon/icons-react';
import TrendChart from './TrendChart';
import './TrendsDrawer.scss';

const TrendsDrawer = ({
  zone,
  onClose,
  timeframe,
  setTimeframe,
  history,
  loading,
  error,
  onRetry,
}) => {
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

  return (
    <>
      {zone && <div className="trends-backdrop" onClick={onClose} />}
      <div className={`trends-drawer ${zone ? 'trends-drawer--open' : ''}`}> 
        {zone ? (
          <div className="trends-drawer__content">
            <div className="trends-drawer__header">
              <h3>{zone.zone_name} - Performance Trends</h3>
              <Button
                kind="ghost"
                size="sm"
                hasIconOnly
                iconDescription="Close"
                renderIcon={Close}
                onClick={onClose}
              />
            </div>
            
            <div className="trends-drawer__controls">
              <Select
                id={`drawer-timeframe-${zone.zone_id}`}
                labelText="Timeframe"
                size="sm"
                value={timeframe}
                onChange={handleTimeframeChange}
              >
                <SelectItem value="24" text="Last 24 Hours" />
                <SelectItem value="48" text="Last 48 Hours" />
                <SelectItem value="72" text="Last 3 Days" />
                <SelectItem value="168" text="Last 7 Days" />
              </Select>
            </div>
            
            <div className="trends-drawer__body">
              {loading ? (
                <div className="trends-drawer__loading">
                  <SkeletonText paragraph lineCount={6} />
                </div>
              ) : error ? (
                <div className="trends-drawer__error">
                  <p>{error}</p>
                  <Button kind="ghost" size="sm" onClick={onRetry}>
                    Retry
                  </Button>
                </div>
              ) : history ? (
                <TrendChart data={history} title={getTimeframeLabel()} />
              ) : (
                <div className="trends-drawer__empty">
                  <p>No historical data available for this zone.</p>
                </div>
              )}
            </div>
          </div>
        ) : null}
      </div>
    </>
  );
};

export default TrendsDrawer;
