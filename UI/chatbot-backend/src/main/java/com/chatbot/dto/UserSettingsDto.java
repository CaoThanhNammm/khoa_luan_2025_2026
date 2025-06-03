package com.chatbot.dto;

import java.time.LocalDateTime;

public class UserSettingsDto {
    private String theme;
    private Boolean notifications;
    private String language;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // Constructors
    public UserSettingsDto() {}

    public UserSettingsDto(String theme, Boolean notifications, String language) {
        this.theme = theme;
        this.notifications = notifications;
        this.language = language;
    }

    // Getters and Setters
    public String getTheme() {
        return theme;
    }

    public void setTheme(String theme) {
        this.theme = theme;
    }

    public Boolean getNotifications() {
        return notifications;
    }

    public void setNotifications(Boolean notifications) {
        this.notifications = notifications;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}
