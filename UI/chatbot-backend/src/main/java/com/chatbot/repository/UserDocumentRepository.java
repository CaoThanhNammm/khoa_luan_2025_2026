package com.chatbot.repository;

import com.chatbot.model.UserDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserDocumentRepository extends JpaRepository<UserDocument, Long> {
    
    /**
     * Tìm tài liệu theo user ID
     */
    List<UserDocument> findByUserIdOrderByUploadDateDesc(Long userId);
    
    /**
     * Tìm tài liệu theo user ID và conversation ID
     */
    List<UserDocument> findByUserIdAndConversationIdOrderByUploadDateDesc(Long userId, Long conversationId);
    
    /**
     * Tìm tài liệu theo user ID và conversation ID (simple version)
     */
    List<UserDocument> findByUserIdAndConversationId(Long userId, Long conversationId);
    
    /**
     * Tìm tài liệu theo document ID
     */
    Optional<UserDocument> findByDocumentId(String documentId);
    
    /**
     * Tìm tài liệu theo user ID và document ID
     */
    Optional<UserDocument> findByUserIdAndDocumentId(Long userId, String documentId);
    
    /**
     * Kiểm tra xem user có tài liệu nào không
     */
    boolean existsByUserId(Long userId);
    
    /**
     * Kiểm tra xem document ID đã tồn tại chưa
     */
    boolean existsByDocumentId(String documentId);
    
    /**
     * Đếm số lượng tài liệu của user
     */
    @Query("SELECT COUNT(ud) FROM UserDocument ud WHERE ud.userId = :userId")
    long countByUserId(@Param("userId") Long userId);
    
    /**
     * Tìm tài liệu theo filename và user ID
     */
    List<UserDocument> findByUserIdAndFilenameContainingIgnoreCase(Long userId, String filename);
}
