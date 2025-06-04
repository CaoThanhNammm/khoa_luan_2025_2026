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
  isLoadingConversation?: boolean;
  conversationId?: string;
}

const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isTyping,
  isThinking = false,
  pendingMessage = null,
  onSendMessage,
  isLoadingConversation = false,
  conversationId
}) => {return (
    <div className="flex-1 flex flex-col h-full relative">
      {/* Loading overlay when switching conversations */}
      {isLoadingConversation && (
        <div className="absolute inset-0 z-50 bg-white/70 dark:bg-slate-900/70 backdrop-blur-sm flex items-center justify-center">
          <div className="flex flex-col items-center space-y-3">
            <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm text-gray-600 dark:text-gray-300 font-medium">Loading conversation...</p>
          </div>
        </div>
      )}
        <ChatHeader isTyping={isTyping || isThinking} />
      <div className="flex-1 flex flex-col min-h-0">
        <ChatMessages 
          messages={messages} 
          isTyping={isTyping} 
          isThinking={isThinking} 
          pendingMessage={pendingMessage} 
          conversationId={conversationId}
        />
        <MessageInput onSendMessage={onSendMessage} isTyping={isTyping || isThinking} />
      </div>
    </div>
  );
};

export default ChatContainer;
