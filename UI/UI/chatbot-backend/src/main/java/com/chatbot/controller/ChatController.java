package com.chatbot.controller;

import com.chatbot.dto.ConversationDto;
import com.chatbot.dto.MessageDto;
import com.chatbot.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:5173"})
public class ChatController {

    @Autowired
    private ChatService chatService;

    @Autowired
    private com.chatbot.service.UserService userService;

    @GetMapping("/conversations")
    public ResponseEntity<List<ConversationDto>> getConversations(Authentication authentication) {
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        Long userId = userService.findByUsername(userDetails.getUsername()).orElseThrow().getId();
        
        List<ConversationDto> conversations = chatService.getUserConversations(userId);
        return ResponseEntity.ok(conversations);
    }

    @GetMapping("/conversations/{id}")
    public ResponseEntity<?> getConversation(@PathVariable Long id, Authentication authentication) {
        ConversationDto conversation = chatService.getConversation(id);
        if (conversation == null) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Conversation not found");
            return ResponseEntity.notFound().build();
        }
        
        return ResponseEntity.ok(conversation);
    }

    @PostMapping("/conversations")
    public ResponseEntity<ConversationDto> startConversation(@RequestBody Map<String, String> payload, 
                                                   Authentication authentication) {
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        Long userId = userService.findByUsername(userDetails.getUsername()).orElseThrow().getId();
        
        String message = payload.get("message");
        ConversationDto newConversation = chatService.startNewConversation(userId, message);
        
        return ResponseEntity.ok(newConversation);
    }

    @PostMapping("/conversations/{id}/messages")
    public ResponseEntity<MessageDto> sendMessage(@PathVariable Long id, 
                                     @RequestBody Map<String, String> payload,
                                     Authentication authentication) {
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        Long userId = userService.findByUsername(userDetails.getUsername()).orElseThrow().getId();
        
        String message = payload.get("message");
        MessageDto response = chatService.sendMessage(id, message, userId);
        
        if (response == null) {
            return ResponseEntity.notFound().build();
        }
        
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/conversations/{id}")
    public ResponseEntity<?> deleteConversation(@PathVariable Long id, Authentication authentication) {
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        Long userId = userService.findByUsername(userDetails.getUsername()).orElseThrow().getId();
        
        boolean deleted = chatService.deleteConversation(id, userId);
        
        if (!deleted) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Conversation not found or access denied");
            return ResponseEntity.notFound().build();
        }
        
        Map<String, String> response = new HashMap<>();
        response.put("message", "Conversation deleted successfully");
        return ResponseEntity.ok(response);
    }
}