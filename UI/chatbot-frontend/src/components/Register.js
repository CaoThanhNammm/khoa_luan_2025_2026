import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Form, Button, Alert, Card, InputGroup } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import AuthService from '../services/AuthService';

const Register = ({ darkMode }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();
  const { t } = useTranslation();

  const validateEmail = (email) => {
    const re = /\S+@\S+\.\S+/;
    return re.test(email);
  };

  const handleRegister = (e) => {
    e.preventDefault();
    
    // Reset messages
    setError('');
    setSuccess(false);
    
    // Validation
    if (!username || !email || !password || !confirmPassword) {
      setError(t('required_fields'));
      return;
    }
    
    if (!validateEmail(email)) {
      setError(t('invalid_email'));
      return;
    }
    
    if (password.length < 6) {
      setError(t('password_length'));
      return;
    }
    
    if (password !== confirmPassword) {
      setError(t('passwords_not_match'));
      return;
    }
    
    setLoading(true);
    
    AuthService.register(username, email, password)
      .then(() => {
        setSuccess(true);
        setLoading(false);
        // Redirect to login page after 2 seconds
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      })
      .catch(error => {
        console.error("Registration error:", error);
        setError(error.response?.data?.message || t('app.error'));
        setLoading(false);
        
        // Add shake animation to form on error
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
      
      <Card className={`auth-card register-card ${darkMode ? 'dark-mode' : ''}`} style={{
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
            <h2 className="auth-title">{t('create_account')}</h2>
            <p className="auth-subtitle">{t('join_prompt')}</p>
          </div>
          
          {error && (
            <Alert variant="danger" className="error-feedback">
              <i className="bi bi-exclamation-circle me-2"></i>
              {error}
            </Alert>
          )}
          
          {success && (
            <Alert variant="success" className="success-feedback">
              <i className="bi bi-check-circle me-2"></i>
              {t('registration_success')}
            </Alert>
          )}
          
          <Form onSubmit={handleRegister} className="auth-form">
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
                  type="text"
                  placeholder={t('username')}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={loading || success}
                  className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                  style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                />
              </InputGroup>
            </Form.Group>
            
            <Form.Group className="mb-3">
              <Form.Label className={`auth-label ${darkMode ? 'dark-mode-text' : ''}`} style={darkMode ? { color: 'white !important' } : {}}>
                <i className="bi bi-envelope me-2"></i>
                {t('email')}
              </Form.Label>
              <InputGroup>
                <InputGroup.Text className={`auth-input-icon ${darkMode ? 'dark' : ''}`}>
                  <i className="bi bi-envelope-fill"></i>
                </InputGroup.Text>
                <Form.Control
                  type="email"
                  placeholder={t('email')}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading || success}
                  className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                  style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                />
              </InputGroup>
            </Form.Group>
            
            <Form.Group className="mb-3">
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
                  disabled={loading || success}
                  className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                  style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                />
              </InputGroup>
            </Form.Group>
            
            <Form.Group className="mb-4">
              <Form.Label className={`auth-label ${darkMode ? 'dark-mode-text' : ''}`} style={darkMode ? { color: 'white !important' } : {}}>
                <i className="bi bi-shield-lock me-2"></i>
                {t('confirm_password')}
              </Form.Label>
              <InputGroup>
                <InputGroup.Text className={`auth-input-icon ${darkMode ? 'dark' : ''}`}>
                  <i className="bi bi-shield-lock-fill"></i>
                </InputGroup.Text>
                <Form.Control
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder={t('confirm_password')}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  disabled={loading || success}
                  className={`auth-input ${darkMode ? 'dark-mode-text' : ''}`}
                  style={darkMode ? { color: 'white !important', WebkitTextFillColor: 'white' } : {}}
                />
              </InputGroup>
            </Form.Group>
            
            <div className="form-check mb-4">
              <input
                type="checkbox"
                className="form-check-input"
                id="termsCheck"
                required
              />
              <label className="form-check-label" style={darkMode ? { color: 'white' } : {}} htmlFor="termsCheck">
                {t('i_agree')} <a href="#" className="auth-link">{t('terms_conditions')}</a>
              </label>
            </div>
            
            <Button 
              variant="primary" 
              type="submit" 
              className="auth-button"
              disabled={loading || success}
            >
              {loading ? (
                <div className="auth-loading">
                  <span className="spinner-grow spinner-grow-sm me-2" role="status" aria-hidden="true"></span>
                  {t('app.loading')}
                </div>
              ) : (
                <>
                  <i className="bi bi-person-plus me-2"></i>
                  {t('register')}
                </>
              )}
            </Button>
          </Form>
          
          <div className="text-center mt-4 auth-footer">
            <p className="mb-0">
              {t('already_have_account')} 
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

export default Register;