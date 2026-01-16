import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for ML processing
});

export const generateMCQs = async (data) => {
  try {
    const response = await api.post('/generate', data);
    return response.data;
  } catch (error) {
    throw {
      message: error.response?.data?.error || error.message || 'Failed to generate MCQs',
      status: error.response?.status || 500,
    };
  }
};

export default api;
