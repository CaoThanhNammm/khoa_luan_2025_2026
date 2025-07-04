import { AxiosError } from 'axios';
import axios from './api';
import AuthService from './AuthService';

export interface FileUploadResponse {
  message: string;
  document_id: string;
  conversation_id?: number;
  filename: string;
  file_size: number;
  sentences_count: number;
  s3_key: string;
  s3_url: string;
  status: string;
}

export const uploadFile = async (file: File, conversationId?: number): Promise<FileUploadResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    // Add conversation_id if provided
    if (conversationId !== undefined) {
      formData.append('conversation_id', conversationId.toString());
    }

    // Get auth headers from AuthService
    const authHeaders = AuthService.getAuthHeader();
    
    const response = await axios.post<FileUploadResponse>('/api/upload-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...authHeaders,
      },
      timeout: 600000, // 10 minutes timeout for file upload
    });

    return response.data;
  } catch (error: unknown) {
    console.error('File upload error:', error);
    
    // Handle different types of errors
    if (error && typeof error === 'object' && 'response' in error) {
      // Server responded with error status
      const axiosError = error as AxiosError<{ message?: string }>;
      const errorMessage = axiosError.response?.data?.message || 'Failed to upload file';
      throw new Error(errorMessage);
    } else if (error && typeof error === 'object' && 'request' in error) {
      // Request was made but no response received
      throw new Error('Network error: Unable to connect to server');
    } else {
      // Something else happened
      throw new Error((error as Error)?.message || 'An unexpected error occurred');
    }
  }
};

export const getUserDocuments = async (): Promise<unknown[]> => {
  try {
    const authHeaders = AuthService.getAuthHeader();
    const response = await axios.get('/api/user-documents', {
      headers: authHeaders,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching user documents:', error);
    throw error;
  }
};

export const FileUploadService = {
  uploadFile,
  getUserDocuments,
};
