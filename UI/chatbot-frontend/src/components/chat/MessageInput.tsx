import React, { useState } from 'react';
import { BiPaperPlane } from 'react-icons/bi';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isTyping: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, isTyping }) => {
  const [inputMessage, setInputMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isTyping) return;
    
    onSendMessage(inputMessage);
    setInputMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as React.FormEvent);
    }
  };

  return (
    <div className="border-t border-white/20 bg-white/90 backdrop-blur-xl px-6 py-4 shadow-xl shadow-gray-100/50">
      <form onSubmit={handleSubmit} className="flex space-x-4 items-end">
        <div className="flex-1 relative group">            
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts with me..."
            className="w-full px-5 py-4 pr-14 border-2 border-gray-200/80 rounded-2xl focus:outline-none focus:ring-4 focus:ring-lavender/30 focus:border-lavender transition-all duration-300 bg-white/90 backdrop-blur-sm shadow-lg shadow-gray-100/50 font-medium placeholder-gray-500 text-charcoal group-hover:shadow-xl"
            disabled={isTyping}
            maxLength={1000}
          />
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
            <div className="text-xs font-semibold bg-gray-100 px-2 py-1 rounded-lg">
              {inputMessage.length}/1000
            </div>
          </div>
        </div>
        <button
          type="submit"
          disabled={!inputMessage.trim() || isTyping}
          className="h-14 w-14 bg-gradient-to-br from-charcoal via-gray-800 to-slate-900 text-white rounded-2xl disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center shadow-lg shadow-charcoal/20 hover:shadow-xl hover:shadow-charcoal/30 transition-all duration-300 transform hover:scale-110 disabled:hover:scale-100 active:scale-95"
        >
          <BiPaperPlane className="h-6 w-6 transform transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
        </button>
      </form>
      <div className="text-xs text-gray-500 mt-3 text-center font-medium flex items-center justify-center space-x-4">
        <span className="flex items-center space-x-1">
          <kbd className="px-2 py-1 bg-gray-100 rounded text-xs font-semibold">Enter</kbd>
          <span>to send</span>
        </span>
        <span className="text-gray-300">•</span>
        <span className="flex items-center space-x-1">
          <kbd className="px-2 py-1 bg-gray-100 rounded text-xs font-semibold">Shift</kbd>
          <span>+</span>
          <kbd className="px-2 py-1 bg-gray-100 rounded text-xs font-semibold">Enter</kbd>
          <span>for new line</span>
        </span>
      </div>
    </div>
  );
};

export default MessageInput;
