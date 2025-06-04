import React, { useRef, useEffect, useMemo, useState } from 'react';
import type { Message } from '../../types/chat';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';
import ThinkingIndicator from './ThinkingIndicator';

interface ChatMessagesProps {
  messages: Message[];
  isTyping: boolean;
  isThinking?: boolean; // Thêm prop để phân biệt giữa typing và thinking
  pendingMessage?: Message | null; // Thêm prop cho pending message
  conversationId?: string; // Thêm để detect conversation change
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, isTyping, isThinking = false, pendingMessage = null, conversationId }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [previousMessageCount, setPreviousMessageCount] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Tạo danh sách tin nhắn bao gồm cả pending message
  const allMessages = useMemo(() => {
    const messageList = [...messages];
    if (pendingMessage) {
      messageList.push(pendingMessage);
    }
    return messageList;
  }, [messages, pendingMessage]);  // Track message count changes to determine which messages should animate
  useEffect(() => {
    // Reset animation state when conversation changes completely
    // This happens when messages array changes dramatically (different conversation)
    if (messages.length === 0 || (previousMessageCount > 0 && previousMessageCount > messages.length)) {
      setPreviousMessageCount(0);
      setIsTransitioning(true);
      // Reset transition after animation
      const timeout = setTimeout(() => setIsTransitioning(false), 300);
      return () => clearTimeout(timeout);
    }
  }, [messages.length, previousMessageCount]);

  // Handle conversation changes
  useEffect(() => {
    if (conversationId) {
      setIsTransitioning(true);
      const timeout = setTimeout(() => setIsTransitioning(false), 300);
      return () => clearTimeout(timeout);
    }
  }, [conversationId]);

  // Memoize message components với animation logic
  const messageComponents = useMemo(() => {
    return allMessages.map((message, index) => {
      // Only animate new messages (those beyond the previous count)
      // When switching conversations, previousMessageCount should be reset to 0
      const shouldAnimate = index >= previousMessageCount && previousMessageCount > 0;
      return (
        <MessageItem 
          key={message.id} 
          message={message} 
          index={index} 
          shouldAnimate={shouldAnimate}
        />
      );
    });
  }, [allMessages, previousMessageCount]);

  // Update previous count only when new messages are actually added
  useEffect(() => {
    if (allMessages.length > previousMessageCount) {
      setPreviousMessageCount(allMessages.length);
    }
  }, [allMessages.length, previousMessageCount]);

  useEffect(() => {
    scrollToBottom();
  }, [allMessages, isThinking]); // Thêm allMessages và isThinking vào dependency

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  return (
    <div className={`flex-1 overflow-y-auto px-6 py-6 space-y-6 relative hide-scrollbar transition-opacity duration-300 ${
      isTransitioning ? 'opacity-50' : 'opacity-100'
    }`}>
      {messageComponents}
      
      {/* Show thinking indicator when waiting for API response */}
      {isThinking && <ThinkingIndicator />}
      
      {/* Show typing indicator when processing (legacy) */}
      {isTyping && !isThinking && <TypingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;
