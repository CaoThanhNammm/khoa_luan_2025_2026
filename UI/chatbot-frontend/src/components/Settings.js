import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import UserService from '../services/UserService';

const Settings = ({ currentUser, darkMode, toggleDarkMode }) => {
  const { t, i18n } = useTranslation();
  const [settings, setSettings] = useState({
    language: i18n.language && i18n.language.includes('vi') ? 'vi' : 'en',
    notifications: true,
    displayMode: darkMode ? 'dark' : 'light'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    
    setSettings({ ...settings, [name]: newValue });
    
    // Apply language change immediately
    if (name === 'language') {
      i18n.changeLanguage(value);
      localStorage.setItem('language', value);
    }
    
    // Apply display mode change immediately
    if (name === 'displayMode') {
      const isDark = value === 'dark';
      if (isDark !== darkMode) {
        toggleDarkMode();
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    UserService.updateSettings(settings)
      .then(response => {
        setMessage({ text: t('settings.updateSuccess'), type: 'success' });
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
      <h2 className="mb-4">{t('settings.title')}</h2>
      
      {message.text && (
        <Alert variant={message.type} onClose={() => setMessage({ text: '', type: '' })} dismissible>
          {message.text}
        </Alert>
      )}
      
      <Row>
        <Col md={8} className="mx-auto">
          <Card className={darkMode ? 'bg-dark text-white border-secondary' : ''}>
            <Card.Header className={darkMode ? 'border-secondary' : ''}>
              <h4>{t('settings.preferences')}</h4>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-4">
                  <Form.Label>{t('settings.language')}</Form.Label>
                  <div className="d-flex flex-wrap gap-3">
                    <div className={`language-option ${settings.language === 'en' ? 'active' : ''}`}>
                      <Form.Check
                        type="radio"
                        id="language-en"
                        name="language"
                        value="en"
                        checked={settings.language === 'en'}
                        onChange={handleChange}
                        className="visually-hidden"
                      />
                      <label htmlFor="language-en" className="d-flex align-items-center">
                        <span className="me-2">🇺🇸</span>
                        <span>English</span>
                      </label>
                    </div>
                    
                    <div className={`language-option ${settings.language === 'vi' ? 'active' : ''}`}>
                      <Form.Check
                        type="radio"
                        id="language-vi"
                        name="language"
                        value="vi"
                        checked={settings.language === 'vi'}
                        onChange={handleChange}
                        className="visually-hidden"
                      />
                      <label htmlFor="language-vi" className="d-flex align-items-center">
                        <span className="me-2">🇻🇳</span>
                        <span>Tiếng Việt</span>
                      </label>
                    </div>
                  </div>
                </Form.Group>
                
                <Form.Group className="mb-4">
                  <Form.Label>{t('settings.displayMode')}</Form.Label>
                  <div className="theme-toggle-container">
                    <div className={`theme-toggle ${settings.displayMode === 'dark' ? 'dark-active' : ''}`}>
                      <Form.Check
                        type="radio"
                        id="display-light"
                        name="displayMode"
                        value="light"
                        checked={settings.displayMode === 'light'}
                        onChange={handleChange}
                        className="visually-hidden"
                      />
                      <Form.Check
                        type="radio"
                        id="display-dark"
                        name="displayMode"
                        value="dark"
                        checked={settings.displayMode === 'dark'}
                        onChange={handleChange}
                        className="visually-hidden"
                      />
                      <label htmlFor="display-light" className="theme-option light">
                        <i className="bi bi-sun"></i>
                        <span>{t('settings.lightMode')}</span>
                      </label>
                      <label htmlFor="display-dark" className="theme-option dark">
                        <i className="bi bi-moon"></i>
                        <span>{t('settings.darkMode')}</span>
                      </label>
                      <div className="toggle-indicator"></div>
                    </div>
                  </div>
                </Form.Group>
                
                <Form.Group className="mb-4">
                  <Form.Check
                    type="checkbox"
                    id="notifications"
                    name="notifications"
                    label={t('settings.enableNotifications')}
                    checked={settings.notifications}
                    onChange={handleChange}
                    className="custom-checkbox"
                    style={darkMode ? { color: 'white' } : {}}
                  />
                  <Form.Text className={`${darkMode ? 'text-light' : 'text-muted'}`}>
                    {t('settings.notificationsHelp')}
                  </Form.Text>
                </Form.Group>
                
                <hr className={`my-4 ${darkMode ? 'border-secondary' : ''}`} />
                
                <div className="d-grid">
                  <Button 
                    variant={darkMode ? "info" : "primary"}
                    type="submit" 
                    disabled={loading}
                    className="save-settings-btn"
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        {t('settings.saving')}
                      </>
                    ) : (
                      <><i className="bi bi-check-circle me-2"></i>{t('settings.saveSettings')}</>
                    )}
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Settings;