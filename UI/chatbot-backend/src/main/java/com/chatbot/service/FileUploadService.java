package com.chatbot.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

@Service
public class FileUploadService {
    
    private static final Logger logger = LoggerFactory.getLogger(FileUploadService.class);
    
    @Value("${python.api.url}")
    private String pythonApiUrl;
    
    private final WebClient webClient;
    private final ObjectMapper objectMapper;
    
    public FileUploadService() {
        this.webClient = WebClient.builder()
                .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(50 * 1024 * 1024)) // 50MB
                .build();
        this.objectMapper = new ObjectMapper();
    }
    
    public Map<String, Object> uploadFile(MultipartFile file, Long conversationId) throws Exception {
        logger.info("Uploading file to Python API: {} for conversation: {}", file.getOriginalFilename(), conversationId);
        
        try {
            // Prepare multipart form data
            MultiValueMap<String, Object> parts = new LinkedMultiValueMap<>();
            
            // Add file part
            ByteArrayResource fileResource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
            parts.add("file", fileResource);
            
            // Add conversation_id if provided
            if (conversationId != null) {
                parts.add("conversation_id", conversationId.toString());
            }
            
            // Build the API endpoint URL
            String uploadEndpoint = pythonApiUrl + "/upload-file";
            
            logger.info("Sending upload request to: {}", uploadEndpoint);
            
            // Call Python API
            String response = webClient.post()
                    .uri(uploadEndpoint)
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .header("ngrok-skip-browser-warning", "true")
                    .body(BodyInserters.fromMultipartData(parts))
                    .retrieve()
                    .onStatus(status -> !status.is2xxSuccessful(), 
                        clientResponse -> clientResponse.bodyToMono(String.class)
                            .map(errorBody -> {
                                logger.error("Python API error response: {}", errorBody);
                                return new RuntimeException("Python API error: " + errorBody);
                            }))
                    .bodyToMono(String.class)
                    .timeout(Duration.ofMinutes(10)) // Increase timeout for large files
                    .doOnNext(resp -> logger.info("Received response from Python API: {}", resp))
                    .doOnError(error -> logger.error("Error calling Python API: {}", error.getMessage()))
                    .block();
            
            if (response == null) {
                throw new Exception("No response received from Python API");
            }
            
            logger.info("Raw response from Python API: {}", response);
            
            // Parse the response
            JsonNode responseNode = objectMapper.readTree(response);
            logger.info("Parsed JSON response: {}", responseNode.toString());
            
            // Check if the response indicates successful processing
            String status = responseNode.has("status") && !responseNode.get("status").isNull() ? 
                responseNode.get("status").asText() : "";
            
            // Accept success, completed, or processing status
            if (!"success".equalsIgnoreCase(status) && 
                !"completed".equalsIgnoreCase(status) && 
                !"processing".equalsIgnoreCase(status)) {
                String errorMessage = responseNode.has("message") && !responseNode.get("message").isNull() ? 
                    responseNode.get("message").asText() : "Python API did not return a valid status";
                throw new Exception("File processing failed: " + errorMessage + " (Status: " + status + ")");
            }
            
            // Validate that essential fields are present (only for completed processing)
            if ("success".equalsIgnoreCase(status) || "completed".equalsIgnoreCase(status)) {
                if (!responseNode.has("document_id") || responseNode.get("document_id").isNull() || 
                    responseNode.get("document_id").asText().isEmpty()) {
                    throw new Exception("Python API did not return a valid document_id - processing may not be complete");
                }
            }
            
            Map<String, Object> result = new HashMap<>();
            
            // Safely extract fields with null checks
            String message = responseNode.has("message") && !responseNode.get("message").isNull() ? 
                responseNode.get("message").asText() : "File processed successfully";
            result.put("message", message);
            
            // Handle document_id based on processing status
            if (responseNode.has("document_id") && !responseNode.get("document_id").isNull() && 
                !responseNode.get("document_id").asText().isEmpty()) {
                result.put("document_id", responseNode.get("document_id").asText());
            } else {
                // Generate a temporary document_id for processing status
                result.put("document_id", "processing_" + System.currentTimeMillis());
            }
            result.put("filename", responseNode.has("filename") && !responseNode.get("filename").isNull() ? 
                responseNode.get("filename").asText() : file.getOriginalFilename());
            result.put("file_size", responseNode.has("file_size") && !responseNode.get("file_size").isNull() ? 
                responseNode.get("file_size").asLong() : file.getSize());
            result.put("sentences_count", responseNode.has("sentences_count") && !responseNode.get("sentences_count").isNull() ? 
                responseNode.get("sentences_count").asInt() : 0);
            result.put("s3_key", responseNode.has("s3_key") && !responseNode.get("s3_key").isNull() ? 
                responseNode.get("s3_key").asText() : "");
            result.put("s3_url", responseNode.has("s3_url") && !responseNode.get("s3_url").isNull() ? 
                responseNode.get("s3_url").asText() : "");
            result.put("status", status);
            
            // Add conversation_id if present in response
            if (responseNode.has("conversation_id") && !responseNode.get("conversation_id").isNull()) {
                result.put("conversation_id", responseNode.get("conversation_id").asLong());
            } else if (conversationId != null) {
                result.put("conversation_id", conversationId);
            }
            
            logger.info("File uploaded successfully. Document ID: {}", result.get("document_id"));
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error uploading file to Python API", e);
            throw new Exception("Failed to upload file: " + e.getMessage(), e);
        }
    }
    
    public Map<String, Object> getDocuments() throws Exception {
        logger.info("Getting documents list from Python API");
        
        try {
            // For now, return a mock response since we don't have a list documents endpoint
            // You can implement this endpoint in Python API later
            Map<String, Object> result = new HashMap<>();
            result.put("message", "Documents list retrieved successfully");
            result.put("documents", new HashMap<>());
            
            return result;
            
        } catch (Exception e) {
            logger.error("Error getting documents from Python API", e);
            throw new Exception("Failed to get documents: " + e.getMessage(), e);
        }
    }
}
