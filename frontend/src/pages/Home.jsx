import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getHello } from '../services/api'

export default function Home({ isAuthenticated }) {
  const [message, setMessage] = useState('Loading...')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    getHello()
      .then((res) => {
        setMessage(res.data.message)
        setIsLoading(false)
      })
      .catch(() => {
        setMessage('Welcome to EduBot!')
        setIsLoading(false)
      })
  }, [])

  const features = [
    {
      icon: '📚',
      title: 'Smart Document Processing',
      description: 'Upload PDFs and text files for intelligent text extraction and analysis.'
    },
    {
      icon: '🤖',
      title: 'AI-Powered Learning',
      description: 'Get instant answers and explanations using advanced AI technology.'
    },
    {
      icon: '🔒',
      title: 'Secure & Private',
      description: 'Your documents and data are protected with enterprise-grade security.'
    },
    {
      icon: '📱',
      title: 'Always Accessible',
      description: 'Access your learning materials from anywhere, anytime.'
    }
  ]

  return (
    <div className="fade-in">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1>Transform Your Learning with AI</h1>
          <p>EduBot combines the power of artificial intelligence with educational content to create an unparalleled learning experience.</p>
          <div className="hero-buttons">
            {!isAuthenticated ? (
              <>
                <Link to="/register" className="btn btn-success">
                  🚀 Get Started Free
                </Link>
                <Link to="/login" className="btn btn-secondary">
                  🔐 Sign In
                </Link>
              </>
            ) : (
              <Link to="/upload" className="btn btn-success">
                📤 Upload Document
              </Link>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <div className="card-header mb-5">
            <h2 className="card-title">Why Choose EduBot?</h2>
            <p className="card-subtitle">Discover the features that make learning smarter and more efficient</p>
          </div>
          <div className="grid grid-2">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">
                  {feature.icon}
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mb-5">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">How It Works</h2>
            <p className="card-subtitle">Three simple steps to enhance your learning</p>
          </div>
          <div className="grid grid-3">
            <div className="text-center">
              <div className="feature-icon">📤</div>
              <h3>1. Upload</h3>
              <p>Upload your educational documents in PDF or text format</p>
            </div>
            <div className="text-center">
              <div className="feature-icon">🔍</div>
              <h3>2. Process</h3>
              <p>Our AI extracts and analyzes the content automatically</p>
            </div>
            <div className="text-center">
              <div className="feature-icon">💡</div>
              <h3>3. Learn</h3>
              <p>Get instant answers and insights from your documents</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!isAuthenticated && (
        <section className="container mb-5">
          <div className="card" style={{ background: 'var(--gradient-secondary)', color: 'white' }}>
            <div className="card-header">
              <h2 style={{ color: 'white' }}>Ready to Get Started?</h2>
              <p style={{ color: 'rgba(255,255,255,0.9)' }}>Join thousands of students already using EduBot</p>
            </div>
            <div className="text-center">
              <Link to="/register" className="btn" style={{ background: 'white', color: 'var(--text-primary)' }}>
                ✨ Create Free Account
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* Status Section */}
      <section className="container">
      <div className="card">
          <div className="card-header">
            <h3>System Status</h3>
          </div>
          <div className="text-center">
            <p><strong>Backend Status:</strong> {isLoading ? 'Checking...' : message}</p>
            <div className="mt-3">
              <span className="btn btn-success" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
                ✅ System Online
              </span>
            </div>
          </div>
        </div>
      </section>
      </div>
  )
}


