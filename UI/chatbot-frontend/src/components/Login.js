import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Form, Button, Alert, Card, InputGroup } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import AuthService from '../services/AuthService';

const Login = ({ setCurrentUser, darkMode }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const { t } = useTranslation();


  // Focus username input on mount
  useEffect(() => {
    document.getElementById('username-input')?.focus();
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    
    // Reset error
    setError('');
    
    // Validation
    if (!username || !password) {
      setError(t('required_fields'));
      return;
    }
    
    setLoading(true);
    
    AuthService.login(username, password)
      .then((userData) => {
        // Update the currentUser in the parent component
        setCurrentUser(userData);
        navigate('/chat');
      })
      .catch(error => {
        console.error("Login error:", error);
        setError(error.response?.data?.message || t('auth.failed'));
        setLoading(false);
        
        // Add shake animation to form
        const form = document.querySelector('.auth-form');
        form.classList.add('shake-animation');
        setTimeout(() => {
          form.classList.remove('shake-animation');
        }, 500);
      });
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className={`auth-page ${darkMode ? 'dark-mode' : ''}`} style={{
      backgroundColor: darkMode ? '#1a1a1a' : '#f0f2f5',
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div className="auth-background" style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        zIndex: 0
      }}>
        <div className="auth-shape" style={{
          backgroundColor: darkMode ? 'rgba(66, 66, 66, 0.3)' : 'rgba(200, 200, 200, 0.3)',
          borderRadius: '50%',
          position: 'absolute',
          top: '-150px',
          right: '-150px',
          width: '500px',
          height: '500px'
        }}></div>
        <div className="auth-shape" style={{
          backgroundColor: darkMode ? 'rgba(66, 66, 66, 0.2)' : 'rgba(200, 200, 200, 0.2)',
          borderRadius: '50%',
          position: 'absolute',
          bottom: '-150px',
          left: '-150px',
          width: '600px',
          height: '600px'
        }}></div>
      </div>
      
      <Card className={`auth-card ${darkMode ? 'dark-mode' : ''}`} style={{
        maxWidth: '480px',
        width: '100%',
        boxShadow: darkMode ? '0 5px 20px rgba(0, 0, 0, 0.3)' : '0 5px 20px rgba(0, 0, 0, 0.1)',
        borderRadius: '15px',
        overflow: 'hidden',
        border: darkMode ? '1px solid #2d2d2d' : '1px solid #ddd',
        backgroundColor: darkMode ? '#2d2d2d' : 'white',
        position: 'relative',
        zIndex: 1
      }}>
        <Card.Body className="p-4 p-md-5">
          <div className="auth-header text-center mb-4">
            <div className="auth-logo mb-3">
              <i className="bi bi-chat-dots-fill"></i>
            </div>
            <h2 className="auth-title">{t('welcome_back')}</h2>
            <p className="auth-subtitle">{t('login_prompt')}</p>
          </div>
          
          {error && (
            <Alert variant="danger" className="error-feedback">
              <i className="bi bi-exclamation-circle me-2"></i>
              {error}
            </Alert>
          )}
          
          <Form onSubmit={handleLogin} className="auth-form">
            <Form.Group className="mb-3">
              <Form.Label className={`auth-label ${darkMode ? 'dark-mode-text' : ''}`} style={darkMode ? { color: 'white !important' } : {}}>
                <i className="bi bi-person me-2"></i>
                {t('username')}
              </Form.Label>
              <InputGroup>
                <InputGroup.Text className={`auth-input-icon ${darkMode ? 'dark' : ''}`}>
                  <i className="bi bi-person-fill"></i>
                </InputGroup.Text>
                <Form.Control
                  id="username-input"
                  type="text"
                  placeholder={t('username')}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={loading}
                  className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                  style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                />
              </InputGroup>
            </Form.Group>
            
            <Form.Group className="mb-4">
              <Form.Label className={`auth-label ${darkMode ? 'dark-mode-text' : ''}`} style={darkMode ? { color: 'white !important' } : {}}>
                <i className="bi bi-lock me-2"></i>
                {t('password')}
              </Form.Label>
              <InputGroup>
                <InputGroup.Text className={`auth-input-icon ${darkMode ? 'dark' : ''}`}>
                  <i className="bi bi-lock-fill"></i>
                </InputGroup.Text>
                <Form.Control
                  type={showPassword ? "text" : "password"}
                  placeholder={t('password')}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                  style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                />
              </InputGroup>
              <div className="d-flex justify-content-end mt-2">
                <Link to="/forgot-password" className="auth-link">
                  {t('forgot_password')}
                </Link>
              </div>
            </Form.Group>
            
            <Button 
              variant="primary" 
              type="submit" 
              className="auth-button"
              disabled={loading}
            >
              {loading ? (
                <div className="auth-loading">
                  <span className="spinner-grow spinner-grow-sm me-2" role="status" aria-hidden="true"></span>
                  {t('app.loading')}
                </div>
              ) : (
                <>
                  <i className="bi bi-box-arrow-in-right me-2"></i>
                  {t('login')}
                </>
              )}
            </Button>
          </Form>
          
          <div className="auth-divider">
            <span>{t('or')}</span>
          </div>
          
          <div className="auth-social">
            <button className="auth-social-button google">
              <i className="bi bi-google"></i>
            </button>
            <button className="auth-social-button facebook">
              <i className="bi bi-facebook"></i>
            </button>
            <button className="auth-social-button github">
              <i className="bi bi-github"></i>
            </button>
          </div>
          
          <div className="text-center mt-4 auth-footer">
            <p className="mb-0">
              {t('dont_have_account')} 
              <Link to="/register" className="auth-link ms-1">
                {t('register_here')}
              </Link>
            </p>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Login;