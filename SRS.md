# Software Requirements Specification (SRS)
## EduBot - AI-Powered Learning Platform

**Version:** 1.0  
**Date:** November 2025  
**Author:** EduBot Development Team

---

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for EduBot, an AI-powered web application that helps students process educational documents, generate summaries, create flashcards, and test their knowledge through interactive quizzes.

### 1.2 Scope
EduBot is a full-stack web application consisting of:
- **Frontend**: React-based single-page application
- **Backend**: Flask REST API
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Integration**: Google Gemini API for content generation

### 1.3 Definitions and Acronyms
- **SRS**: Software Requirements Specification
- **API**: Application Programming Interface
- **JWT**: JSON Web Token
- **REST**: Representational State Transfer
- **AI**: Artificial Intelligence
- **PDF**: Portable Document Format

---

## 2. Overall Description

### 2.1 Product Perspective
EduBot is a standalone web application that integrates with Google Gemini AI service for intelligent content processing. The system operates independently and does not require integration with other educational platforms.

### 2.2 Product Functions
- User authentication and account management
- Document upload and text extraction
- AI-powered text summarization
- Flashcard generation from content
- Interactive quiz mode
- Document management (view, delete)
- Export functionality (text, JSON)

### 2.3 User Classes
- **Students/Learners**: Primary users who upload documents and use learning features
- **Educators**: Secondary users who may use the platform for content preparation

### 2.4 Operating Environment
- **Frontend**: Modern web browsers (Chrome, Firefox, Safari, Edge)
- **Backend**: Python 3.12+, Flask framework
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Deployment**: Cloud or on-premise servers

---

## 3. System Features

### 3.1 User Authentication

#### 3.1.1 User Registration
**Priority:** High

**Description:** Users can create accounts with email and password.

**Functional Requirements:**
- FR-001: System shall accept email and password for registration
- FR-002: System shall validate email format
- FR-003: System shall enforce minimum password length of 8 characters
- FR-004: System shall prevent duplicate email registration
- FR-005: System shall hash passwords before storage

**Inputs:** Email address, password  
**Outputs:** Registration confirmation or error message

#### 3.1.2 User Login
**Priority:** High

**Description:** Registered users can log in to access their accounts.

**Functional Requirements:**
- FR-006: System shall authenticate users with email and password
- FR-007: System shall return JWT token upon successful authentication
- FR-008: System shall reject invalid credentials
- FR-009: System shall maintain user session via JWT

**Inputs:** Email address, password  
**Outputs:** JWT access token or error message

#### 3.1.3 User Logout
**Priority:** Medium

**Description:** Users can log out from their accounts.

**Functional Requirements:**
- FR-010: System shall invalidate user session on logout
- FR-011: System shall clear authentication tokens

---

### 3.2 Document Management

#### 3.2.1 Document Upload
**Priority:** High

**Description:** Authenticated users can upload PDF and text documents.

**Functional Requirements:**
- FR-012: System shall accept PDF (.pdf) and text (.txt) files
- FR-013: System shall validate file type before processing
- FR-014: System shall enforce maximum file size of 16MB
- FR-015: System shall extract text from uploaded documents
- FR-016: System shall store documents securely per user
- FR-017: System shall associate documents with user accounts

**Inputs:** File (PDF or TXT)  
**Outputs:** Document metadata and confirmation

#### 3.2.2 Document Listing
**Priority:** High

**Description:** Users can view all their uploaded documents.

**Functional Requirements:**
- FR-018: System shall list all documents for authenticated user
- FR-019: System shall display document metadata (name, type, size, date)
- FR-020: System shall sort documents by most recent first

**Inputs:** User authentication token  
**Outputs:** List of document metadata

#### 3.2.3 Document Viewing
**Priority:** Medium

**Description:** Users can view full details and extracted text of documents.

**Functional Requirements:**
- FR-021: System shall display complete document information
- FR-022: System shall show extracted text content
- FR-023: System shall restrict access to user's own documents only

**Inputs:** Document ID, user authentication  
**Outputs:** Document details and extracted text

#### 3.2.4 Document Deletion
**Priority:** Medium

