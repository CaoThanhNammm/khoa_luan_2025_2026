// API Adapters for converting between frontend and backend data formats

import type { Message, ChatSession } from "../types/chat";
import type { ConversationResponse, MessageResponse } from "../services/ChatService";

/**
 * Convert backend ConversationDto to frontend ChatSession
 */
export function adaptConversationToSession(conversation: ConversationResponse): ChatSession {
  return {
    id: conversation.id,
    title: conversation.title,
    createdAt: conversation.createdAt,
    messages: conversation.messages.map(adaptMessageToFrontend),
    hasDocument: conversation.hasDocument || false,
    documentInfo: conversation.documentInfo ? {
      documentId: conversation.documentInfo.documentId,
      filename: conversation.documentInfo.filename,
      fileSize: conversation.documentInfo.fileSize,
      sentencesCount: conversation.documentInfo.sentencesCount,
      uploadDate: conversation.documentInfo.uploadDate,
      status: conversation.documentInfo.status
    } : undefined
  };
}

/**
 * Convert backend MessageDto to frontend Message
 */
export function adaptMessageToFrontend(message: MessageResponse): Message {
  return {
    id: message.id,
    content: message.content,
    type: message.type,
    timestamp: message.timestamp,
    conversationId: message.conversationId
  };
}

/**
 * Convert frontend message type to display format
 */
export function getMessageSender(type: 'USER' | 'BOT'): 'user' | 'bot' {
  return type === 'USER' ? 'user' : 'bot';
}

/**
 * Format timestamp for display
 */
export function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleString();
}

/**
 * Get conversation title or generate one from first message
 */
export function getConversationTitle(conversation: ChatSession): string {
  if (conversation.title && conversation.title.trim() !== '') {
    return conversation.title;
  }
  
  const firstMessage = conversation.messages.find(m => m.type === 'USER');
  if (firstMessage) {
    // Take first 50 characters as title
    return firstMessage.content.length > 50 
      ? firstMessage.content.substring(0, 50) + '...'
      : firstMessage.content;
  }
  
  return 'New Conversation';
}
