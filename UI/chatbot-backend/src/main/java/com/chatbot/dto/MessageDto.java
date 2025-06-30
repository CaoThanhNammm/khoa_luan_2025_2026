package com.chatbot.dto;

import com.chatbot.model.Message.MessageType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class MessageDto {
    private Long id;
    private String content;
    private MessageType type;
    private LocalDateTime timestamp;
    private Long conversationId;
}