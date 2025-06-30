package com.chatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AccountStatsDto {
    private Long totalConversations;
    private Long totalMessages;
    private String accountStatus;
    private String memberSince;
}
