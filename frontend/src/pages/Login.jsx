import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login } from '../services/api'

export default function LoginPage({ setIsAuthenticated }) {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    if (!formData.email) {
      newErrors.email = 'Email is required'
    }

    if (!formData.password) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setMessage('')

    try {
      const response = await login(formData.email, formData.password)
      if (response.data.access_token) {
        setIsAuthenticated(true)
        setMessage('Login successful! Redirecting...')
        setTimeout(() => {
          navigate('/')
        }, 1500)
      }
    } catch (error) {
      setMessage(error.response?.data?.error || 'Login failed. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container fade-in">
      <div className="card" style={{ maxWidth: '500px', margin: '0 auto' }}>
        <div className="card-header">
          <h1 className="card-title">Welcome Back</h1>
          <p className="card-subtitle">Sign in to continue your learning journey with EduBot</p>
        </div>

        {message && (
          <div className={`text-center mb-4 p-3 rounded ${message.includes('successful') ? 'bg-success-color' : 'bg-error-color'}`} style={{ color: 'white' }}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              📧 Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className={`form-input ${errors.email ? 'error' : ''}`}
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email address"
              disabled={isLoading}
            />
            {errors.email && <div className="form-error">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              🔒 Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className={`form-input ${errors.password ? 'error' : ''}`}
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              disabled={isLoading}
            />
            {errors.password && <div className="form-error">{errors.password}</div>}
          </div>

          <button
            type="submit"
            className="btn w-100"
            disabled={isLoading}
            style={{ width: '100%' }}
          >
            {isLoading ? '�� Signing In...' : '🔐 Sign In'}
          </button>
        </form>

        <div className="text-center mt-4">
          <p className="text-secondary">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary" style={{ color: 'var(--primary-color)', textDecoration: 'none' }}>
              Create one here
            </Link>
          </p>
        </div>

        <div className="mt-4 p-3 bg-light rounded">
          <h4 className="mb-2">🔑 Demo Account</h4>
          <p className="text-secondary mb-2">You can test the system with:</p>
          <div className="text-secondary">
            <p><strong>Email:</strong> test@example.com</p>
            <p><strong>Password:</strong> password123</p>
          </div>
        </div>
      </div>
    </div>
  )
}


