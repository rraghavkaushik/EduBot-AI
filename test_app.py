import pytest
import json
import tempfile
import os
from app import app, db, User, Document
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    """Create authentication headers for protected endpoints."""
    # Create a test user
    user = User(
        email='test@example.com',
        password_hash=generate_password_hash('password123')
    )
    db.session.add(user)
    db.session.commit()
    
    # Login to get token
    response = client.post('/api/auth/login', 
                          json={'email': 'test@example.com', 'password': 'password123'})
    token = response.json['access_token']
    
    return {'Authorization': f'Bearer {token}'}

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_hello_endpoint(self, client):
        """Test that the hello endpoint returns success."""
        response = client.get('/api/hello')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'Hello from EduBot!' in data['message']

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_user_registration_success(self, client):
        """Test successful user registration."""
        response = client.post('/api/auth/register', 
                             json={'email': 'new@example.com', 'password': 'password123'})
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'registration successful'
    
    def test_user_registration_duplicate_email(self, client):
        """Test registration with duplicate email."""
        # Register first user
        client.post('/api/auth/register', 
                   json={'email': 'duplicate@example.com', 'password': 'password123'})
        
        # Try to register again
        response = client.post('/api/auth/register', 
                             json={'email': 'duplicate@example.com', 'password': 'password123'})
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'email already registered' in data['error']
    
    def test_user_registration_validation(self, client):
        """Test registration validation."""
        # Test short password
        response = client.post('/api/auth/register', 
                             json={'email': 'test@example.com', 'password': '123'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'password must be at least 8 characters' in data['error']
        
        # Test missing email
        response = client.post('/api/auth/register', 
                             json={'password': 'password123'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email and password are required' in data['error']
    
    def test_user_login_success(self, client):
        """Test successful user login."""
        # Register user first
        client.post('/api/auth/register', 
                   json={'email': 'login@example.com', 'password': 'password123'})
        
        # Login
        response = client.post('/api/auth/login', 
                             json={'email': 'login@example.com', 'password': 'password123'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['token_type'] == 'Bearer'
    
    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/api/auth/login', 
                             json={'email': 'nonexistent@example.com', 'password': 'wrong'})
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'invalid credentials' in data['error']

class TestProtectedEndpoints:
    """Test endpoints that require authentication."""
    
    def test_me_endpoint_success(self, client, auth_headers):
        """Test successful access to protected endpoint."""
        response = client.get('/api/me', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'
    
    def test_me_endpoint_no_token(self, client):
        """Test access to protected endpoint without token."""
        response = client.get('/api/me')
        assert response.status_code == 401
    
    def test_me_endpoint_invalid_token(self, client):
        """Test access to protected endpoint with invalid token."""
        response = client.get('/api/me', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 422  # JWT decode error

class TestFileUpload:
    """Test file upload functionality."""
    
    def test_file_upload_success(self, client, auth_headers):
        """Test successful file upload."""
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Test content for upload')
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = client.post('/api/upload', 
                                    headers=auth_headers,
                                    data={'file': (f, 'test.txt')})
            
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['message'] == 'file uploaded and text extracted successfully'
            assert data['file']['original_name'] == 'test.txt'
            assert data['extracted_text_chars'] > 0
            
        finally:
            os.unlink(temp_file_path)
    
    def test_file_upload_no_file(self, client, auth_headers):
        """Test upload without file."""
        response = client.post('/api/upload', headers=auth_headers)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'no file part in the request' in data['error']
    
    def test_file_upload_invalid_type(self, client, auth_headers):
        """Test upload with invalid file type."""
        # Create a temporary file with invalid extension
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jpg', delete=False) as f:
            f.write('Test content')
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = client.post('/api/upload', 
                                    headers=auth_headers,
                                    data={'file': (f, 'test.jpg')})
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'only PDF and TXT files are allowed' in data['error']
            
        finally:
            os.unlink(temp_file_path)

class TestAIEndpoints:
    """Test AI generation endpoints."""
    
    def test_ai_generate_no_prompt(self, client, auth_headers):
        """Test AI generation without prompt."""
        response = client.post('/api/ai/generate', 
                             headers=auth_headers,
                             json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'prompt is required' in data['error']
    
    def test_ai_generate_with_prompt(self, client, auth_headers):
        """Test AI generation with prompt."""
        response = client.post('/api/ai/generate', 
                             headers=auth_headers,
                             json={'prompt': 'Hello, how are you?'})
        # This will likely fail due to missing API key, but we can test the endpoint exists
        assert response.status_code in [400, 500]  # Expected to fail without API key

class TestDatabaseModels:
    """Test database models."""
    
    def test_user_model(self, client):
        """Test User model creation and methods."""
        with app.app_context():
            user = User(
                email='model@example.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.email == 'model@example.com'
            assert user.created_at is not None
            
            # Test to_public_dict method
            public_data = user.to_public_dict()
            assert 'password_hash' not in public_data
            assert public_data['email'] == 'model@example.com'
    
    def test_document_model(self, client):
        """Test Document model creation."""
        with app.app_context():
            user = User(
                email='docuser@example.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            document = Document(
                user_id=user.id,
                original_name='test.pdf',
                stored_name='stored.pdf',
                relative_path='uploads/test.pdf',
                mime_type='application/pdf',
                size_bytes=1024,
                extracted_text='Test extracted text'
            )
            db.session.add(document)
            db.session.commit()
            
            assert document.id is not None
            assert document.user_id == user.id
            assert document.original_name == 'test.pdf'
            assert document.extracted_text == 'Test extracted text'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
