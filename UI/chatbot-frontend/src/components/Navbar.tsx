import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiLogOut, BiChat, BiHome, BiUser, BiInfoCircle, BiEnvelope } from 'react-icons/bi';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-100 dark:border-gray-700 sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">          
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <BiChat className="h-8 w-8 text-charcoal dark:text-white" />
            <span className="font-heading text-xl font-semibold text-charcoal dark:text-white">
              NLU AI
            </span>
          </Link>          
          {/* Navigation Icons */}
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <Link
                  to="/"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-black transition-colors"
                  title={t('nav.home')}
                >
                  <BiHome className="h-5 w-5" />
                </Link>
                <Link
                  to="/about"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-black transition-colors"
                  title={t('nav.about')}
                >
                  <BiInfoCircle className="h-5 w-5" />
                </Link>
                <Link
                  to="/contact"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-black transition-colors"
                  title={t('nav.contact')}
                >
                  <BiEnvelope className="h-5 w-5" />
                </Link>
                <Link
                  to="/chat"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-black transition-colors"
                  title={t('nav.chat')}
                >
                  <BiChat className="h-5 w-5" />
                </Link>
                <Link
                  to="/profile"
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-black transition-colors"
                  title={t('nav.profile')}
                >
                  <BiUser className="h-5 w-5" />
                </Link>                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg text-charcoal dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-black transition-colors"
                  title={t('nav.logout')}
                >
                  <BiLogOut className="h-5 w-5" />
                </button>
              </>
            ) : (
              <>                <Link
                to="/about"
                className="px-4 py-2 text-charcoal dark:text-white hover:text-black transition-colors font-medium"
              >
                {t('nav.about')}
              </Link>
                <Link
                  to="/contact"
                  className="px-4 py-2 text-charcoal dark:text-white hover:text-black transition-colors font-medium"
                >
                  {t('nav.contact')}
                </Link>
                <Link
                  to="/login"
                  className="px-4 py-2 text-charcoal dark:text-white hover:text-black transition-colors font-medium"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  {t('nav.register')}
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
