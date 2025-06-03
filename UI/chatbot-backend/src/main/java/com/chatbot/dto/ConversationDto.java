package com.chatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ConversationDto {
    private Long id;
    private String title;
    private LocalDateTime createdAt;
    private List<MessageDto> messages = new ArrayList<>();
}