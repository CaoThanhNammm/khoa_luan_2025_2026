import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useChat } from '../context/ChatContext';
import { useSettings } from '../context/SettingsContext';
import { useNavigate } from 'react-router-dom';
import { ChatSidebar, ChatContainer } from '../components/chat';
import { FileUploadService } from '../services/FileUploadService';
import type { ChatSession, SidebarChatSession } from '../types/chat';
import PageTransition from '../components/PageTransition';

const ChatPage: React.FC = () => {
  const { user } = useAuth();
  const { showNotification } = useSettings();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  
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
  };  const handleCreateNewSession = async () => {
    // Clear the current conversation to start fresh
    // The actual new conversation will be created when sending the first message
    chatContext.clearError(); // Clear any existing errors
    chatContext.clearCurrentConversation(); // Clear the current conversation
  };

  const handleSwitchToSession = async (conversationId: string) => {
    await chatContext.switchToConversation(Number(conversationId));
  };

  const handleDeleteSession = async (conversationId: string) => {
    await chatContext.deleteConversation(Number(conversationId));
  };

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    
    try {
      // Get current conversation ID if available
      const conversationId = chatContext.currentConversation?.id;
      console.log('Uploading file with conversation ID:', conversationId);
      
      const response = await FileUploadService.uploadFile(file, conversationId);
      
      if (response.filename) {
        showNotification(
          `File "${response.filename}" uploaded successfully! Document ID: ${response.document_id}${conversationId ? ` linked to conversation ${conversationId}` : ''}`,
          'success'
        );
        
        // If no current conversation, create a new one with the uploaded file info
        if (!chatContext.currentConversation) {
          await chatContext.createNewConversation(`I've uploaded a PDF file: ${response.filename}. Please help me analyze this document.`);
        } else {
          // If there's a current conversation, send a message about the uploaded file
          await chatContext.sendMessage(
            chatContext.currentConversation.id, 
            `I've uploaded a PDF file: ${response.filename}. Please help me analyze this document.`
          );
        }
        
        // Reload conversations to get updated document information
        await chatContext.loadConversations();
      } else {
        throw new Error(response.message || 'Upload failed');
      }
    } catch (error) {
      console.error('File upload failed:', error);
      showNotification(
        `File upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        'error'
      );
    } finally {
      setIsUploading(false);
    }
  };

  if (!user) {
    return null; // Will redirect in useEffect
  }// Convert conversations to SidebarChatSession format for sidebar
  const chatSessions: SidebarChatSession[] = chatContext.conversations.map((conv: ChatSession) => ({
    id: conv.id.toString(),
    title: conv.title,
    lastMessage: conv.messages.length > 0 ? conv.messages[conv.messages.length - 1].content : 'No messages yet',
    timestamp: new Date(conv.createdAt),
    hasDocument: conv.hasDocument || false,
    documentFilename: conv.documentInfo?.filename
  }));

  const currentSessionId = chatContext.currentConversation?.id.toString() || '';
  return (
    <PageTransition>
      <div className="chat-layout flex bg-gradient-to-br from-slate-50 via-purple-50/30 to-blue-50/40 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 relative overflow-hidden transition-colors duration-500">
        {/* Enhanced decorative background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-lavender/10 to-sky-blue/10 dark:from-indigo-500/10 dark:to-purple-500/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-sky-blue/10 to-lavender/10 dark:from-purple-500/10 dark:to-indigo-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-purple-200/5 to-blue-200/5 dark:from-indigo-400/5 dark:to-purple-400/5 rounded-full blur-3xl animate-aurora"></div>
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
        isThinking={chatContext.isThinking}
        pendingMessage={chatContext.pendingMessage}
        onSendMessage={handleSendMessage}
        onFileUpload={handleFileUpload}
        isUploading={isUploading}
        conversationId={chatContext.currentConversation?.id}
        hasDocument={chatContext.currentConversation?.hasDocument || false}
        documentInfo={chatContext.currentConversation?.documentInfo}
      />

      {/* Enhanced Error Display */}
      {chatContext.error && (
        <div className="fixed bottom-4 right-4 bg-gradient-to-r from-red-500 to-rose-500 dark:from-red-600 dark:to-rose-600 text-white px-6 py-3 rounded-xl shadow-lg dark:shadow-red-500/25 backdrop-blur-xl border border-red-400/20 animate-fade-in">
          {chatContext.error}
          <button 
            onClick={chatContext.clearError}
            className="ml-3 text-white/80 hover:text-white transition-colors rounded-lg p-1 hover:bg-white/10"
          >
            ×
          </button>
        </div>        )}
      </div>
    </PageTransition>
  );
};

export default ChatPage;
