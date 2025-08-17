import React from 'react';
import { SessionDemo } from '../components/SessionDemo';
import { SessionStatus } from '../components/SessionStatus';

const SessionTestPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-8">
          Session Management Test
        </h1>
        
        <div className="space-y-6">
          {/* Session Status Component */}
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
              Session Status Component
            </h2>
            <SessionStatus showDetails={true} />
          </div>

          {/* Session Demo Component */}
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
              Session Demo Component
            </h2>
            <SessionDemo />
          </div>

          {/* Instructions */}
          <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-3 text-blue-800 dark:text-blue-200">
              How to Test 24h Session TTL
            </h3>
            <div className="space-y-2 text-blue-700 dark:text-blue-300">
              <p><strong>1. Login:</strong> Session timestamp will be saved automatically</p>
              <p><strong>2. Check localStorage:</strong> Look for 'session_timestamp' key</p>
              <p><strong>3. Auto-refresh:</strong> Session extends on API calls and every 30 minutes</p>
              <p><strong>4. Manual extend:</strong> Click "Extend Session" button</p>
              <p><strong>5. Test expiry:</strong> Change system time or wait 24 hours</p>
            </div>
          </div>

          {/* Technical Details */}
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-3 text-gray-800 dark:text-gray-200">
              Technical Implementation
            </h3>
            <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <p><strong>TTL:</strong> 24 hours (86,400,000 milliseconds)</p>
              <p><strong>Storage:</strong> localStorage with timestamp</p>
              <p><strong>Auto-refresh:</strong> Every 30 minutes + on API success</p>
              <p><strong>Validation:</strong> Checked on getCurrentUser() calls</p>
              <p><strong>Warning:</strong> Shows when &lt; 1 hour remaining</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SessionTestPage;