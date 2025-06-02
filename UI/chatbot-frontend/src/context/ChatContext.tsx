import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import ChatService from '../services/ChatService';
import type { ChatSession } from '../types/chat';
import { useAuth } from './AuthContext';
import { getErrorMessage } from '../utils/errorHandler';

interface ChatContextType {
  conversations: ChatSession[];
  currentConversation: ChatSession | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  loadConversations: () => Promise<void>;
  createNewConversation: (message: string) => Promise<number | null>;
  switchToConversation: (id: number) => Promise<void>;
  deleteConversation: (id: number) => Promise<void>;
  sendMessage: (conversationId: number, message: string) => Promise<void>;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<ChatSession[]>([]);
  const [currentConversation, setCurrentConversation] = useState<ChatSession | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load all conversations for the current user
  const loadConversations = useCallback(async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const conversations = await ChatService.getConversations();
      setConversations(conversations);
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error loading conversations:', err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  // Create a new conversation
  const createNewConversation = async (message: string): Promise<number | null> => {
    if (!user) return null;
    
    setLoading(true);
    try {
      const newConversation = await ChatService.startNewConversation(message);
      
      setConversations(prev => [newConversation, ...prev]);
      setCurrentConversation(newConversation);
      setError(null);
      
      return newConversation.id;
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error creating conversation:', err);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Switch to a specific conversation
  const switchToConversation = async (id: number) => {
    setLoading(true);
    try {
      const conversation = await ChatService.getConversation(id);
      setCurrentConversation(conversation);
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error loading conversation:', err);
    } finally {
      setLoading(false);
    }
  };

  // Delete a conversation
  const deleteConversation = async (id: number) => {
    try {
      await ChatService.deleteConversation(id);
      
      setConversations(prev => prev.filter(conv => conv.id !== id));
      
      if (currentConversation?.id === id) {
        setCurrentConversation(null);
      }
      
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error deleting conversation:', err);
    }
  };

  // Send a message in a conversation
  const sendMessage = async (conversationId: number, message: string) => {
    try {
      await ChatService.sendMessage(conversationId, message);
      
      // Reload the conversation to get the latest messages
      if (currentConversation?.id === conversationId) {
        const updatedConversation = await ChatService.getConversation(conversationId);
        setCurrentConversation(updatedConversation);
      }
      
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error sending message:', err);
    }
  };

  const clearError = () => {
    setError(null);
  };

  // Load conversations when user changes
  useEffect(() => {
    if (user) {
      loadConversations();
    } else {
      setConversations([]);
      setCurrentConversation(null);
    }
  }, [user, loadConversations]);

  const value: ChatContextType = {
    conversations,
    currentConversation,
    loading,
    error,
    loadConversations,
    createNewConversation,
    switchToConversation,
    deleteConversation,
    sendMessage,
    clearError
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
