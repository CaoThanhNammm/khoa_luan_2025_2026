# NLU ChatBot - Frontend

A modern, elegant European-style chatbot UI built with Vite + React + TypeScript + TailwindCSS. Inspired by Claude's minimalist design, this application provides a beautiful and intuitive interface for AI conversations.

## ✨ Features

- **🎨 European Minimalist Design**: Clean, elegant interface inspired by Claude
- **🔐 User Authentication**: Login and registration system
- **💬 Real-time Chat**: Interactive chat interface with typing indicators
- **📱 Responsive Design**: Mobile-first, works on all devices
- **♿ Accessible**: Semantic HTML, keyboard navigation, focus states
- **🎯 TypeScript**: Full type safety throughout the application

## 🛠 Tech Stack

- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Routing**: React Router DOM
- **Icons**: React Icons
- **HTTP Client**: Axios
- **State Management**: React Context API

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## 🔌 Backend Integration

The chat functionality is currently using mock responses. To integrate with your backend, update the API endpoints in `ChatPage.tsx` and `AuthContext.tsx`.

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
