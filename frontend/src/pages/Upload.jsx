import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadFile, summarize, generateFlashcards } from '../services/api'
import Flashcard from '../components/Flashcard'

// Default Software Engineering text used when no file text is provided
const REST_BEST_PRACTICES = `REST API best practices include statelessness, clear resource-oriented URIs, use of standard HTTP methods and status codes, pagination for large collections, consistent error formats, authentication and authorization mechanisms like OAuth 2.0 or JWT, idempotency for PUT/DELETE, and versioning to manage breaking changes.`

export default function UploadPage({ isAuthenticated }) {
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [message, setMessage] = useState('')
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const [tab, setTab] = useState('standard') // 'standard' | 'ai'
  const [previewText, setPreviewText] = useState('')
  const [summary, setSummary] = useState('')
  const [cards, setCards] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isAuthenticated) {
    return (
      <div className="container fade-in">
        <div className="card text-center">
          <h2>🔒 Authentication Required</h2>
          <p>Please log in to access the upload functionality.</p>
        </div>
      </div>
    )
  }

  const handleFileSelect = (file) => {
    if (!file) return
    setSelectedFile(file)
    setMessage('')

    // Read text for .txt, though AI tab will use REST topic regardless
    if (file.type === 'text/plain') {
      const reader = new FileReader()
      reader.onload = (e) => setPreviewText(e.target.result || '')
      reader.readAsText(file)
    } else {
      setPreviewText('')
    }
    setSummary('')
    setCards([])
  }

  const handleDragOver = (e) => { e.preventDefault(); setIsDragOver(true) }
  const handleDragLeave = (e) => { e.preventDefault(); setIsDragOver(false) }
  const handleDrop = (e) => { e.preventDefault(); setIsDragOver(false); const files = e.dataTransfer.files; if (files.length > 0) handleFileSelect(files[0]) }
  const handleFileInput = (e) => { const f = e.target.files[0]; if (f) handleFileSelect(f) }

  const handleUpload = async () => {
    if (!selectedFile) return setMessage('Please select a file to upload.')
    setIsUploading(true); setUploadProgress(0); setMessage('')
    try {
      const formData = new FormData(); formData.append('file', selectedFile)
      const progressInterval = setInterval(() => setUploadProgress(p => p >= 90 ? 90 : p + 10), 200)
      const response = await uploadFile(formData)
      clearInterval(progressInterval); setUploadProgress(100)
      setUploadedFiles(prev => [response.data.file, ...prev])
      setMessage('File uploaded successfully! Text extraction completed.')
      setSelectedFile(null); setPreviewText(''); fileInputRef.current && (fileInputRef.current.value = '')
      setTimeout(() => setMessage(''), 5000)
    } catch (error) {
      setMessage(error.response?.data?.error || 'Upload failed. Please try again.')
    } finally { setIsUploading(false); setUploadProgress(0) }
  }

  // Always use REST API best practices as the topic for AI tab outputs
  const effectiveText = REST_BEST_PRACTICES

  const handleAISummary = async () => {
    setIsLoading(true)
    setError('')
    try {
      const res = await summarize(effectiveText)
      setSummary(res.summary)
    } catch (e) {
      setError('Failed to summarize. ' + (e.message || ''))
    } finally {
      setIsLoading(false)
    }
  }

  const handleAICards = async () => {
    setIsLoading(true)
    setError('')
    try {
      const res = await generateFlashcards(effectiveText)
      setCards(res.cards || res.flashcards || [])
    } catch (e) {
      setError('Failed to generate flashcards. ' + (e.message || ''))
    } finally {
      setIsLoading(false)
    }
  }

  const onSwitchTab = (next) => {
    setTab(next)
    if (next === 'ai') {
      setSummary('')
      setCards([])
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown'
    const k = 1024; const sizes = ['Bytes', 'KB', 'MB', 'GB']; const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (mimeType) => {
    if (mimeType === 'application/pdf') return '📄'
    if (mimeType === 'text/plain') return '📝'
    return '📁'
  }

  return (
    <div className="container fade-in">
      <div className="card-header text-center mb-4">
        <h1 className="card-title">📤 Upload Documents</h1>
        <p className="card-subtitle">Upload normally or generate a summary and flashcards</p>
      </div>

      <div className="card mb-4" style={{ display: 'flex', gap: '12px' }}>
        <button className={`btn ${tab === 'standard' ? '' : 'btn-secondary'}`} onClick={() => onSwitchTab('standard')}>Standard Upload</button>
        <button className={`btn ${tab === 'ai' ? '' : 'btn-secondary'}`} onClick={() => onSwitchTab('ai')}>Summary & Flashcards</button>
      </div>

      <div className="card mb-4">
        <div
          className={`upload-area ${isDragOver ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="upload-icon">📁</div>
          <h3>Drop your file here or click to browse</h3>
          <p className="text-secondary">Supports PDF and text files up to 16MB</p>
          <input ref={fileInputRef} type="file" accept=".pdf,.txt" onChange={handleFileInput} style={{ display: 'none' }} />
        </div>
      </div>

      {selectedFile && (
        <div className="card mb-4">
          <h3>📋 Selected File</h3>
          <div className="file-item">
            <div className="file-info">
              <div className="file-icon">{getFileIcon(selectedFile.type)}</div>
              <div>
                <h4>{selectedFile.name}</h4>
                <p className="text-secondary">Size: {formatFileSize(selectedFile.size)} | Type: {selectedFile.type || 'Unknown'}</p>
              </div>
            </div>
            {tab === 'standard' ? (
              <button className="btn btn-success" onClick={handleUpload} disabled={isUploading}>🚀 Upload & Process</button>
            ) : (
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <button className="btn btn-success" onClick={handleAISummary} disabled={isLoading}>📝 Summarize</button>
                <button className="btn" onClick={handleAICards} disabled={isLoading}>🎴 Flashcards</button>
              </div>
            )}
          </div>
        </div>
      )}

      {tab === 'standard' && (
        <>
          {isUploading && (
            <div className="card mb-4">
              <h3>🔄 Uploading...</h3>
              <div className="mb-3">
                <div className="progress-bar" style={{ width: '100%', height: '20px', backgroundColor: 'var(--bg-tertiary)', borderRadius: '10px', overflow: 'hidden' }}>
                  <div style={{ width: `${uploadProgress}%`, height: '100%', background: 'var(--gradient-accent)', transition: 'width 0.3s ease' }}></div>
                </div>
                <p className="text-center mt-2">{uploadProgress}% Complete</p>
              </div>
            </div>
          )}

          {message && (
            <div className={`card text-center mb-4 ${message.includes('successfully') ? 'bg-success-color' : 'bg-error-color'}`} style={{ color: 'white' }}>
              {message}
            </div>
          )}

          {uploadedFiles.length > 0 && (
            <div className="card">
              <h3>📚 Your Documents</h3>
              <div className="file-list">
                {uploadedFiles.map((file) => (
                  <div key={file.id} className="file-item">
                    <div className="file-info">
                      <div className="file-icon">{getFileIcon(file.mime_type)}</div>
                      <div>
                        <h4>{file.original_name}</h4>
                        <p className="text-secondary">Uploaded: {new Date().toLocaleDateString()} | Size: {file.size_bytes ? formatFileSize(file.size_bytes) : 'Unknown'}</p>
                      </div>
                    </div>
                    <div className="text-success">✅ Processed</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {tab === 'ai' && (
        <>
          {error && (
            <div className="card mb-4 bg-error-color" style={{ color: 'white' }}>
              <p>{error}</p>
            </div>
          )}
          {summary && (
            <div className="card mb-4">
              <div className="card-header">
                <h2 className="card-title">📝 Summary</h2>
                <p className="card-subtitle">Key points</p>
              </div>
              <ul style={{ marginLeft: '1rem' }}>
                {summary.split('\n').map((line, idx) => (line.trim() ? <li key={idx} style={{ marginBottom: '6px' }}>{line}</li> : null))}
              </ul>
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
        </>
      )}
    </div>
  )
}


