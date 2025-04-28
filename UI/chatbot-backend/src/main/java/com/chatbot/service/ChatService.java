package com.chatbot.service;

import com.chatbot.dto.ConversationDto;
import com.chatbot.dto.MessageDto;
import com.chatbot.model.Conversation;
import com.chatbot.model.Message;
import com.chatbot.model.User;
import com.chatbot.repository.ConversationRepository;
import com.chatbot.repository.MessageRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class ChatService {
    private static final Logger logger = LoggerFactory.getLogger(ChatService.class);

    @Autowired
    private ConversationRepository conversationRepository;

    @Autowired
    private MessageRepository messageRepository;

    @Autowired
    private UserService userService;

    @Value("${gemini.api.url}")
    private String geminiApiUrl;
    
    @Value("${gemini.api.key}")
    private String geminiApiKey;

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    public ChatService() {
        this.webClient = WebClient.builder().build();
        this.objectMapper = new ObjectMapper();
    }

    public List<ConversationDto> getUserConversations(Long userId) {
        User user = userService.getUserById(userId);
        List<Conversation> conversations = conversationRepository.findByUserOrderByCreatedAtDesc(user);
        
        return conversations.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    public ConversationDto getConversation(Long conversationId) {
        Conversation conversation = conversationRepository.findById(conversationId).orElse(null);
        if (conversation == null) {
            return null;
        }
        
        return convertToDto(conversation);
    }

    @Transactional
    public ConversationDto startNewConversation(Long userId, String userMessage) {
        User user = userService.getUserById(userId);
        
        // Create new conversation
        Conversation conversation = new Conversation();
        conversation.setTitle(generateTitle(userMessage));
        conversation.setUser(user);
        conversation.setCreatedAt(LocalDateTime.now());
        conversation = conversationRepository.save(conversation);
        
        // Add user message
        Message userMessageEntity = new Message();
        userMessageEntity.setContent(userMessage);
        userMessageEntity.setType(Message.MessageType.USER);
        userMessageEntity.setConversation(conversation);
        userMessageEntity = messageRepository.save(userMessageEntity);
        
        // Get bot response from external API
        String botResponse = getChatbotResponse(userMessage);
        
        // Add bot response
        Message botMessageEntity = new Message();
        botMessageEntity.setContent(botResponse);
        botMessageEntity.setType(Message.MessageType.BOT);
        botMessageEntity.setConversation(conversation);
        botMessageEntity = messageRepository.save(botMessageEntity);
        
        // Return conversation with messages
        conversation.setMessages(List.of(userMessageEntity, botMessageEntity));
        
        return convertToDto(conversation);
    }

    @Transactional
    public MessageDto sendMessage(Long conversationId, String userMessage, Long userId) {
        Conversation conversation = conversationRepository.findById(conversationId).orElse(null);
        
        if (conversation == null || !conversation.getUser().getId().equals(userId)) {
            return null;
        }
        
        // Add user message
        Message userMessageEntity = new Message();
        userMessageEntity.setContent(userMessage);
        userMessageEntity.setType(Message.MessageType.USER);
        userMessageEntity.setConversation(conversation);
        userMessageEntity = messageRepository.save(userMessageEntity);
        
        // Get bot response from external API
        String botResponse = getChatbotResponse(userMessage);
        
        // Add bot response
        Message botMessageEntity = new Message();
        botMessageEntity.setContent(botResponse);
        botMessageEntity.setType(Message.MessageType.BOT);
        botMessageEntity.setConversation(conversation);
        botMessageEntity = messageRepository.save(botMessageEntity);
        
        return convertToMessageDto(botMessageEntity);
    }
    
    @Transactional
    public boolean deleteConversation(Long conversationId, Long userId) {
        Conversation conversation = conversationRepository.findById(conversationId).orElse(null);
        
        // Check if conversation exists and belongs to the user
        if (conversation == null || !conversation.getUser().getId().equals(userId)) {
            return false;
        }
        
        // Delete the conversation
        conversationRepository.delete(conversation);
        
        return true;
    }
    
    private String getChatbotResponse(String userMessage) {
        try {
            logger.info("Preparing request to Gemini API for message: {}", userMessage);
            
            // Create Gemini API request payload according to the API documentation
            Map<String, Object> requestBody = new HashMap<>();
            
            // Format message in proper Gemini 1.5 format
            Map<String, Object> textPart = new HashMap<>();
            textPart.put("text", userMessage);
            
            List<Map<String, Object>> parts = new ArrayList<>();
            parts.add(textPart);
            
            Map<String, Object> content = new HashMap<>();
            content.put("parts", parts);
            
            requestBody.put("contents", List.of(content));
            
            // Add configuration parameters
            Map<String, Object> generationConfig = new HashMap<>();
            generationConfig.put("temperature", 0.7);
            generationConfig.put("maxOutputTokens", 1024);
            requestBody.put("generationConfig", generationConfig);
            
            // For debugging - log the request
            logger.info("Sending request to Gemini API: {}", objectMapper.writeValueAsString(requestBody));
            
            // Build the full URL with API key
            String fullUrl = geminiApiUrl + "?key=" + geminiApiKey;
            logger.info("Calling Gemini API at: {}", fullUrl.replaceAll(geminiApiKey, "API_KEY_HIDDEN"));
            
            try {
                // Call Gemini API with API key in query parameter
                String response = webClient.post()
                        .uri(fullUrl)
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(requestBody)
                        .retrieve()
                        .bodyToMono(String.class)
                        .doOnNext(resp -> logger.info("Received response from Gemini: {}", resp))
                        .flatMap(rawResponse -> {
                            try {
                                // Parse the JSON response
                                JsonNode rootNode = objectMapper.readTree(rawResponse);
                                
                                // Navigate the response structure
                                if (rootNode.has("candidates") && rootNode.get("candidates").size() > 0) {
                                    JsonNode candidate = rootNode.get("candidates").get(0);
                                    if (candidate.has("content") && candidate.get("content").has("parts")) {
                                        JsonNode parts1 = candidate.get("content").get("parts");
                                        if (parts1.size() > 0 && parts1.get(0).has("text")) {
                                            return Mono.just(parts1.get(0).get("text").asText());
                                        }
                                    }
                                }
                                
                                logger.warn("Could not parse Gemini API response: {}", rawResponse);
                                return Mono.just(getSimulatedResponse(userMessage));
                            } catch (Exception e) {
                                logger.error("Error parsing Gemini API response", e);
                                return Mono.just(getSimulatedResponse(userMessage));
                            }
                        })
                        .onErrorResume(e -> {
                            logger.error("Error calling Gemini API: {}", e.getMessage());
                            return Mono.just(getSimulatedResponse(userMessage));
                        })
                        .block();
                        
                return response != null ? response : getSimulatedResponse(userMessage);
            } catch (Exception e) {
                logger.error("Exception in Gemini API call: {}", e.getMessage());
                return getSimulatedResponse(userMessage);
            }
        } catch (Exception e) {
            logger.error("Exception in getChatbotResponse", e);
            return getSimulatedResponse(userMessage);
        }
    }

    /**
     * Generate a simulated response if Gemini API is unavailable or fails
     */
    private String getSimulatedResponse(String userMessage) {
        logger.info("Falling back to simulated response for: {}", userMessage);
        
        String lowerCase = userMessage.toLowerCase();
        if (lowerCase.contains("hello") || lowerCase.contains("hi") || lowerCase.contains("hey")) {
            return "Hello! How can I help you today?";
        } else if (lowerCase.contains("how are you")) {
            return "I'm doing well, thank you for asking! How can I assist you today?";
        } else if (lowerCase.contains("name") && lowerCase.contains("your")) {
            return "I'm Gemini, your AI assistant. How can I help you?";
        } else if (lowerCase.contains("thank")) {
            return "You're welcome! Is there anything else I can help you with?";
        } else if (lowerCase.contains("bye") || lowerCase.contains("goodbye")) {
            return "Goodbye! Feel free to come back if you have more questions.";
        } else if (lowerCase.contains("help")) {
            return "I'm here to help! You can ask me questions about various topics, and I'll do my best to assist you.";
        } else if (lowerCase.contains("weather")) {
            return "I don't have access to real-time weather data at the moment, but I'd be happy to discuss other topics with you.";
        } else if (lowerCase.contains("time") || lowerCase.contains("date")) {
            return "I don't have access to the current time or date. Is there something else I can help you with?";
        } else if (lowerCase.contains("joke") || lowerCase.contains("funny")) {
            return "Why don't scientists trust atoms? Because they make up everything! Is there anything I can actually help you with today?";
        } else if (lowerCase.contains("who created you") || lowerCase.contains("who made you")) {
            return "I was created by a team of developers who wanted to build a helpful AI assistant. How can I assist you today?";
        } else if (lowerCase.contains("what can you do") || lowerCase.contains("capabilities")) {
            return "I can assist with answering questions, providing information, and engaging in conversation on a wide range of topics. What would you like to know?";
        } else if (lowerCase.contains("language") && lowerCase.contains("speak")) {
            return "I primarily communicate in English, but I'm designed to be helpful to users around the world.";
        } else if (lowerCase.contains("smart") || lowerCase.contains("intelligent")) {
            return "I'm designed to be helpful and informative, though I'm always learning and improving. What can I help you with today?";
        } else {
            return "I'd like to provide more information on that, but I'm currently operating in a simplified mode. Can I help you with something else in the meantime?";
        }
    }
    
    private String generateTitle(String message) {
        // Generate a title based on the first message
        if (message.length() <= 30) {
            return message;
        }
        return message.substring(0, 27) + "...";
    }
    
    private ConversationDto convertToDto(Conversation conversation) {
        ConversationDto dto = new ConversationDto();
        dto.setId(conversation.getId());
        dto.setTitle(conversation.getTitle());
        dto.setCreatedAt(conversation.getCreatedAt());
        
        List<Message> messages = messageRepository.findByConversationOrderByTimestampAsc(conversation);
        dto.setMessages(messages.stream()
                .map(this::convertToMessageDto)
                .collect(Collectors.toList()));
                
        return dto;
    }
    
    private MessageDto convertToMessageDto(Message message) {
        MessageDto dto = new MessageDto();
        dto.setId(message.getId());
        dto.setContent(message.getContent());
        dto.setType(message.getType());
        dto.setTimestamp(message.getTimestamp());
        dto.setConversationId(message.getConversation().getId());
        return dto;
    }
}