**Description:** Users can delete their uploaded documents.

**Functional Requirements:**
- FR-024: System shall allow users to delete their documents
- FR-025: System shall permanently remove document and associated data
- FR-026: System shall verify user ownership before deletion

**Inputs:** Document ID, user authentication  
**Outputs:** Deletion confirmation

---

### 3.3 AI-Powered Features

#### 3.3.1 Text Summarization
**Priority:** High

**Description:** System generates concise summaries of text content using AI.

**Functional Requirements:**
- FR-027: System shall accept text input for summarization
- FR-028: System shall generate bullet-point summaries
- FR-029: System shall highlight key concepts and main points
- FR-030: System shall format summaries for readability
- FR-031: System shall handle errors gracefully with fallback

**Inputs:** Text content  
**Outputs:** Formatted summary

#### 3.3.2 Flashcard Generation
**Priority:** High

**Description:** System creates educational flashcards from text content.

**Functional Requirements:**
- FR-032: System shall generate 5-6 question-answer pairs
- FR-033: System shall create flashcards covering key concepts
- FR-034: System shall format flashcards in JSON structure
- FR-035: System shall handle errors gracefully with fallback

**Inputs:** Text content  
**Outputs:** Array of flashcard objects (question, answer)

#### 3.3.3 AI Playground
**Priority:** Medium

**Description:** Users can experiment with AI features without uploading documents.

**Functional Requirements:**
- FR-036: System shall allow text input for AI processing
- FR-037: System shall provide summarization and flashcard generation
- FR-038: System shall not require authentication for playground access

**Inputs:** Custom text  
**Outputs:** AI-generated content

---

### 3.4 Quiz Mode

#### 3.4.1 Interactive Quiz
**Priority:** High

**Description:** Users can take quizzes using generated flashcards.

**Functional Requirements:**
- FR-039: System shall present one question at a time
- FR-040: System shall accept text answers from users
- FR-041: System shall validate answers and provide immediate feedback
- FR-042: System shall track quiz progress and score
- FR-043: System shall display results with percentage score
- FR-044: System shall allow quiz review after completion

**Inputs:** Flashcards, user answers  
**Outputs:** Quiz results and review

---

### 3.5 Export Functionality

#### 3.5.1 Export Flashcards as Text
**Priority:** Medium

**Description:** Users can export flashcards as text files.

**Functional Requirements:**
- FR-045: System shall generate downloadable .txt file
- FR-046: System shall format flashcards in readable text format
- FR-047: System shall include all questions and answers

**Inputs:** Flashcard data  
**Outputs:** Text file download

#### 3.5.2 Export Flashcards as JSON
**Priority:** Low

**Description:** Users can export flashcards as JSON files.

**Functional Requirements:**
- FR-048: System shall generate downloadable .json file
- FR-049: System shall format data in valid JSON structure
- FR-050: System shall enable import into other applications

**Inputs:** Flashcard data  
**Outputs:** JSON file download

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **Response Time**: API endpoints shall respond within 2 seconds for standard operations
- **File Upload**: Document upload and processing shall complete within 10 seconds for files up to 16MB
- **AI Processing**: AI operations shall complete within 15 seconds or provide fallback

### 4.2 Security Requirements
- **Authentication**: All protected endpoints require valid JWT tokens
- **Password Security**: Passwords shall be hashed using PBKDF2 with SHA-256
- **Data Isolation**: Users can only access their own documents
- **Input Validation**: All user inputs shall be validated and sanitized
- **File Security**: File uploads shall be validated for type and size

### 4.3 Usability Requirements
- **Interface**: System shall provide intuitive, responsive user interface
- **Accessibility**: System shall work on desktop, tablet, and mobile devices
- **Error Messages**: System shall display clear, user-friendly error messages
- **Loading States**: System shall show progress indicators for long operations

### 4.4 Reliability Requirements
- **Availability**: System shall be available 99% of the time during operational hours
- **Error Handling**: System shall handle errors gracefully without crashing
- **Data Persistence**: User data and documents shall be reliably stored

