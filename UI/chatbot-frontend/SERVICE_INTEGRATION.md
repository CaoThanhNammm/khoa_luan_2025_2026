# Service Integration Guide

This document describes how to integrate the TypeScript services with your backend API.

## Services Overview

### AuthService (`src/services/AuthService.ts`)
Handles user authentication including login, registration, password reset, and token management.

**Methods:**
- `login(username, password)` - User login
- `register(username, email, password)` - User registration  
- `forgotPassword(email)` - Request password reset
- `resetPassword(token, password)` - Reset password with token
- `logout()` - Clear user session
- `getCurrentUser()` - Get current logged-in user
- `getAuthHeader()` - Get authorization header for API calls

### ChatService (`src/services/ChatService.ts`)
Manages chat conversations and messages.

**Methods:**
- `getConversations()` - Get all user conversations
- `getConversation(id)` - Get specific conversation by ID
- `startNewConversation(message)` - Create new conversation
- `sendMessage(conversationId, message)` - Send message to conversation
- `deleteConversation(id)` - Delete a conversation

### UserService (`src/services/UserService.ts`)
Handles user profile and settings management.

**Methods:**
- `getUserProfile()` - Get user profile data
- `updateProfile(userData)` - Update user profile
- `updatePassword(passwordData)` - Change user password
- `updateSettings(settingsData)` - Update user preferences

## Context Integration

### AuthContext (`src/context/AuthContext.tsx`)
- Integrates with `AuthService` for real authentication
- Manages global user state
- Handles automatic token refresh

### ChatContext (`src/context/ChatContext.tsx`)
- Integrates with `ChatService` for conversation management
- Provides chat state management across components
- Handles real-time message updates

### UserContext (`src/context/UserContext.tsx`)
- Integrates with `UserService` for profile management
- Provides user settings and profile state

## API Configuration

### Base URL Configuration (`src/services/api.ts`)
The API base URL is configured in `src/services/api.ts`:

```typescript
export const API_CONFIG = {
  BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://your-api-domain.com' 
    : 'http://localhost:8080',
  // ...
};
```

### Vite Proxy Configuration
Development API calls are proxied through Vite config:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
      secure: false,
    },
  },
}
```

## Backend Integration Steps

1. **Update API Base URL**: 
   - Modify `API_CONFIG.BASE_URL` in `src/services/api.ts`
   - Update the proxy target in `vite.config.ts`

2. **Authentication Flow**:
   - Backend should return JWT token on login/register
   - Token is automatically included in subsequent requests
   - 401 responses automatically redirect to login

3. **Expected API Endpoints**:

   **Authentication:**
   - `POST /api/auth/login` - Login user
   - `POST /api/auth/register` - Register new user
   - `POST /api/auth/forgot-password` - Request password reset
   - `POST /api/auth/reset-password` - Reset password

   **Chat:**
   - `GET /api/chat/conversations` - Get all conversations
   - `GET /api/chat/conversations/:id` - Get specific conversation
   - `POST /api/chat/conversations` - Create new conversation
   - `POST /api/chat/conversations/:id/messages` - Send message
   - `DELETE /api/chat/conversations/:id` - Delete conversation

   **User:**
   - `GET /api/users/profile` - Get user profile
   - `PUT /api/users/profile` - Update profile
   - `PUT /api/users/password` - Change password
   - `PUT /api/users/settings` - Update settings

4. **Response Formats**:
   All API responses should follow the TypeScript interfaces defined in the service files.

## Usage Examples

### Login a User
```typescript
import { AuthService } from '../services';

try {
  const response = await AuthService.login('username', 'password');
  // User is automatically logged in and token stored
} catch (error) {
  console.error('Login failed:', error);
}
```

### Send a Chat Message
```typescript
import { ChatService } from '../services';

try {
  const response = await ChatService.sendMessage('conversationId', 'Hello!');
  // Handle bot response
} catch (error) {
  console.error('Message failed:', error);
}
```

### Update User Profile
```typescript
import { UserService } from '../services';

try {
  await UserService.updateProfile({
    username: 'newUsername',
    email: 'new@email.com'
  });
} catch (error) {
  console.error('Update failed:', error);
}
```

## Error Handling

The services include automatic error handling:
- 401 responses redirect to login page
- Network errors are caught and logged
- Specific error messages are provided for different scenarios

## Development vs Production

- **Development**: Uses proxy to localhost:8080
- **Production**: Configure HTTPS backend URL in environment variables

## Environment Variables

Create a `.env` file for production configuration:

```
VITE_API_BASE_URL=https://your-api-domain.com
```

Then update `api.ts` to use environment variables:

```typescript
BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'
```
