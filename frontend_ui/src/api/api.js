// src/api/api.jsx
import axios from 'axios';
import { useAuth } from '@clerk/clerk-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// This custom hook provides a configured axios instance + helper methods
export function useApi() {
  const { getToken } = useAuth();

  const api = axios.create({
    baseURL: API_BASE_URL,
  });

  // Automatically attach Clerk JWT to each request
  api.interceptors.request.use(
    async (config) => {
      const token = await getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Prediction for a specific symbol and model
  const getPrediction = (symbol, model_type = 'lstm') =>
    api.post('/predict', { symbol, model_type });

  // Fetch top 10 daily signals
  const fetchTop10Signals = () => api.get('/daily-signals');

  // Start model training
  const startTraining = () => api.post('/train');

  // Fetch historical predictions (for table/chart)
  const fetchPredictionHistory = async () => {
    try {
      const response = await api.get('/predictions');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch predictions:', error);
      throw error;
    }
  };

  return {
    api, // raw axios instance if needed
    getPrediction,
    fetchTop10Signals,
    startTraining,
    fetchPredictionHistory,
  };
}

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

