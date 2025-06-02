import React from 'react';
import { BiBot } from 'react-icons/bi';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-start space-x-4 opacity-0 animate-fade-in">
      <div className="h-10 w-10 bg-gradient-to-br from-lavender via-purple-200 to-sky-blue rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg animate-pulse">
        <BiBot className="h-5 w-5 text-charcoal" />
      </div>
      <div className="bg-white/95 backdrop-blur-sm px-5 py-4 rounded-2xl shadow-lg border border-white/50 relative">
        <div className="flex space-x-2 items-center">
          <span className="text-sm text-gray-600 mr-3 font-medium">AI is thinking</span>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gradient-to-r from-lavender to-sky-blue rounded-full animate-bounce shadow-sm"></div>
            <div className="w-2 h-2 bg-gradient-to-r from-lavender to-sky-blue rounded-full animate-bounce shadow-sm" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-gradient-to-r from-lavender to-sky-blue rounded-full animate-bounce shadow-sm" style={{ animationDelay: '0.4s' }}></div>
          </div>
        </div>
        <div className="absolute top-4 w-3 h-3 bg-white/95 border-l border-b border-white/50 transform rotate-45 -left-1.5"></div>
      </div>
    </div>
  );
};

export default TypingIndicator;
