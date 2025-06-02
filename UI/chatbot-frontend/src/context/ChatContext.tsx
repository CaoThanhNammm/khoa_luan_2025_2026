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
  clearCurrentConversation: () => void;
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

  // Save current conversation ID to localStorage
  const saveCurrentConversationId = useCallback((conversationId: number | null) => {
    if (user) {
      const key = `chatbot_current_conversation_${user.id}`;
      if (conversationId) {
        localStorage.setItem(key, conversationId.toString());
      } else {
        localStorage.removeItem(key);
      }
    }
  }, [user]);

  // Get saved conversation ID from localStorage
  const getSavedConversationId = useCallback((): number | null => {
    if (user) {
      const key = `chatbot_current_conversation_${user.id}`;
      const saved = localStorage.getItem(key);
      return saved ? parseInt(saved, 10) : null;
    }
    return null;
  }, [user]);
  // Load all conversations for the current user
  const loadConversations = useCallback(async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const conversations = await ChatService.getConversations();
      setConversations(conversations);
      
      // Try to restore the previously selected conversation
      const savedConversationId = getSavedConversationId();
      if (savedConversationId) {
        // Find the conversation in the loaded conversations
        const savedConversation = conversations.find(conv => conv.id === savedConversationId);
        if (savedConversation) {
          // Load the full conversation details
          try {
            const fullConversation = await ChatService.getConversation(savedConversationId);
            setCurrentConversation(fullConversation);
          } catch (err) {
            // If loading the specific conversation fails, just clear the saved ID
            console.warn('Failed to load saved conversation:', err);
            saveCurrentConversationId(null);
          }
        } else {
          // Conversation no longer exists, clear the saved ID
          saveCurrentConversationId(null);
        }
      }
      
      setError(null);
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      console.error('Error loading conversations:', err);
    } finally {
      setLoading(false);
    }
  }, [user, getSavedConversationId, saveCurrentConversationId]);
  // Create a new conversation
  const createNewConversation = async (message: string): Promise<number | null> => {
    if (!user) return null;
    
    setLoading(true);
    try {
      const newConversation = await ChatService.startNewConversation(message);
      
      setConversations(prev => [newConversation, ...prev]);
      setCurrentConversation(newConversation);
      saveCurrentConversationId(newConversation.id); // Save the new conversation ID
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
      saveCurrentConversationId(id); // Save the current conversation ID
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
        saveCurrentConversationId(null); // Clear saved conversation ID
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
  const clearCurrentConversation = () => {
    setCurrentConversation(null);
    saveCurrentConversationId(null); // Clear saved conversation ID
  };
  // Load conversations when user changes
  useEffect(() => {
    if (user) {
      loadConversations();
    } else {
      setConversations([]);
      setCurrentConversation(null);
      // Clear any saved conversation data when user logs out
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith('chatbot_current_conversation_')) {
          localStorage.removeItem(key);
        }
      });
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
    clearCurrentConversation,
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
