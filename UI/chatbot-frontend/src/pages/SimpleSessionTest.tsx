import React from 'react';
import { useAuth } from '../context/AuthContext';

const SimpleSessionTest: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Simple Session Test</h1>
      
      {user ? (
        <div className="bg-green-100 p-4 rounded">
          <p>✅ User is logged in: {user.username}</p>
          <p>User ID: {user.id}</p>
          <p>Email: {user.email}</p>
          
          <div className="mt-4">
            <h3 className="font-semibold">LocalStorage Debug:</h3>
            <pre className="bg-gray-100 p-2 rounded mt-2 text-sm">
              {JSON.stringify({
                user: localStorage.getItem('user'),
                session_timestamp: localStorage.getItem('session_timestamp'),
                current_time: Date.now()
              }, null, 2)}
            </pre>
          </div>
        </div>
      ) : (
        <div className="bg-red-100 p-4 rounded">
          <p>❌ No user logged in</p>
          <p>Please login first</p>
        </div>
      )}
    </div>
  );
};

export default SimpleSessionTest;