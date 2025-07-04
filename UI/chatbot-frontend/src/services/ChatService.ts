import axios from "./api";
import type { AxiosResponse } from "axios";
import type { ChatSession, Message } from "../types/chat";
import { adaptConversationToSession, adaptMessageToFrontend } from "../utils/apiAdapters";

const API_URL = "/api/chat/";

export interface ConversationResponse {
  id: number;
  title: string;
  createdAt: string;
  messages: Message[];
  hasDocument?: boolean;
  documentInfo?: {
    documentId: string;
    filename: string;
    fileSize: number;
    sentencesCount: number;
    uploadDate: string;
    status: string;
  };
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  id: number;
  content: string;
  type: 'USER' | 'BOT';
  timestamp: string;
  conversationId: number;
}

class ChatService {
  async getConversations(): Promise<ChatSession[]> {
    const response = await axios.get<ConversationResponse[]>(API_URL + "conversations");
    return response.data.map(adaptConversationToSession);
  }

  async getConversation(id: number): Promise<ChatSession> {
    const response = await axios.get<ConversationResponse>(API_URL + "conversations/" + id);
    return adaptConversationToSession(response.data);
  }

  async startNewConversation(message: string): Promise<ChatSession> {
    const response = await axios.post<ConversationResponse>(
      API_URL + "conversations",
      { message }
    );
    return adaptConversationToSession(response.data);
  }

  async sendMessage(conversationId: number, message: string): Promise<Message> {
    const response = await axios.post<MessageResponse>(
      API_URL + `conversations/${conversationId}/messages`,
      { message }
    );
    return adaptMessageToFrontend(response.data);
  }
  
  deleteConversation(id: number): Promise<AxiosResponse<{ message: string }>> {
    return axios.delete<{ message: string }>(API_URL + "conversations/" + id);
  }

  // Raw API methods for backward compatibility
  getConversationsRaw(): Promise<AxiosResponse<ConversationResponse[]>> {
    return axios.get<ConversationResponse[]>(API_URL + "conversations");
  }

  getConversationRaw(id: number): Promise<AxiosResponse<ConversationResponse>> {
    return axios.get<ConversationResponse>(API_URL + "conversations/" + id);
  }

  startNewConversationRaw(message: string): Promise<AxiosResponse<ConversationResponse>> {
    return axios.post<ConversationResponse>(
      API_URL + "conversations",
      { message }
    );
  }

  sendMessageRaw(conversationId: number, message: string): Promise<AxiosResponse<MessageResponse>> {
    return axios.post<MessageResponse>(
      API_URL + `conversations/${conversationId}/messages`,
      { message }
    );
  }
}

const chatServiceInstance = new ChatService();
export default chatServiceInstance;
