import axios from 'axios';

// Configuración base de axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8080/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('donaton_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para responses
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('donaton_token');
      localStorage.removeItem('donaton_user');
    }
    return Promise.reject(error);
  }
);

export default api;
