import axios from "./api";
import type { AxiosResponse } from "axios";

const API_URL = "/api/users/";

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

export interface UpdateProfileRequest {
  username: string;
  email: string;
}

export interface UpdatePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export interface UserSettings {
  theme: 'light' | 'dark';
  notifications: boolean;
  language: string;
}

class UserService {
  getUserProfile(): Promise<AxiosResponse<UserProfile>> {
    return axios.get<UserProfile>(API_URL + "profile");
  }

  updateProfile(userData: UpdateProfileRequest): Promise<AxiosResponse<UserProfile>> {
    return axios.put<UserProfile>(API_URL + "profile", userData);
  }

  updatePassword(passwordData: UpdatePasswordRequest): Promise<AxiosResponse<{ message: string }>> {
    return axios.put<{ message: string }>(API_URL + "password", passwordData);
  }

  updateSettings(settingsData: UserSettings): Promise<AxiosResponse<UserSettings>> {
    return axios.put<UserSettings>(API_URL + "settings", settingsData);
  }
}

const userServiceInstance = new UserService();
export default userServiceInstance;
