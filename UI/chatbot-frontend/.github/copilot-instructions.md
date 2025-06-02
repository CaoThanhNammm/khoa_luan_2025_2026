# NLU ChatBot Frontend - Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a modern, elegant European-style chatbot UI built with Vite + React + TypeScript + TailwindCSS. The application is designed with minimalist aesthetics inspired by Claude (Anthropic).

## Tech Stack
- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS with custom European design system
- **Routing**: React Router DOM
- **Icons**: React Icons (BiXxx icons)
- **HTTP Client**: Axios
- **State Management**: React Context API

## Design System
- **Color Palette**:
  - Neutrals: white, off-white (#fefbff), beige (#f6f3eb), charcoal (#111827)
  - Accents: pastel lavender (#d6ccf2), sky blue (#c3e0f0)
- **Typography**:
  - Headings: Playfair Display (font-heading)
  - Body: Inter/Lato (font-body)
- **Style**: European minimalism with clean lines and subtle shadows

## Architecture
- **Pages**: Home (/), Login (/login), Register (/register), Chat (/chat)
- **Components**: Layout, Navbar
- **Context**: AuthContext for authentication state
- **Responsive**: Mobile-first design with TailwindCSS

## Key Features
- User authentication (login/register)
- Real-time chat interface with typing indicators
- European minimalist design
- Accessibility features (semantic HTML, keyboard navigation, focus states)
- Backend API integration ready (currently using mock responses)

## API Integration Notes
The chat functionality is currently using mock responses. To integrate with your backend:
1. Replace the mock `generateBotResponse` function in ChatPage.tsx
2. Update the API endpoint in the axios call
3. Configure proper error handling
4. Add authentication headers as needed

## Custom CSS Classes
- `.btn-primary`: Primary button styling
- `.btn-secondary`: Secondary button styling  
- `.input-field`: Input field styling
- `.chat-message`: Base chat message styling
- `.chat-message-user`: User message styling
- `.chat-message-bot`: Bot message styling
