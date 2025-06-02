import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiArrowBack, BiEnvelope, BiCheckCircle } from 'react-icons/bi';

const ForgotPasswordPage: React.FC = () => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isEmailSent, setIsEmailSent] = useState(false);
  const [error, setError] = useState('');

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email.trim()) {
      setError(t('auth.fill_all_fields'));
      return;
    }

    if (!validateEmail(email)) {
      setError(t('auth.invalid_email'));
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      // TODO: Implement forgot password API call
      const response = await fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setIsEmailSent(true);
      } else {
        const errorData = await response.json();
        setError(errorData.message || t('forgot_password.error_general'));
      }
    } catch {
      setError(t('forgot_password.error_connection'));
    } finally {
      setIsLoading(false);
    }
  };

  if (isEmailSent) {
    return (
      <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-2 transition-colors duration-300">
              {t('forgot_password.email_sent')}
            </h2>
            <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
              {t('forgot_password.check_email_instructions').replace('{email}', email)}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 transition-colors duration-300">
            <div className="space-y-4">
              <Link
                to="/login"
                className="w-full btn-primary inline-block text-center"
              >
                {t('forgot_password.back_to_login')}
              </Link>
              
              <button
                onClick={() => {
                  setIsEmailSent(false);
                  setEmail('');
                }}
                className="w-full px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-charcoal dark:hover:text-white transition-colors text-center"
              >
                {t('forgot_password.resend_email')}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-2 transition-colors duration-300">
            {t('forgot_password.title')}
          </h2>
          <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
            {t('forgot_password.instructions')}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 transition-colors duration-300">
          <div className="mb-6">
            <Link
              to="/login"
              className="inline-flex items-center text-gray-600 dark:text-gray-300 hover:text-charcoal dark:hover:text-white transition-colors"
            >
              <BiArrowBack className="h-5 w-5 mr-2" />
              {t('forgot_password.back_to_login')}
            </Link>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                {t('forgot_password.email_label')}
              </label>
              <div className="relative">
                <BiEnvelope className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field pl-10"
                  placeholder={t('forgot_password.email_placeholder')}
                  disabled={isLoading}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading || !email.trim()}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? t('forgot_password.sending') : t('forgot_password.send_button')}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
              {t('forgot_password.remember_password')}{' '}
              <Link
                to="/login"
                className="font-medium text-charcoal dark:text-white hover:text-lavender dark:hover:text-indigo-400 transition-colors"
              >
                {t('forgot_password.login_now')}
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;