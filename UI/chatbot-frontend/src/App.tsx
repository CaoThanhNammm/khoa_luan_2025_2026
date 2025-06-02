import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import { UserProvider } from './context/UserContext';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ChatPage from './pages/ChatPage';

function App() {
  return (
    <AuthProvider>
      <UserProvider>
        <ChatProvider>
          <Router>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<HomePage />} />
                <Route path="login" element={<LoginPage />} />
                <Route path="register" element={<RegisterPage />} />
                <Route path="chat" element={<ChatPage />} />
              </Route>
            </Routes>
          </Router>
        </ChatProvider>
      </UserProvider>
    </AuthProvider>
  );
}

export default App;
