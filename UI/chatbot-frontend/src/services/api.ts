// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.PROD 
    ? 'https://your-api-domain.com' 
    : 'http://localhost:8080',
  ENDPOINTS: {
    AUTH: '/api/auth',
    CHAT: '/api/chat',
    USERS: '/api/users'
  },
  TIMEOUT: 300000, // Increase timeout to 5 minutes for slow AI responses
};

// Axios default configuration
import axios from 'axios';
import AuthService from './AuthService';

// Set default base URL
axios.defaults.baseURL = API_CONFIG.BASE_URL;
axios.defaults.timeout = API_CONFIG.TIMEOUT;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Request interceptor to add auth token
axios.interceptors.request.use(
  (config) => {
    const authHeader = AuthService.getAuthHeader();
    if (authHeader.Authorization) {
      config.headers.Authorization = authHeader.Authorization;
    }
    
    // Log request for debugging (remove in production)
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling common errors
axios.interceptors.response.use(
  (response) => {
    // Log successful response for debugging (remove in production)
    console.log(`Received response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    // Log error details for debugging (remove in production)
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers
    });
    
    // Only redirect to login if not already on login or register page
    if (error.response?.status === 401) {
      const currentPath = window.location.pathname;
      if (currentPath !== '/login' && currentPath !== '/register') {
        AuthService.logout();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default axios;
