import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { summarize, generateFlashcards } from '../services/api'
import Flashcard from '../components/Flashcard'

const SAMPLE_TEXT = `Artificial Intelligence (AI) is a field of computer science focused on creating systems capable of performing tasks that typically require human intelligence. These tasks include understanding natural language, recognizing patterns, making decisions, and learning from data. Modern AI leverages machine learning and deep learning to build models that can generalize from examples. Responsible AI emphasizes fairness, transparency, and privacy.`

export default function AIPage() {
  const navigate = useNavigate()
  const [input, setInput] = useState(SAMPLE_TEXT)
  const [summary, setSummary] = useState('')
  const [cards, setCards] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSummarize = async () => {
    setIsLoading(true)
    setError('')
    try {
      const res = await summarize(input)
      setSummary(res.summary)
    } catch (e) {
      setError('Failed to summarize. ' + (e.message || ''))
    } finally {
      setIsLoading(false)
    }
  }

  const handleFlashcards = async () => {
    setIsLoading(true)
    setError('')
    try {
      const res = await generateFlashcards(input)
      setCards(res.cards || res.flashcards || [])
    } catch (e) {
      setError('Failed to generate flashcards. ' + (e.message || ''))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container fade-in">
      <div className="card-header mb-5">
        <h1 className="card-title">✨ AI</h1>
        <p className="card-subtitle">Summarization and flashcard generation</p>
      </div>

      <div className="card mb-4">
        <label className="form-label">📄 Input Text</label>
        <textarea
          className="form-input"
          style={{ minHeight: '140px', fontFamily: 'inherit' }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Paste your study text here..."
        />
        <div className="mt-3" style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button className="btn btn-success" onClick={handleSummarize} disabled={isLoading}>📝 Summarize</button>
          <button className="btn" onClick={handleFlashcards} disabled={isLoading}>🎴 Generate Flashcards</button>
          <button className="btn btn-secondary" onClick={() => { setInput(SAMPLE_TEXT); setSummary(''); setCards([]); }}>↺ Reset Sample</button>
        </div>
        {error && <div className="form-error mt-2">{error}</div>}
      </div>

      {summary && (
        <div className="card mb-4">
          <div className="card-header">
            <h2 className="card-title">📝 Summary</h2>
            <p className="card-subtitle">Key points</p>
          </div>
          <div className="grid" style={{ gridTemplateColumns: '1fr' }}>
            <ul style={{ marginLeft: '1rem' }}>
              {summary.split('\n').map((line, idx) => (
                line.trim() ? <li key={idx} style={{ marginBottom: '6px' }}>{line}</li> : null
              ))}
            </ul>
          </div>
        </div>
      )}

      {cards.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">🎴 Flashcards</h2>
            <p className="card-subtitle">Tap a card to flip</p>
            <div className="mt-3" style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <button 
                className="btn btn-success" 
                onClick={() => navigate('/quiz', { state: { cards } })}
              >
                📝 Start Quiz Mode
              </button>
              <button 
                className="btn" 
                onClick={() => {
                  const text = cards.map((c, i) => `Q${i + 1}: ${c.question}\nA${i + 1}: ${c.answer}\n`).join('\n')
                  const blob = new Blob([text], { type: 'text/plain' })
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement('a')
                  a.href = url
                  a.download = 'flashcards.txt'
                  a.click()
                  URL.revokeObjectURL(url)
                }}
              >
                💾 Export as Text
              </button>
              <button 
                className="btn" 
                onClick={() => {
                  const json = JSON.stringify({ flashcards: cards }, null, 2)
                  const blob = new Blob([json], { type: 'application/json' })
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement('a')
                  a.href = url
                  a.download = 'flashcards.json'
                  a.click()
                  URL.revokeObjectURL(url)
                }}
              >
                📦 Export as JSON
              </button>
            </div>
          </div>
          <div className="grid grid-2">
            {cards.map((c, idx) => (
              <Flashcard key={idx} index={idx} question={c.question} answer={c.answer} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
