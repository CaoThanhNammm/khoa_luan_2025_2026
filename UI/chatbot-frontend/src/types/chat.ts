export interface Message {
  id: number;
  content: string;
  type: 'USER' | 'BOT';
  timestamp: string;
  conversationId: number;
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
