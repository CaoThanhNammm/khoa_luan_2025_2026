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
                    .bodyToMono(String.class)
                    .timeout(Duration.ofMinutes(10)) // Increase timeout for large files
                    .doOnNext(resp -> logger.info("Received response from Python API: {}", resp))
                    .block();
            
            if (response == null) {
                throw new Exception("No response received from Python API");
            }
            
            // Parse the response
            JsonNode responseNode = objectMapper.readTree(response);
            
            Map<String, Object> result = new HashMap<>();
            result.put("message", responseNode.get("message").asText());
            result.put("document_id", responseNode.get("document_id").asText());
            result.put("filename", responseNode.get("filename").asText());
            result.put("file_size", responseNode.get("file_size").asLong());
            result.put("sentences_count", responseNode.get("sentences_count").asInt());
            result.put("s3_key", responseNode.get("s3_key").asText());
            result.put("s3_url", responseNode.get("s3_url").asText());
            result.put("status", responseNode.get("status").asText());
            
            // Add conversation_id if present in response
            if (responseNode.has("conversation_id") && !responseNode.get("conversation_id").isNull()) {
                result.put("conversation_id", responseNode.get("conversation_id").asLong());
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
