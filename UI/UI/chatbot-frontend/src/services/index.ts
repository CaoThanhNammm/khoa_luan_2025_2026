// Services barrel export
export { default as AuthService } from './AuthService';
export { default as ChatService } from './ChatService';
export { default as UserService } from './UserService';
export { default as ContactService } from './ContactService';
export { default as axios } from './api';

// Types exports
export type { 
  AuthResponse, 
  User, 
  LoginRequest, 
  RegisterRequest, 
  ForgotPasswordRequest, 
  ResetPasswordRequest 
} from './AuthService';

export type { 
  ConversationResponse, 
  MessageRequest, 
  MessageResponse
} from './ChatService';

export type {
  ContactMessage,
  ContactResponse,
  ContactMessageDetails,
  ContactMessagePage
} from './ContactService';

export type { 
  UserProfile, 
  UpdateProfileRequest, 
  UpdatePasswordRequest, 
  UserSettings 
} from './UserService';
