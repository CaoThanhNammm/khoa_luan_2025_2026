---
description: Repository Information Overview
alwaysApply: true
---

# Repository Information Overview

## Repository Summary
This repository contains a chatbot application with multiple components: a React-based frontend, a Java Spring Boot backend, and a Python-based backend (backup). The system appears to be a conversational AI application with knowledge graph capabilities, vector database integration, and multiple LLM integrations.

## Repository Structure
- **chatbot-frontend**: React-based UI for the chatbot application
- **chatbot-backend**: Java Spring Boot backend with authentication system
- **chat-backend-backup**: Python-based backend with LLM integration and knowledge graph capabilities

## Projects

### Chatbot Frontend
**Configuration File**: package.json

#### Language & Runtime
**Language**: TypeScript/JavaScript
**Version**: TypeScript ~5.8.3
**Build System**: Vite 6.3.5
**Package Manager**: npm

#### Dependencies
**Main Dependencies**:
- React 19.1.0
- React DOM 19.1.0
- React Router DOM 7.6.1
- Axios 1.9.0
- Framer Motion 12.15.0
- Prismjs 1.30.0

**Development Dependencies**:
- Vite 6.3.5
- TypeScript 5.8.3
- TailwindCSS 3.4.17
- ESLint 9.25.0

#### Build & Installation
```bash
npm install
npm run dev    # Development server
npm run build  # Production build
```

### Chatbot Backend (Java)
**Configuration File**: pom.xml

#### Language & Runtime
**Language**: Java
**Version**: Java 17
**Build System**: Maven
**Framework**: Spring Boot 2.7.12

#### Dependencies
**Main Dependencies**:
- Spring Boot Web
- Spring Boot Data JPA
- Spring Boot Security
- JWT (jsonwebtoken 0.11.5)
- MySQL Connector 8.0.28
- Spring Boot WebFlux
- Spring Boot Mail
- Thymeleaf

**Development Dependencies**:
- Spring Boot Test
- Spring Security Test
- Lombok 1.18.30

#### Build & Installation
```bash
mvn clean install
mvn spring-boot:run
```

### Chat Backend Backup (Python)
**Main File**: Chat.py

#### Language & Runtime
**Language**: Python
**Framework**: Custom implementation with LLM integrations

#### Dependencies
**Main Dependencies**:
- torch/torch_geometric
- langchain_core
- dotenv
- Various LLM APIs (Gemini, Llama)

#### Key Components
**Main Modules**:
- LLM: Integration with Gemini and Llama models
- VectorDatabase: Qdrant integration for vector storage
- knowledge_graph: Neo4j integration and graph processing
- PreProcessing: Document and text processing utilities
- ModelLLM: Embedding and model interaction components

#### Usage & Operations
```bash
# No explicit build commands found
# Likely executed directly with Python interpreter
python Chat.py
```

#### Key Features
- Multi-step reasoning (S2S) for question answering
- Knowledge graph integration with Neo4j
- Vector database retrieval with Qdrant
- Multiple LLM model integration (Gemini, Llama)
- Document processing and chunking capabilities