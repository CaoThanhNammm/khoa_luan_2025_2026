import React from 'react';
import { useSession } from '../hooks/useSession';
import { useAuth } from '../context/AuthContext';

export const SessionDemo: React.FC = () => {
  const { user, logout } = useAuth();
  const { 
    isValid, 
    timeRemaining, 
    timeRemainingFormatted, 
    expiresAt, 
    refreshSession 
  } = useSession();

  if (!user) {
    return (
      <div className="p-4 bg-gray-100 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Session Status</h3>
        <p className="text-gray-600">Not logged in</p>
      </div>
    );
  }

  const isExpiringSoon = timeRemaining < (60 * 60 * 1000); // Less than 1 hour
  const progressPercentage = Math.max(0, (timeRemaining / (24 * 60 * 60 * 1000)) * 100);

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Session Management (24h TTL)
      </h3>
      
      {/* Session Status */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <span className={`w-3 h-3 rounded-full ${isValid ? 'bg-green-500' : 'bg-red-500'}`}></span>
          <span className="font-medium text-gray-700 dark:text-gray-300">
            Status: {isValid ? 'Active' : 'Expired'}
          </span>
        </div>
        
        {/* Progress Bar */}
        {isValid && (
          <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
            <div 
              className={`h-2 rounded-full transition-all duration-300 ${
                isExpiringSoon ? 'bg-orange-500' : 'bg-green-500'
              }`}
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
        )}
      </div>

      {/* Time Information */}
      {isValid && (
        <div className="space-y-2 mb-4">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Time Remaining:</span>
            <span className={`font-medium ${isExpiringSoon ? 'text-orange-600' : 'text-green-600'}`}>
              {timeRemainingFormatted}
            </span>
          </div>
          
          {expiresAt && (
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Expires At:</span>
              <span className="text-sm text-gray-500">
                {expiresAt.toLocaleString()}
              </span>
            </div>
          )}
          
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Progress:</span>
            <span className="text-sm text-gray-500">
              {progressPercentage.toFixed(1)}%
            </span>
          </div>
        </div>
      )}

      {/* Warning for expiring session */}
      {isExpiringSoon && isValid && (
        <div className="bg-orange-50 border-l-4 border-orange-400 p-3 mb-4">
          <div className="flex items-center">
            <span className="text-orange-600 mr-2">⚠️</span>
            <span className="text-orange-700 text-sm">
              Your session will expire soon! Consider extending it.
            </span>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-2 flex-wrap">
        {isValid && (
          <button
            onClick={refreshSession}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm"
          >
            Extend Session (24h)
          </button>
        )}
        
        <button
          onClick={logout}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors text-sm"
        >
          Logout
        </button>
      </div>

      {/* Debug Info */}
      <details className="mt-4">
        <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
          Debug Information
        </summary>
        <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-700 rounded text-xs font-mono">
          <div>User ID: {user.id}</div>
          <div>Username: {user.username}</div>
          <div>Session Valid: {isValid.toString()}</div>
          <div>Time Remaining (ms): {timeRemaining}</div>
          <div>Timestamp: {localStorage.getItem('session_timestamp')}</div>
          <div>Current Time: {Date.now()}</div>
        </div>
      </details>
    </div>
  );
};