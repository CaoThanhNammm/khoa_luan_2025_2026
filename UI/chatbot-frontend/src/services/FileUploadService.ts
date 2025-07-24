import { AxiosError } from 'axios';
import axios from 'axios';
import AuthService from './AuthService';

export interface FileUploadResponse {
  message: string;
  document_id: string;
  conversation_uuid?: string;
  filename: string;
  file_size: number;
  sentences_count?: number;
  s3_key: string;
  s3_url: string;
  status: string;
}

// Track ongoing uploads to prevent duplicates with Promise tracking
let ongoingUploads = new Map<string, Promise<FileUploadResponse>>();

export const uploadFile = async (file: File): Promise<FileUploadResponse> => {
  // Create unique identifier for this file upload
  const fileId = `${file.name}-${file.size}-${file.lastModified}`;
  
  // Check if this exact file is already being uploaded
  if (ongoingUploads.has(fileId)) {
    console.log('File upload already in progress, returning existing promise');
    return ongoingUploads.get(fileId)!;
  }

  // Create and store the upload promise
  const uploadPromise = performUpload(file, fileId);
  ongoingUploads.set(fileId, uploadPromise);
  
  return uploadPromise;
};

const performUpload = async (file: File, fileId: string): Promise<FileUploadResponse> => {

  try {
    const formData = new FormData();
    formData.append('file', file);

    // Call local FastAPI backend
    const uploadUrl = 'http://localhost:8000/api/upload-file';
    
    const response = await axios.post<FileUploadResponse>(uploadUrl, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'User-Agent': 'ChatBot-Frontend/1.0',
        ...AuthService.getAuthHeader() // Add authentication header
      },
      timeout: 1200000, // 20 minutes timeout for large files
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
  } finally {
    // Always remove from ongoing uploads when done (success or failure)
    ongoingUploads.delete(fileId);
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
