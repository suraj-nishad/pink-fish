import { useState } from 'react';
import {
  Grid,
  Column,
  Form,
  TextInput,
  Select,
  SelectItem,
  NumberInput,
  Button,
  Tile,
  InlineNotification,
  Loading,
} from '@carbon/react';
import { Play, Reset } from '@carbon/icons-react';
import axios from 'axios';
import './Simulation.scss';

const Simulation = () => {
  const [formData, setFormData] = useState({
    simulationName: '',
    zoneName: 'Paint Shop',
    modificationType: 'add_production_lines',
    value: 1,
    durationHours: 24,
  });
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const zones = [
    'Stamping Shop',
    'Body Shop (BIW)',
    'Paint Shop',
    'General Assembly',
    'Powertrain Assembly',
    'Quality Control',
    'Logistics',
  ];

  const modificationTypes = [
    { id: 'add_production_lines', label: 'Add Production Lines' },
    { id: 'temperature_offset', label: 'Temperature Offset (°C)' },
    { id: 'efficiency_modifier', label: 'Efficiency Modifier (%)' },
    { id: 'energy_multiplier', label: 'Energy Multiplier' },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const modifications = [{
        zone_name: formData.zoneName,
        [formData.modificationType]: parseFloat(formData.value),
      }];

      const response = await axios.post('/api/simulation/run', {
        simulation_name: formData.simulationName || `Simulate ${formData.zoneName}`,
        modifications: JSON.stringify(modifications),
        duration_hours: parseInt(formData.durationHours),
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Simulation failed. Please try again.');
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      simulationName: '',
      zoneName: 'Paint Shop',
      modificationType: 'add_production_lines',
      value: 1,
      durationHours: 24,
    });
    setResult(null);
    setError(null);
  };

  return (
    <div className="simulation-page">
      <div className="page-header">
        <h1>Digital Twin Simulation</h1>
        <p>Test "what-if" scenarios and predict impact before implementation</p>
      </div>

      <Grid>
        {/* Simulation Form */}
        <Column lg={6} md={8} sm={4}>
          <Tile className="simulation-form">
            <h3>Configure Simulation</h3>
            <Form onSubmit={handleSubmit}>
              <TextInput
                id="simulation-name"
                labelText="Simulation Name"
                placeholder="e.g., Add second production line"
                value={formData.simulationName}
                onChange={(e) => setFormData({ ...formData, simulationName: e.target.value })}
              />

              <Select
                id="zone-select"
                labelText="Select Zone"
                value={formData.zoneName}
                onChange={(e) => setFormData({ ...formData, zoneName: e.target.value })}
              >
                {zones.map((zone) => (
                  <SelectItem key={zone} value={zone} text={zone} />
                ))}
              </Select>

              <Select
                id="modification-type"
                labelText="Modification Type"
                value={formData.modificationType}
                onChange={(e) => setFormData({ ...formData, modificationType: e.target.value })}
              >
                {modificationTypes.map((type) => (
                  <SelectItem key={type.id} value={type.id} text={type.label} />
                ))}
              </Select>

              <NumberInput
                id="value-input"
                label="Value"
                value={formData.value}
                onChange={(e, { value }) => setFormData({ ...formData, value })}
                step={formData.modificationType === 'energy_multiplier' ? 0.1 : 1}
              />

              <NumberInput
                id="duration-input"
                label="Duration (hours)"
                min={1}
                max={720}
                value={formData.durationHours}
                onChange={(e, { value }) => setFormData({ ...formData, durationHours: value })}
              />

              <div className="form-buttons">
                <Button
                  kind="primary"
                  renderIcon={Play}
                  type="submit"
                  disabled={loading}
                >
                  {loading ? 'Running...' : 'Run Simulation'}
                </Button>
                <Button
                  kind="secondary"
                  renderIcon={Reset}
                  onClick={handleReset}
                  disabled={loading}
                >
                  Reset
                </Button>
              </div>
            </Form>
          </Tile>
        </Column>

        {/* Results Panel */}
        <Column lg={10} md={8} sm={4}>
          {loading && (
            <div className="simulation-loading">
              <Loading description="Running simulation..." withOverlay={false} />
            </div>
          )}

          {error && (
            <InlineNotification
              kind="error"
              title="Simulation Error"
              subtitle={error}
              onClose={() => setError(null)}
            />
          )}

          {result && !loading && (
            <div className="simulation-results">
              <Tile>
                <h3>Simulation Results</h3>
                <p className="results-id">ID: {result.simulation_id}</p>

                <div className="results-grid">
                  <div className="result-card">
                    <h4>Energy Impact</h4>
                    <p className="result-value result-value--large">
                      {result.comparison.delta.energy_kwh > 0 ? '+' : ''}
                      {result.comparison.delta.energy_kwh.toFixed(0)} kWh
                    </p>
                    <p className="result-change">
                      {result.comparison.percent_change.energy_kwh > 0 ? '+' : ''}
                      {result.comparison.percent_change.energy_kwh.toFixed(1)}%
                    </p>
                  </div>

                  <div className="result-card">
                    <h4>Cost Impact</h4>
                    <p className="result-value result-value--large">
                      {result.comparison.delta.cost_usd > 0 ? '+' : ''}
                      ${result.comparison.delta.cost_usd.toFixed(2)}
                    </p>
                    <p className="result-change">
                      {result.comparison.percent_change.cost_usd > 0 ? '+' : ''}
                      {result.comparison.percent_change.cost_usd.toFixed(1)}%
                    </p>
                  </div>

                  <div className="result-card">
                    <h4>Production Impact</h4>
                    <p className="result-value result-value--large">
                      {result.comparison.delta.production_units > 0 ? '+' : ''}
                      {result.comparison.delta.production_units} units
                    </p>
                    <p className="result-change">
                      {result.comparison.percent_change.production_units > 0 ? '+' : ''}
                      {result.comparison.percent_change.production_units.toFixed(1)}%
                    </p>
                  </div>

                  <div className="result-card">
                    <h4>Efficiency Impact</h4>
                    <p className="result-value result-value--large">
                      {result.comparison.delta.efficiency_pct > 0 ? '+' : ''}
                      {result.comparison.delta.efficiency_pct.toFixed(1)}%
                    </p>
                    <p className="result-change">Change from baseline</p>
                  </div>
                </div>

                {result.recommendations && result.recommendations.length > 0 && (
                  <div className="recommendations">
                    <h4>Recommendations</h4>
                    {result.recommendations.map((rec, idx) => (
                      <p key={idx} className="recommendation-item">• {rec}</p>
                    ))}
                  </div>
                )}
              </Tile>
            </div>
          )}
        </Column>
      </Grid>
    </div>
  );
};

export default Simulation;
