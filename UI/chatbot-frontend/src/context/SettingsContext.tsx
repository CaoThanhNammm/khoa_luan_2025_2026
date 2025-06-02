import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

export interface AppSettings {
  theme: 'light' | 'dark';
  language: string;
  notifications: boolean;
}

interface SettingsContextType {
  settings: AppSettings;
  updateTheme: (theme: 'light' | 'dark') => void;
  updateLanguage: (language: string) => void;
  updateNotifications: (enabled: boolean) => void;
  showNotification: (message: string, type?: 'success' | 'error' | 'info') => void;
  notifications: Array<{
    id: string;
    message: string;
    type: 'success' | 'error' | 'info';
    timestamp: Date;
  }>;
  dismissNotification: (id: string) => void;
  getSupportedLanguages: () => Array<{ code: string; name: string; nativeName: string }>;

}

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

interface SettingsProviderProps {
  children: ReactNode;
}

export const SettingsProvider: React.FC<SettingsProviderProps> = ({ children }) => {
  const [settings, setSettings] = useState<AppSettings>({
    theme: 'light',
    language: 'en',
    notifications: true
  });

  const [notifications, setNotifications] = useState<Array<{
    id: string;
    message: string;
    type: 'success' | 'error' | 'info';
    timestamp: Date;
  }>>([]);

  // Supported languages with their native names
  const getSupportedLanguages = () => [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'vi', name: 'Vietnamese', nativeName: 'Tiếng Việt' },
    { code: 'fr', name: 'French', nativeName: 'Français' },
    { code: 'de', name: 'German', nativeName: 'Deutsch' },
    { code: 'es', name: 'Spanish', nativeName: 'Español' }
  ];

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('app-settings');
    if (savedSettings) {
      const parsed = JSON.parse(savedSettings);
      // Validate language code
      const supportedLanguageCodes = getSupportedLanguages().map(lang => lang.code);
      if (!supportedLanguageCodes.includes(parsed.language)) {
        parsed.language = 'en'; // Fallback to English
      }
      setSettings(parsed);
      applyTheme(parsed.theme);
    }
  }, []);

  // Apply theme to document
  const applyTheme = (theme: 'light' | 'dark') => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const updateTheme = (theme: 'light' | 'dark') => {
    const newSettings = { ...settings, theme };
    setSettings(newSettings);
    localStorage.setItem('app-settings', JSON.stringify(newSettings));
    applyTheme(theme);
  };

  const updateLanguage = (language: string) => {
    // Validate language code
    const supportedLanguageCodes = getSupportedLanguages().map(lang => lang.code);
    if (!supportedLanguageCodes.includes(language)) {
      console.warn(`Unsupported language code: ${language}. Falling back to English.`);
      language = 'en';
    }
    
    const newSettings = { ...settings, language };
    setSettings(newSettings);
    localStorage.setItem('app-settings', JSON.stringify(newSettings));
  };

  const updateNotifications = (notifications: boolean) => {
    const newSettings = { ...settings, notifications };
    setSettings(newSettings);
    localStorage.setItem('app-settings', JSON.stringify(newSettings));
  };

  const showNotification = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    if (!settings.notifications) return;

    const notification = {
      id: Date.now().toString(),
      message,
      type,
      timestamp: new Date()
    };

    setNotifications(prev => [...prev, notification]);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
      dismissNotification(notification.id);
    }, 5000);
  };

  const dismissNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const value: SettingsContextType = {
    settings,
    updateTheme,
    updateLanguage,
    updateNotifications,
    showNotification,
    notifications,
    dismissNotification,
    getSupportedLanguages
  };

  return (
    <SettingsContext.Provider value={value}>
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = (): SettingsContextType => {
  const context = useContext(SettingsContext);
  if (context === undefined) {
    throw new Error('useSettings must be used within a SettingsProvider');
  }
  return context;
};
