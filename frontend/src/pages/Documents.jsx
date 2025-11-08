import { useState, useEffect } from 'react'
import { getDocuments, deleteDocument, getDocument } from '../services/api'

export default function DocumentsPage({ isAuthenticated }) {
  const [documents, setDocuments] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [selectedDoc, setSelectedDoc] = useState(null)
  const [showViewer, setShowViewer] = useState(false)

  useEffect(() => {
    if (isAuthenticated) {
      loadDocuments()
    }
  }, [isAuthenticated])

  const loadDocuments = async () => {
    setIsLoading(true)
    setError('')
    try {
      const response = await getDocuments()
      setDocuments(response.data.documents || [])
    } catch (e) {
      setError('Failed to load documents. ' + (e.response?.data?.error || e.message))
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (docId, docName) => {
    if (!window.confirm(`Are you sure you want to delete "${docName}"?`)) {
      return
    }

    try {
      await deleteDocument(docId)
      setMessage(`Document "${docName}" deleted successfully`)
      loadDocuments() // Reload list
      setTimeout(() => setMessage(''), 3000)
    } catch (e) {
      setError('Failed to delete document. ' + (e.response?.data?.error || e.message))
    }
  }

  const handleView = async (docId) => {
    try {
      const response = await getDocument(docId)
      setSelectedDoc(response.data.document)
      setShowViewer(true)
    } catch (e) {
      setError('Failed to load document. ' + (e.response?.data?.error || e.message))
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getFileIcon = (mimeType) => {
    if (mimeType === 'application/pdf') return '📄'
    if (mimeType === 'text/plain') return '📝'
    return '📁'
  }

  if (!isAuthenticated) {
    return (
      <div className="container fade-in">
        <div className="card text-center">
          <h2>🔒 Authentication Required</h2>
          <p>Please log in to view your documents.</p>
        </div>
      </div>
    )
  }

  if (showViewer && selectedDoc) {
    return (
      <div className="container fade-in">
        <div className="card mb-4">
          <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h1 className="card-title">{selectedDoc.original_name}</h1>
              <p className="card-subtitle">
                {formatFileSize(selectedDoc.size_bytes)} • {formatDate(selectedDoc.created_at)}
              </p>
            </div>
            <button className="btn btn-secondary" onClick={() => { setShowViewer(false); setSelectedDoc(null) }}>
              ← Back to List
            </button>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2 className="card-title">📄 Extracted Text</h2>
            <p className="card-subtitle">{selectedDoc.extracted_text_length} characters</p>
          </div>
          <div style={{ 
            maxHeight: '600px', 
            overflowY: 'auto', 
            padding: '1rem',
            backgroundColor: 'var(--bg-secondary)',
            borderRadius: '8px',
            whiteSpace: 'pre-wrap',
            fontFamily: 'monospace',
            fontSize: '0.9rem',
            lineHeight: '1.6'
          }}>
            {selectedDoc.extracted_text || 'No text extracted from this document.'}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container fade-in">
      <div className="card-header mb-4">
        <h1 className="card-title">📚 My Documents</h1>
        <p className="card-subtitle">View and manage your uploaded documents</p>
      </div>

      {message && (
        <div className="card mb-4 bg-success-color" style={{ color: 'white' }}>
          {message}
        </div>
      )}

      {error && (
        <div className="card mb-4 bg-error-color" style={{ color: 'white' }}>
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="card text-center">
          <div className="loading-spinner" style={{ margin: '2rem auto' }}></div>
          <p>Loading documents...</p>
        </div>
      ) : documents.length === 0 ? (
        <div className="card text-center">
          <h2>📭 No Documents Yet</h2>
          <p>Upload your first document to get started!</p>
          <a href="/upload" className="btn btn-success mt-3">
            📤 Upload Document
          </a>
        </div>
      ) : (
        <div className="card">
          <div className="file-list">
            {documents.map((doc) => (
              <div key={doc.id} className="file-item">
                <div className="file-info">
                  <div className="file-icon">{getFileIcon(doc.mime_type)}</div>
                  <div>
                    <h4>{doc.original_name}</h4>
                    <p className="text-secondary">
                      {formatFileSize(doc.size_bytes)} • {formatDate(doc.created_at)} • {doc.extracted_text_length} chars
                    </p>
                  </div>
                </div>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  <button 
                    className="btn" 
                    onClick={() => handleView(doc.id)}
                  >
                    👁️ View
                  </button>
                  <button 
                    className="btn btn-danger" 
                    onClick={() => handleDelete(doc.id, doc.original_name)}
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

