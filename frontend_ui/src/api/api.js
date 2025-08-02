import axios from 'axios';
import { clerkClient } from '@clerk/clerk-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach Clerk JWT
api.interceptors.request.use(async (config) => {
  const token = await clerkClient.sessions.getToken({ template: 'jwt' });
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Example API call using Axios instance
export async function fetchPredictionHistory() {
  try {
    const response = await api.get('/predictions');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch predictions:', error);
    throw error;
  }
}

export default api;
