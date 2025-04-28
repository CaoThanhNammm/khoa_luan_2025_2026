package com.chatbot.controller;

import com.chatbot.dto.JwtResponse;
import com.chatbot.dto.LoginRequest;
import com.chatbot.dto.SignupRequest;
import com.chatbot.model.User;
import com.chatbot.repository.UserRepository;
import com.chatbot.security.JwtTokenProvider;
import com.chatbot.service.EmailService;
import com.chatbot.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import javax.mail.MessagingException;
import javax.validation.Valid;
import java.sql.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "http://localhost:3000")
public class AuthController {
    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserService userService;

    @Autowired
    private JwtTokenProvider tokenProvider;
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private EmailService emailService;

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        loginRequest.getUsername(),
                        loginRequest.getPassword()));

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);
        
        User user = userService.findByUsername(loginRequest.getUsername()).orElseThrow();
        
        return ResponseEntity.ok(new JwtResponse(jwt, user.getId(), user.getUsername(), user.getEmail()));
    }

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@Valid @RequestBody SignupRequest signupRequest) {
        Map<String, String> response = new HashMap<>();
        
        if (userService.existsByUsername(signupRequest.getUsername())) {
            response.put("error", "Username is already taken");
            return ResponseEntity.badRequest().body(response);
        }

        if (userService.existsByEmail(signupRequest.getEmail())) {
            response.put("error", "Email is already in use");
            return ResponseEntity.badRequest().body(response);
        }

        User user = userService.registerUser(
                signupRequest.getUsername(),
                signupRequest.getEmail(),
                signupRequest.getPassword());

        response.put("message", "User registered successfully");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<?> forgotPassword(@Valid @RequestBody Map<String, String> request) {
        String email = request.get("email");
        Map<String, String> response = new HashMap<>();
        
        logger.info("Processing forgot password request for email: {}", email);
        
        // Kiểm tra xem email có tồn tại không
        Optional<User> userOptional = userRepository.findByEmail(email);
        if (!userOptional.isPresent()) {
            // Để tránh tiết lộ thông tin, vẫn trả về thành công
            logger.warn("Email not found: {}", email);
            response.put("message", "Nếu email của bạn tồn tại trong hệ thống, chúng tôi đã gửi đường dẫn đặt lại mật khẩu.");
            return ResponseEntity.ok(response);
        }
        
        User user = userOptional.get();
        
        // Tạo token đặt lại mật khẩu 
        String resetToken = UUID.randomUUID().toString();
        
        // Lưu token và thời hạn (24h) vào cơ sở dữ liệu
        user.setPasswordResetToken(resetToken);
        // Thời hạn token là 24 giờ kể từ hiện tại
        user.setPasswordResetTokenExpiry(new Date(System.currentTimeMillis() + 24 * 60 * 60 * 1000));
        userRepository.save(user);
        
        try {
            // Gửi email với link reset password
            logger.info("Sending password reset email to: {}", user.getEmail());
            emailService.sendPasswordResetEmail(user.getEmail(), resetToken);
            logger.info("Password reset email sent successfully");
            
            response.put("message", "Nếu email của bạn tồn tại trong hệ thống, chúng tôi đã gửi đường dẫn đặt lại mật khẩu.");
            
            // Trong môi trường phát triển, trả về thêm thông tin cho việc debug
            response.put("resetLink", "/reset-password?token=" + resetToken);
            response.put("resetToken", resetToken); 
            
            return ResponseEntity.ok(response);
        } catch (MessagingException e) {
            logger.error("Failed to send password reset email", e);
            response.put("message", "Có lỗi xảy ra khi gửi email. Vui lòng thử lại sau.");
            return ResponseEntity.internalServerError().body(response);
        }
    }

    @PostMapping("/reset-password")
    public ResponseEntity<?> resetPassword(@Valid @RequestBody Map<String, String> request) {
        String token = request.get("token");
        String newPassword = request.get("newPassword");
        
        Map<String, String> response = new HashMap<>();
        
        // Tìm người dùng với token
        Optional<User> userOptional = userRepository.findByPasswordResetToken(token);
        if (!userOptional.isPresent()) {
            response.put("message", "Token không hợp lệ hoặc đã hết hạn.");
            return ResponseEntity.badRequest().body(response);
        }
        
        User user = userOptional.get();
        
        // Kiểm tra xem token có hết hạn không
        if (user.getPasswordResetTokenExpiry().before(new Date(System.currentTimeMillis()))) {
            response.put("message", "Token đã hết hạn.");
            return ResponseEntity.badRequest().body(response);
        }
        
        // Cập nhật mật khẩu mới
        user.setPassword(passwordEncoder.encode(newPassword));
        
        // Xóa token
        user.setPasswordResetToken(null);
        user.setPasswordResetTokenExpiry(null);
        
        userRepository.save(user);
        
        response.put("message", "Mật khẩu đã được đặt lại thành công.");
        return ResponseEntity.ok(response);
    }
}