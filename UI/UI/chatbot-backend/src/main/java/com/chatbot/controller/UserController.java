package com.chatbot.controller;

import com.chatbot.dto.AccountStatsDto;
import com.chatbot.dto.UserProfileDto;
import com.chatbot.dto.UserSettingsDto;
import com.chatbot.model.User;
import com.chatbot.model.UserSettings;
import com.chatbot.repository.ConversationRepository;
import com.chatbot.repository.MessageRepository;
import com.chatbot.repository.UserRepository;
import com.chatbot.repository.UserSettingsRepository;
import com.chatbot.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import javax.mail.MessagingException;
import javax.validation.Valid;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:5173"})
public class UserController {    @Autowired
    private UserService userService;
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private UserSettingsRepository userSettingsRepository;
    
    @Autowired
    private ConversationRepository conversationRepository;
    
    @Autowired
    private MessageRepository messageRepository;
      @GetMapping("/profile")
    public ResponseEntity<?> getCurrentUserProfile() {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        // Create DTO to avoid serialization issues
        UserProfileDto profileDto = new UserProfileDto();
        profileDto.setId(user.getId());
        profileDto.setUsername(user.getUsername());
        profileDto.setEmail(user.getEmail());
        profileDto.setCreatedAt(user.getCreatedAt());
        profileDto.setUpdatedAt(user.getUpdatedAt());
        
        return ResponseEntity.ok(profileDto);
    }
      @PutMapping("/profile")
    public ResponseEntity<?> updateProfile(@Valid @RequestBody Map<String, String> profileData) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        String newEmail = profileData.get("email");
        
