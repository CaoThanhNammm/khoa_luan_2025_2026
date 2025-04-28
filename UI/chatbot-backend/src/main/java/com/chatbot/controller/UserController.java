package com.chatbot.controller;

import com.chatbot.model.User;
import com.chatbot.repository.UserRepository;
import com.chatbot.security.CustomUserDetailsService;
import com.chatbot.service.EmailService;
import com.chatbot.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
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
@CrossOrigin(origins = "http://localhost:3000")
public class UserController {

    @Autowired
    private UserService userService;
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private CustomUserDetailsService userDetailsService;

    @GetMapping("/profile")
    public ResponseEntity<?> getCurrentUserProfile() {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        // Don't send password in response
        user.setPassword(null);
        
        return ResponseEntity.ok(user);
    }
    
    @PutMapping("/profile")
    public ResponseEntity<?> updateProfile(@Valid @RequestBody Map<String, String> profileData) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        String newUsername = profileData.get("username");
        String newEmail = profileData.get("email");
        
        // Check if username already exists (if changed)
        if (!user.getUsername().equals(newUsername) && userService.existsByUsername(newUsername)) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "Username is already taken");
            return ResponseEntity.badRequest().body(response);
        }
        
        // Check if email already exists (if changed)
        if (!user.getEmail().equals(newEmail) && userService.existsByEmail(newEmail)) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "Email is already in use");
            return ResponseEntity.badRequest().body(response);
        }
        
        // Update user profile
        user.setUsername(newUsername);
        user.setEmail(newEmail);
        userRepository.save(user);
        
        Map<String, String> response = new HashMap<>();
        response.put("message", "Profile updated successfully");
        return ResponseEntity.ok(response);
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
    
    @PutMapping("/settings")
    public ResponseEntity<?> updateSettings(@Valid @RequestBody Map<String, Object> settingsData) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        User user = userService.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        
        // We can add user settings (preferences) to the database in the future if needed
        // For now, we'll just acknowledge the request as the settings are stored in localStorage
        
        Map<String, String> response = new HashMap<>();
        response.put("message", "Settings updated successfully");
        return ResponseEntity.ok(response);
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
            userService.resetPassword(userOpt.get(), newPassword);
            response.put("message", "Password has been reset successfully");
            return ResponseEntity.ok(response);
        } else {
            response.put("message", "Token is invalid or expired");
            return ResponseEntity.badRequest().body(response);
        }
    }
}