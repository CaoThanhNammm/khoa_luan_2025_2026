package com.chatbot.service;

import com.chatbot.model.User;
import com.chatbot.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.mail.MessagingException;
import java.sql.Date;
import java.time.LocalDate;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;

@Service
public class UserService {

    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private EmailService emailService;

    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    public boolean existsByUsername(String username) {
        return userRepository.existsByUsername(username);
    }

    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }

    public User registerUser(String username, String email, String password) {
        User user = new User();
        user.setUsername(username);
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(password));
        user.setRoles(Collections.singleton("USER"));
        
        return userRepository.save(user);
    }
    
    public User getUserById(Long id) {
        return userRepository.findById(id).orElse(null);
    }

    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }
    
    public void createPasswordResetTokenForUser(String email) throws MessagingException {
        logger.info("Creating password reset token for email: {}", email);
        Optional<User> userOpt = findByEmail(email);
        
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            String token = UUID.randomUUID().toString();
            logger.info("Generated token for user ID: {}", user.getId());
            
            // Set token expiry to 24 hours from now
            LocalDate tomorrow = LocalDate.now().plusDays(1);
            Date expiryDate = Date.valueOf(tomorrow);
            
            user.setPasswordResetToken(token);
            user.setPasswordResetTokenExpiry(expiryDate);
            userRepository.save(user);
            logger.info("Token saved to database");
            
            // Send email with reset link
            try {
                emailService.sendPasswordResetEmail(user.getEmail(), token);
                logger.info("Password reset email sent");
            } catch (MessagingException e) {
                logger.error("Failed to send password reset email: {}", e.getMessage(), e);
                throw e;
            }
        } else {
            logger.warn("No user found with email: {}", email);
        }
    }
    
    public Optional<User> getUserByPasswordResetToken(String token) {
        return userRepository.findByPasswordResetToken(token);
    }
    
    public boolean isPasswordResetTokenValid(User user) {
        Date now = Date.valueOf(LocalDate.now());
        return user.getPasswordResetTokenExpiry() != null && 
               user.getPasswordResetTokenExpiry().after(now);
    }
    
    public void resetPassword(User user, String newPassword) {
        user.setPassword(passwordEncoder.encode(newPassword));
        user.setPasswordResetToken(null);
        user.setPasswordResetTokenExpiry(null);
        userRepository.save(user);
    }
}