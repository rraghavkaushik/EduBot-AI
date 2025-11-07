# Gemini API Setup Guide

## Quick Setup

1. **Get your free API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your API key

2. **Set the environment variable:**

   **macOS/Linux:**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```

   **Make it permanent (macOS/Linux):**
   ```bash
   echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify it's set:**
   ```bash
   echo $GEMINI_API_KEY  # Should print your key
   ```

4. **Restart your Flask server** (if it's already running):
   ```bash
   # Stop the server (Ctrl+C), then:
   source venv/bin/activate
   python app.py
   ```

## Testing

Once set up, the AI features will automatically use Gemini. If the API key is missing, the app will gracefully fall back to mock data.

### Test with curl:

```bash
# First, get a token (login)
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"password123"}' | \
  python -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')

# Test summarization
curl -X POST http://localhost:5001/api/ai/summarize \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"text":"REST APIs are stateless and use standard HTTP methods."}'

# Test flashcard generation
curl -X POST http://localhost:5001/api/ai/flashcards \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"text":"REST APIs are stateless and use standard HTTP methods."}'
```

## Troubleshooting

- **"GEMINI_API_KEY is not set"**: Make sure you exported the variable in the same terminal session where you're running the Flask server
- **"google-generativeai is not installed"**: Run `pip install -r requirements.txt`
- **API errors**: Check that your API key is valid and has not exceeded rate limits
- **Fallback to mocks**: If you see mock data, check the browser console for warnings about API failures

