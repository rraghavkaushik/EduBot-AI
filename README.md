# EduBot Flask API

A simple Flask backend API project.

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API Key (for AI features):**
   
   Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   
   Then set it as an environment variable:
   ```bash
   # On macOS/Linux:
   export GEMINI_API_KEY="your-api-key-here"
   
   # On Windows (PowerShell):
   $env:GEMINI_API_KEY="your-api-key-here"
   
   # Or add to your shell profile (~/.bashrc, ~/.zshrc, etc.) for persistence:
   echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
   ```
   
   **Note:** If the API key is not set, the app will still work but AI features (summarization and flashcards) will use mock data as a fallback.

## Running the Application

1. **Make sure your virtual environment is activated:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the Flask app:**
   ```bash
   python app.py
   ```

3. **The server will start on:** `http://localhost:5001`

## API Endpoints

### Public Endpoints
- **GET** `/api/hello` - Returns a simple JSON message

### AI Endpoints (Requires Authentication)
- **POST** `/api/ai/summarize` - Generate a summary of provided text
  - Body: `{ "text": "Your text here..." }`
  - Response: `{ "summary": "• Point 1\n• Point 2..." }`

- **POST** `/api/ai/flashcards` - Generate flashcards from provided text
  - Body: `{ "text": "Your text here..." }`
  - Response: `{ "cards": [{"question": "...", "answer": "..."}, ...] }`

- **POST** `/api/ai/generate` - General AI text generation
  - Body: `{ "prompt": "Your prompt", "model": "gemini-1.5-flash" }`
  - Response: `{ "output": "Generated text..." }`

## Testing the API

You can test the API using curl:
```bash
curl http://localhost:5001/api/hello
```

Or visit `http://localhost:5001/api/hello` in your browser.

## Auth Endpoints

- `POST /api/auth/register` — Register a user
  - Body: `{ "email": "you@example.com", "password": "yourStrongPass" }`

- `POST /api/auth/login` — Login and receive a JWT access token
  - Body: `{ "email": "you@example.com", "password": "yourStrongPass" }`
  - Response: `{ "access_token": "<JWT>", "token_type": "Bearer" }`

- `GET /api/me` — Get current user info
  - Header: `Authorization: Bearer <JWT>`

### Quick test with curl

```bash
# Register (first time)
curl -X POST http://localhost:5001/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"password123"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"password123"}' | \
  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')

# Call protected endpoint
curl http://localhost:5001/api/me -H "Authorization: Bearer $TOKEN"
```

## Project Structure

```
EduBot/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore file
├── README.md          # This file
└── venv/              # Virtual environment (not in git)
```
