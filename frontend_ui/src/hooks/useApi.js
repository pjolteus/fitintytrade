// frontend_ui/src/hooks/useApi.js
import axios from 'axios';
import { useAuth } from '@clerk/clerk-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export function useApi() {
  const { getToken } = useAuth();

  const api = axios.create({
    baseURL: API_BASE_URL,
  });

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

  const getPrediction = (symbol, model_type = 'lstm') =>
    api.post('/predict', { symbol, model_type });

  const fetchTop10Signals = () => api.get('/daily-signals');
  const startTraining = () => api.post('/train');

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
    api,
    getPrediction,
    fetchTop10Signals,
    startTraining,
    fetchPredictionHistory,
  };
}
