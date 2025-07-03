package com.chatbot.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "user_documents")
public class UserDocument {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    @Column(name = "conversation_id")
    private Long conversationId;
    
    @Column(name = "document_id", nullable = false, unique = true)
    private String documentId;
    
    @Column(name = "filename", nullable = false)
    private String filename;
    
    @Column(name = "file_size")
    private Long fileSize;
    
    @Column(name = "s3_key")
    private String s3Key;
    
    @Column(name = "s3_url")
    private String s3Url;
    
    @Column(name = "sentences_count")
    private Integer sentencesCount;
    
    @Column(name = "upload_date", nullable = false)
    private LocalDateTime uploadDate;
    
    @Column(name = "status")
    private String status;
    
    // Constructors
    public UserDocument() {
        this.uploadDate = LocalDateTime.now();
        this.status = "processing";
    }
    
    public UserDocument(Long userId, String documentId, String filename) {
        this();
        this.userId = userId;
        this.documentId = documentId;
        this.filename = filename;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Long getUserId() {
        return userId;
    }
    
    public void setUserId(Long userId) {
        this.userId = userId;
    }
    
    public Long getConversationId() {
        return conversationId;
    }
    
    public void setConversationId(Long conversationId) {
        this.conversationId = conversationId;
    }
    
    public String getDocumentId() {
        return documentId;
    }
    
    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }
    
    public String getFilename() {
        return filename;
    }
    
    public void setFilename(String filename) {
        this.filename = filename;
    }
    
    public Long getFileSize() {
        return fileSize;
    }
    
    public void setFileSize(Long fileSize) {
        this.fileSize = fileSize;
    }
    
    public String getS3Key() {
        return s3Key;
    }
    
    public void setS3Key(String s3Key) {
        this.s3Key = s3Key;
    }
    
    public String getS3Url() {
        return s3Url;
    }
    
    public void setS3Url(String s3Url) {
        this.s3Url = s3Url;
    }
    
    public Integer getSentencesCount() {
        return sentencesCount;
    }
    
    public void setSentencesCount(Integer sentencesCount) {
        this.sentencesCount = sentencesCount;
    }
    
    public LocalDateTime getUploadDate() {
        return uploadDate;
    }
    
    public void setUploadDate(LocalDateTime uploadDate) {
        this.uploadDate = uploadDate;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
}
