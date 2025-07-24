import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import AuthService from '../services/AuthService';
import { getErrorMessage } from '../utils/errorHandler';

interface User {
  id: number;
  name: string;
  email: string;
  username: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  isLoading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if user is already logged in using AuthService
    const savedUser = AuthService.getCurrentUser();
    if (savedUser) {
      const user: User = {
        id: savedUser.id,
        name: savedUser.username,
        email: savedUser.email,
        username: savedUser.username
      };
      setUser(user);
    }
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    setError(null);
    try {
      console.log('AuthContext: Attempting login for:', username);
      const response = await AuthService.login(username, password);
      const userData = response.data;
      
      // Ensure we have valid data before setting the user
      // Handle both id and user_id formats for compatibility with FastAPI
      const userId = userData.user_id || userData.id;
      
      if (userData && (userId !== undefined)) {
        const user: User = {
          id: userId,
          name: userData.username,
          email: userData.email,
          username: userData.username
        };
        
        setUser(user);
        console.log('AuthContext: Login successful, user set:', user);
        setIsLoading(false);
        return true;
      } else {
        console.error('AuthContext: Invalid response data from server:', userData);
        throw new Error('Invalid response data from server');
      }
    } catch (error: unknown) {
      console.error('AuthContext: Login error:', error);
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
      setIsLoading(false);
      return false;
    }
  };

  const register = async (username: string, email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await AuthService.register(username, email, password);
      
      // For FastAPI, registration might not return user data, just a success message
      // We'll redirect to login page after successful registration
      console.log('Registration successful:', response.data);
      
      setIsLoading(false);
      return true;
    } catch (error: unknown) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
      setIsLoading(false);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setError(null);
    AuthService.logout();
  };

  const value: AuthContextType = {
    user,
    login,
    register,
    logout,
    isLoading,
    error
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
