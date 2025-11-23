/**
 * API Configuration
 * Handles backend URL based on environment
 */

// Get API URL from environment variable
// In development: uses Vite dev server proxy (/)
// In production: uses VITE_API_URL from Railway environment variable
const getApiUrl = () => {
  // In production, use the environment variable
  if (import.meta.env.PROD && import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // In development, use relative path (Vite proxy handles it)
  return '';
};

export const API_URL = getApiUrl();

// API endpoints
export const API_ENDPOINTS = {
  HEALTH: `${API_URL}/health`,
  ZONES_STATUS: `${API_URL}/api/zones/status`,
  ZONE_HISTORY: (zoneId, hours = 24) => `${API_URL}/api/zones/${zoneId}/history?hours=${hours}`,
  ANALYZE_ENERGY: `${API_URL}/api/analyze-energy`,
  CHATOPS: `${API_URL}/api/chatops`,
  MAINTENANCE_SCHEDULE: `${API_URL}/api/maintenance/schedule`,
  KPIS: `${API_URL}/api/kpis`,
};

// Log API configuration in console (only in development)
if (import.meta.env.DEV) {
  console.log('🔧 API Configuration:', {
    mode: import.meta.env.MODE,
    apiUrl: API_URL,
    isDev: import.meta.env.DEV,
  });
}
