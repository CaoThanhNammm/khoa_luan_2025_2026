export interface Message {
  id: number;
  content: string;
  type: 'USER' | 'BOT';
  timestamp: string;
  conversationId: string;
  isStreaming?: boolean; // Để xác định tin nhắn đang được gõ
  isLatest?: boolean; // Để xác định tin nhắn mới nhất của bot
}

export interface ChatSession {
  id: string;
  title: string;
  createdAt: string;
  messages: Message[];
  hasDocument?: boolean; // Indicates if this conversation has uploaded documents
  documentInfo?: DocumentInfo; // Information about the uploaded document
}

export interface DocumentInfo {
  documentId: string;
  filename: string;
  fileSize: number;
  sentencesCount: number;
  uploadDate: string;
  status: string;
}

// Extended interface for sidebar display
export interface SidebarChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
  hasDocument?: boolean;
  documentFilename?: string;
  documentType?: 'default' | 'upload'; // Thêm type để phân biệt
}
