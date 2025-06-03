import React, { useState, useEffect } from 'react';
import { BiBot } from 'react-icons/bi';

interface ThinkingIndicatorProps {
  className?: string;
}

const ThinkingIndicator: React.FC<ThinkingIndicatorProps> = ({ className = '' }) => {
  const [dots, setDots] = useState('');
  const [thinkingText, setThinkingText] = useState('Đang suy nghĩ');

  const thinkingMessages = [
    'Đang suy nghĩ',
    'Đang phân tích',
    'Đang xử lý',
    'Đang tìm kiếm thông tin',
    'Đang chuẩn bị câu trả lời'
  ];

  useEffect(() => {
    // Animation for dots
    const dotsInterval = setInterval(() => {
      setDots(prev => {
        if (prev.length >= 3) return '';
        return prev + '.';
      });
    }, 500);

    // Randomly change thinking text
    const textInterval = setInterval(() => {
      setThinkingText(thinkingMessages[Math.floor(Math.random() * thinkingMessages.length)]);
    }, 2000);

    return () => {
      clearInterval(dotsInterval);
      clearInterval(textInterval);
    };
  }, []);

  return (
    <div className={`flex items-start space-x-4 animate-fade-in ${className}`}>
      {/* Bot Avatar */}
      <div className="h-10 w-10 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg bg-gradient-to-br from-lavender via-purple-200 to-sky-blue shadow-lavender/20 dark:from-slate-600 dark:via-slate-700 dark:to-slate-800">
        <BiBot className="h-5 w-5 text-charcoal dark:text-white" />
      </div>
      
      {/* Thinking Message */}
      <div className="flex flex-col max-w-xs lg:max-w-2xl xl:max-w-3xl items-start">
        <div className="relative px-5 py-4 rounded-2xl shadow-lg bg-white/95 backdrop-blur-sm text-charcoal border border-white/50 shadow-gray-100/80 dark:bg-slate-800/90 dark:text-gray-100 dark:border-slate-700/50">
          <div className="flex items-center space-x-3">
            {/* Animated brain icon or dots */}
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '300ms' }}></div>
            </div>
            
            {/* Thinking text */}
            <div className="text-sm font-medium">
              <span className="text-blue-600 dark:text-blue-400">
                {thinkingText}
                <span className="inline-block w-6 text-left">{dots}</span>
              </span>
            </div>
          </div>

          {/* Animated progress bar */}
          <div className="mt-3 w-full bg-gray-200 dark:bg-slate-700 rounded-full h-1 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-pulse-slow origin-left"></div>
          </div>

          {/* Message tail */}
          <div className="absolute top-4 w-3 h-3 transform rotate-45 bg-white/95 border-l border-b border-white/50 -left-1.5 dark:bg-slate-800/90 dark:border-slate-700/50"></div>
        </div>
        
        {/* Timestamp placeholder */}
        <span className="text-xs text-gray-500 dark:text-gray-400 mt-2 px-2 opacity-70">
          Đang xử lý...
        </span>
      </div>
    </div>
  );
};

export default ThinkingIndicator;
