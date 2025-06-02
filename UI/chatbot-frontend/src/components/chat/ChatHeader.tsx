import React from 'react';
import { BiBot } from 'react-icons/bi';

interface ChatHeaderProps {
  isTyping: boolean;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ isTyping }) => {
  return (
    <div className="bg-white/90 backdrop-blur-xl border-b border-white/20 px-6 py-4 shadow-xl shadow-gray-100/50">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="relative group">
            <div className="h-12 w-12 bg-gradient-to-br from-lavender via-purple-200 to-sky-blue rounded-2xl flex items-center justify-center shadow-lg shadow-lavender/20 group-hover:shadow-xl group-hover:shadow-lavender/30 transition-all duration-300 group-hover:scale-105">
              <BiBot className="h-6 w-6 text-charcoal" />
            </div>
            <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-emerald-500 rounded-full border-2 border-white shadow-lg animate-pulse"></div>
          </div>
          <div>
            <h1 className="font-heading text-2xl font-bold text-charcoal tracking-wide">NLU ChatBot</h1>
            <p className="text-sm text-gray-600 flex items-center space-x-2 font-medium">
              <span className="h-2 w-2 bg-emerald-500 rounded-full animate-pulse shadow-sm"></span>
              <span>{isTyping ? 'Crafting response...' : 'Ready to assist you'}</span>
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-500 font-semibold uppercase tracking-wider">
            {new Date().toLocaleDateString('en-US', { weekday: 'short' })}
          </div>
          <div className="text-sm text-gray-700 font-bold">
            {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;
