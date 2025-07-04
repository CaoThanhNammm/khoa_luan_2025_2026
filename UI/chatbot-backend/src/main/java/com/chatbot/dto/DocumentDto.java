package com.chatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DocumentDto {
    private String documentId;
    private String filename;
    private Long fileSize;
    private Integer sentencesCount;
    private LocalDateTime uploadDate;
    private String status;
}