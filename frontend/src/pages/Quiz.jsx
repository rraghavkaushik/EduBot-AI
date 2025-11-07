import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

export default function QuizPage() {
  const location = useLocation()
  const navigate = useNavigate()
  
  // Get flashcards from location state or use empty array
  const initialCards = location.state?.cards || []
  
  const [cards, setCards] = useState(initialCards)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [userAnswer, setUserAnswer] = useState('')
  const [showAnswer, setShowAnswer] = useState(false)
  const [score, setScore] = useState(0)
  const [answered, setAnswered] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)
  const [quizComplete, setQuizComplete] = useState(false)
  const [answers, setAnswers] = useState([]) // Track all answers for review

  // If no cards, redirect or show message
  useEffect(() => {
    if (cards.length === 0) {
      // Could redirect to AI page or show a message
    }
  }, [cards])

  const currentCard = cards[currentIndex]
  const progress = ((currentIndex + 1) / cards.length) * 100

  const handleAnswerSubmit = () => {
    if (!userAnswer.trim()) return

    const userAnswerLower = userAnswer.trim().toLowerCase()
    const correctAnswerLower = currentCard.answer.toLowerCase()
    
    // Simple check: see if user's answer contains key words from correct answer
    // or if it's an exact match
    const isAnswerCorrect = 
      userAnswerLower === correctAnswerLower ||
      correctAnswerLower.includes(userAnswerLower) ||
      userAnswerLower.includes(correctAnswerLower.split(' ')[0]) // First word match

    setIsCorrect(isAnswerCorrect)
    setShowAnswer(true)
    setAnswered(true)
    
    if (isAnswerCorrect) {
      setScore(score + 1)
    }

    // Save answer for review
    setAnswers([...answers, {
      question: currentCard.question,
      userAnswer: userAnswer,
      correctAnswer: currentCard.answer,
      isCorrect: isAnswerCorrect
    }])
  }

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setUserAnswer('')
      setShowAnswer(false)
      setAnswered(false)
      setIsCorrect(false)
    } else {
      setQuizComplete(true)
    }
  }

  const handleRestart = () => {
    setCurrentIndex(0)
    setUserAnswer('')
    setShowAnswer(false)
    setAnswered(false)
    setIsCorrect(false)
    setScore(0)
    setQuizComplete(false)
    setAnswers([])
  }

  const handleNewQuiz = () => {
    navigate('/ai')
  }

  if (cards.length === 0) {
    return (
      <div className="container fade-in">
        <div className="card text-center">
          <h2>📝 No Flashcards Available</h2>
          <p>Generate some flashcards first to start a quiz!</p>
          <button className="btn btn-success mt-3" onClick={() => navigate('/ai')}>
            🧠 Go to AI Playground
          </button>
        </div>
      </div>
    )
  }

  if (quizComplete) {
    const percentage = Math.round((score / cards.length) * 100)
    return (
      <div className="container fade-in">
        <div className="card text-center">
          <div className="card-header">
            <h1 className="card-title">🎉 Quiz Complete!</h1>
            <p className="card-subtitle">Great job completing the quiz</p>
          </div>
          
          <div className="mb-4" style={{ fontSize: '3rem' }}>
            {percentage >= 80 ? '🌟' : percentage >= 60 ? '👍' : '💪'}
          </div>
          
          <div className="mb-4">
            <h2 style={{ fontSize: '2.5rem', margin: '1rem 0' }}>
              {score} / {cards.length}
            </h2>
            <p style={{ fontSize: '1.5rem', color: 'var(--text-secondary)' }}>
              {percentage}% Correct
            </p>
          </div>

          <div className="mb-4">
            {percentage >= 80 && <p style={{ color: 'var(--success-color)' }}>Excellent work! 🎓</p>}
            {percentage >= 60 && percentage < 80 && <p style={{ color: 'var(--accent-color)' }}>Good job! Keep practicing! 📚</p>}
            {percentage < 60 && <p style={{ color: 'var(--warning-color)' }}>Keep studying! You'll get better! 💪</p>}
          </div>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button className="btn btn-success" onClick={handleRestart}>
              🔄 Retake Quiz
            </button>
            <button className="btn" onClick={handleNewQuiz}>
              🧠 New Flashcards
            </button>
          </div>

          {/* Review Section */}
          <div className="mt-5" style={{ textAlign: 'left' }}>
            <h3 className="mb-3">📋 Review Your Answers</h3>
            <div className="grid grid-1">
              {answers.map((answer, idx) => (
                <div key={idx} className="card mb-3" style={{ 
                  borderLeft: `4px solid ${answer.isCorrect ? 'var(--success-color)' : 'var(--error-color)'}` 
                }}>
                  <div className="mb-2">
                    <strong>Q{idx + 1}:</strong> {answer.question}
                  </div>
                  <div className="mb-2" style={{ color: answer.isCorrect ? 'var(--success-color)' : 'var(--error-color)' }}>
                    <strong>Your Answer:</strong> {answer.userAnswer}
                    {answer.isCorrect ? ' ✅' : ' ❌'}
                  </div>
                  {!answer.isCorrect && (
                    <div style={{ color: 'var(--text-secondary)' }}>
                      <strong>Correct Answer:</strong> {answer.correctAnswer}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container fade-in">
      <div className="card mb-4">
        <div className="card-header">
          <h1 className="card-title">📝 Quiz Mode</h1>
          <p className="card-subtitle">Test your knowledge!</p>
        </div>
        
        {/* Progress Bar */}
        <div className="mb-4">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span>Question {currentIndex + 1} of {cards.length}</span>
            <span>Score: {score} / {cards.length}</span>
          </div>
          <div className="progress-bar" style={{ 
            width: '100%', 
            height: '8px', 
            backgroundColor: 'var(--bg-tertiary)', 
            borderRadius: '4px', 
            overflow: 'hidden' 
          }}>
            <div style={{ 
              width: `${progress}%`, 
              height: '100%', 
              background: 'var(--gradient-accent)', 
              transition: 'width 0.3s ease' 
            }}></div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title" style={{ fontSize: '1.5rem' }}>
            {currentCard.question}
          </h2>
        </div>

        {!showAnswer ? (
          <div>
            <label className="form-label">Your Answer:</label>
            <textarea
              className="form-input"
              style={{ minHeight: '120px', fontFamily: 'inherit' }}
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Type your answer here..."
              disabled={answered}
            />
            <div className="mt-3">
              <button 
                className="btn btn-success" 
                onClick={handleAnswerSubmit}
                disabled={!userAnswer.trim() || answered}
              >
                ✓ Submit Answer
              </button>
            </div>
          </div>
        ) : (
          <div>
            <div className={`card mb-3 ${isCorrect ? 'bg-success-color' : 'bg-error-color'}`} style={{ color: 'white' }}>
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>
                {isCorrect ? '✅ Correct!' : '❌ Incorrect'}
              </div>
              <div>
                <strong>Your Answer:</strong> {userAnswer}
              </div>
              {!isCorrect && (
                <div className="mt-2">
                  <strong>Correct Answer:</strong> {currentCard.answer}
                </div>
              )}
            </div>

            <div>
              <button 
                className="btn btn-success" 
                onClick={handleNext}
              >
                {currentIndex < cards.length - 1 ? '➡️ Next Question' : '🏁 Finish Quiz'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

