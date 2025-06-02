import React, { useRef, useEffect } from 'react';
import type { Message } from '../../types/chat';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';

interface ChatMessagesProps {
  messages: Message[];
  isTyping: boolean;
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, isTyping }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 relative hide-scrollbar">
      {messages.map((message, index) => (
        <MessageItem key={message.id} message={message} index={index} />
      ))}
      
      {/* Enhanced Typing Indicator */}
      {isTyping && <TypingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
