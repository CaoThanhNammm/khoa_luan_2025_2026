package com.chatbot.service;

import com.chatbot.dto.ContactMessageDto;
import com.chatbot.model.ContactMessage;
import com.chatbot.repository.ContactMessageRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class ContactMessageService {
    
    @Autowired
    private ContactMessageRepository contactMessageRepository;
    
    @Autowired
    private EmailService emailService;
    
    /**
     * Submit a new contact message
     */
    public ContactMessage submitContactMessage(ContactMessageDto contactMessageDto) {
        ContactMessage contactMessage = new ContactMessage(
            contactMessageDto.getName(),
            contactMessageDto.getEmail(),
            contactMessageDto.getSubject(),
            contactMessageDto.getMessage()
        );
        
        ContactMessage savedMessage = contactMessageRepository.save(contactMessage);
        
        // Send notification email to admin
        try {
            sendAdminNotification(savedMessage);
        } catch (Exception e) {
            // Log error but don't fail the contact submission
            System.err.println("Failed to send admin notification: " + e.getMessage());
        }
        
        // Send confirmation email to user
        try {
            sendUserConfirmation(savedMessage);
        } catch (Exception e) {
            // Log error but don't fail the contact submission
            System.err.println("Failed to send user confirmation: " + e.getMessage());
        }
        
        return savedMessage;
    }
    
    /**
     * Get all contact messages with pagination
     */
    @Transactional(readOnly = true)
    public Page<ContactMessage> getAllMessages(Pageable pageable) {
        return contactMessageRepository.findAllByOrderByCreatedAtDesc(pageable);
    }
    
    /**
     * Get unread messages with pagination
     */
    @Transactional(readOnly = true)
    public Page<ContactMessage> getUnreadMessages(Pageable pageable) {
        return contactMessageRepository.findByIsReadFalseOrderByCreatedAtDesc(pageable);
    }
    
    /**
     * Get message by ID
     */
    @Transactional(readOnly = true)
    public Optional<ContactMessage> getMessageById(Long id) {
        return contactMessageRepository.findById(id);
    }
    
    /**
     * Mark message as read
     */
    public ContactMessage markAsRead(Long id) {
        Optional<ContactMessage> messageOpt = contactMessageRepository.findById(id);
        if (messageOpt.isPresent()) {
            ContactMessage message = messageOpt.get();
            message.setIsRead(true);
            return contactMessageRepository.save(message);
        }
        throw new RuntimeException("Contact message not found with id: " + id);
    }
    
    /**
     * Reply to a contact message
     */
    public ContactMessage replyToMessage(Long id, String adminReply) {
        Optional<ContactMessage> messageOpt = contactMessageRepository.findById(id);
        if (messageOpt.isPresent()) {
            ContactMessage message = messageOpt.get();
            message.setAdminReply(adminReply);
            message.setRepliedAt(LocalDateTime.now());
            message.setIsRead(true);
            
            ContactMessage savedMessage = contactMessageRepository.save(message);
            
            // Send reply email to user
            try {
                sendReplyToUser(savedMessage);
            } catch (Exception e) {
                System.err.println("Failed to send reply email: " + e.getMessage());
            }
            
            return savedMessage;
        }
        throw new RuntimeException("Contact message not found with id: " + id);
    }
    
    /**
     * Count unread messages
     */
    @Transactional(readOnly = true)
    public Long countUnreadMessages() {
        return contactMessageRepository.countUnreadMessages();
    }
    
    /**
     * Search messages by keyword
     */
    @Transactional(readOnly = true)
    public Page<ContactMessage> searchMessages(String keyword, Pageable pageable) {
        return contactMessageRepository.findBySubjectContainingIgnoreCaseOrderByCreatedAtDesc(keyword, pageable);
    }
    
    /**
     * Get messages by email
     */
    @Transactional(readOnly = true)
    public List<ContactMessage> getMessagesByEmail(String email) {
        return contactMessageRepository.findByEmailOrderByCreatedAtDesc(email);
    }
    
    // Private helper methods for email notifications
    
    private void sendAdminNotification(ContactMessage message) {
        String subject = "[NLU AI Contact] New Message: " + message.getSubject();
        String body = String.format(
            "New contact message received:\n\n" +
            "From: %s (%s)\n" +
            "Subject: %s\n" +
            "Message:\n%s\n\n" +
            "Submitted at: %s",
            message.getName(),
            message.getEmail(),
            message.getSubject(),
            message.getMessage(),
            message.getCreatedAt()
        );
        
        // Send to admin emails
        emailService.sendSimpleMessage("21130467@st.hcmuaf.edu.vn", subject, body);
        emailService.sendSimpleMessage("21130448@st.hcmuaf.edu.vn", subject, body);
    }
    
    private void sendUserConfirmation(ContactMessage message) {
        String subject = "Thank you for contacting NLU AI - Message Received";
        String body = String.format(
            "Dear %s,\n\n" +
            "Thank you for contacting us. We have received your message with the subject: \"%s\"\n\n" +
            "We will review your message and get back to you as soon as possible.\n\n" +
            "Best regards,\n" +
            "NLU AI Team\n\n" +
            "---\n" +
            "Your message:\n%s",
            message.getName(),
            message.getSubject(),
            message.getMessage()
        );
        
        emailService.sendSimpleMessage(message.getEmail(), subject, body);
    }
    
    private void sendReplyToUser(ContactMessage message) {
        String subject = "Re: " + message.getSubject();
        String body = String.format(
            "Dear %s,\n\n" +
            "Thank you for contacting NLU AI. Here is our response to your message:\n\n" +
            "%s\n\n" +
            "If you have any additional questions, please don't hesitate to contact us.\n\n" +
            "Best regards,\n" +
            "NLU AI Team\n\n" +
            "---\n" +
            "Your original message:\n%s",
            message.getName(),
            message.getAdminReply(),
            message.getMessage()
        );
        
        emailService.sendSimpleMessage(message.getEmail(), subject, body);
    }
}
