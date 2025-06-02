import React, { createContext, useContext, useState} from 'react';
import type { ReactNode } from 'react';
import UserService, { type UserProfile, type UpdateProfileRequest, type UpdatePasswordRequest, type UserSettings } from '../services/UserService';
import { useAuth } from './AuthContext';

interface UserContextType {
  profile: UserProfile | null;
  settings: UserSettings | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  loadProfile: () => Promise<void>;
  updateProfile: (data: UpdateProfileRequest) => Promise<boolean>;
  updatePassword: (data: UpdatePasswordRequest) => Promise<boolean>;
  updateSettings: (data: UserSettings) => Promise<boolean>;
  clearError: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const response = await UserService.getUserProfile();
      setProfile(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load user profile');
      console.error('Error loading profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (data: UpdateProfileRequest): Promise<boolean> => {
    setLoading(true);
    try {
      const response = await UserService.updateProfile(data);
      setProfile(response.data);
      setError(null);
      return true;
    } catch (err) {
      setError('Failed to update profile');
      console.error('Error updating profile:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const updatePassword = async (data: UpdatePasswordRequest): Promise<boolean> => {
    setLoading(true);
    try {
      await UserService.updatePassword(data);
      setError(null);
      return true;
    } catch (err) {
      setError('Failed to update password');
      console.error('Error updating password:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const updateSettings = async (data: UserSettings): Promise<boolean> => {
    setLoading(true);
    try {
      const response = await UserService.updateSettings(data);
      setSettings(response.data);
      setError(null);
      return true;
    } catch (err) {
      setError('Failed to update settings');
      console.error('Error updating settings:', err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value: UserContextType = {
    profile,
    settings,
    loading,
    error,
    loadProfile,
    updateProfile,
    updatePassword,
    updateSettings,
    clearError
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
