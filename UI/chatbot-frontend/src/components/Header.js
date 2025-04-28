import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Navbar, Nav, Container, Button, Dropdown } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import AuthService from '../services/AuthService';

const Header = ({ currentUser, setCurrentUser, darkMode, toggleDarkMode }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [expanded, setExpanded] = useState(false);
  const { t, i18n } = useTranslation();

  const handleLogout = () => {
    AuthService.logout();
    setCurrentUser(null);
    navigate('/login');
  };

  const closeNavbar = () => setExpanded(false);

  return (
    <Navbar 
      bg={darkMode ? "dark" : "light"} 
      variant={darkMode ? "dark" : "light"}
      expand="lg" 
      expanded={expanded} 
      onToggle={setExpanded} 
      className={`navbar ${darkMode ? 'navbar-dark' : ''}`}
    >
      <Container>
        <Navbar.Brand as={Link} to="/" onClick={closeNavbar} className="d-flex align-items-center">
          <i className="bi bi-chat-dots-fill me-2" style={{ color: darkMode ? '#4cc9f0' : '#0d6efd', fontSize: '1.5rem' }}></i>
          {t('app.title')}
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {currentUser && (
              <>
                <Nav.Link 
                  as={Link} 
                  to="/chat" 
                  onClick={closeNavbar}
                  className={location.pathname === '/chat' ? 'active' : ''}
                >
                  <i className="bi bi-chat-text me-1"></i> {t('chat')}
                </Nav.Link>
                <Nav.Link 
                  as={Link} 
                  to="/conversations" 
                  onClick={closeNavbar}
                  className={location.pathname === '/conversations' ? 'active' : ''}
                >
                  <i className="bi bi-clock-history me-1"></i> {t('history')}
                </Nav.Link>
              </>
            )}
          </Nav>
          <Nav>
            {currentUser ? (
              <Dropdown align="end">
                <Dropdown.Toggle variant={darkMode ? "info" : "primary"} id="dropdown-user" className="d-flex align-items-center user-dropdown">
                  <i className="bi bi-person-circle me-1"></i>
                  {currentUser.username}
                </Dropdown.Toggle>
                <Dropdown.Menu className={darkMode ? 'dropdown-menu-dark' : ''}>
                  <Dropdown.Item as={Link} to="/profile" onClick={closeNavbar}>
                    <i className="bi bi-person me-2"></i> {t('profile.title')}
                  </Dropdown.Item>
                  <Dropdown.Item as={Link} to="/settings" onClick={closeNavbar}>
                    <i className="bi bi-gear me-2"></i> {t('settings')}
                  </Dropdown.Item>
                  <Dropdown.Divider />
                  <Dropdown.Item onClick={handleLogout} className="logout-item">
                    <i className="bi bi-box-arrow-right me-2"></i> {t('auth.logout')}
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            ) : (
              <>
                <Button 
                  as={Link} 
                  to="/login" 
                  variant={darkMode ? "outline-info" : "outline-primary"} 
                  className="me-2 auth-nav-btn"
                  onClick={closeNavbar}
                >
                  <i className="bi bi-box-arrow-in-right me-1"></i> {t('auth.login')}
                </Button>
                <Button 
                  as={Link} 
                  to="/register" 
                  variant={darkMode ? "info" : "primary"}
                  className="auth-nav-btn"
                  onClick={closeNavbar}
                >
                  <i className="bi bi-person-plus me-1"></i> {t('auth.register')}
                </Button>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;