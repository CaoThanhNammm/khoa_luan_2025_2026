    package com.chatbot.service;

import com.chatbot.model.UserDocument;
import com.chatbot.repository.UserDocumentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
@Transactional
public class UserDocumentService {
    
    private static final Logger logger = LoggerFactory.getLogger(UserDocumentService.class);
    
    @Autowired
    private UserDocumentRepository userDocumentRepository;
    
    /**
     * Lưu thông tin tài liệu mới
     */
    public UserDocument saveDocument(Long userId, String documentId, String filename, Map<String, Object> uploadResult) {
        logger.info("Saving document for user {}: documentId={}, filename={}", userId, documentId, filename);
        
        UserDocument userDocument = new UserDocument(userId, documentId, filename);
        
        // Set additional info from upload result
        if (uploadResult != null) {
            if (uploadResult.containsKey("file_size")) {
                userDocument.setFileSize(((Number) uploadResult.get("file_size")).longValue());
            }
            if (uploadResult.containsKey("s3_key")) {
                userDocument.setS3Key((String) uploadResult.get("s3_key"));
            }
            if (uploadResult.containsKey("s3_url")) {
                userDocument.setS3Url((String) uploadResult.get("s3_url"));
            }
            if (uploadResult.containsKey("sentences_count")) {
                userDocument.setSentencesCount(((Number) uploadResult.get("sentences_count")).intValue());
            }
            if (uploadResult.containsKey("status")) {
                userDocument.setStatus((String) uploadResult.get("status"));
            }
        }
        
        return userDocumentRepository.save(userDocument);
    }
    
    /**
     * Lưu thông tin tài liệu mới với conversation ID
     */
    public UserDocument saveDocument(Long userId, Long conversationId, String documentId, String filename, Map<String, Object> uploadResult) {
        logger.info("Saving document for user {} and conversation {}: documentId={}, filename={}", userId, conversationId, documentId, filename);
        
        UserDocument userDocument = new UserDocument(userId, documentId, filename);
        userDocument.setConversationId(conversationId);
        
        // Set additional info from upload result
        if (uploadResult != null) {
            if (uploadResult.containsKey("file_size")) {
                userDocument.setFileSize(((Number) uploadResult.get("file_size")).longValue());
            }
            if (uploadResult.containsKey("s3_key")) {
                userDocument.setS3Key((String) uploadResult.get("s3_key"));
            }
            if (uploadResult.containsKey("s3_url")) {
                userDocument.setS3Url((String) uploadResult.get("s3_url"));
            }
            if (uploadResult.containsKey("sentences_count")) {
                userDocument.setSentencesCount(((Number) uploadResult.get("sentences_count")).intValue());
            }
            if (uploadResult.containsKey("status")) {
                userDocument.setStatus((String) uploadResult.get("status"));
            }
        }
        
        return userDocumentRepository.save(userDocument);
    }
    
    /**
     * Lấy danh sách tài liệu của user
     */
    public List<UserDocument> getUserDocuments(Long userId) {
        logger.info("Getting documents for user {}", userId);
        return userDocumentRepository.findByUserIdOrderByUploadDateDesc(userId);
    }
    
    /**
     * Lấy danh sách tài liệu theo conversation
     */
    public List<UserDocument> getDocumentsByConversation(Long userId, Long conversationId) {
        logger.info("Getting documents for user {} and conversation {}", userId, conversationId);
        return userDocumentRepository.findByUserIdAndConversationId(userId, conversationId);
    }
    
    /**
     * Tìm tài liệu theo document ID
     */
    public Optional<UserDocument> findByDocumentId(String documentId) {
        return userDocumentRepository.findByDocumentId(documentId);
    }
    
    /**
     * Tìm tài liệu theo user ID và document ID
     */
    public Optional<UserDocument> findByUserIdAndDocumentId(Long userId, String documentId) {
        return userDocumentRepository.findByUserIdAndDocumentId(userId, documentId);
    }
    
    /**
     * Kiểm tra xem user có quyền truy cập document không
     */
    public boolean canUserAccessDocument(Long userId, String documentId) {
        return userDocumentRepository.findByUserIdAndDocumentId(userId, documentId).isPresent();
    }
    
    /**
     * Cập nhật status của document
     */
    public UserDocument updateDocumentStatus(String documentId, String status) {
        Optional<UserDocument> optionalDocument = userDocumentRepository.findByDocumentId(documentId);
        if (optionalDocument.isPresent()) {
            UserDocument document = optionalDocument.get();
            document.setStatus(status);
            return userDocumentRepository.save(document);
        }
        return null;
    }
    
    /**
     * Xóa tài liệu
     */
    public boolean deleteDocument(Long userId, String documentId) {
        Optional<UserDocument> optionalDocument = userDocumentRepository.findByUserIdAndDocumentId(userId, documentId);
        if (optionalDocument.isPresent()) {
            userDocumentRepository.delete(optionalDocument.get());
            logger.info("Deleted document {} for user {}", documentId, userId);
            return true;
        }
        return false;
    }
    
    /**
     * Đếm số lượng tài liệu của user
     */
    public long countUserDocuments(Long userId) {
        return userDocumentRepository.countByUserId(userId);
    }
    
    /**
     * Tìm tài liệu theo filename
     */
    public List<UserDocument> searchDocumentsByFilename(Long userId, String filename) {
        return userDocumentRepository.findByUserIdAndFilenameContainingIgnoreCase(userId, filename);
    }
}
