import React from 'react';
import { useSettings } from '../context/SettingsContext';
import { BiX, BiCheck, BiError, BiInfoCircle } from 'react-icons/bi';

const NotificationContainer: React.FC = () => {
  const { notifications, dismissNotification } = useSettings();

  if (notifications.length === 0) return null;

  const getIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <BiCheck className="h-5 w-5" />;
      case 'error':
        return <BiError className="h-5 w-5" />;
      default:
        return <BiInfoCircle className="h-5 w-5" />;
    }
  };

  const getStyles = (type: string) => {
    switch (type) {
      case 'success':
        return 'bg-gradient-to-r from-green-500 to-emerald-500 border-green-600 dark:from-green-600 dark:to-emerald-600 dark:border-green-700 shadow-lg dark:shadow-green-500/25';
      case 'error':
        return 'bg-gradient-to-r from-red-500 to-rose-500 border-red-600 dark:from-red-600 dark:to-rose-600 dark:border-red-700 shadow-lg dark:shadow-red-500/25';
      default:
        return 'bg-gradient-to-r from-blue-500 to-indigo-500 border-blue-600 dark:from-blue-600 dark:to-indigo-600 dark:border-blue-700 shadow-lg dark:shadow-blue-500/25';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`${getStyles(notification.type)} text-white px-4 py-3 rounded-xl border-l-4 max-w-sm animate-fade-in flex items-center space-x-3 transition-all duration-300 backdrop-blur-xl hover-lift`}
        >
          {getIcon(notification.type)}
          <span className="flex-1 text-sm font-medium">{notification.message}</span>
          <button
            onClick={() => dismissNotification(notification.id)}
            className="text-white/80 hover:text-white transition-colors rounded-lg p-1 hover:bg-white/10"
          >
            <BiX className="h-4 w-4" />
          </button>
        </div>
      ))}
    </div>
  );
};

export default NotificationContainer;
