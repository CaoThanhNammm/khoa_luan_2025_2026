import React from 'react';
import { useSession } from '../hooks/useSession';
import { useAuth } from '../context/AuthContext';

interface SessionStatusProps {
  showDetails?: boolean;
  className?: string;
}

export const SessionStatus: React.FC<SessionStatusProps> = ({ 
  showDetails = false, 
  className = '' 
}) => {
  const { user } = useAuth();
  const { isValid, timeRemainingFormatted, expiresAt, refreshSession } = useSession();

  if (!user) return null;

  const isExpiringSoon = isValid && expiresAt && (expiresAt.getTime() - Date.now()) < (60 * 60 * 1000); // Less than 1 hour

  return (
    <div className={`session-status ${className}`}>
      {showDetails && (
        <div className="text-sm text-gray-600 dark:text-gray-400">
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isValid ? 'bg-green-500' : 'bg-red-500'}`}></span>
            <span>Session: {isValid ? 'Active' : 'Expired'}</span>
          </div>
          
          {isValid && (
            <div className="mt-1">
              <span className={isExpiringSoon ? 'text-orange-500' : 'text-gray-600 dark:text-gray-400'}>
                Time remaining: {timeRemainingFormatted}
              </span>
              {isExpiringSoon && (
                <button
                  onClick={refreshSession}
                  className="ml-2 text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
                >
                  Extend Session
                </button>
              )}
            </div>
          )}
          
          {expiresAt && (
            <div className="text-xs text-gray-500 mt-1">
              Expires: {expiresAt.toLocaleString()}
            </div>
          )}
        </div>
      )}
      
      {/* Warning for expiring session */}
      {isExpiringSoon && !showDetails && (
        <div className="bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-2 text-sm">
          <div className="flex items-center justify-between">
            <span>⚠️ Session expires in {timeRemainingFormatted}</span>
            <button
              onClick={refreshSession}
              className="text-xs bg-orange-500 text-white px-2 py-1 rounded hover:bg-orange-600"
            >
              Extend
            </button>
          </div>
        </div>
      )}
    </div>
  );
};