        // Check if email already exists (if changed)
        if (!user.getEmail().equals(newEmail) && userService.existsByEmail(newEmail)) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "Email is already in use");
            return ResponseEntity.badRequest().body(response);
        }
          // Update user profile - only email can be changed
        user.setEmail(newEmail);
        User savedUser = userRepository.save(user);
        
        // Return updated profile as DTO
        UserProfileDto profileDto = new UserProfileDto();
        profileDto.setId(savedUser.getId());
        profileDto.setUsername(savedUser.getUsername());
        profileDto.setEmail(savedUser.getEmail());
        profileDto.setCreatedAt(savedUser.getCreatedAt());
        profileDto.setUpdatedAt(savedUser.getUpdatedAt());
        
        return ResponseEntity.ok(profileDto);
    }
    
    @PutMapping("/password")
    public ResponseEntity<?> updatePassword(@Valid @RequestBody Map<String, String> passwordData) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        String currentPassword = passwordData.get("currentPassword");
        String newPassword = passwordData.get("newPassword");
        
        // Check if current password is correct
        if (!passwordEncoder.matches(currentPassword, user.getPassword())) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "Current password is incorrect");
            return ResponseEntity.badRequest().body(response);
        }
        
        // Update password
        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);
        
        Map<String, String> response = new HashMap<>();
        response.put("message", "Password updated successfully");
        return ResponseEntity.ok(response);
    }
      @GetMapping("/settings")
    public ResponseEntity<?> getUserSettings() {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        Optional<UserSettings> userSettingsOpt = userSettingsRepository.findByUser(user);
        UserSettings userSettings;
        
        if (userSettingsOpt.isPresent()) {
            userSettings = userSettingsOpt.get();
        } else {
            // Create default settings if not exists
            userSettings = new UserSettings(user);
            userSettings = userSettingsRepository.save(userSettings);
        }
        
        // Convert to DTO
        UserSettingsDto settingsDto = new UserSettingsDto();
        settingsDto.setTheme(userSettings.getTheme());
        settingsDto.setNotifications(userSettings.getNotifications());
        settingsDto.setLanguage(userSettings.getLanguage());
        settingsDto.setCreatedAt(userSettings.getCreatedAt());
        settingsDto.setUpdatedAt(userSettings.getUpdatedAt());
        
        return ResponseEntity.ok(settingsDto);
    }
    
    @PutMapping("/settings")
    public ResponseEntity<?> updateSettings(@Valid @RequestBody Map<String, Object> settingsData) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        Optional<UserSettings> userSettingsOpt = userSettingsRepository.findByUser(user);
        UserSettings userSettings;
        
        if (userSettingsOpt.isPresent()) {
            userSettings = userSettingsOpt.get();
        } else {
            // Create new settings if not exists
            userSettings = new UserSettings(user);
        }
        
        // Update settings from request data
        if (settingsData.containsKey("theme")) {
            String theme = (String) settingsData.get("theme");
            if ("light".equals(theme) || "dark".equals(theme)) {
                userSettings.setTheme(theme);
            }
        }
        
        if (settingsData.containsKey("notifications")) {
            Boolean notifications = (Boolean) settingsData.get("notifications");
            userSettings.setNotifications(notifications);
        }
        
        if (settingsData.containsKey("language")) {
            String language = (String) settingsData.get("language");
            userSettings.setLanguage(language);
        }
        
        // Save updated settings
        UserSettings savedSettings = userSettingsRepository.save(userSettings);
        
        // Convert to DTO for response
        UserSettingsDto settingsDto = new UserSettingsDto();
        settingsDto.setTheme(savedSettings.getTheme());
        settingsDto.setNotifications(savedSettings.getNotifications());
        settingsDto.setLanguage(savedSettings.getLanguage());
        settingsDto.setCreatedAt(savedSettings.getCreatedAt());
        settingsDto.setUpdatedAt(savedSettings.getUpdatedAt());
        
        return ResponseEntity.ok(settingsDto);
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<?> forgotPassword(@Valid @RequestBody Map<String, String> emailRequest) {
        String email = emailRequest.get("email");
        Map<String, String> response = new HashMap<>();
        
        try {
            userService.createPasswordResetTokenForUser(email);
            response.put("message", "If that email address is in our system, a password reset link has been sent to it");
            return ResponseEntity.ok(response);
        } catch (MessagingException e) {
            response.put("message", "Failed to send email. Please try again later.");
            return ResponseEntity.internalServerError().body(response);
        }
    }
    
    @GetMapping("/reset-password/validate")
    public ResponseEntity<?> validatePasswordResetToken(@RequestParam("token") String token) {
        Optional<User> userOpt = userService.getUserByPasswordResetToken(token);
        Map<String, String> response = new HashMap<>();
        
        if (userOpt.isPresent() && userService.isPasswordResetTokenValid(userOpt.get())) {
            response.put("message", "Token is valid");
            return ResponseEntity.ok(response);
        } else {
            response.put("message", "Token is invalid or expired");
            return ResponseEntity.badRequest().body(response);
        }
    }
    
    @PostMapping("/reset-password")
    public ResponseEntity<?> resetPassword(@Valid @RequestBody Map<String, String> resetRequest) {
        String token = resetRequest.get("token");
        String newPassword = resetRequest.get("password");
        Map<String, String> response = new HashMap<>();
        
        Optional<User> userOpt = userService.getUserByPasswordResetToken(token);
        
        if (userOpt.isPresent() && userService.isPasswordResetTokenValid(userOpt.get())) {
            userService.resetPassword(userOpt.get(), newPassword);        response.put("message", "Password has been reset successfully");
            return ResponseEntity.ok(response);
        } else {
            response.put("message", "Token is invalid or expired");
            return ResponseEntity.badRequest().body(response);
        }
    }    @GetMapping("/stats")
    public ResponseEntity<?> getAccountStats() {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        // Count user's conversations
        Long totalConversations = conversationRepository.countByUser(user);
        
        // Count user's messages
        Long totalMessages = messageRepository.countByConversationUser(user);
          // Create stats DTO
        AccountStatsDto statsDto = new AccountStatsDto();
        statsDto.setTotalConversations(totalConversations);
        statsDto.setTotalMessages(totalMessages);
        statsDto.setAccountStatus("Active");
        
        // Handle null createdAt for existing users
        String memberSince = user.getCreatedAt() != null 
            ? user.getCreatedAt().toString() 
            : "Unknown";
        statsDto.setMemberSince(memberSince);
        
        return ResponseEntity.ok(statsDto);
    }
}