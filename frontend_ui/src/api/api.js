// frontend_ui/src/api/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({ baseURL: API_BASE_URL });

export const getPrediction = (symbol, model_type = 'lstm') =>
  api.post('/predict', { symbol, model_type });

export const fetchTop10Signals = () => api.get('/daily-signals');

export const startTraining = () => api.post('/train');

export const fetchPredictionHistory = async () => {
  try {
    const response = await api.get('/predictions');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch predictions:', error);
    throw error;
  }
};

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
