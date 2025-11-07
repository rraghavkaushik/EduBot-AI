import { Link, useNavigate, useLocation } from 'react-router-dom'
import { clearToken, getToken } from '../services/api'

export default function Header({ isAuthenticated, setIsAuthenticated }) {
  const navigate = useNavigate()
  const location = useLocation()

  const logout = () => {
    clearToken()
    setIsAuthenticated(false)
    navigate('/')
  }

  const isActive = (path) => location.pathname === path

  return (
    <header className="navbar">
      <div className="container">
        <div className="brand">
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            🎓 EduBot
          </Link>
        </div>
        <nav className="nav">
          <Link 
            to="/" 
            className={isActive('/') ? 'active' : ''}
          >
            🏠 Home
          </Link>
          <Link 
            to="/ai" 
            className={isActive('/ai') ? 'active' : ''}
          >
            ✨ AI
          </Link>
          <Link 
            to="/quiz" 
            className={isActive('/quiz') ? 'active' : ''}
          >
            📝 Quiz
          </Link>
          {isAuthenticated && (
            <Link 
              to="/upload" 
              className={isActive('/upload') ? 'active' : ''}
            >
              📤 Upload
            </Link>
          )}
          {!isAuthenticated ? (
            <>
              <Link 
                to="/register" 
                className={isActive('/register') ? 'active' : ''}
              >
                ✨ Register
              </Link>
              <Link 
                to="/login" 
                className={isActive('/login') ? 'active' : ''}
              >
                🔐 Login
              </Link>
            </>
          ) : (
            <button className="btn btn-danger" onClick={logout}>
              🚪 Logout
            </button>
          )}
        </nav>
      </div>
    </header>
  )
}


