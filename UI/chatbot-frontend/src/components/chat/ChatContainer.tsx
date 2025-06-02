import React from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import MessageInput from './MessageInput';
import type { Message } from '../../types/chat';

interface ChatContainerProps {
  messages: Message[];
  isTyping: boolean;
  onSendMessage: (message: string) => void;
}

const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isTyping,
  onSendMessage
}) => {
  return (
    <div className="flex-1 flex flex-col h-full">
      <ChatHeader isTyping={isTyping} />
      <div className="flex-1 flex flex-col min-h-0">
        <ChatMessages messages={messages} isTyping={isTyping} />
        <MessageInput onSendMessage={onSendMessage} isTyping={isTyping} />
      </div>
    </div>
  );
};

export default ChatContainer;
