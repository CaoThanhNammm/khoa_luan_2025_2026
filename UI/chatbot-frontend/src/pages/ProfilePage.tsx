import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useUser } from '../context/UserContext';
import { useSettings } from '../context/SettingsContext';
import { useTranslation } from '../utils/translations';
import { 
  BiUser, 
  BiEnvelope, 
  BiLock, 
  BiEdit, 
  BiSave, 
  BiX, 
  BiShow, 
  BiHide,
  BiCog,
  BiGlobe
} from 'react-icons/bi';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const { 
    profile, 
    stats,
    loading, 
    error, 
    loadProfile, 
    loadStats,
    updateProfile, 
    updatePassword, 
    clearError 
  } = useUser();
  
  const { 
    settings, 
    updateTheme, 
    updateLanguage, 
    updateNotifications,
    showNotification 
  } = useSettings();
  
  const { t } = useTranslation(settings.language);
  const navigate = useNavigate();

  // Form states
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isEditingPassword, setIsEditingPassword] = useState(false);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Profile form (only email is editable)
  const [profileForm, setProfileForm] = useState({
    email: ''
  });

  // Password form
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Error messages
  const [passwordError, setPasswordError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadProfile();
    loadStats();
  }, [user, navigate, loadProfile, loadStats]);

  useEffect(() => {
    if (profile) {
      setProfileForm({
        email: profile.email
      });
    }
  }, [profile]);

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    
    const success = await updateProfile(profileForm);
    if (success) {
      setIsEditingProfile(false);
      showNotification(t('profile.profile_updated'), 'success');
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError('');
    clearError();

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setPasswordError(t('profile.password_no_match'));
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      setPasswordError(t('profile.password_min_length'));
      return;
    }

    const success = await updatePassword({
      currentPassword: passwordForm.currentPassword,
      newPassword: passwordForm.newPassword
    });

    if (success) {
      setIsEditingPassword(false);
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      showNotification(t('profile.password_updated'), 'success');
    }
  };

  const handleSettingsChange = async (settingType: string, value: string | boolean) => {
    switch (settingType) {
      case 'theme':
        updateTheme(value as 'light' | 'dark');
        showNotification(t('settings.theme_updated'), 'success');
        break;
      case 'language':
        updateLanguage(value as string);
        showNotification(t('settings.language_updated'), 'success');
        break;
      case 'notifications':
        updateNotifications(value as boolean);
        showNotification(t('settings.notifications_updated'), 'success');
        break;
    }
  };

  const cancelProfileEdit = () => {
    setIsEditingProfile(false);
    if (profile) {
      setProfileForm({
        email: profile.email
      });
    }
  };

  const cancelPasswordEdit = () => {
    setIsEditingPassword(false);
    setPasswordForm({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    setPasswordError('');
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-8 px-4 transition-colors duration-500 relative overflow-hidden">
      {/* Enhanced decorative background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-lavender/10 to-sky-blue/10 dark:from-indigo-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-blue/10 to-lavender/10 dark:from-purple-500/10 dark:to-indigo-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-purple-200/5 to-blue-200/5 dark:from-indigo-400/5 dark:to-purple-400/5 rounded-full blur-3xl animate-aurora"></div>
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="font-heading text-4xl font-bold text-charcoal dark:text-white mb-2 transition-colors duration-300">
            {t('profile.title')}
          </h1>
          <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
            {t('profile.subtitle')}
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg text-sm backdrop-blur-xl">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Profile */}
            <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl rounded-2xl shadow-lg dark:shadow-2xl border border-white/20 dark:border-slate-600/30 p-6 transition-all duration-300 hover-lift">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-heading text-2xl font-semibold text-charcoal dark:text-white flex items-center">
                  <BiUser className="h-6 w-6 mr-2" />
                  {t('profile.info')}
                </h2>
                {!isEditingProfile && (
                  <button
                    onClick={() => setIsEditingProfile(true)}
                    className="flex items-center space-x-1 text-charcoal dark:text-white hover:text-lavender dark:hover:text-indigo-400 transition-colors"
                  >
                    <BiEdit className="h-5 w-5" />
                    <span>{t('profile.edit')}</span>
                  </button>
                )}
              </div>

              {isEditingProfile ? (
                <form onSubmit={handleProfileSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-charcoal dark:text-white mb-2">
                      {t('auth.email')}
                    </label>
                    <div className="relative">
                      <BiEnvelope className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type="email"
                        value={profileForm.email}
                        onChange={(e) => setProfileForm(prev => ({ ...prev, email: e.target.value }))}
                        className="input-field pl-10"
                        required
                      />
                    </div>
                  </div>

                  <div className="flex space-x-3 pt-4">
                    <button
                      type="submit"
                      disabled={loading}
                      className="flex items-center space-x-1 btn-primary disabled:opacity-50"
                    >
                      <BiSave className="h-4 w-4" />
                      <span>{t('profile.save')}</span>
                    </button>
                    <button
                      type="button"
                      onClick={cancelProfileEdit}
                      className="flex items-center space-x-1 btn-secondary"
                    >
                      <BiX className="h-4 w-4" />
                      <span>{t('profile.cancel')}</span>
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                      {t('auth.username')}
                    </label>
                    <p className="text-charcoal dark:text-white font-medium">{user?.username}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                      {t('auth.email')}
                    </label>
                    <p className="text-charcoal dark:text-white font-medium">{profile?.email}</p>
                  </div>
                  {profile?.createdAt && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                        {t('profile.member_since')}
                      </label>
                      <p className="text-charcoal dark:text-white font-medium">
                        {new Date(profile.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Change Password */}
            <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl rounded-2xl shadow-lg dark:shadow-2xl border border-white/20 dark:border-slate-600/30 p-6 transition-all duration-300 hover-lift">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-heading text-2xl font-semibold text-charcoal dark:text-white flex items-center">
                  <BiLock className="h-6 w-6 mr-2" />
                  {t('profile.change_password')}
                </h2>
                {!isEditingPassword && (
                  <button
                    onClick={() => setIsEditingPassword(true)}
                    className="flex items-center space-x-1 text-charcoal dark:text-white hover:text-lavender dark:hover:text-indigo-400 transition-colors"
                  >
                    <BiEdit className="h-5 w-5" />
                    <span>{t('profile.change')}</span>
                  </button>
                )}
              </div>

              {isEditingPassword ? (
                <form onSubmit={handlePasswordSubmit} className="space-y-4">
                  {passwordError && (
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-3 py-2 rounded text-sm">
                      {passwordError}
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-charcoal dark:text-white mb-2">
                      {t('profile.current_password')}
                    </label>
                    <div className="relative">
                      <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showCurrentPassword ? 'text' : 'password'}
                        value={passwordForm.currentPassword}
                        onChange={(e) => setPasswordForm(prev => ({ ...prev, currentPassword: e.target.value }))}
                        className="input-field pl-10 pr-10"
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showCurrentPassword ? <BiHide className="h-5 w-5" /> : <BiShow className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-charcoal dark:text-white mb-2">
                      {t('profile.new_password')}
                    </label>
                    <div className="relative">
                      <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showNewPassword ? 'text' : 'password'}
                        value={passwordForm.newPassword}
                        onChange={(e) => setPasswordForm(prev => ({ ...prev, newPassword: e.target.value }))}
                        className="input-field pl-10 pr-10"
                        required
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
                    <label className="block text-sm font-medium text-charcoal dark:text-white mb-2">
                      {t('profile.confirm_new_password')}
                    </label>
                    <div className="relative">
                      <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={passwordForm.confirmPassword}
                        onChange={(e) => setPasswordForm(prev => ({ ...prev, confirmPassword: e.target.value }))}
                        className="input-field pl-10 pr-10"
                        required
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

                  <div className="flex space-x-3 pt-4">
                    <button
                      type="submit"
                      disabled={loading}
                      className="flex items-center space-x-1 btn-primary disabled:opacity-50"
                    >
                      <BiSave className="h-4 w-4" />
                      <span>{t('profile.update_password')}</span>
                    </button>
                    <button
                      type="button"
                      onClick={cancelPasswordEdit}
                      className="flex items-center space-x-1 btn-secondary"
                    >
                      <BiX className="h-4 w-4" />
                      <span>{t('profile.cancel')}</span>
                    </button>
                  </div>
                </form>
              ) : (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  <BiLock className="h-12 w-12 mx-auto mb-3 opacity-50" />
                  <p>{t('profile.click_change_password')}</p>
                </div>
              )}
            </div>
          </div>

          {/* Settings Sidebar */}
          <div className="space-y-6">
            {/* Account Settings */}
            <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl rounded-2xl shadow-lg dark:shadow-2xl border border-white/20 dark:border-slate-600/30 p-6 transition-all duration-300 hover-lift">
              <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white flex items-center mb-6 transition-colors duration-300">
                <BiCog className="h-5 w-5 mr-2" />
                {t('profile.settings')}
              </h3>

              <div className="space-y-6">
                {/* Theme Setting */}
                <div>
                  <label className="block text-sm font-medium text-charcoal dark:text-white mb-3 transition-colors duration-300">
                    {t('settings.theme')}
                  </label>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleSettingsChange('theme', 'light')}
                      className={`px-4 py-2 rounded-lg transition-colors ${
                        settings.theme === 'light'
                          ? 'bg-lavender text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {t('settings.light')}
                    </button>
                    <button
                      onClick={() => handleSettingsChange('theme', 'dark')}
                      className={`px-4 py-2 rounded-lg transition-colors ${
                        settings.theme === 'dark'
                          ? 'bg-lavender text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {t('settings.dark')}
                    </button>
                  </div>
                </div>

                {/* Notifications */}
                <div>
                  <label className="flex items-center justify-between">
                    <span className="text-sm font-medium text-charcoal dark:text-white transition-colors duration-300">
                      {t('settings.notifications')}
                    </span>
                    <input
                      type="checkbox"
                      checked={settings.notifications}
                      onChange={(e) => handleSettingsChange('notifications', e.target.checked)}
                      className="rounded"
                    />
                  </label>
                </div>

                {/* Language */}
                <div>
                  <label className="block text-sm font-medium text-charcoal dark:text-white mb-2 transition-colors duration-300">
                    <BiGlobe className="h-4 w-4 inline mr-2" />
                    {t('settings.language')}
                  </label>
                  <select
                    value={settings.language}
                    onChange={(e) => handleSettingsChange('language', e.target.value)}
                    className="w-full input-field backdrop-blur-sm"
                  >
                    <option value="en">English</option>
                    <option value="vi">Tiếng Việt</option>
                    <option value="fr">Français</option>
                    <option value="de">Deutsch</option>
                    <option value="es">Español</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Account Stats */}
            <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl rounded-2xl shadow-lg dark:shadow-2xl border border-white/20 dark:border-slate-600/30 p-6 transition-all duration-300 hover-lift">
              <h3 className="font-heading text-xl font-semibold text-charcoal dark:text-white mb-4 transition-colors duration-300">
                {t('profile.stats')}
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center py-2 border-b border-gray-100/50 dark:border-slate-600/30">
                  <span className="text-gray-600 dark:text-gray-300 transition-colors duration-300">{t('profile.total_conversations')}</span>
                  <span className="font-medium text-charcoal dark:text-white px-3 py-1 bg-gradient-to-r from-lavender/20 to-sky-blue/20 dark:from-indigo-500/20 dark:to-purple-500/20 rounded-full transition-colors duration-300">
                    {stats?.totalConversations || 0}
                  </span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-600 dark:text-gray-300 transition-colors duration-300">{t('profile.messages_sent')}</span>
                  <span className="font-medium text-charcoal dark:text-white px-3 py-1 bg-gradient-to-r from-lavender/20 to-sky-blue/20 dark:from-indigo-500/20 dark:to-purple-500/20 rounded-full transition-colors duration-300">
                    {stats?.totalMessages || 0}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
