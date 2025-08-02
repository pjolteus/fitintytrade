
import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
});

// 🔁 FIXED: use 'symbol' instead of 'ticker', and allow model_type
export const getPrediction = (symbol, model_type = "lstm") =>
  API.post('/predict', { symbol, model_type });

export const fetchTop10Signals = () => 
API.get('/daily-signals');


export const startTraining = () =>
  API.post('/train');

