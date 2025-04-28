import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { Form, Button, Alert, Card, InputGroup } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import AuthService from '../services/AuthService';

const ResetPassword = ({ darkMode }) => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [token, setToken] = useState('');
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();

  // Extract token from URL parameter
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const tokenFromUrl = searchParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    } else {
      setMessage(t('invalid_or_expired_token'));
      setIsError(true);
    }
  }, [location, t]);

  // Focus password input on mount
  useEffect(() => {
    document.getElementById('password-input')?.focus();
  }, []);

  const handleResetPassword = (e) => {
    e.preventDefault();
    
    // Reset messages
    setMessage('');
    setIsError(false);
    
    // Validation
    if (!password || !confirmPassword) {
      setMessage(t('required_fields'));
      setIsError(true);
      return;
    }

    if (password !== confirmPassword) {
      setMessage(t('passwords_do_not_match'));
      setIsError(true);
      return;
    }

    // Password strength validation
    if (password.length < 8) {
      setMessage(t('password_too_short'));
      setIsError(true);
      return;
    }
    
    setLoading(true);
    
    AuthService.resetPassword(token, password)
      .then(() => {
        setMessage(t('password_reset_success'));
        setIsError(false);
        // Redirect to login after 2 seconds
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      })
      .catch(error => {
        console.error("Password reset error:", error);
        setMessage(error.response?.data?.message || t('password_reset_failed'));
        setIsError(true);
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

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
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
              <i className="bi bi-shield-lock-fill"></i>
            </div>
            <h2 className="auth-title">{t('reset_password')}</h2>
            <p className="auth-subtitle">{t('create_new_password')}</p>
          </div>
          
          {message && (
            <Alert variant={isError ? "danger" : "success"} className="feedback-alert">
              <i className={`bi ${isError ? "bi-exclamation-circle" : "bi-check-circle"} me-2`}></i>
              {message}
            </Alert>
          )}
          
          {token && (
            <Form onSubmit={handleResetPassword} className="auth-form">
              <Form.Group className="mb-3">
                <Form.Label className={`auth-label ${darkMode ? 'dark-mode-text' : ''}`} style={darkMode ? { color: 'white !important' } : {}}>
                  <i className="bi bi-lock me-2"></i>
                  {t('new_password')}
                </Form.Label>
                <InputGroup>
                  <InputGroup.Text className={`auth-input-icon ${darkMode ? 'dark' : ''}`}>
                    <i className="bi bi-lock-fill"></i>
                  </InputGroup.Text>
                  <Form.Control
                    id="password-input"
                    type={showPassword ? "text" : "password"}
                    placeholder={t('enter_new_password')}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={loading}
                    className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                    style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                  />
                  <Button 
                    variant="outline-secondary"
                    onClick={togglePasswordVisibility}
                    className={`password-toggle ${darkMode ? 'dark' : ''}`}
                  >
                    <i className={`bi ${showPassword ? "bi-eye-slash" : "bi-eye"}`}></i>
                  </Button>
                </InputGroup>
              </Form.Group>
              
              <Form.Group className="mb-4">
                <Form.Label className={`auth-label ${darkMode ? 'dark-mode-text' : ''}`} style={darkMode ? { color: 'white !important' } : {}}>
                  <i className="bi bi-lock me-2"></i>
                  {t('confirm_password')}
                </Form.Label>
                <InputGroup>
                  <InputGroup.Text className={`auth-input-icon ${darkMode ? 'dark' : ''}`}>
                    <i className="bi bi-lock-fill"></i>
                  </InputGroup.Text>
                  <Form.Control
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder={t('confirm_new_password')}
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    disabled={loading}
                    className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                    style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                  />
                  <Button 
                    variant="outline-secondary"
                    onClick={toggleConfirmPasswordVisibility}
                    className={`password-toggle ${darkMode ? 'dark' : ''}`}
                  >
                    <i className={`bi ${showConfirmPassword ? "bi-eye-slash" : "bi-eye"}`}></i>
                  </Button>
                </InputGroup>
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
                    <i className="bi bi-check-lg me-2"></i>
                    {t('reset_password')}
                  </>
                )}
              </Button>
            </Form>
          )}
          
          <div className="text-center mt-4 auth-footer">
            <p className="mb-0">
              {t('remember_password')} 
              <Link to="/login" className="auth-link ms-1">
                {t('login_here')}
              </Link>
            </p>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default ResetPassword;