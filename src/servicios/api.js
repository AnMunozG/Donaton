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
const authPaths = ["/auth/login", "/auth/register"];
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const url = error.config?.url || "";
    if (error.response?.status === 401 && !authPaths.some((p) => url.includes(p))) {
      localStorage.removeItem('donaton_token');
      localStorage.removeItem('donaton_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
