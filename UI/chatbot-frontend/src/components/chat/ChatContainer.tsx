import React from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import MessageInput from './MessageInput';
import type { Message, DocumentInfo } from '../../types/chat';

interface ChatContainerProps {
  messages: Message[];
  isTyping: boolean;
  isThinking?: boolean;
  pendingMessage?: Message | null;
  onSendMessage: (message: string) => void;
  onFileUpload?: (file: File) => Promise<void>;
  isUploading?: boolean;
  conversationId?: number;
  hasDocument?: boolean;
  documentInfo?: DocumentInfo;
}

const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isTyping,
  isThinking = false,
  pendingMessage = null,
  onSendMessage,
  onFileUpload,
  isUploading = false,
  conversationId,
  hasDocument = false,
  documentInfo
}) => {
  return (
    <div className="flex-1 flex flex-col h-full">
      <ChatHeader 
        isTyping={isTyping || isThinking} 
        hasDocument={hasDocument}
        documentInfo={documentInfo}
      />
      <div className="flex-1 flex flex-col min-h-0">
        <ChatMessages messages={messages} isTyping={isTyping} isThinking={isThinking} pendingMessage={pendingMessage} />
        <MessageInput 
          onSendMessage={onSendMessage} 
          onFileUpload={onFileUpload}
          isTyping={isTyping || isThinking}
          isUploading={isUploading}
          conversationId={conversationId}
        />
      </div>
    </div>
  );
};

export default ChatContainer;
