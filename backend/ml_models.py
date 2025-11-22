"""
Local ML Models for Digital Twin
- Anomaly Detection using Isolation Forest
- Energy Forecasting using Linear Regression and LSTM (when data is sufficient)
- Predictive maintenance scheduling
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pickle
import os
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetector:
    """Isolation Forest-based anomaly detection for plant zones"""
    
    def __init__(self, contamination=0.05):
        self.models = {}
        self.scalers = {}
        self.contamination = contamination
        self.feature_columns = ['energy_kwh', 'temperature_c', 'efficiency_pct', 'hour', 'day_of_week']
        
    def prepare_features(self, df):
        """Prepare features for anomaly detection"""
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        return df
    
    def train(self, df):
        """Train anomaly detection models for each zone"""
        df = self.prepare_features(df)
        
        for zone in df['zone'].unique():
            zone_data = df[df['zone'] == zone].copy()
            
            # Select features
            X = zone_data[self.feature_columns].values
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train Isolation Forest
            model = IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=100
            )
            model.fit(X_scaled)
            
            # Store model and scaler
            self.models[zone] = model
            self.scalers[zone] = scaler
        
        return self
    
    def predict(self, df):
        """Predict anomalies for given data"""
        df = self.prepare_features(df)
        results = []
        
        for zone in df['zone'].unique():
            if zone not in self.models:
                continue
                
            zone_data = df[df['zone'] == zone].copy()
            X = zone_data[self.feature_columns].values
            X_scaled = self.scalers[zone].transform(X)
            
            # Predict (-1 for anomaly, 1 for normal)
            predictions = self.models[zone].predict(X_scaled)
            scores = self.models[zone].score_samples(X_scaled)
            
            for idx, (pred, score) in enumerate(zip(predictions, scores)):
                results.append({
                    'timestamp': zone_data.iloc[idx]['timestamp'],
                    'zone': zone,
                    'is_anomaly': pred == -1,
                    'anomaly_score': float(score),
                    'confidence': float(1 - (score - scores.min()) / (scores.max() - scores.min()))
                })
        
        return pd.DataFrame(results)
    
    def save(self, path='/Users/suraj/digital-twin/backend/models/anomaly_detector.pkl'):
        """Save trained models"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'models': self.models,
                'scalers': self.scalers,
                'contamination': self.contamination,
                'feature_columns': self.feature_columns
            }, f)
    
    @classmethod
    def load(cls, path='/Users/suraj/digital-twin/backend/models/anomaly_detector.pkl'):
        """Load trained models"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        detector = cls(contamination=data['contamination'])
        detector.models = data['models']
        detector.scalers = data['scalers']
        detector.feature_columns = data['feature_columns']
        return detector


class EnergyForecaster:
    """Energy consumption forecasting using Linear Regression"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = ['hour', 'day_of_week', 'is_weekend', 'temperature_c', 'efficiency_pct']
        
    def prepare_features(self, df):
        """Prepare features for forecasting"""
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        return df
    
    def train(self, df):
        """Train forecasting models for each zone"""
        df = self.prepare_features(df)
        
        for zone in df['zone'].unique():
            zone_data = df[df['zone'] == zone].copy()
            
            # Prepare features and target
            X = zone_data[self.feature_columns].values
            y = zone_data['energy_kwh'].values
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = LinearRegression()
            model.fit(X_scaled, y)
            
            # Store model and scaler
            self.models[zone] = model
            self.scalers[zone] = scaler
        
        return self
    
    def predict(self, zone, hours_ahead=24, current_temp=None, current_efficiency=None):
        """Forecast energy consumption for next N hours"""
        if zone not in self.models:
            return None
        
        # Generate future timestamps
        now = datetime.now()
        future_times = [now + timedelta(hours=i) for i in range(1, hours_ahead + 1)]
        
        # Prepare features
        features = []
        for ts in future_times:
            hour = ts.hour
            day_of_week = ts.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            
            # Use current values or defaults
            temp = current_temp if current_temp else 25.0
            efficiency = current_efficiency if current_efficiency else 85.0
            
            features.append([hour, day_of_week, is_weekend, temp, efficiency])
        
        X = np.array(features)
        X_scaled = self.scalers[zone].transform(X)
        
        # Predict
        predictions = self.models[zone].predict(X_scaled)
        
        # Format results
        forecast = []
        for ts, pred in zip(future_times, predictions):
            forecast.append({
                'timestamp': ts.strftime('%Y-%m-%d %H:%M:%S'),
                'hour': ts.hour,
                'predicted_energy_kwh': float(pred),
                'predicted_cost_usd': float(pred * 0.12),
                'predicted_co2_kg': float(pred * 0.233)
            })
        
        return forecast
    
    def save(self, path='/Users/suraj/digital-twin/backend/models/energy_forecaster.pkl'):
        """Save trained models"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'models': self.models,
                'scalers': self.scalers,
                'feature_columns': self.feature_columns
            }, f)
    
    @classmethod
    def load(cls, path='/Users/suraj/digital-twin/backend/models/energy_forecaster.pkl'):
        """Load trained models"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        forecaster = cls()
        forecaster.models = data['models']
        forecaster.scalers = data['scalers']
        forecaster.feature_columns = data['feature_columns']
        return forecaster


