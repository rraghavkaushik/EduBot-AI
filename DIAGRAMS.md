# System Diagrams - EduBot
## DFD, ERD, and UML Diagrams

Comprehensive collection of system diagrams for the EduBot AI-powered learning platform.

---

## Table of Contents

1. [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
2. [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
3. [UML Class Diagram](#uml-class-diagram)
4. [UML Sequence Diagrams](#uml-sequence-diagrams)
5. [UML Use Case Diagram](#uml-use-case-diagram)
6. [UML Component Diagram](#uml-component-diagram)

---

## Data Flow Diagram (DFD)

### Level 0 - Context Diagram

```mermaid
graph LR
    User[User] -->|HTTP Requests| System[EduBot System]
    System -->|HTTP Responses| User
    System -->|API Calls| Gemini[Google Gemini API]
    System -->|Read/Write| DB[(Database)]
    System -->|Read/Write| FS[File Storage]
    
    style User fill:#e1f5ff
    style System fill:#fff4e1
    style Gemini fill:#fce4ec
    style DB fill:#e8f5e9
    style FS fill:#e8f5e9
```

### Level 1 - System Decomposition

```mermaid
graph TB
    subgraph "EduBot System"
        A[Authentication<br/>Process]
        B[Document<br/>Management]
        C[AI Processing]
        D[Quiz<br/>Management]
    end
    
    User[User] -->|Login/Register| A
    User -->|Upload Document| B
    User -->|Request AI| C
    User -->|Take Quiz| D
    
    A -->|Store| DB[(User Database)]
    B -->|Store| DB
    B -->|Store Files| FS[File Storage]
    B -->|Extract Text| C
    C -->|API Call| Gemini[Gemini API]
    C -->|Store Results| DB
    D -->|Read Flashcards| DB
    D -->|Store Results| DB
    
    DB -->|Query| A
    DB -->|Query| B
    DB -->|Query| C
    DB -->|Query| D
    
    style User fill:#e1f5ff
    style A fill:#ffeb3b
    style B fill:#ffeb3b
    style C fill:#ffeb3b
    style D fill:#ffeb3b
    style DB fill:#e8f5e9
    style FS fill:#e8f5e9
    style Gemini fill:#fce4ec
```

### Level 2 - Detailed Process Flow

#### Document Upload Process

```mermaid
graph LR
    A[User Uploads File] -->|File Data| B[Validate File]
    B -->|Valid File| C[Save to Storage]
    B -->|Invalid| E[Return Error]
    C -->|File Path| D[Extract Text]
    D -->|Text Content| F[Store Metadata]
    F -->|Document Record| G[(Database)]
    F -->|Success| H[Return Response]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#fff4e1
    style D fill:#fff4e1
    style E fill:#ffcdd2
    style F fill:#fff4e1
    style G fill:#e8f5e9
    style H fill:#c8e6c9
```

#### AI Processing Flow

```mermaid
graph LR
    A[User Request] -->|Text Input| B[Validate Input]
    B -->|Valid| C[Prepare Prompt]
    B -->|Invalid| D[Return Error]
    C -->|Prompt| E[Call Gemini API]
    E -->|Response| F[Parse Response]
    F -->|Formatted Data| G[Store Results]
    G -->|Response Data| H[Return to User]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#fff4e1
    style E fill:#fce4ec
    style F fill:#fff4e1
    style G fill:#fff4e1
    style H fill:#c8e6c9
    style D fill:#ffcdd2
```

---

## Entity Relationship Diagram (ERD)

### Complete ERD

```mermaid
erDiagram
    USER ||--o{ DOCUMENT : "uploads"
    
    USER {
        int id PK "Primary Key"
        string email UK "Unique, Not Null"
        string password_hash "Not Null"
        datetime created_at "Not Null"
    }
    
    DOCUMENT {
        int id PK "Primary Key"
        int user_id FK "Foreign Key -> USER.id"
        string original_name "Not Null"
        string stored_name "Not Null"
        string relative_path "Not Null"
        string mime_type "Nullable"
        int size_bytes "Nullable"
        text extracted_text "Nullable"
        datetime created_at "Not Null"
    }
```

### Detailed ERD with Attributes

```mermaid
erDiagram
    USER {
        int id PK
        string email UK "VARCHAR(255)"
        string password_hash "VARCHAR(255)"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    DOCUMENT {
        int id PK
        int user_id FK "INDEXED"
        string original_name "VARCHAR(255)"
        string stored_name "VARCHAR(255)"
        string relative_path "VARCHAR(1024)"
        string mime_type "VARCHAR(100)"
        int size_bytes
        text extracted_text
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
    }
    
    USER ||--o{ DOCUMENT : "has many"
```

### Relationship Details

- **Cardinality**: One-to-Many (One User can have many Documents)
- **Foreign Key**: `DOCUMENT.user_id` → `USER.id`
- **Constraint**: Documents are deleted when user is deleted (application-level)
- **Index**: `user_id` is indexed for faster queries

---

## UML Class Diagram

### Backend Classes

```mermaid
classDiagram
    class Flask {
        +Flask(__name__)
        +route()
        +run()
    }
    
    class User {
        +int id
        +string email
        +string password_hash
        +datetime created_at
        +to_public_dict()
    }
    
    class Document {
        +int id
        +int user_id
        +string original_name
        +string stored_name
        +string relative_path
        +string mime_type
        +int size_bytes
        +text extracted_text
        +datetime created_at
    }
    
    class TextExtractor {
        <<interface>>
        +__call__(file_path: str) str
    }
    
    class TextGenerator {
        <<interface>>
        +__call__(prompt: str, model_name: str) str
    }
    
    class DefaultTextExtractor {
        +__call__(file_path: str) str
    }
    
    class GeminiTextGenerator {
        +__call__(prompt: str, model_name: str) str
    }
    
    class SQLAlchemy {
        +Model
        +Column
        +ForeignKey
        +relationship()
    }
    
    User "1" --> "*" Document : owns
    TextExtractor <|.. DefaultTextExtractor : implements
    TextGenerator <|.. GeminiTextGenerator : implements
    User --|> SQLAlchemy : extends
    Document --|> SQLAlchemy : extends
```

### Frontend Classes

```mermaid
classDiagram
    class App {
        +boolean isAuthenticated
        +function setIsAuthenticated
        +Router routes
        +render()
    }
    
    class Header {
        +boolean isAuthenticated
        +function setIsAuthenticated
        +function logout()
        +render()
    }
    
    class Home {
        +boolean isAuthenticated
        +string message
        +render()
    }
    
    class Login {
        +function setIsAuthenticated
        +string email
        +string password
        +function handleSubmit()
        +render()
    }
    
    class Register {
        +function setIsAuthenticated
        +string email
        +string password
        +function handleSubmit()
        +render()
    }
    
    class Upload {
        +boolean isAuthenticated
        +File selectedFile
        +string summary
        +Array flashcards
        +function handleUpload()
        +function handleAISummary()
        +function handleAICards()
        +render()
    }
    
    class AI {
        +string text
        +string summary
        +Array cards
        +function handleSummarize()
        +function handleFlashcards()
        +render()
    }
    
    class Quiz {
        +Array cards
        +int currentIndex
        +int score
        +string userAnswer
        +boolean quizComplete
        +function handleAnswer()
        +function handleNext()
        +render()
    }
    
    class Documents {
        +boolean isAuthenticated
        +Array documents
        +function fetchDocuments()
        +function handleDelete()
        +render()
    }
    
    class Flashcard {
        +int index
        +string question
        +string answer
        +boolean flipped
        +function handleFlip()
        +render()
    }
    
    class ApiService {
        +function register()
        +function login()
        +function upload()
        +function getDocuments()
        +function deleteDocument()
        +function summarize()
        +function generateFlashcards()
    }
    
    App --> Header : contains
    App --> Home : routes to
    App --> Login : routes to
    App --> Register : routes to
    App --> Upload : routes to
    App --> AI : routes to
    App --> Quiz : routes to
    App --> Documents : routes to
    Upload --> Flashcard : uses
    AI --> Flashcard : uses
    Quiz --> Flashcard : uses
    Upload --> ApiService : uses
    AI --> ApiService : uses
    Documents --> ApiService : uses
    Login --> ApiService : uses
    Register --> ApiService : uses
```

---

## UML Sequence Diagrams

### User Registration Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant D as Database
    
    U->>F: Enter email & password
    F->>F: Validate input
    F->>B: POST /api/auth/register
    B->>B: Validate email format
    B->>B: Check password length
    B->>D: Query: Check if email exists
    D-->>B: Email not found
    B->>B: Hash password
    B->>D: INSERT: Create user record
    D-->>B: User created (id)
    B-->>F: 201 Created {message: "registration successful"}
    F-->>U: Show success message
```

### Document Upload Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant FS as File System
    participant TE as Text Extractor
    participant D as Database
    
    U->>F: Select file & click upload
    F->>F: Validate file type
    F->>B: POST /api/upload (multipart/form-data)
    B->>B: Validate JWT token
    B->>B: Validate file type (.pdf, .txt)
    B->>B: Validate file size (< 16MB)
    B->>FS: Save file to disk
    FS-->>B: File saved (path)
    B->>TE: Extract text from file
    TE-->>B: Extracted text
    B->>D: INSERT: Create document record
    D-->>B: Document created (id)
    B-->>F: 201 Created {document: {...}}
    F-->>U: Show upload success
```

### AI Summary Generation Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant G as Gemini API
    participant D as Database
    
    U->>F: Request summary
    F->>B: POST /api/ai/summarize
    B->>B: Validate JWT token
    B->>B: Validate text input
    B->>B: Construct prompt
    B->>G: POST /v1/models/gemini-2.0-flash:generateContent
    G-->>B: Generated summary text
    B->>B: Format response
    B-->>F: 200 OK {summary: "..."}
    F->>F: Display summary
    F-->>U: Show formatted summary
```

### Quiz Mode Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant Q as Quiz Component
    participant S as State Manager
    
    U->>F: Click "Start Quiz Mode"
    F->>Q: Initialize quiz with flashcards
    Q->>S: Set currentIndex = 0
    Q->>S: Set score = 0
    Q->>U: Display question 1
    U->>Q: Enter answer
    Q->>Q: Check answer (string match)
    Q->>S: Update score if correct
    Q->>U: Show feedback (correct/incorrect)
    Q->>S: Increment currentIndex
    loop For each question
        Q->>U: Display next question
        U->>Q: Enter answer
        Q->>Q: Validate & score
    end
    Q->>S: Set quizComplete = true
    Q->>Q: Calculate percentage
    Q->>U: Display results & review
```

---

## UML Use Case Diagram

### Complete Use Case Diagram

```mermaid
graph TB
    subgraph "EduBot System"
        UC1[Register User]
        UC2[Login User]
        UC3[Logout User]
        UC4[Upload Document]
        UC5[View Documents]
        UC6[Delete Document]
        UC7[Generate Summary]
        UC8[Generate Flashcards]
        UC9[Use AI Playground]
        UC10[Take Quiz]
        UC11[Export Flashcards]
        UC12[View Document Details]
    end
    
    Student[Student User] --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Student --> UC5
    Student --> UC6
    Student --> UC7
    Student --> UC8
    Student --> UC10
    Student --> UC11
    Student --> UC12
    
    Visitor[Visitor] --> UC9
    
    UC4 --> UC7
    UC4 --> UC8
    UC8 --> UC10
    UC8 --> UC11
    UC7 --> UC11
    
    style Student fill:#e1f5ff
    style Visitor fill:#fff4e1
    style UC1 fill:#c8e6c9
    style UC2 fill:#c8e6c9
    style UC3 fill:#c8e6c9
    style UC4 fill:#c8e6c9
    style UC5 fill:#c8e6c9
    style UC6 fill:#c8e6c9
    style UC7 fill:#c8e6c9
    style UC8 fill:#c8e6c9
    style UC9 fill:#fff9c4
    style UC10 fill:#c8e6c9
    style UC11 fill:#fff9c4
    style UC12 fill:#fff9c4
```

### Detailed Use Case Diagram

```mermaid
graph LR
    subgraph "Actors"
        A1[Student]
        A2[Visitor]
    end
    
    subgraph "Authentication"
        UC1[Register]
        UC2[Login]
        UC3[Logout]
    end
    
    subgraph "Document Management"
        UC4[Upload Document]
        UC5[List Documents]
        UC6[View Document]
        UC7[Delete Document]
    end
    
    subgraph "AI Features"
        UC8[Generate Summary]
        UC9[Generate Flashcards]
        UC10[AI Playground]
    end
    
    subgraph "Learning Tools"
        UC11[Take Quiz]
        UC12[Review Results]
        UC13[Export Flashcards]
    end
    
    A1 --> UC1
    A1 --> UC2
    A1 --> UC3
    A1 --> UC4
    A1 --> UC5
    A1 --> UC6
    A1 --> UC7
    A1 --> UC8
    A1 --> UC9
    A1 --> UC11
    A1 --> UC12
    A1 --> UC13
    
    A2 --> UC10
    
    UC4 -.->|enables| UC8
    UC4 -.->|enables| UC9
    UC9 -.->|enables| UC11
    UC9 -.->|enables| UC13
    UC11 -.->|shows| UC12
    
    style A1 fill:#e1f5ff
    style A2 fill:#fff4e1
```

---

## UML Component Diagram

### System Components

```mermaid
graph TB
    subgraph "Frontend Layer"
        C1[React App]
        C2[API Client]
        C3[Router]
        C4[Components]
    end
    
    subgraph "Backend Layer"
        C5[Flask Application]
        C6[Authentication Module]
        C7[Document Service]
        C8[AI Service]
    end
    
    subgraph "Service Layer"
        C9[Text Extractor]
        C10[Text Generator]
    end
    
    subgraph "Data Layer"
        C11[(Database)]
        C12[File Storage]
    end
    
    subgraph "External Services"
        C13[Gemini API]
    end
    
    C1 --> C2
    C1 --> C3
    C1 --> C4
    C2 --> C5
    C5 --> C6
    C5 --> C7
    C5 --> C8
    C7 --> C9
    C8 --> C10
    C10 --> C13
    C6 --> C11
    C7 --> C11
    C7 --> C12
    C8 --> C11
    
    style C1 fill:#61dafb
    style C5 fill:#ffeb3b
    style C11 fill:#4caf50
    style C13 fill:#fce4ec
```

### Detailed Component Diagram

```mermaid
graph LR
    subgraph "Client Components"
        A[Browser]
        B[React SPA]
        C[Axios Client]
    end
    
    subgraph "Application Components"
        D[Flask API]
        E[Auth Handler]
        F[Document Handler]
        G[AI Handler]
    end
    
    subgraph "Business Logic"
        H[Text Extractor]
        I[Text Generator]
        J[File Validator]
    end
    
    subgraph "Data Components"
        K[(SQLite DB)]
        L[File System]
    end
    
    subgraph "External"
        M[Gemini API]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    E --> K
    F --> H
    F --> J
    F --> K
    F --> L
    G --> I
    I --> M
    G --> K
    
    style A fill:#e1f5ff
    style B fill:#61dafb
    style D fill:#ffeb3b
    style K fill:#4caf50
    style M fill:#fce4ec
```

---

## Diagram Summary

### DFD (Data Flow Diagram)
- **Level 0**: Context diagram showing external entities
- **Level 1**: System decomposition into major processes
- **Level 2**: Detailed process flows for document upload and AI processing

### ERD (Entity Relationship Diagram)
- **Entities**: User, Document
- **Relationship**: One-to-Many (User → Documents)
- **Attributes**: All fields with types and constraints
- **Keys**: Primary keys, foreign keys, unique constraints

### UML Diagrams
1. **Class Diagram**: Backend and Frontend classes with relationships
2. **Sequence Diagrams**: 
   - User Registration
   - Document Upload
   - AI Summary Generation
   - Quiz Mode
3. **Use Case Diagram**: All system use cases with actors
4. **Component Diagram**: System components and their interactions

---

## Diagram Usage

### For Documentation
- Include in project report
- Use for system documentation
- Reference in architecture documentation

### For Presentation
- Export diagrams as images
- Use in slides
- Include in project demos

### For Development
- Guide implementation
- Understand system structure
- Plan new features

---

## Tools for Rendering

All diagrams use **Mermaid** syntax and can be rendered in:
- **GitHub/GitLab**: Native markdown support
- **VS Code**: Mermaid extension
- **Online**: https://mermaid.live/
- **Documentation**: MkDocs, Docusaurus, etc.

### Exporting as Images

1. Copy Mermaid code
2. Go to https://mermaid.live/
3. Paste code
4. Export as PNG/SVG
5. Include in documents

---

## Diagram Relationships

```
DFD (Data Flow)
    ↓
ERD (Data Structure)
    ↓
UML Class Diagram (Code Structure)
    ↓
UML Sequence Diagram (Process Flow)
    ↓
UML Use Case Diagram (User Interactions)
    ↓
UML Component Diagram (System Architecture)
```

All diagrams are interconnected and provide different perspectives of the same system.

---

**Document Status:** Complete  
**Last Updated:** November 2025  
**Version:** 1.0

