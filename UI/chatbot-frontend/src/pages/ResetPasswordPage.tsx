import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { BiArrowBack, BiLock, BiShow, BiHide, BiCheckCircle } from 'react-icons/bi';

const ResetPasswordPage: React.FC = () => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [formData, setFormData] = useState({
    newPassword: '',
    confirmPassword: ''
  });
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) {
      setError(t('reset_password.invalid_token'));
    }
  }, [token, t]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.newPassword || !formData.confirmPassword) {
      setError(t('auth.fill_all_fields'));
      return;
    }

    if (formData.newPassword !== formData.confirmPassword) {
      setError(t('reset_password.passwords_no_match'));
      return;
    }

    if (formData.newPassword.length < 6) {
      setError(t('reset_password.password_min_length'));
      return;
    }

    if (!token) {
      setError(t('reset_password.invalid_token'));
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          token, 
          newPassword: formData.newPassword 
        }),
      });

      if (response.ok) {
        setIsSuccess(true);
      } else {
        const errorData = await response.json();
        setError(errorData.message || t('reset_password.error_general'));
      }
    } catch {
      setError(t('reset_password.error_connection'));
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-off-white via-beige to-lavender/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-2 transition-colors duration-300">
              {t('reset_password.success')}
            </h2>
            <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
              {t('reset_password.success_message')}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 transition-colors duration-300">
            <div className="space-y-4">
              <button
                onClick={() => navigate('/login')}
                className="w-full btn-primary"
              >
                {t('reset_password.login_now')}
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
            {t('reset_password.title')}
          </h2>
          <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
            {t('reset_password.instructions')}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 transition-colors duration-300">
          <div className="mb-6">
            <Link
              to="/login"
              className="inline-flex items-center text-gray-600 dark:text-gray-300 hover:text-charcoal dark:hover:text-white transition-colors"
            >
              <BiArrowBack className="h-5 w-5 mr-2" />
              {t('reset_password.back_to_login')}
            </Link>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="newPassword" className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                {t('reset_password.new_password')}
              </label>
              <div className="relative">
                <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  id="newPassword"
                  name="newPassword"
                  type={showNewPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  value={formData.newPassword}
                  onChange={handleChange}
                  className="input-field pl-10 pr-10"
                  placeholder={t('reset_password.new_password_placeholder')}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showNewPassword ? <BiHide className="h-5 w-5" /> : <BiShow className="h-5 w-5" />}
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                {t('reset_password.confirm_password')}
              </label>
              <div className="relative">
                <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="input-field pl-10 pr-10"
                  placeholder={t('reset_password.confirm_password_placeholder')}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showConfirmPassword ? <BiHide className="h-5 w-5" /> : <BiShow className="h-5 w-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading || !formData.newPassword.trim() || !formData.confirmPassword.trim()}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? t('reset_password.resetting') : t('reset_password.reset_button')}
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

export default ResetPasswordPage;