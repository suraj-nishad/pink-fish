import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './TrendChart.scss';

const TrendChart = ({ data, title }) => {
  if (!data || data.length === 0) {
    return (
      <div className="trend-chart trend-chart--empty">
        <p>No historical data available</p>
      </div>
    );
  }

  // Transform data for recharts format
  const chartData = data.map(point => ({
    time: new Date(point.timestamp).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    }),
    energy: point.energy_kwh,
    efficiency: point.efficiency_pct,
    temperature: point.temperature_c,
  }));

  return (
    <div className="trend-chart">
      {title && <h4 className="trend-chart__title">{title}</h4>}
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#393939" />
          <XAxis 
            dataKey="time" 
            stroke="#f4f4f4"
            tick={{ fill: '#f4f4f4', fontSize: 10 }}
            interval="preserveStartEnd"
          />
          <YAxis 
            yAxisId="left"
            stroke="#0f62fe"
            tick={{ fill: '#f4f4f4', fontSize: 10 }}
            width={40}
          />
          <YAxis 
            yAxisId="right" 
            orientation="right"
            stroke="#24a148"
            tick={{ fill: '#f4f4f4', fontSize: 10 }}
            width={40}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#262626', 
              border: '1px solid #393939',
              borderRadius: '4px',
              color: '#f4f4f4',
              fontSize: '11px'
            }}
            labelStyle={{ color: '#f4f4f4', fontSize: '11px' }}
          />
          <Legend 
            wrapperStyle={{ color: '#f4f4f4', fontSize: '11px' }}
            iconType="line"
          />
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="energy" 
            stroke="#0f62fe" 
            strokeWidth={2}
            dot={false}
            name="Energy (kWh)"
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="efficiency" 
            stroke="#24a148" 
            strokeWidth={2}
            dot={false}
            name="Efficiency (%)"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendChart;
