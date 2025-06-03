package com.chatbot.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;

@Service
public class EmailService {

    private static final Logger logger = LoggerFactory.getLogger(EmailService.class);

    @Autowired
    private JavaMailSender mailSender;

    @Value("${spring.mail.username}")
    private String fromEmail;

    @Value("${app.url}")
    private String appUrl;

    public void sendPasswordResetEmail(String to, String token) throws MessagingException {
        logger.info("Preparing to send password reset email to: {}", to);
        
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            
            helper.setFrom(fromEmail);
            helper.setTo(to);
            helper.setSubject("Password Reset Request");
            
            String resetUrl = appUrl + "/reset-password?token=" + token;
            logger.info("Reset URL: {}", resetUrl);
            
            String emailContent = 
                "<div style='font-family: Arial, sans-serif; padding: 20px;'>" +
                "<h2 style='color: #333;'>Password Reset Request</h2>" +
                "<p>You've requested to reset your password. Please click the link below to set a new password:</p>" +
                "<p><a href='" + resetUrl + "' style='background-color: #4CAF50; color: white; padding: 10px 15px; " +
                "text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;'>" +
                "Reset Password</a></p>" +
                "<p>If you didn't request a password reset, please ignore this email.</p>" +
                "<p>The link will expire in 24 hours.</p>" +
                "<p>Best regards,<br>Chatbot Support Team</p>" +
                "</div>";
            
            helper.setText(emailContent, true);
            logger.info("Email content prepared, sending email...");
              mailSender.send(message);
            logger.info("Password reset email sent successfully to: {}", to);
        } catch (Exception e) {
            logger.error("Failed to send email: {}", e.getMessage(), e);
            throw new MessagingException("Failed to send email: " + e.getMessage(), e);
        }
    }
    
    public void sendSimpleMessage(String to, String subject, String text) {
        logger.info("Preparing to send simple email to: {} with subject: {}", to, subject);
        
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            
            helper.setFrom(fromEmail);
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(text, false); // false means plain text
            
            mailSender.send(message);
            logger.info("Simple email sent successfully to: {}", to);
        } catch (Exception e) {
            logger.error("Failed to send simple email: {}", e.getMessage(), e);
            // Don't throw exception to avoid breaking the contact form submission
        }
    }
}
