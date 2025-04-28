import React, { useState, useEffect, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './App.css';
import './i18n';

// Components
import Header from './components/Header';
import Login from './components/Login';
import Register from './components/Register';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import ChatInterface from './components/ChatInterface';
import ConversationList from './components/ConversationList';
import Profile from './components/Profile';
import Settings from './components/Settings';

// Services
import AuthService from './services/AuthService';

// Loading spinner component
const LoadingSpinner = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
  </div>
);

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(localStorage.getItem('darkMode') === 'true');
  const { i18n } = useTranslation();

  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    // Apply dark mode to body element
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    // Save preference to localStorage
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Router>
        <div className={`app-container ${darkMode ? 'dark-mode' : ''}`}>
          <Header 
            currentUser={currentUser} 
            setCurrentUser={setCurrentUser} 
            darkMode={darkMode}
            toggleDarkMode={toggleDarkMode}
          />
          
          {!loading && (
            <Routes>
              <Route path="/" element={currentUser ? <Navigate to="/chat" /> : <Navigate to="/login" />} />
              <Route path="/login" element={!currentUser ? <Login setCurrentUser={setCurrentUser} darkMode={darkMode} /> : <Navigate to="/chat" />} />
              <Route path="/register" element={!currentUser ? <Register darkMode={darkMode} /> : <Navigate to="/chat" />} />
              <Route path="/forgot-password" element={!currentUser ? <ForgotPassword darkMode={darkMode} /> : <Navigate to="/chat" />} />
              <Route path="/reset-password" element={!currentUser ? <ResetPassword darkMode={darkMode} /> : <Navigate to="/chat" />} />
              <Route path="/chat" element={currentUser ? <ChatInterface currentUser={currentUser} darkMode={darkMode} /> : <Navigate to="/login" />} />
              <Route path="/conversations" element={currentUser ? <ConversationList currentUser={currentUser} darkMode={darkMode} /> : <Navigate to="/login" />} />
              <Route path="/profile" element={currentUser ? <Profile currentUser={currentUser} setCurrentUser={setCurrentUser} darkMode={darkMode} /> : <Navigate to="/login" />} />
              <Route path="/settings" element={currentUser ? <Settings currentUser={currentUser} darkMode={darkMode} toggleDarkMode={toggleDarkMode} /> : <Navigate to="/login" />} />
            </Routes>
          )}
        </div>
      </Router>
    </Suspense>
  );
}

export default App;