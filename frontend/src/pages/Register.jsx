import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../services/api'

export default function RegisterPage({ setIsAuthenticated }) {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
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
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long'
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password'
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
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
      await register(formData.email, formData.password)
      setMessage('Registration successful! Redirecting to login...')
      setTimeout(() => {
        navigate('/login')
      }, 2000)
    } catch (error) {
      setMessage(error.response?.data?.error || 'Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container fade-in">
      <div className="card" style={{ maxWidth: '500px', margin: '0 auto' }}>
        <div className="card-header">
          <h1 className="card-title">Create Account</h1>
          <p className="card-subtitle">Join EduBot and start your AI-powered learning journey</p>
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
              placeholder="Create a strong password"
              disabled={isLoading}
            />
            {errors.password && <div className="form-error">{errors.password}</div>}
            <small className="text-secondary">Must be at least 8 characters long</small>
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword" className="form-label">
              🔐 Confirm Password
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              className={`form-input ${errors.confirmPassword ? 'error' : ''}`}
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm your password"
              disabled={isLoading}
            />
            {errors.confirmPassword && <div className="form-error">{errors.confirmPassword}</div>}
          </div>

          <button
            type="submit"
            className="btn w-100"
            disabled={isLoading}
            style={{ width: '100%' }}
          >
            {isLoading ? '🔄 Creating Account...' : '✨ Create Account'}
          </button>
        </form>

        <div className="text-center mt-4">
          <p className="text-secondary">
            Already have an account?{' '}
            <Link to="/login" className="text-primary" style={{ color: 'var(--primary-color)', textDecoration: 'none' }}>
              Sign in here
            </Link>
          </p>
        </div>

        <div className="mt-4 p-3 bg-light rounded">
          <h4 className="mb-2">🎯 What you'll get:</h4>
          <ul className="text-secondary" style={{ listStyle: 'none', padding: 0 }}>
            <li>✅ Free document processing</li>
            <li>✅ AI-powered learning assistance</li>
            <li>✅ Secure file storage</li>
            <li>✅ 24/7 access to your materials</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
