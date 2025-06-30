import React from 'react';
import { BiChat, BiPlus, BiTrash, BiTime, BiMessage } from 'react-icons/bi';
import { useSettings } from '../../context/SettingsContext';
import { useTranslation } from '../../utils/translations';
import type { SidebarChatSession } from '../../types/chat';

interface ChatSidebarProps {
  isSidebarOpen: boolean;
  setIsSidebarOpen: (open: boolean) => void;
  chatSessions: SidebarChatSession[];
  currentSessionId: string;
  onCreateNewSession: () => void;
  onSwitchToSession: (sessionId: string) => void;
  onDeleteSession: (sessionId: string) => void;
}

const ChatSidebar: React.FC<ChatSidebarProps> = ({
  isSidebarOpen,
  setIsSidebarOpen,
  chatSessions,
  currentSessionId,
  onCreateNewSession,
  onSwitchToSession,
  onDeleteSession
}) => {
  const { settings } = useSettings();
  const { t } = useTranslation(settings.language);

  const formatTimeAgo = (date: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className={`${isSidebarOpen ? 'w-80' : 'w-16'} bg-white/98 dark:bg-slate-900/98 backdrop-blur-xl border-r border-gray-200/60 dark:border-slate-700/60 shadow-xl dark:shadow-2xl transition-all duration-300 flex flex-col relative z-10`}>
      {/* Enhanced Sidebar Header */}
      <div className="p-4 border-b border-gray-200/60 dark:border-slate-700/60 bg-gradient-to-r from-gray-50/95 to-gray-100/95 dark:from-slate-800/95 dark:to-slate-900/95 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          {isSidebarOpen && (
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 bg-gradient-to-br from-blue-500 to-indigo-600 dark:from-blue-400 dark:to-indigo-500 rounded-lg flex items-center justify-center shadow-lg">
                <BiChat className="h-4 w-4 text-white" />
              </div>
              <h2 className="font-heading text-lg font-bold text-gray-800 dark:text-gray-100 transition-colors duration-300">
                {t('chat.history')}
              </h2>
            </div>
          )}
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2.5 rounded-xl bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:hover:bg-slate-600 transition-all duration-200 group hover-lift shadow-md border border-gray-200/50 dark:border-slate-600/50"
          >
            <BiChat className="h-5 w-5 text-gray-600 dark:text-gray-300 group-hover:scale-110 transition-transform" />
          </button>
        </div>
        
        {isSidebarOpen && (
          <button
            onClick={onCreateNewSession}
            className="w-full mt-4 flex items-center justify-center space-x-2 p-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-2xl hover:shadow-lg transition-all duration-200 font-semibold hover-lift group"
          >
            <BiPlus className="h-5 w-5 group-hover:rotate-90 transition-transform duration-200" />
            <span>{t('chat.new_chat')}</span>
          </button>
        )}
      </div>

      {/* Chat Sessions List */}
      {isSidebarOpen && (
        <div className="flex-1 overflow-y-auto p-3 space-y-2 hide-scrollbar custom-scrollbar bg-gray-50/30 dark:bg-slate-900/30">
          {chatSessions.length === 0 ? (
            <div className="text-center py-12 px-4">
              <BiMessage className="h-12 w-12 text-gray-400 dark:text-slate-500 mx-auto mb-3 opacity-50" />
              <p className="text-gray-600 dark:text-slate-400 text-sm font-medium">
                {t('chat.no_messages')}
              </p>
              <p className="text-gray-500 dark:text-slate-500 text-xs mt-1">
                Start a new conversation to begin
              </p>
            </div>
          ) : (
            chatSessions.map((session) => (
              <div
                key={session.id}
                className={`group relative p-4 rounded-2xl cursor-pointer transition-all duration-200 border-2 hover:shadow-md dark:hover:shadow-lg ${
                  session.id === currentSessionId
                    ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700/50 shadow-md shadow-blue-100/50 dark:shadow-blue-900/20'
                    : 'bg-white dark:bg-slate-800/80 border-gray-200/50 dark:border-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700/80 hover:border-gray-300/70 dark:hover:border-slate-600/70 hover-lift'
                }`}
                onClick={() => onSwitchToSession(session.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0 pr-3">
                    {/* Session Title */}
                    <div className="flex items-center space-x-2 mb-2">
                      <div className={`h-2 w-2 rounded-full flex-shrink-0 ${
                        session.id === currentSessionId 
                          ? 'bg-blue-500 dark:bg-blue-400' 
                          : 'bg-gray-400 dark:bg-slate-500'
                      }`}></div>
                      <h3 className={`font-black text-sm truncate transition-colors duration-300 ${
                        session.id === currentSessionId
                          ? 'text-indigo-800 dark:text-indigo-200'
                          : 'text-slate-900 dark:text-slate-100'
                      }`}>
                        {session.title || 'New Conversation'}
                      </h3>
                    </div>
                    
                    {/* Last Message Preview */}
                    <p className={`text-xs mb-3 line-clamp-2 leading-relaxed transition-colors duration-300 font-medium ${
                      session.id === currentSessionId
                        ? 'text-blue-800 dark:text-blue-100'
                        : 'text-gray-700 dark:text-gray-200'
                    }`}>
                      {session.lastMessage}
                    </p>
                    
                    {/* Timestamp */}
                    <div className={`flex items-center space-x-1 text-xs transition-colors duration-300 ${
                      session.id === currentSessionId
                        ? 'text-blue-600 dark:text-blue-300'
                        : 'text-gray-500 dark:text-gray-400'
                    }`}>
                      <BiTime className="h-3 w-3" />
                      <span>{formatTimeAgo(session.timestamp)}</span>
                    </div>
                  </div>
                  
                  {/* Delete Button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteSession(session.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-2 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 text-red-500 dark:text-red-400 transition-all duration-200 flex-shrink-0 hover:scale-110"
                  >
                    <BiTrash className="h-4 w-4" />
                  </button>
                </div>
                
                {/* Active Session Indicator */}
                {session.id === currentSessionId && (
                  <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1 h-8 bg-blue-500 dark:bg-blue-400 rounded-r-full shadow-lg"></div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Collapsed sidebar content */}
      {!isSidebarOpen && (
        <div className="flex-1 flex flex-col items-center justify-start p-2 space-y-3 mt-4 bg-gray-50/30 dark:bg-slate-900/30">
          {/* New Chat Button - Collapsed */}
          <button
            onClick={onCreateNewSession}
            className="w-12 h-12 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg flex items-center justify-center transition-all duration-200 hover-lift group"
          >
            <BiPlus className="h-5 w-5 text-white group-hover:rotate-90 transition-transform duration-200" />
          </button>
          
          {/* Session Icons */}
          {chatSessions.slice(0, 5).map((session, index) => (
            <button
              key={session.id}
              onClick={() => onSwitchToSession(session.id)}
              className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200 hover-lift relative group border-2 ${
                session.id === currentSessionId
                  ? 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-700/50 shadow-md shadow-blue-100/50 dark:shadow-blue-900/20'
                  : 'bg-white dark:bg-slate-800/80 border-gray-200/50 dark:border-slate-700/50 hover:bg-gray-50 dark:hover:bg-slate-700/80 shadow-md hover:shadow-lg hover:border-gray-300/70 dark:hover:border-slate-600/70'
              }`}
              title={session.title}
            >
              <BiChat className={`h-5 w-5 ${
                session.id === currentSessionId
                  ? 'text-blue-600 dark:text-blue-300'
                  : 'text-gray-600 dark:text-gray-300'
              }`} />
              
              {/* Session Number Badge */}
              <div className="absolute -top-1 -right-1 h-5 w-5 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-full flex items-center justify-center text-xs font-bold text-white shadow-lg">
                {index + 1}
              </div>
            </button>
          ))}
          
          {/* More Sessions Indicator */}
          {chatSessions.length > 5 && (
            <div className="w-12 h-8 bg-gray-200 dark:bg-slate-700 rounded-lg flex items-center justify-center border border-gray-300/50 dark:border-slate-600/50">
              <span className="text-xs font-semibold text-gray-600 dark:text-gray-300">
                +{chatSessions.length - 5}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatSidebar;
