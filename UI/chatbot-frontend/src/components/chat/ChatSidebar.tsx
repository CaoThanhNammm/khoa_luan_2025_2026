import React from 'react';
import { BiChat, BiPlus, BiTrash } from 'react-icons/bi';
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
  return (
    <div className={`${isSidebarOpen ? 'w-80' : 'w-16'} bg-white/90 backdrop-blur-xl border-r border-white/20 shadow-xl shadow-gray-100/50 transition-all duration-300 flex flex-col relative z-10`}>
      {/* Sidebar Header */}
      <div className="p-4 border-b border-white/20">
        <div className="flex items-center justify-between">
          {isSidebarOpen && (
            <h2 className="font-heading text-lg font-bold text-charcoal">Chat History</h2>
          )}
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 rounded-xl bg-lavender/20 hover:bg-lavender/30 transition-all duration-200 group"
          >
            <BiChat className="h-5 w-5 text-charcoal group-hover:scale-110 transition-transform" />
          </button>
        </div>
        {isSidebarOpen && (
          <button
            onClick={onCreateNewSession}
            className="w-full mt-4 flex items-center justify-center space-x-2 p-3 bg-gradient-to-r from-lavender to-sky-blue text-charcoal rounded-2xl hover:shadow-lg transition-all duration-200 font-medium"
          >
            <BiPlus className="h-5 w-5" />
            <span>New Chat</span>
          </button>
        )}
      </div>

      {/* Chat Sessions List */}
      {isSidebarOpen && (
        <div className="flex-1 overflow-y-auto p-4 space-y-3 hide-scrollbar">
          {chatSessions.map((session) => (
            <div
              key={session.id}
              className={`group relative p-4 rounded-2xl cursor-pointer transition-all duration-200 border-2 ${
                session.id === currentSessionId
                  ? 'bg-gradient-to-r from-lavender/30 to-sky-blue/30 border-lavender/50 shadow-lg'
                  : 'bg-white/60 border-transparent hover:bg-white/80 hover:shadow-md'
              }`}
              onClick={() => onSwitchToSession(session.id)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-charcoal text-sm truncate mb-1">
                    {session.title}
                  </h3>
                  <p className="text-xs text-gray-600 truncate mb-2">
                    {session.lastMessage}
                  </p>
                  <span className="text-xs text-gray-500">
                    {session.timestamp.toLocaleDateString()}
                  </span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(session.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 rounded-lg hover:bg-red-100 text-red-500 transition-all duration-200"
                >
                  <BiTrash className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Collapsed sidebar content */}
      {!isSidebarOpen && (
        <div className="flex-1 flex flex-col items-center justify-start p-2 space-y-3 mt-4">
          {chatSessions.slice(0, 3).map((session) => (
            <button
              key={session.id}
              onClick={() => onSwitchToSession(session.id)}
              className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200 ${
                session.id === currentSessionId
                  ? 'bg-gradient-to-r from-lavender to-sky-blue shadow-lg'
                  : 'bg-white/60 hover:bg-white/80'
              }`}
            >
              <BiChat className="h-5 w-5 text-charcoal" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ChatSidebar;
