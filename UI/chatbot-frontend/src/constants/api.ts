// API Constants and Configuration

export const API_ENDPOINTS = {
  // Base URLs
  BASE_URL: import.meta.env.PROD 
    ? 'https://your-api-domain.com' 
    : 'http://localhost:8080',
  
  // Auth endpoints
  AUTH: {
    BASE: '/api/auth',
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    FORGOT_PASSWORD: '/api/auth/forgot-password',
    RESET_PASSWORD: '/api/auth/reset-password',
  },
  
  // Chat endpoints
  CHAT: {
    BASE: '/api/chat',
    CONVERSATIONS: '/api/chat/conversations',
    CONVERSATION_BY_ID: (id: number) => `/api/chat/conversations/${id}`,
    MESSAGES: (conversationId: number) => `/api/chat/conversations/${conversationId}/messages`,
  },
  
  // User endpoints
  USER: {
    BASE: '/api/users',
    PROFILE: '/api/users/profile',
    PASSWORD: '/api/users/password',
    SETTINGS: '/api/users/settings',
  }
} as const;

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
} as const;

export const REQUEST_TIMEOUT = 10000; // 10 seconds

export const LOCAL_STORAGE_KEYS = {
  USER: 'user',
  TOKEN: 'token',
  THEME: 'theme',
  LANGUAGE: 'language',
} as const;
