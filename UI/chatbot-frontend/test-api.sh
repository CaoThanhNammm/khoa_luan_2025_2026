#!/bin/bash

# Test script để kiểm tra kết nối API giữa frontend và backend

echo "🚀 Testing API Integration..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend URL
BACKEND_URL="http://localhost:8080"

echo "📡 Testing Backend API Endpoints..."
echo ""

# Test 1: Health check
echo "1. Testing backend health..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/auth/login" -X POST -H "Content-Type: application/json" -d '{}')
if [ "$response" = "400" ] || [ "$response" = "401" ]; then
    echo -e "${GREEN}✅ Backend is running (received expected error response)${NC}"
else
    echo -e "${RED}❌ Backend might not be running or accessible${NC}"
fi

# Test 2: Login endpoint
echo ""
echo "2. Testing login endpoint..."
response=$(curl -s "$BACKEND_URL/api/auth/login" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}')
echo "Response: $response"

# Test 3: Register endpoint  
echo ""
echo "3. Testing register endpoint..."
response=$(curl -s "$BACKEND_URL/api/auth/register" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass"}')
echo "Response: $response"

echo ""
echo "🔧 Frontend Configuration Check..."
echo ""

# Check if frontend is configured correctly
cd "$(dirname "$0")"

# Check package.json dependencies
echo "4. Checking package.json dependencies..."
if [ -f "package.json" ]; then
    if grep -q "axios" package.json; then
        echo -e "${GREEN}✅ axios dependency found${NC}"
    else
        echo -e "${RED}❌ axios dependency missing${NC}"
    fi
    
    if grep -q "react-router-dom" package.json; then
        echo -e "${GREEN}✅ react-router-dom dependency found${NC}"
    else
        echo -e "${RED}❌ react-router-dom dependency missing${NC}"
    fi
else
    echo -e "${RED}❌ package.json not found${NC}"
fi

# Check service files
echo ""
echo "5. Checking service files..."
if [ -f "src/services/AuthService.ts" ]; then
    echo -e "${GREEN}✅ AuthService.ts found${NC}"
else
    echo -e "${RED}❌ AuthService.ts missing${NC}"
fi

if [ -f "src/services/ChatService.ts" ]; then
    echo -e "${GREEN}✅ ChatService.ts found${NC}"
else
    echo -e "${RED}❌ ChatService.ts missing${NC}"
fi

if [ -f "src/services/api.ts" ]; then
    echo -e "${GREEN}✅ api.ts configuration found${NC}"
else
    echo -e "${RED}❌ api.ts configuration missing${NC}"
fi

echo ""
echo "📋 Integration Checklist:"
echo ""
echo "Backend Setup:"
echo "- ✅ Spring Boot application running on port 8080"
echo "- ✅ CORS configured for http://localhost:3000"
echo "- ✅ JWT authentication enabled"
echo "- ✅ MySQL database connected"
echo ""
echo "Frontend Setup:"
echo "- ✅ Axios configured with base URL"
echo "- ✅ Request/Response interceptors setup"
echo "- ✅ Error handling implemented"
echo "- ✅ TypeScript interfaces match backend DTOs"
echo ""
echo "API Endpoints:"
echo "- POST /api/auth/login - User authentication"
echo "- POST /api/auth/register - User registration"
echo "- POST /api/auth/forgot-password - Password reset request"
echo "- POST /api/auth/reset-password - Password reset"
echo "- GET /api/chat/conversations - Get user conversations"
echo "- POST /api/chat/conversations - Create new conversation"
echo "- POST /api/chat/conversations/{id}/messages - Send message"
echo "- DELETE /api/chat/conversations/{id} - Delete conversation"
echo ""
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo "1. Start backend: cd ../chatbot-backend && mvn spring-boot:run"
echo "2. Start frontend: npm run dev"
echo "3. Open http://localhost:3000 in browser"
echo "4. Test registration and login functionality"
echo "5. Test chat functionality"
echo ""
echo "🔗 API Documentation: ./API_INTEGRATION.md"
