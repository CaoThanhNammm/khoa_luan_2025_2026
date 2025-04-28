import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import UserService from '../services/UserService';

const Profile = ({ currentUser, setCurrentUser, darkMode }) => {
  const { t } = useTranslation();
  const [profile, setProfile] = useState({
    username: currentUser?.username || '',
    email: currentUser?.email || ''
  });
  const [password, setPassword] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleProfileChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handlePasswordChange = (e) => {
    setPassword({ ...password, [e.target.name]: e.target.value });
  };

  const handleProfileSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    UserService.updateProfile(profile)
      .then(response => {
        setMessage({ text: t('profile.updateSuccess'), type: 'success' });
        // Update current user in parent component
        if (setCurrentUser) {
          setCurrentUser({
            ...currentUser,
            username: profile.username,
            email: profile.email
          });
        }
      })
      .catch(error => {
        const resMessage = error.response?.data?.message || error.message || t('error.generic');
        setMessage({ text: resMessage, type: 'danger' });
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    
    // Validate passwords
    if (password.newPassword !== password.confirmPassword) {
      setMessage({ text: t('profile.passwordsMismatch'), type: 'danger' });
      return;
    }

    setLoading(true);
    setMessage({ text: '', type: '' });

    UserService.updatePassword({
      currentPassword: password.currentPassword,
      newPassword: password.newPassword
    })
      .then(response => {
        setMessage({ text: t('profile.passwordUpdateSuccess'), type: 'success' });
        setPassword({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        });
      })
      .catch(error => {
        const resMessage = error.response?.data?.message || error.message || t('error.generic');
        setMessage({ text: resMessage, type: 'danger' });
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Container className={`mt-4 ${darkMode ? 'dark-mode' : ''}`}>
      <h2 className="mb-4">{t('profile.title')}</h2>
      
      {message.text && (
        <Alert variant={message.type} onClose={() => setMessage({ text: '', type: '' })} dismissible>
          {message.text}
        </Alert>
      )}
      
      <Row>
        <Col md={6} className="mb-4">
          <Card className={darkMode ? 'bg-dark text-white' : ''}>
            <Card.Header className={darkMode ? 'border-secondary' : ''}>
              <h4>{t('profile.personalInfo')}</h4>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleProfileSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>{t('profile.username')}</Form.Label>
                  <Form.Control
                    type="text"
                    name="username"
                    value={profile.username}
                    onChange={handleProfileChange}
                    required
                    className={darkMode ? 'bg-dark text-white border-secondary' : ''}
                  />
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>{t('profile.email')}</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={profile.email}
                    onChange={handleProfileChange}
                    required
                    className={darkMode ? 'bg-dark text-white border-secondary' : ''}
                  />
                </Form.Group>
                
                <Button 
                  variant="primary" 
                  type="submit" 
                  disabled={loading}
                  className="w-100"
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      {t('profile.updating')}
                    </>
                  ) : (
                    <>{t('profile.updateProfile')}</>
                  )}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card className={darkMode ? 'bg-dark text-white' : ''}>
            <Card.Header className={darkMode ? 'border-secondary' : ''}>
              <h4>{t('profile.changePassword')}</h4>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handlePasswordSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>{t('profile.currentPassword')}</Form.Label>
                  <Form.Control
                    type="password"
                    name="currentPassword"
                    value={password.currentPassword}
                    onChange={handlePasswordChange}
                    required
                    className={darkMode ? 'bg-dark text-white border-secondary' : ''}
                  />
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>{t('profile.newPassword')}</Form.Label>
                  <Form.Control
                    type="password"
                    name="newPassword"
                    value={password.newPassword}
                    onChange={handlePasswordChange}
                    required
                    className={darkMode ? 'bg-dark text-white border-secondary' : ''}
                  />
                </Form.Group>
                
                <Form.Group className="mb-3">
                  <Form.Label>{t('profile.confirmPassword')}</Form.Label>
                  <Form.Control
                    type="password"
                    name="confirmPassword"
                    value={password.confirmPassword}
                    onChange={handlePasswordChange}
                    required
                    className={darkMode ? 'bg-dark text-white border-secondary' : ''}
                  />
                </Form.Group>
                
                <Button 
                  variant="primary" 
                  type="submit" 
                  disabled={loading}
                  className="w-100"
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      {t('profile.updating')}
                    </>
                  ) : (
                    <>{t('profile.updatePassword')}</>
                  )}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Profile;