class PredictiveMaintenanceModel:
    """Predictive maintenance based on anomaly patterns"""
    
    def __init__(self):
        self.maintenance_thresholds = {
            'energy_spike_count': 5,  # Number of energy spikes before maintenance
            'temp_anomaly_count': 3,
            'efficiency_drop_count': 4,
            'days_window': 7
        }
    
    def analyze_maintenance_needs(self, df, anomaly_predictions):
        """Analyze which zones need maintenance"""
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Merge with anomaly predictions
        anomaly_df = anomaly_predictions[anomaly_predictions['is_anomaly'] == True].copy()
        
        maintenance_recommendations = []
        
        for zone in df['zone'].unique():
            zone_anomalies = anomaly_df[anomaly_df['zone'] == zone]
            
            if len(zone_anomalies) == 0:
                continue
            
            # Get recent data (last 7 days)
            recent_cutoff = df['timestamp'].max() - timedelta(days=self.maintenance_thresholds['days_window'])
            recent_anomalies = zone_anomalies[zone_anomalies['timestamp'] >= recent_cutoff]
            
            if len(recent_anomalies) >= self.maintenance_thresholds['energy_spike_count']:
                # Get zone metrics
                zone_data = df[df['zone'] == zone].tail(24)
                avg_energy = zone_data['energy_kwh'].mean()
                avg_efficiency = zone_data['efficiency_pct'].mean()
                
                priority = 'high' if len(recent_anomalies) > 10 else 'medium'
                
                maintenance_recommendations.append({
                    'zone': zone,
                    'priority': priority,
                    'anomaly_count': len(recent_anomalies),
                    'issue': f'{len(recent_anomalies)} anomalies detected in last {self.maintenance_thresholds["days_window"]} days',
                    'recommended_action': 'Schedule preventive maintenance inspection',
                    'current_avg_energy': round(avg_energy, 2),
                    'current_avg_efficiency': round(avg_efficiency, 2),
                    'estimated_downtime_hours': 4 if priority == 'high' else 2
                })
        
        return maintenance_recommendations


def train_all_models(data_path='/Users/suraj/digital-twin/data/plant_data_30days.csv'):
    """Train all ML models on the generated data"""
    # Load data
    df = pd.read_csv(data_path)
    
    # Train anomaly detector
    anomaly_detector = AnomalyDetector(contamination=0.05)
    anomaly_detector.train(df)
    anomaly_detector.save()
    
    # Train energy forecaster
    energy_forecaster = EnergyForecaster()
    energy_forecaster.train(df)
    energy_forecaster.save()
    
    return {
        'anomaly_detector': anomaly_detector,
        'energy_forecaster': energy_forecaster,
        'records_trained': len(df),
        'zones_trained': df['zone'].nunique()
    }


if __name__ == '__main__':
    results = train_all_models()
