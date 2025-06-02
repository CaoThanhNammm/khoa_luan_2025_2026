package com.chatbot.repository;

import com.chatbot.model.Conversation;
import com.chatbot.model.Message;
import com.chatbot.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MessageRepository extends JpaRepository<Message, Long> {
    List<Message> findByConversationOrderByTimestampAsc(Conversation conversation);
    
    @Query("SELECT COUNT(m) FROM Message m WHERE m.conversation.user = :user")
    Long countByConversationUser(@Param("user") User user);
}