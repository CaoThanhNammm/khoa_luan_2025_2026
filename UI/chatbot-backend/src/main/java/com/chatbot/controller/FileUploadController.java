package com.chatbot.controller;

import com.chatbot.model.UserDocument;
import com.chatbot.service.FileUploadService;
import com.chatbot.service.UserDocumentService;
import com.chatbot.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = {"http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"})
public class FileUploadController {
    
    private static final Logger logger = LoggerFactory.getLogger(FileUploadController.class);
    
    @Autowired
    private FileUploadService fileUploadService;
    
    @Autowired
    private UserDocumentService userDocumentService;
    
    @Autowired
    private UserService userService;
    
    @PostMapping("/upload-file")
    public ResponseEntity<Map<String, Object>> uploadFile(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "conversation_id", required = false) Long conversationId) {
        logger.info("Received file upload request: {} for conversation: {}", file.getOriginalFilename(), conversationId);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Validate file
            if (file.isEmpty()) {
                response.put("success", false);
                response.put("message", "Không có file được upload");
                return ResponseEntity.badRequest().body(response);
            }
            
            // Check file size (10MB = 10 * 1024 * 1024 bytes)
            long maxFileSize = 10 * 1024 * 1024;
            if (file.getSize() > maxFileSize) {
                response.put("success", false);
                response.put("message", String.format("File quá lớn. Kích thước tối đa: 10MB. Kích thước hiện tại: %.2fMB", 
                    file.getSize() / (1024.0 * 1024.0)));
                return ResponseEntity.badRequest().body(response);
            }
            
            // Check file type
            String filename = file.getOriginalFilename();
            if (filename == null || !filename.toLowerCase().endsWith(".pdf")) {
                response.put("success", false);
                response.put("message", "Chỉ chấp nhận file PDF (.pdf)");
                return ResponseEntity.badRequest().body(response);
            }
            
            // Get current user ID (if authenticated)
            Long userId = getCurrentUserId();
            
            // Upload file via service
            Map<String, Object> uploadResult = fileUploadService.uploadFile(file, conversationId);
            
            // Save document info to database if user is authenticated
            if (userId != null && uploadResult.containsKey("document_id")) {
                String documentId = (String) uploadResult.get("document_id");
                UserDocument savedDocument = userDocumentService.saveDocument(userId, conversationId, documentId, filename, uploadResult);
                logger.info("Saved document to database: {} for conversation: {}", savedDocument.getId(), conversationId);
            }
            
            // Merge upload result with response
            response.put("success", true);
            response.put("message", "Upload thành công");
            
            // Add all fields from uploadResult directly to response
            response.putAll(uploadResult);
            
            // Ensure required fields are present with fallback values
            if (!response.containsKey("filename") || response.get("filename") == null || response.get("filename").toString().isEmpty()) {
                response.put("filename", filename);
            }
            if (!response.containsKey("file_size") || response.get("file_size") == null) {
                response.put("file_size", file.getSize());
            }
            if (!response.containsKey("document_id") || response.get("document_id") == null || response.get("document_id").toString().isEmpty()) {
                response.put("document_id", "doc_" + System.currentTimeMillis());
            }
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("Error uploading file: {}", e.getMessage(), e);
            response.put("success", false);
            
            // Provide more specific error messages
            String errorMessage = e.getMessage();
            if (errorMessage.contains("timeout") || errorMessage.contains("Timeout")) {
                response.put("message", "File processing timed out. Please try again with a smaller file or check your connection.");
            } else if (errorMessage.contains("connection") || errorMessage.contains("Connection")) {
                response.put("message", "Unable to connect to processing server. Please try again later.");
            } else if (errorMessage.contains("processing failed") || errorMessage.contains("did not return success")) {
                response.put("message", "File processing failed on server. Please check the file format and try again.");
            } else {
                response.put("message", "Lỗi khi upload file: " + errorMessage);
            }
            
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    @DeleteMapping("/documents/{documentId}")
    public ResponseEntity<Map<String, Object>> deleteDocument(@PathVariable String documentId) {
        logger.info("Received request to delete document: {}", documentId);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            Long userId = getCurrentUserId();
            if (userId == null) {
                response.put("success", false);
                response.put("message", "Cần đăng nhập để xóa tài liệu");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
            }
            
            boolean deleted = userDocumentService.deleteDocument(userId, documentId);
            
            if (deleted) {
                response.put("success", true);
                response.put("message", "Xóa tài liệu thành công");
            } else {
                response.put("success", false);
                response.put("message", "Không tìm thấy tài liệu hoặc bạn không có quyền xóa");
            }
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("Error deleting document", e);
            response.put("success", false);
            response.put("message", "Lỗi khi xóa tài liệu: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    private Long getCurrentUserId() {
        try {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            if (authentication != null && authentication.isAuthenticated() && 
                !authentication.getName().equals("anonymousUser")) {
                String username = authentication.getName();
                return userService.findByUsername(username)
                    .map(user -> user.getId())
                    .orElse(null);
            }
        } catch (Exception e) {
            logger.debug("Could not get current user ID: {}", e.getMessage());
        }
        return null;
    }
    
    @GetMapping("/documents")
    public ResponseEntity<Map<String, Object>> getDocuments(
            @RequestParam(value = "conversation_id", required = false) Long conversationId) {
        logger.info("Received request to get documents list for conversation: {}", conversationId);
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            Long userId = getCurrentUserId();
            if (userId == null) {
                response.put("success", false);
                response.put("message", "Cần đăng nhập để xem danh sách tài liệu");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
            }
            
            List<UserDocument> documents;
            if (conversationId != null) {
                documents = userDocumentService.getDocumentsByConversation(userId, conversationId);
            } else {
                documents = userDocumentService.getUserDocuments(userId);
            }
            
            response.put("success", true);
            response.put("message", "Lấy danh sách tài liệu thành công");
            response.put("data", documents);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("Error getting documents", e);
            response.put("success", false);
            response.put("message", "Lỗi khi lấy danh sách tài liệu: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
}