### 4.5 Scalability Requirements
- **Database**: System shall support migration to PostgreSQL for production scale
- **File Storage**: System shall support cloud storage integration
- **Horizontal Scaling**: Backend shall support multiple instances

### 4.6 Maintainability Requirements
- **Code Quality**: Code shall follow SOLID principles
- **Documentation**: Code shall be well-documented
- **Testing**: System shall maintain 85%+ test coverage

---

## 5. System Constraints

### 5.1 Technical Constraints
- **Backend**: Python 3.12+ required
- **Frontend**: Modern browsers with JavaScript enabled
- **Database**: SQLite for development, PostgreSQL for production
- **File Types**: Only PDF and TXT files supported
- **File Size**: Maximum 16MB per file

### 5.2 Business Constraints
- **AI Service**: Requires Google Gemini API key
- **Cost**: AI API usage may incur costs based on usage
- **Storage**: Local file storage in development, cloud storage recommended for production

### 5.3 Regulatory Constraints
- **Data Privacy**: User data must be protected and not shared
- **Security**: Passwords must be securely hashed
- **Compliance**: System should comply with data protection regulations

---

## 6. Assumptions and Dependencies

### 6.1 Assumptions
- Users have access to modern web browsers
- Users have internet connectivity
- Google Gemini API is available and accessible
- Users understand basic file upload operations

### 6.2 Dependencies
- **External Services**: Google Gemini API
- **Libraries**: Flask, React, SQLAlchemy, PyPDF2
- **Infrastructure**: Web server, database server, file storage

---

## 7. User Stories Summary

### High Priority Features
1. User registration and authentication
2. Document upload and text extraction
3. AI-powered summarization
4. Flashcard generation
5. Interactive quiz mode

### Medium Priority Features
1. Document management (view, delete)
2. AI playground
3. Export functionality
4. User logout

### Low Priority Features
1. JSON export format
2. Advanced quiz features

---

## 8. Acceptance Criteria

### 8.1 Functional Acceptance
- ✅ All 21 user stories implemented and tested
- ✅ All API endpoints functional
- ✅ Authentication and authorization working
- ✅ AI features integrated (with fallback)
- ✅ Document management complete

### 8.2 Non-Functional Acceptance
- ✅ Test coverage ≥ 85%
- ✅ All tests passing (36 tests)
- ✅ Security measures implemented
- ✅ Responsive design working
- ✅ Error handling in place

---

## 9. Glossary

- **Flashcard**: A learning tool with a question on one side and answer on the other
- **JWT Token**: A secure token used for authentication
- **Text Extraction**: Process of extracting text content from documents
- **AI Summarization**: Automatic generation of concise summaries using AI
- **Quiz Mode**: Interactive testing feature using flashcards

---

## 10. Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | Nov 2025 | Development Team | Initial SRS for EduBot v1.3.0 |

---

## Appendix A: API Endpoints Summary

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/me` - Get current user

### Documents
- `POST /api/upload` - Upload document
- `GET /api/documents` - List documents
- `GET /api/documents/<id>` - Get document
- `DELETE /api/documents/<id>` - Delete document

### AI Features
- `POST /api/ai/summarize` - Generate summary
- `POST /api/ai/flashcards` - Generate flashcards
- `POST /api/ai/generate` - General AI generation

### Public
- `GET /api/hello` - Health check

---

## Appendix B: Database Schema

### Users Table
- `id` (INTEGER, PRIMARY KEY)
- `email` (VARCHAR(255), UNIQUE, NOT NULL)
- `password_hash` (VARCHAR(255), NOT NULL)
- `created_at` (DATETIME, NOT NULL)

### Documents Table
- `id` (INTEGER, PRIMARY KEY)
- `user_id` (INTEGER, FOREIGN KEY, NOT NULL)
- `original_name` (VARCHAR(255), NOT NULL)
- `stored_name` (VARCHAR(255), NOT NULL)
- `relative_path` (VARCHAR(1024), NOT NULL)
- `mime_type` (VARCHAR(100))
- `size_bytes` (INTEGER)
- `extracted_text` (TEXT)
- `created_at` (DATETIME, NOT NULL)

---

**Document Status:** Approved  
**Next Review Date:** As needed for version updates


