"""
Regression Tests for EduBot
Tests to ensure existing functionality continues to work after changes
"""
import pytest
import json
from app import app, db, User
from datetime import datetime


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def auth_headers(client):
    """Create a user and return auth headers"""
    client.post('/api/auth/register', 
               json={'email': 'regression@example.com', 'password': 'testpass123'})
    response = client.post('/api/auth/login',
                          json={'email': 'regression@example.com', 'password': 'testpass123'})
    token = json.loads(response.data)['access_token']
    return {'Authorization': f'Bearer {token}'}


class TestAPIEndpointsRegression:
    """Regression tests: Ensure all API endpoints still work"""
    
    def test_hello_endpoint_regression(self, client):
        """Regression: /api/hello should always return success"""
        response = client.get('/api/hello')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'message' in data
    
    def test_register_endpoint_regression(self, client):
        """Regression: Registration should work as before"""
        response = client.post('/api/auth/register',
                              json={'email': 'regtest@example.com', 'password': 'pass123'})
        assert response.status_code == 201
        
        # Try registering again (should fail)
        response = client.post('/api/auth/register',
                              json={'email': 'regtest@example.com', 'password': 'pass123'})
        assert response.status_code == 409
    
    def test_login_endpoint_regression(self, client):
        """Regression: Login should work as before"""
        # Register first
        client.post('/api/auth/register',
                   json={'email': 'logintest@example.com', 'password': 'pass123'})
        
        # Login
        response = client.post('/api/auth/login',
                              json={'email': 'logintest@example.com', 'password': 'pass123'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['token_type'] == 'Bearer'
    
    def test_me_endpoint_regression(self, client, auth_headers):
        """Regression: /api/me should return user info"""
        response = client.get('/api/me', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert 'email' in data['user']


class TestAuthenticationRegression:
    """Regression tests: Authentication should remain secure"""
    
    def test_invalid_credentials_regression(self, client):
        """Regression: Invalid credentials should be rejected"""
        response = client.post('/api/auth/login',
                              json={'email': 'nonexistent@example.com', 'password': 'wrong'})
        assert response.status_code == 401
    
    def test_missing_token_regression(self, client):
        """Regression: Protected endpoints should require token"""
        response = client.get('/api/me')
        assert response.status_code == 401
    
    def test_invalid_token_regression(self, client):
        """Regression: Invalid tokens should be rejected"""
        headers = {'Authorization': 'Bearer invalid_token_here'}
        response = client.get('/api/me', headers=headers)
        assert response.status_code == 422  # JWT decode error


class TestFileUploadRegression:
    """Regression tests: File upload functionality"""
    
    def test_upload_requires_auth_regression(self, client):
        """Regression: Upload should require authentication"""
        files = {'file': ('test.txt', 'content', 'text/plain')}
        response = client.post('/api/upload', data=files)
        assert response.status_code == 401
    
    def test_upload_validates_file_type_regression(self, client, auth_headers):
        """Regression: Only PDF and TXT should be accepted"""
        files = {'file': ('test.exe', 'binary content', 'application/x-msdownload')}
        response = client.post('/api/upload', headers=auth_headers, data=files)
        assert response.status_code == 400
    
    def test_upload_txt_file_regression(self, client, auth_headers):
        """Regression: TXT file upload should work"""
        files = {'file': ('regression.txt', 'Regression test content', 'text/plain')}
        response = client.post('/api/upload', headers=auth_headers, data=files)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'file' in data
        assert data['file']['original_name'] == 'regression.txt'


class TestAIFeaturesRegression:
    """Regression tests: AI features should work consistently"""
    
    def test_summarize_requires_text_regression(self, client, auth_headers):
        """Regression: Summarize should require text parameter"""
        response = client.post('/api/ai/summarize', headers=auth_headers, json={})
        assert response.status_code == 400
    
    def test_flashcards_requires_text_regression(self, client, auth_headers):
        """Regression: Flashcards should require text parameter"""
        response = client.post('/api/ai/flashcards', headers=auth_headers, json={})
        assert response.status_code == 400
    
    def test_ai_endpoints_require_auth_regression(self, client):
        """Regression: AI endpoints should require authentication"""
        response = client.post('/api/ai/summarize', json={'text': 'test'})
        assert response.status_code == 401
        
        response = client.post('/api/ai/flashcards', json={'text': 'test'})
        assert response.status_code == 401


class TestDataModelRegression:
    """Regression tests: Data models should maintain structure"""
    
    def test_user_model_regression(self, client):
        """Regression: User model should have expected fields"""
        client.post('/api/auth/register',
                   json={'email': 'modeltest@example.com', 'password': 'pass123'})
        
        with app.app_context():
            user = User.query.filter_by(email='modeltest@example.com').first()
            assert user is not None
            assert hasattr(user, 'id')
            assert hasattr(user, 'email')
            assert hasattr(user, 'password_hash')
            assert hasattr(user, 'created_at')
            assert isinstance(user.created_at, datetime)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

