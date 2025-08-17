import { useState, useEffect } from 'react';
import AuthService from '../services/AuthService';
import { SESSION_CONFIG } from '../constants/api';

interface SessionInfo {
  isValid: boolean;
  timeRemaining: number; // in milliseconds
  timeRemainingFormatted: string;
  expiresAt: Date | null;
}

export const useSession = () => {
  const [sessionInfo, setSessionInfo] = useState<SessionInfo>({
    isValid: false,
    timeRemaining: 0,
    timeRemainingFormatted: '',
    expiresAt: null
  });

  const formatTimeRemaining = (milliseconds: number): string => {
    if (milliseconds <= 0) return 'Expired';
    
    const hours = Math.floor(milliseconds / (1000 * 60 * 60));
    const minutes = Math.floor((milliseconds % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else {
      return `${minutes}m`;
    }
  };

  const updateSessionInfo = () => {
    const user = AuthService.getCurrentUser();
    const isValid = AuthService.isSessionValid();
    
    if (user && isValid) {
      const timestamp = localStorage.getItem(SESSION_CONFIG.TIMESTAMP_KEY);
      if (timestamp) {
        const sessionStart = parseInt(timestamp, 10);
        const expiresAt = new Date(sessionStart + SESSION_CONFIG.TTL);
        const timeRemaining = Math.max(0, expiresAt.getTime() - Date.now());
        
        setSessionInfo({
          isValid: true,
          timeRemaining,
          timeRemainingFormatted: formatTimeRemaining(timeRemaining),
          expiresAt
        });
      }
    } else {
      setSessionInfo({
        isValid: false,
        timeRemaining: 0,
        timeRemainingFormatted: 'Expired',
        expiresAt: null
      });
    }
  };

  useEffect(() => {
    updateSessionInfo();
    
    // Update session info every minute
    const interval = setInterval(updateSessionInfo, 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  const refreshSession = () => {
    AuthService.refreshSession();
    updateSessionInfo();
  };

  return {
    ...sessionInfo,
    refreshSession,
    updateSessionInfo
  };
};