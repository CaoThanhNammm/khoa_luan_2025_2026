---
description: Repository Information Overview
alwaysApply: true
---

# Repository Information Overview

## Repository Summary
This repository contains a chatbot application with a React frontend and FastAPI backend. The system is designed to provide an AI-powered chat interface with document processing capabilities, user authentication, and conversation management.

## Repository Structure
- **chatbot-frontend**: React-based UI with TypeScript and TailwindCSS
- **chat-backend**: Python FastAPI backend with multiple components:
  - **be**: Main FastAPI application
  - **LLM**: Large Language Model integration
  - **ModelLLM**: Model embedding and interaction components
  - **PreProcessing**: Document processing utilities
  - **VectorDatabase**: Vector database integration for semantic search
  - **knowledge_graph**: Knowledge graph implementation

## Projects

### Chatbot Frontend
**Configuration File**: package.json

#### Language & Runtime
**Language**: TypeScript
**Version**: TypeScript ~5.8.3
**Build System**: Vite 6.3.5
**Package Manager**: npm

#### Dependencies
**Main Dependencies**:
- React 19.1.0
- React Router DOM 7.6.1
- Axios 1.9.0
- Framer Motion 12.15.0
- PrismJS 1.30.0

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

### Chat Backend
**Configuration File**: requirements.txt

#### Language & Runtime
**Language**: Python
**Version**: Python 3.8+
**Package Manager**: pip

#### Dependencies
**Main Dependencies**:
- FastAPI 0.104.1
- Uvicorn 0.24.0
- SQLAlchemy 2.0.23
- Pydantic 2.4.2
- Neo4j 5.14.0
- Langchain-core 0.1.4
- Google-generativeai
- Torch
- Sentence_transformers
- Qdrant-client

#### Build & Installation
```bash
cd chat-backend/be
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python main.py
```

#### Database
**Type**: MySQL
**ORM**: SQLAlchemy
**Setup**: Automatic creation of tables on startup
**Additional Storage**:
- Neo4j for knowledge graph
- Qdrant for vector database
- AWS S3 for document storage

#### External Services
- Local LLM API for chat functionality
- AWS S3 for document storage
- Email service for password reset

### Architecture

#### Frontend Architecture
- **React + TypeScript**: Core UI framework
- **TailwindCSS**: Styling
- **React Router**: Navigation
- **Context API**: State management
- **Axios**: API communication

#### Backend Architecture
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **LLM Integration**: Multiple model support
- **Vector Database**: Semantic search
- **Knowledge Graph**: Neo4j-based graph database