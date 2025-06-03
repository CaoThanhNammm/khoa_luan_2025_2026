import React from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import MessageInput from './MessageInput';
import type { Message } from '../../types/chat';

interface ChatContainerProps {
  messages: Message[];
  isTyping: boolean;
  isThinking?: boolean;
  pendingMessage?: Message | null;
  onSendMessage: (message: string) => void;
}

const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isTyping,
  isThinking = false,
  pendingMessage = null,
  onSendMessage
}) => {  return (
    <div className="flex-1 flex flex-col h-full">
      <ChatHeader isTyping={isTyping || isThinking} />
      <div className="flex-1 flex flex-col min-h-0">
        <ChatMessages messages={messages} isTyping={isTyping} isThinking={isThinking} pendingMessage={pendingMessage} />
        <MessageInput onSendMessage={onSendMessage} isTyping={isTyping || isThinking} />
      </div>
    </div>
  );
};

export default ChatContainer;
