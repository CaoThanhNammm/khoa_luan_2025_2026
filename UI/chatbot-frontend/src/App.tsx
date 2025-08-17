import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import { UserProvider } from './context/UserContext';
import { SettingsProvider } from './context/SettingsContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import NotificationContainer from './components/NotificationContainer';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import ChatPage from './pages/ChatPage';
import ProfilePage from './pages/ProfilePage';
import SessionTestPage from './pages/SessionTestPage';
import SimpleSessionTest from './pages/SimpleSessionTest';
import SyntaxTest from './components/test/SyntaxTest';
import { ApiDebugger } from './components/test';

function App() {
  return (
    <SettingsProvider>
      <AuthProvider>
        <UserProvider>
          <ChatProvider>
            <Router>             
               <Routes>
                <Route path="/" element={<Layout />}>
                  <Route index element={<HomePage />} />                  
                  <Route path="about" element={<AboutPage />} />
                  <Route path="contact" element={<ContactPage />} />
                  <Route path="login" element={<LoginPage />} />
                  <Route path="register" element={<RegisterPage />} />
                  <Route path="forgot-password" element={<ForgotPasswordPage />} />
                  <Route path="reset-password" element={<ResetPasswordPage />} />
                  <Route path="chat" element={
                    <ProtectedRoute>
                      <ChatPage />
                    </ProtectedRoute>
                  } />                  <Route path="profile" element={
                    <ProtectedRoute>
                      <ProfilePage />
                    </ProtectedRoute>
                  } />
                  <Route path="session-test" element={
                    <ProtectedRoute>
                      <SessionTestPage />
                    </ProtectedRoute>
                  } />
                  <Route path="simple-session" element={
                    <ProtectedRoute>
                      <SimpleSessionTest />
                    </ProtectedRoute>
                  } />
                  <Route path="syntax-test" element={<SyntaxTest />} />
                  <Route path="api-debug" element={
                    <ProtectedRoute>
                      <ApiDebugger />
                    </ProtectedRoute>
                  } />
                </Route>
              </Routes>
              <NotificationContainer />
            </Router>
          </ChatProvider>
        </UserProvider>
      </AuthProvider>
    </SettingsProvider>
  );
}

export default App;
