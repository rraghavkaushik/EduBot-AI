import { useState } from 'react'

export default function Flashcard({ index, question, answer }) {
  const [flipped, setFlipped] = useState(false)
  return (
    <div className={`flashcard ${flipped ? 'flipped' : ''}`} onClick={() => setFlipped(!flipped)} role="button" tabIndex={0} onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setFlipped(!flipped)}>
      <div className="flashcard-inner">
        <div className="flashcard-face flashcard-front">
          <div className="flashcard-index">Q{index + 1}</div>
          <div className="flashcard-title">{question}</div>
          <div className="flashcard-hint">Tap to reveal</div>
        </div>
        <div className="flashcard-face flashcard-back">
          <div className="flashcard-index">A{index + 1}</div>
          <div className="flashcard-answer">{answer}</div>
          <div className="flashcard-hint">Tap to hide</div>
        </div>
      </div>
    </div>
  )
}

