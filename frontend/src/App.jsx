import { useState, useEffect } from 'react'
import './App.css'
import { Route, Routes } from 'react-router-dom'
import Header from './components/Header'
import Home from './pages/Home'
import RegisterPage from './pages/Register'
import LoginPage from './pages/Login'
import UploadPage from './pages/Upload'
import { getToken } from './services/api'
import AIPage from './pages/AI'
import QuizPage from './pages/Quiz'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    setIsAuthenticated(!!token)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <h2>Loading EduBot...</h2>
      </div>
    )
  }

  return (
    <div className="app">
      <Header isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home isAuthenticated={isAuthenticated} />} />
          <Route path="/ai" element={<AIPage />} />
          <Route path="/quiz" element={<QuizPage />} />
          <Route path="/register" element={<RegisterPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/upload" element={<UploadPage isAuthenticated={isAuthenticated} />} />
        </Routes>
      </main>
      <footer className="footer">
        <div className="container">
          <p>&copy; 2025 EduBot. Empowering education through AI.</p>
        </div>
      </footer>
    </div>
  )
}

export default App
