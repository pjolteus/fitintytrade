// frontend_ui/src/api/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Axios instance configured with the backend base URL
const api = axios.create({ baseURL: API_BASE_URL });

/**
 * Send a prediction request for a given symbol and model type.
 * @param {string} symbol - Ticker symbol (e.g., AAPL, EURUSD).
 * @param {string} model_type - Model to use (default: 'lstm').
 * @returns {Promise<AxiosResponse>}
 */
export const getPrediction = (symbol, model_type = 'lstm') => {
  return api.post('/predict', { symbol, model_type });
};

/**
 * Fetch top 10 daily signals from the backend.
 * @returns {Promise<AxiosResponse>}
 */
export const fetchTop10Signals = () => {
  return api.get('/daily-signals');
};

/**
 * Trigger model training on the backend.
 * @returns {Promise<AxiosResponse>}
 */
export const startTraining = () => {
  return api.post('/train');
};

/**
 * Retrieve historical prediction results.
 * @returns {Promise<Object[]>} - List of past predictions.
 */
export const fetchPredictionHistory = async () => {
  try {
    const response = await api.get('/predictions');
    return response.data;
  } catch (error) {
    console.error('[API] Failed to fetch predictions:', error);
    throw error;
  }
};

/**
 * Execute a trade request.
 * @param {Object} payload - Trade data (symbol, action, quantity, etc).
 * @returns {Promise<Object>} - Execution result.
 */
export const executeTrade = async (payload) => {
  const res = await fetch('/api/execute-trade', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Trade execution failed.');
  }

  return res.json();
};
