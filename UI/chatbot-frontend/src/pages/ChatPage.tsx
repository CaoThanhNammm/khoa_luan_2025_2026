import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../context/ChatContext';
import { useNavigate } from 'react-router-dom';
import { ChatSidebar, ChatContainer } from '../components/chat';
import type { ChatSession, SidebarChatSession } from '../types/chat';

const ChatPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  const chatContext = useChat();

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
  }, [user, navigate]);

  // Get messages from current conversation directly (no conversion needed)
  const messages = chatContext.currentConversation?.messages || [];

  const handleSendMessage = async (inputMessage: string) => {
    if (!inputMessage.trim()) return;

    try {
      if (chatContext.currentConversation) {
        // Send message to existing conversation
        await chatContext.sendMessage(chatContext.currentConversation.id, inputMessage);
      } else {
        // Create new conversation
        await chatContext.createNewConversation(inputMessage);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleCreateNewSession = async () => {
    // Just clear the current conversation to start fresh
    // The actual new conversation will be created when sending the first message
  };

  const handleSwitchToSession = async (conversationId: string) => {
    await chatContext.switchToConversation(Number(conversationId));
  };

  const handleDeleteSession = async (conversationId: string) => {
    await chatContext.deleteConversation(Number(conversationId));
  };

  if (!user) {
    return null; // Will redirect in useEffect
  }// Convert conversations to SidebarChatSession format for sidebar
  const chatSessions: SidebarChatSession[] = chatContext.conversations.map((conv: ChatSession) => ({
    id: conv.id.toString(),
    title: conv.title,
    lastMessage: conv.messages.length > 0 ? conv.messages[conv.messages.length - 1].content : 'No messages yet',
    timestamp: new Date(conv.createdAt)
  }));

  const currentSessionId = chatContext.currentConversation?.id.toString() || '';

  return (
    <div className="chat-layout flex bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-lavender/10 to-sky-blue/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-blue/10 to-lavender/10 rounded-full blur-3xl"></div>
      </div>

      <ChatSidebar
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        chatSessions={chatSessions}
        currentSessionId={currentSessionId}
        onCreateNewSession={handleCreateNewSession}
        onSwitchToSession={handleSwitchToSession}
        onDeleteSession={handleDeleteSession}
      />      <ChatContainer
        messages={messages}
        isTyping={chatContext.loading}
        onSendMessage={handleSendMessage}
      />

      {/* Error Display */}
      {chatContext.error && (
        <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg">
          {chatContext.error}
          <button 
            onClick={chatContext.clearError}
            className="ml-2 text-white hover:text-gray-200"
          >
            ×
          </button>
        </div>
      )}
    </div>
  );
};

export default ChatPage;
