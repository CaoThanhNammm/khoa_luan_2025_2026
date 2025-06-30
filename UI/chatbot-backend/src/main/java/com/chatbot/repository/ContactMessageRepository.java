package com.chatbot.repository;

import com.chatbot.model.ContactMessage;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ContactMessageRepository extends JpaRepository<ContactMessage, Long> {
    
    // Find all messages ordered by creation date (newest first)
    Page<ContactMessage> findAllByOrderByCreatedAtDesc(Pageable pageable);
    
    // Find unread messages
    Page<ContactMessage> findByIsReadFalseOrderByCreatedAtDesc(Pageable pageable);
    
    // Find messages by email
    List<ContactMessage> findByEmailOrderByCreatedAtDesc(String email);
    
    // Find messages created between dates
    List<ContactMessage> findByCreatedAtBetweenOrderByCreatedAtDesc(LocalDateTime startDate, LocalDateTime endDate);
    
    // Count unread messages
    @Query("SELECT COUNT(cm) FROM ContactMessage cm WHERE cm.isRead = false")
    Long countUnreadMessages();
    
    // Find messages by subject containing keyword
    Page<ContactMessage> findBySubjectContainingIgnoreCaseOrderByCreatedAtDesc(String keyword, Pageable pageable);
    
    // Find messages by name containing keyword
    Page<ContactMessage> findByNameContainingIgnoreCaseOrderByCreatedAtDesc(String keyword, Pageable pageable);
}
