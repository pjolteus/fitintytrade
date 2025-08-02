// frontend/src/api/email.js
import axios from 'axios';
import { getAuthHeaders } from './auth'; // make sure it includes Clerk JWT

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function sendEmailReport(predictionIds, recipientEmail) {
  const response = await axios.post(
    `${API_BASE_URL}/email-report`,
    {
      prediction_ids: predictionIds,
      recipient_email: recipientEmail,
    },
    {
      headers: getAuthHeaders(),
    }
  );
  return response.data;
}
