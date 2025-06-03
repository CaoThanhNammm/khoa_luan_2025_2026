package com.chatbot.controller;

import com.chatbot.dto.ContactMessageDto;
import com.chatbot.model.ContactMessage;
import com.chatbot.service.ContactMessageService;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/contact")
@CrossOrigin(origins = "*", maxAge = 3600)
public class ContactController {
    
    @Autowired
    private ContactMessageService contactMessageService;
    
    /**
     * Submit a contact message (Public endpoint)
     */
    @PostMapping("/submit")
    public ResponseEntity<?> submitContactMessage(@Valid @RequestBody ContactMessageDto contactMessageDto) {
        try {
            ContactMessage savedMessage = contactMessageService.submitContactMessage(contactMessageDto);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Your message has been sent successfully! We will get back to you soon.");
            response.put("messageId", savedMessage.getId());
            response.put("submittedAt", savedMessage.getCreatedAt());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Failed to send message. Please try again later.");
            errorResponse.put("error", e.getMessage());
            
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }
    
    /**
     * Get all contact messages (Admin only)
     */
    @GetMapping("/admin/messages")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Page<ContactMessage>> getAllMessages(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        Page<ContactMessage> messages = contactMessageService.getAllMessages(pageable);
        return ResponseEntity.ok(messages);
    }
    
    /**
     * Get unread contact messages (Admin only)
     */
    @GetMapping("/admin/unread")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Page<ContactMessage>> getUnreadMessages(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        Page<ContactMessage> messages = contactMessageService.getUnreadMessages(pageable);
        return ResponseEntity.ok(messages);
    }
    
    /**
     * Get contact message by ID (Admin only)
     */
    @GetMapping("/admin/messages/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> getMessageById(@PathVariable Long id) {
        Optional<ContactMessage> messageOpt = contactMessageService.getMessageById(id);
        
        if (messageOpt.isPresent()) {
            return ResponseEntity.ok(messageOpt.get());
        } else {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Contact message not found");
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse);
        }
    }
    
    /**
     * Mark message as read (Admin only)
     */
    @PutMapping("/admin/messages/{id}/read")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> markAsRead(@PathVariable Long id) {
        try {
            ContactMessage updatedMessage = contactMessageService.markAsRead(id);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Message marked as read");
            response.put("contactMessage", updatedMessage);
            
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse);
        }
    }
    
    /**
     * Reply to a contact message (Admin only)
     */
    @PutMapping("/admin/messages/{id}/reply")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<?> replyToMessage(
            @PathVariable Long id,
            @RequestBody Map<String, String> replyData) {
        
        String adminReply = replyData.get("adminReply");
        if (adminReply == null || adminReply.trim().isEmpty()) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Admin reply cannot be empty");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse);
        }
        
        try {
            ContactMessage updatedMessage = contactMessageService.replyToMessage(id, adminReply);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Reply sent successfully");
            response.put("contactMessage", updatedMessage);
            
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse);
        }
    }
    
    /**
     * Get unread message count (Admin only)
     */
    @GetMapping("/admin/unread-count")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Map<String, Long>> getUnreadCount() {
        Long count = contactMessageService.countUnreadMessages();
        Map<String, Long> response = new HashMap<>();
        response.put("unreadCount", count);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Search messages (Admin only)
     */
    @GetMapping("/admin/search")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Page<ContactMessage>> searchMessages(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        Page<ContactMessage> messages = contactMessageService.searchMessages(keyword, pageable);
        return ResponseEntity.ok(messages);
    }
    
    /**
     * Get messages by email (Admin only)
     */
    @GetMapping("/admin/by-email")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<ContactMessage>> getMessagesByEmail(@RequestParam String email) {
        List<ContactMessage> messages = contactMessageService.getMessagesByEmail(email);
        return ResponseEntity.ok(messages);
    }
}
