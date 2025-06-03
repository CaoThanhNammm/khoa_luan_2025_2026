import React, { createContext, useContext, useState, useCallback} from 'react';
import type { ReactNode } from 'react';
import UserService, { type UserProfile, type UpdateProfileRequest, type UpdatePasswordRequest, type UserSettings, type AccountStats } from '../services/UserService';
import { useAuth } from './AuthContext';

interface UserContextType {
  profile: UserProfile | null;
  settings: UserSettings | null;
  stats: AccountStats | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  loadProfile: () => Promise<void>;
  loadSettings: () => Promise<void>;
  loadStats: () => Promise<void>;
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
  const [stats, setStats] = useState<AccountStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const loadProfile = useCallback(async () => {
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
  }, [user]);
  const loadSettings = useCallback(async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const response = await UserService.getUserSettings();
      setSettings(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load user settings');
      console.error('Error loading settings:', err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  const loadStats = useCallback(async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const response = await UserService.getAccountStats();
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load account statistics');
      console.error('Error loading stats:', err);
    } finally {
      setLoading(false);
    }
  }, [user]);

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
  };  const value: UserContextType = {
    profile,
    settings,
    stats,
    loading,
    error,
    loadProfile,
    loadSettings,
    loadStats,
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
