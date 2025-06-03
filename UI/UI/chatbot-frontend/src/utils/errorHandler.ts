import { AxiosError } from 'axios';

export interface ApiError {
  message: string;
  status?: number;
  code?: string;
}

export function handleApiError(error: unknown): ApiError {
  if (error instanceof AxiosError) {
    const response = error.response;
    
    if (response) {
      // Server responded with error status
      const message = response.data?.message || response.data?.error || 'Có lỗi xảy ra từ server';
      return {
        message,
        status: response.status,
        code: response.data?.code
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'Không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng.',
        code: 'NETWORK_ERROR'
      };
    } else {
      // Something else happened
      return {
        message: error.message || 'Có lỗi không xác định xảy ra',
        code: 'UNKNOWN_ERROR'
      };
    }
  }
  
  // Non-axios error
  if (error instanceof Error) {
    return {
      message: error.message,
      code: 'GENERAL_ERROR'
    };
  }
  
  return {
    message: 'Có lỗi không xác định xảy ra',
    code: 'UNKNOWN_ERROR'
  };
}

export function getErrorMessage(error: unknown): string {
  return handleApiError(error).message;
}

export function isNetworkError(error: unknown): boolean {
  const apiError = handleApiError(error);
  return apiError.code === 'NETWORK_ERROR';
}

export function isAuthenticationError(error: unknown): boolean {
  const apiError = handleApiError(error);
  return apiError.status === 401;
}

export function isValidationError(error: unknown): boolean {
  const apiError = handleApiError(error);
  return apiError.status === 400;
}

export function isServerError(error: unknown): boolean {
  const apiError = handleApiError(error);
  return apiError.status ? apiError.status >= 500 : false;
}