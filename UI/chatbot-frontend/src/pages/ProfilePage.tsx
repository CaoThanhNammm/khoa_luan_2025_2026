import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useUser } from '../context/UserContext';
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
  BiMoon,
  BiSun,
  BiBell,
  BiGlobe
} from 'react-icons/bi';

const ProfilePage: React.FC = () => {
  const { user } = useAuth();  const { 
    profile, 
    settings, 
    stats,
    loading, 
    error, 
    loadProfile, 
    loadSettings,
    loadStats,
    updateProfile, 
    updatePassword, 
    updateSettings,
    clearError 
  } = useUser();
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

  // Settings form
  const [settingsForm, setSettingsForm] = useState({
    theme: 'light' as 'light' | 'dark',
    notifications: true,
    language: 'en'
  });

  // Success and error messages
  const [successMessage, setSuccessMessage] = useState('');
  const [passwordError, setPasswordError] = useState('');  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadProfile();
    loadSettings();
    loadStats();
  }, [user, navigate, loadProfile, loadSettings, loadStats]);
  useEffect(() => {
    if (profile) {
      setProfileForm({
        email: profile.email
      });
    }
  }, [profile]);

  useEffect(() => {
    if (settings) {
      setSettingsForm(settings);
    }
  }, [settings]);

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    setSuccessMessage('');
    
    const success = await updateProfile(profileForm);
    if (success) {
      setIsEditingProfile(false);
      setSuccessMessage('Profile updated successfully!');
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError('');
    clearError();
    setSuccessMessage('');

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setPasswordError('New passwords do not match');
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      setPasswordError('New password must be at least 6 characters long');
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
      setSuccessMessage('Password updated successfully!');
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  };

  const handleSettingsChange = async (newSettings: Partial<typeof settingsForm>) => {
    const updatedSettings = { ...settingsForm, ...newSettings };
    setSettingsForm(updatedSettings);
    
    const success = await updateSettings(updatedSettings);
    if (success) {
      setSuccessMessage('Settings updated successfully!');
      setTimeout(() => setSuccessMessage(''), 3000);
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
    <div className="min-h-screen bg-gradient-to-br from-off-white via-beige to-lavender/20 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="font-heading text-4xl font-bold text-charcoal mb-2">
            My Profile
          </h1>
          <p className="text-gray-600">
            Manage your account settings and preferences
          </p>
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
            {successMessage}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Profile */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-heading text-2xl font-semibold text-charcoal flex items-center">
                  <BiUser className="h-6 w-6 mr-2" />
                  Profile Information
                </h2>
                {!isEditingProfile && (
                  <button
                    onClick={() => setIsEditingProfile(true)}
                    className="flex items-center space-x-1 text-charcoal hover:text-lavender transition-colors"
                  >
                    <BiEdit className="h-5 w-5" />
                    <span>Edit</span>
                  </button>
                )}
              </div>              {isEditingProfile ? (
                <form onSubmit={handleProfileSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-charcoal mb-2">
                      Email
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
                      <span>Save Changes</span>
                    </button>
                    <button
                      type="button"
                      onClick={cancelProfileEdit}
                      className="flex items-center space-x-1 btn-secondary"
                    >
                      <BiX className="h-4 w-4" />
                      <span>Cancel</span>
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-500 mb-1">
                      Username
                    </label>
                    <p className="text-charcoal font-medium">{profile?.username || user.username}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500 mb-1">
                      Email
                    </label>
                    <p className="text-charcoal font-medium">{profile?.email || user.email}</p>
                  </div>
                  {profile?.createdAt && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">
                        Member Since
                      </label>
                      <p className="text-charcoal font-medium">
                        {new Date(profile.createdAt).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Change Password */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-heading text-2xl font-semibold text-charcoal flex items-center">
                  <BiLock className="h-6 w-6 mr-2" />
                  Change Password
                </h2>
                {!isEditingPassword && (
                  <button
                    onClick={() => setIsEditingPassword(true)}
                    className="flex items-center space-x-1 text-charcoal hover:text-lavender transition-colors"
                  >
                    <BiEdit className="h-5 w-5" />
                    <span>Change</span>
                  </button>
                )}
              </div>

              {isEditingPassword ? (
                <form onSubmit={handlePasswordSubmit} className="space-y-4">
                  {passwordError && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded text-sm">
                      {passwordError}
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-charcoal mb-2">
                      Current Password
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
                    <label className="block text-sm font-medium text-charcoal mb-2">
                      New Password
                    </label>
                    <div className="relative">
                      <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showNewPassword ? 'text' : 'password'}
                        value={passwordForm.newPassword}
                        onChange={(e) => setPasswordForm(prev => ({ ...prev, newPassword: e.target.value }))}
                        className="input-field pl-10 pr-10"
                        required
                        minLength={6}
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
                    <label className="block text-sm font-medium text-charcoal mb-2">
                      Confirm New Password
                    </label>
                    <div className="relative">
                      <BiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={passwordForm.confirmPassword}
                        onChange={(e) => setPasswordForm(prev => ({ ...prev, confirmPassword: e.target.value }))}
                        className="input-field pl-10 pr-10"
                        required
                        minLength={6}
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
                      <span>Update Password</span>
                    </button>
                    <button
                      type="button"
                      onClick={cancelPasswordEdit}
                      className="flex items-center space-x-1 btn-secondary"
                    >
                      <BiX className="h-4 w-4" />
                      <span>Cancel</span>
                    </button>
                  </div>
                </form>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <BiLock className="h-12 w-12 mx-auto mb-3 opacity-50" />
                  <p>Click "Change" to update your password</p>
                </div>
              )}
            </div>
          </div>

          {/* Settings Sidebar */}
          <div className="space-y-6">
            {/* Account Settings */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="font-heading text-xl font-semibold text-charcoal flex items-center mb-6">
                <BiCog className="h-5 w-5 mr-2" />
                Settings
              </h3>

              <div className="space-y-6">
                {/* Theme Setting */}
                <div>
                  <label className="block text-sm font-medium text-charcoal mb-3">
                    Theme
                  </label>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleSettingsChange({ theme: 'light' })}
                      className={`flex items-center space-x-2 px-3 py-2 rounded-lg border transition-colors ${
                        settingsForm.theme === 'light'
                          ? 'bg-lavender/20 border-lavender text-charcoal'
                          : 'border-gray-200 text-gray-600 hover:border-lavender'
                      }`}
                    >
                      <BiSun className="h-4 w-4" />
                      <span>Light</span>
                    </button>
                    <button
                      onClick={() => handleSettingsChange({ theme: 'dark' })}
                      className={`flex items-center space-x-2 px-3 py-2 rounded-lg border transition-colors ${
                        settingsForm.theme === 'dark'
                          ? 'bg-lavender/20 border-lavender text-charcoal'
                          : 'border-gray-200 text-gray-600 hover:border-lavender'
                      }`}
                    >
                      <BiMoon className="h-4 w-4" />
                      <span>Dark</span>
                    </button>
                  </div>
                </div>

                {/* Notifications */}
                <div>
                  <label className="flex items-center justify-between">
                    <span className="text-sm font-medium text-charcoal flex items-center">
                      <BiBell className="h-4 w-4 mr-2" />
                      Notifications
                    </span>
                    <button
                      onClick={() => handleSettingsChange({ notifications: !settingsForm.notifications })}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        settingsForm.notifications ? 'bg-lavender' : 'bg-gray-200'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          settingsForm.notifications ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </label>
                </div>

                {/* Language */}
                <div>
                  <label className="block text-sm font-medium text-charcoal mb-2">
                    <BiGlobe className="h-4 w-4 inline mr-2" />
                    Language
                  </label>
                  <select
                    value={settingsForm.language}
                    onChange={(e) => handleSettingsChange({ language: e.target.value })}
                    className="w-full input-field"
                  >
                    <option value="en">English</option>
                    <option value="vi">Tiếng Việt</option>
                    <option value="fr">Français</option>
                    <option value="de">Deutsch</option>
                    <option value="es">Español</option>
                  </select>
                </div>
              </div>
            </div>            {/* Account Stats */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="font-heading text-xl font-semibold text-charcoal mb-4">
                Account Statistics
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Conversations</span>
                  <span className="font-medium text-charcoal">{stats?.totalConversations || '-'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Messages Sent</span>
                  <span className="font-medium text-charcoal">{stats?.totalMessages || '-'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Account Status</span>
                  <span className="font-medium text-green-600">{stats?.accountStatus || 'Active'}</span>
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
