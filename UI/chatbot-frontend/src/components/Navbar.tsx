import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useSettings } from '../context/SettingsContext';
import { BiLogOut, BiChat, BiHome, BiUser, BiMoon, BiSun } from 'react-icons/bi';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { settings, updateTheme } = useSettings();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const toggleTheme = () => {
    updateTheme(settings.theme === 'light' ? 'dark' : 'light');
  };
  return (
    <nav className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-100 dark:border-gray-700 sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <BiChat className="h-8 w-8 text-charcoal dark:text-white" />
            <span className="font-heading text-xl font-semibold text-charcoal dark:text-white">
              NLU ChatBot
            </span>
          </Link>

          {/* Navigation Icons */}
          <div className="flex items-center space-x-4">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              title={settings.theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
            >
              {settings.theme === 'light' ? (
                <BiMoon className="h-5 w-5" />
              ) : (
                <BiSun className="h-5 w-5" />
              )}
            </button>

            {user ? (
              <>
                <Link
                  to="/"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-lavender dark:hover:text-indigo-400 transition-colors"
                  title="Home"
                >
                  <BiHome className="h-5 w-5" />
                </Link>
                <Link
                  to="/chat"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-lavender dark:hover:text-indigo-400 transition-colors"
                  title="Chat"
                >
                  <BiChat className="h-5 w-5" />
                </Link>
                <Link
                  to="/profile"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-lavender dark:hover:text-indigo-400 transition-colors"
                  title="Profile"
                >
                  <BiUser className="h-5 w-5" />
                </Link>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-red-600 transition-colors"
                  title="Logout"
                >
                  <BiLogOut className="h-5 w-5" />
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 text-charcoal dark:text-white hover:text-lavender dark:hover:text-indigo-400 transition-colors font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
