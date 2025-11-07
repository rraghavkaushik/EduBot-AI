# EduBot Backend Demo Script for Presentation

## 🎯 **Demo Flow for Screenshots**

### **1. System Overview (30 seconds)**
```bash
# Show backend is running
curl http://localhost:5001/api/hello
```
**Screenshot**: Terminal showing successful API response
**Narrative**: "Here you can see our Flask backend is running and responding to requests"

### **2. Database & Architecture (1 minute)**
```bash
# Show database structure
sqlite3 instance/edubot.db ".schema"
```
**Screenshot**: Database schema showing users and documents tables
**Narrative**: "Our backend uses SQLite with two main tables: users for authentication and documents for file storage"

### **3. Authentication System (1.5 minutes)**
```bash
# Step 1: Register new user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"password123"}'

# Step 2: Login and get token
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"password123"}'

# Step 3: Access protected endpoint
curl -H "Authorization: Bearer TOKEN_HERE" http://localhost:5001/api/me
```
**Screenshots**: 
- Registration success
- Login with JWT token
- Protected endpoint access
**Narrative**: "We implemented a complete JWT-based authentication system with secure endpoints"

### **4. File Processing Engine (2 minutes)**
```bash
# Upload and process file
curl -X POST -H "Authorization: Bearer TOKEN_HERE" \
  -F "file=@sample.txt" http://localhost:5001/api/upload
```
**Screenshot**: File upload response with extracted text
**Narrative**: "Our backend can process PDF and text files, extract content, and store metadata"

### **5. AI Integration (1 minute)**
```bash
# Show AI generation endpoint (if API key is set)
curl -X POST -H "Authorization: Bearer TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain machine learning"}' \
  http://localhost:5001/api/ai/generate
```
**Screenshot**: AI response (or error if no API key)
**Narrative**: "We've integrated Google Gemini AI for intelligent text generation and analysis"

### **6. Error Handling & Validation (30 seconds)**
```bash
# Show validation errors
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid-email","password":"123"}'
```
**Screenshot**: Validation error response
**Narrative**: "Our backend includes comprehensive input validation and error handling"

## 📸 **Screenshot Tips**

### **Terminal Screenshots:**
- Use a dark theme for better readability
- Zoom in to make text clear
- Include the command and response in one shot
- Use `clear` command before each demo for clean screenshots

### **API Tool Screenshots:**
- Show the request URL, headers, and body
- Display the response with status code
- Include response time for performance demonstration

### **Database Screenshots:**
- Show table structure clearly
- Include sample data if available
- Use `.mode column` in SQLite for better formatting

## 🎬 **Presentation Flow**

1. **Introduction** (30s) - Show running backend
2. **Architecture** (1m) - Database schema and structure
3. **Authentication** (1.5m) - Complete auth flow
4. **Core Features** (2m) - File upload and processing
5. **AI Integration** (1m) - Gemini AI capabilities
6. **Quality Assurance** (30s) - Error handling and validation
7. **Q&A** (2-3m)

## 🔧 **Setup Commands**

```bash
# Ensure backend is running
cd /Users/rraghavkaushik/Documents/SEM-7/SWE/EduBot
source venv/bin/activate
python app.py

# In another terminal, test endpoints
curl http://localhost:5001/api/hello
```

## 📱 **Alternative: Use Postman**

1. **Import this collection:**
```json
{
  "info": {
    "name": "EduBot Backend Demo",
    "description": "Complete API testing for presentation"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:5001/api/hello"
      }
    },
    {
      "name": "Register User",
      "request": {
        "method": "POST",
        "url": "http://localhost:5001/api/auth/register",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {"mode": "raw", "raw": "{\"email\":\"demo@example.com\",\"password\":\"password123\"}"}
      }
    }
  ]
}
```

2. **Take screenshots of each request/response**
3. **Show the complete workflow**

## 🎯 **Key Points to Highlight**

- **Scalability**: Flask + SQLAlchemy architecture
- **Security**: JWT authentication, input validation
- **Performance**: Efficient file processing and storage
- **Integration**: AI capabilities with Gemini
- **User Experience**: Comprehensive error handling
- **Professional Quality**: Production-ready code structure

---

**Total Demo Time: 7-8 minutes + Q&A**
**Screenshots Needed: 6-8 key moments**
**Focus: Show technical competence and system reliability**
