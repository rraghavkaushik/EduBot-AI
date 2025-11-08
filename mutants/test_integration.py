"""
Integration Tests for EduBot
Tests the integration between multiple components and API endpoints
"""
import pytest
import json
from io import BytesIO
from app import app, db, User, Document
from werkzeug.security import check_password_hash


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
    # Register user
    response = client.post('/api/auth/register', 
                           json={'email': 'test@example.com', 'password': 'testpass123'})
    assert response.status_code == 201
    
    # Login
    response = client.post('/api/auth/login',
                          json={'email': 'test@example.com', 'password': 'testpass123'})
    assert response.status_code == 200
    token = json.loads(response.data)['access_token']
    
    return {'Authorization': f'Bearer {token}'}


class TestUserRegistrationAndLogin:
    """Integration test: User registration and login flow"""
    
    def test_register_then_login_flow(self, client):
        """Test complete registration and login integration"""
        # Register
        response = client.post('/api/auth/register',
                              json={'email': 'newuser@example.com', 'password': 'securepass123'})
        assert response.status_code == 201
        
        # Verify user exists in database
        with app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert check_password_hash(user.password_hash, 'securepass123')
        
        # Login with registered credentials
        response = client.post('/api/auth/login',
                              json={'email': 'newuser@example.com', 'password': 'securepass123'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data


class TestFileUploadAndTextExtraction:
    """Integration test: File upload with text extraction"""
    
    def test_upload_txt_file_integration(self, client, auth_headers):
        """Test uploading a text file and extracting its content"""
        # Create a test file
        test_content = "This is a test document for integration testing."
        file_data = BytesIO(test_content.encode('utf-8'))
        files = {'file': (file_data, 'test.txt')}
        
        # Upload file
        response = client.post('/api/upload',
                              headers=auth_headers,
                              data=files,
                              content_type='multipart/form-data')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        # Verify file was saved
        assert 'file' in data
        assert data['file']['original_name'] == 'test.txt'
        assert data['extracted_text_chars'] > 0
        
        # Verify document in database
        with app.app_context():
            doc = Document.query.filter_by(original_name='test.txt').first()
            assert doc is not None
            assert doc.extracted_text == test_content


class TestAIFeaturesIntegration:
    """Integration test: AI features with authentication"""
    
    def test_summarize_with_auth(self, client, auth_headers):
        """Test AI summarization requires authentication"""
        # Try without auth (should fail)
        response = client.post('/api/ai/summarize',
                              json={'text': 'Test text for summarization'})
        assert response.status_code == 401
        
        # Try with auth (should succeed if API key is set, or fail gracefully)
        response = client.post('/api/ai/summarize',
                              headers=auth_headers,
                              json={'text': 'REST APIs are stateless and use HTTP methods'})
        # Should be 200 (success) or 400 (API key missing) but not 401
        assert response.status_code != 401
    
    def test_flashcards_with_auth(self, client, auth_headers):
        """Test flashcard generation requires authentication"""
        # Try without auth
        response = client.post('/api/ai/flashcards',
                              json={'text': 'Test text for flashcards'})
        assert response.status_code == 401
        
        # Try with auth
        response = client.post('/api/ai/flashcards',
                              headers=auth_headers,
                              json={'text': 'REST APIs are stateless'})
        assert response.status_code != 401


class TestEndToEndWorkflow:
    """End-to-end integration test: Complete user workflow"""
    
    def test_complete_user_workflow(self, client):
        """Test complete workflow: Register -> Login -> Upload -> AI -> Quiz"""
        # Step 1: Register
        response = client.post('/api/auth/register',
                              json={'email': 'workflow@example.com', 'password': 'password123'})
        assert response.status_code == 201
        
        # Step 2: Login
        response = client.post('/api/auth/login',
                              json={'email': 'workflow@example.com', 'password': 'password123'})
        assert response.status_code == 200
        token = json.loads(response.data)['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Step 3: Get user info
        response = client.get('/api/me', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['email'] == 'workflow@example.com'
        
        # Step 4: Upload file
        file_content = 'Sample text for workflow test'
        file_data = BytesIO(file_content.encode('utf-8'))
        files = {'file': (file_data, 'workflow.txt')}
        response = client.post('/api/upload', headers=headers, data=files)
        assert response.status_code == 201
        
        # Step 5: AI summarization (may fail if no API key, but should not be 401)
        response = client.post('/api/ai/summarize',
                              headers=headers,
                              json={'text': 'REST API testing workflow'})
        assert response.status_code != 401  # Should be authenticated


class TestDatabaseIntegration:
    """Integration test: Database operations"""
    
    def test_user_document_relationship(self, client, auth_headers):
        """Test that user-document relationship works correctly"""
        # Upload a file
        file_content = 'Relationship test'
        file_data = BytesIO(file_content.encode('utf-8'))
        files = {'file': (file_data, 'reltest.txt')}
        response = client.post('/api/upload', headers=auth_headers, data=files)
        assert response.status_code == 201
        
        # Verify relationship in database
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user is not None
            assert len(user.documents) > 0
            doc = user.documents[0]
            assert doc.original_name == 'reltest.txt'
            assert doc.user_id == user.id


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

