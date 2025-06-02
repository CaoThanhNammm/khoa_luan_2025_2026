import React from 'react';
import { BiBot, BiUser } from 'react-icons/bi';
import type { Message } from '../../types/chat';

interface MessageItemProps {
  message: Message;
  index: number;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, index }) => {
  const formatTime = (timestamp: string): string => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const isUser = message.type === 'USER';

  return (
    <div
      className={`flex items-start space-x-4 opacity-0 animate-fade-in ${
        isUser ? 'flex-row-reverse space-x-reverse' : ''
      }`}
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      <div className={`h-10 w-10 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg transition-all duration-300 hover:scale-110 ${
        isUser 
          ? 'bg-gradient-to-br from-charcoal via-gray-800 to-slate-900 shadow-charcoal/20'
          : 'bg-gradient-to-br from-lavender via-purple-200 to-sky-blue shadow-lavender/20'
      }`}>
        {isUser ? (
          <BiUser className="h-5 w-5 text-white" />
        ) : (
          <BiBot className="h-5 w-5 text-charcoal" />
        )}
      </div>
      <div className={`flex flex-col max-w-xs lg:max-w-md ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`relative px-5 py-4 rounded-2xl shadow-lg transition-all duration-300 hover:shadow-xl transform hover:-translate-y-1 ${
          isUser 
            ? 'bg-gradient-to-br from-charcoal via-gray-800 to-slate-900 text-white shadow-charcoal/20'
            : 'bg-white/95 backdrop-blur-sm text-charcoal border border-white/50 shadow-gray-100/80'
        }`}>
          <p className="text-sm leading-relaxed font-medium tracking-wide">{message.content}</p>
          {/* Enhanced message tail */}
          <div className={`absolute top-4 w-3 h-3 transform rotate-45 ${
            isUser
              ? 'bg-gradient-to-br from-charcoal to-gray-800 -right-1.5'
              : 'bg-white/95 border-l border-b border-white/50 -left-1.5'
          }`}></div>
        </div>
        <span className="text-xs text-gray-500 mt-2 px-2 font-semibold tracking-wider opacity-70">
          {formatTime(message.timestamp)}
        </span>
      </div>
    </div>
  );
};

export default MessageItem;
