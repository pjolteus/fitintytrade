// frontend_ui/src/hooks/useApi.js
import axios from 'axios';
import { useAuth } from '@clerk/clerk-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

/**
 * useApi - Custom React hook that provides an Axios instance with
 * Clerk-authenticated JWT support and core API methods.
 */
export function useApi() {
  const { getToken } = useAuth();

  // Create base axios instance
  const api = axios.create({
    baseURL: API_BASE_URL,
  });

  // Automatically attach Clerk JWT to all requests
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

  // Predict a symbol using a specific model
  const getPrediction = (symbol, model_type = 'lstm') =>
    api.post('/predict', { symbol, model_type });

  // Get top 10 daily trading signals
  const fetchTop10Signals = () => api.get('/daily-signals');

  // Trigger model training
  const startTraining = () => api.post('/train');

  // Fetch all historical predictions
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
    api, // Raw axios instance
    getPrediction,
    fetchTop10Signals,
    startTraining,
    fetchPredictionHistory,
  };
}
