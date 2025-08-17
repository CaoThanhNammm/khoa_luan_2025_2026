import React, { useRef, useEffect, useMemo } from 'react';
import type { Message } from '../../types/chat';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';
import ThinkingIndicator from './ThinkingIndicator';

interface ChatMessagesProps {
  messages: Message[];
  isTyping: boolean;
  isThinking?: boolean; // Thêm prop để phân biệt giữa typing và thinking
  pendingMessage?: Message | null; // Thêm prop cho pending message
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, isTyping, isThinking = false, pendingMessage = null }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Tạo danh sách tin nhắn bao gồm cả pending message
  const allMessages = useMemo(() => {
    const messageList = [...messages];
    if (pendingMessage) {
      messageList.push(pendingMessage);
    }
    return messageList;
  }, [messages, pendingMessage]);

  // Memoize message components để tránh re-render không cần thiết
  const messageComponents = useMemo(() => {
    return allMessages.map((message, index) => (
      <MessageItem key={message.id} message={message} index={index} />
    ));
  }, [allMessages]);

  useEffect(() => {
    scrollToBottom();
  }, [allMessages, isThinking]); // Thêm allMessages và isThinking vào dependency

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto px-6 py-6 custom-scrollbar chat-messages-scroll">
        <div className="space-y-6">
          {messageComponents}
          
          {/* Show thinking indicator when waiting for API response */}
          {isThinking && <ThinkingIndicator />}
          
          {/* Show typing indicator when processing (legacy) */}
          {isTyping && !isThinking && <TypingIndicator />}
        </div>
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatMessages;
