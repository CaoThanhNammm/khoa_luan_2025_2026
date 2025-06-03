export interface Message {
  id: number;
  content: string;
  type: 'USER' | 'BOT';
  timestamp: string;
  conversationId: number;
  isStreaming?: boolean; // Để xác định tin nhắn đang được gõ
  isLatest?: boolean; // Để xác định tin nhắn mới nhất của bot
}

export interface ChatSession {
  id: number;
  title: string;
  createdAt: string;
  messages: Message[];
}

// Extended interface for sidebar display
export interface SidebarChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: Date;
}
