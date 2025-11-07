import axios from 'axios'

export const api = axios.create({
  // Base URL left empty to use Vite proxy in dev; in prod set an env var
  baseURL: '/',
  headers: { 'Content-Type': 'application/json' },
})

// Token persistence helpers
const TOKEN_KEY = 'edubot_token'
const stored = typeof window !== 'undefined' ? window.localStorage.getItem(TOKEN_KEY) : null
if (stored) {
  api.defaults.headers.common['Authorization'] = `Bearer ${stored}`
}

export const getHello = () => api.get('/api/hello')

export const register = (email, password) =>
  api.post('/api/auth/register', { email, password })

export const login = (email, password) => {
  const response = api.post('/api/auth/login', { email, password })
  response.then(res => {
    if (res.data.access_token) {
      persistToken(res.data.access_token)
    }
  })
  return response
}

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}

export const persistToken = (token) => {
  if (typeof window !== 'undefined') window.localStorage.setItem(TOKEN_KEY, token)
  setAuthToken(token)
}

export const clearToken = () => {
  if (typeof window !== 'undefined') window.localStorage.removeItem(TOKEN_KEY)
  setAuthToken(null)
}

export const getToken = () => (typeof window !== 'undefined' ? window.localStorage.getItem(TOKEN_KEY) : null)

export const me = () => api.get('/api/me')

export const upload = (file) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/api/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const uploadFile = (formData) => {
  return api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// -----------------------------
// Real AI API functions (with fallback to mocks)
// -----------------------------

// Real API functions that call the backend Gemini endpoints
export const summarize = async (text) => {
  try {
    const response = await api.post('/api/ai/summarize', { text })
    return response.data
  } catch (error) {
    console.warn('Real API failed, using mock:', error.response?.data || error.message)
    // Fallback to mock if API fails (e.g., missing GEMINI_API_KEY)
    return await mockSummarize(text)
  }
}

export const generateFlashcards = async (text) => {
  try {
    const response = await api.post('/api/ai/flashcards', { text })
    return response.data
  } catch (error) {
    console.warn('Real API failed, using mock:', error.response?.data || error.message)
    // Fallback to mock if API fails (e.g., missing GEMINI_API_KEY)
    return await mockFlashcards(text)
  }
}

// -----------------------------
// Mock AI helpers (fallback)
// -----------------------------
const looksLikeREST = (t) => /\b(REST|HTTP|URI|endpoint|status\s*codes?|JWT|OAuth|idempot|pagination|versioning|resource)\b/i.test(t || '')

export const mockSummarize = async (text) => {
  if (looksLikeREST(text)) {
    const bullets = [
      'Design endpoints around resources with clear, noun-based URIs.',
      'Use standard HTTP methods: GET, POST, PUT, PATCH, DELETE.',
      'Return meaningful status codes and consistent error bodies.',
      'Support pagination, filtering, and sorting for collections.',
      'Ensure idempotency for PUT/DELETE; use PATCH for partial updates.',
      'Secure with JWT/OAuth; never expose secrets in URLs.',
      'Version your API and document breaking changes clearly.',
    ]
    return { summary: bullets.map(b => `• ${b}`).join('\n') }
  }
  // Fallback: general AI summary
  const bullets = [
    'AI simulates human-like intelligence (language, patterns, decisions, learning).',
    'Modern AI uses machine learning and deep learning on data to generalize.',
    'Responsible AI focuses on fairness, transparency, and privacy.',
  ]
  const words = (text || '').split(/[^a-zA-Z]+/).filter(w => w.length > 6).slice(0, 3)
  const extra = words.length ? `Key concepts: ${words.join(', ')}.` : 'Key concepts: models, data, learning.'
  return { summary: bullets.map(b => `• ${b}`).join('\n') + `\n• ${extra}` }
}

export const mockFlashcards = async (text) => {
  if (looksLikeREST(text)) {
    return {
      cards: [
        { question: 'What is a REST resource?', answer: 'A conceptual object or collection exposed via a URI, manipulated with standard HTTP methods.' },
        { question: 'When to use PUT vs PATCH?', answer: 'PUT is idempotent full replacement; PATCH is for partial updates.' },
        { question: 'Why version an API?', answer: 'To introduce breaking changes without impacting existing clients.' },
        { question: 'How to handle large lists?', answer: 'Use pagination (limit/offset or cursor) with filtering and sorting.' },
        { question: 'Which status codes are common?', answer: '200/201/204 success, 400/401/403 client errors, 404 not found, 409 conflict, 500 server error.' },
        { question: 'How to secure endpoints?', answer: 'Use JWT/OAuth; validate and sanitize inputs; enforce least privilege.' },
      ]
    }
  }
  // Fallback: general AI cards
  return {
    cards: [
      { question: 'What is Artificial Intelligence (AI)?', answer: 'A field of computer science that enables systems to perform tasks that typically require human intelligence.' },
      { question: 'Name two techniques used in modern AI.', answer: 'Machine Learning and Deep Learning.' },
      { question: 'What are pillars of Responsible AI?', answer: 'Fairness, transparency, and privacy.' },
      { question: 'Why are datasets important for AI?', answer: 'They enable models to learn patterns and generalize to new examples.' },
    ]
  }
}


