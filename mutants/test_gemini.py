#!/usr/bin/env python3
"""
Test script to verify Gemini API integration
"""
import os
import sys
import requests
import json

BASE_URL = "http://localhost:5001"

def test_gemini_setup():
    """Test if Gemini API key is configured"""
    print("=" * 60)
    print("Testing Gemini API Setup")
    print("=" * 60)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print(f"✅ GEMINI_API_KEY is set: {api_key[:20]}...")
        return True
    else:
        print("❌ GEMINI_API_KEY is NOT set")
        print("   Set it with: export GEMINI_API_KEY='your-key'")
        return False

def test_backend_health():
    """Test if backend is running"""
    print("\n" + "=" * 60)
    print("Testing Backend Health")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/hello", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend is running: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is Flask server running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_authentication():
    """Test user registration and login"""
    print("\n" + "=" * 60)
    print("Testing Authentication")
    print("=" * 60)
    
    # Try to register a test user
    test_email = "gemini_test@example.com"
    test_password = "testpass123"
    
    try:
        # Register
        reg_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": test_email, "password": test_password},
            timeout=5
        )
        
        if reg_response.status_code in [201, 409]:  # 409 = already exists
            print(f"✅ Registration: {'Created' if reg_response.status_code == 201 else 'Already exists'}")
        else:
            print(f"⚠️  Registration returned: {reg_response.status_code}")
        
        # Login
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": test_email, "password": test_password},
            timeout=5
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            if token:
                print(f"✅ Login successful, token: {token[:30]}...")
                return token
            else:
                print("❌ No token in login response")
                return None
        else:
            print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_summarize(token):
    """Test summarization endpoint"""
    print("\n" + "=" * 60)
    print("Testing Summarization (Gemini AI)")
    print("=" * 60)
    
    test_text = "REST APIs are stateless and use standard HTTP methods like GET, POST, PUT, and DELETE."
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/summarize",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get("summary", "")
            print("✅ Summarization successful!")
            print(f"\nGenerated Summary:\n{summary}\n")
            return True
        else:
            print(f"❌ Summarization failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_flashcards(token):
    """Test flashcard generation endpoint"""
    print("\n" + "=" * 60)
    print("Testing Flashcard Generation (Gemini AI)")
    print("=" * 60)
    
    test_text = "REST APIs are stateless and use standard HTTP methods like GET, POST, PUT, and DELETE."
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/flashcards",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            cards = result.get("cards", [])
            print("✅ Flashcard generation successful!")
            print(f"\nGenerated {len(cards)} flashcards:\n")
            for i, card in enumerate(cards, 1):
                print(f"{i}. Q: {card.get('question', 'N/A')}")
                print(f"   A: {card.get('answer', 'N/A')}\n")
            return True
        else:
            print(f"❌ Flashcard generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🚀 EduBot Gemini API Test Suite" + "\n")
    
    # Test 1: API Key
    if not test_gemini_setup():
        print("\n⚠️  Please set GEMINI_API_KEY before continuing")
        sys.exit(1)
    
    # Test 2: Backend
    if not test_backend_health():
        print("\n⚠️  Please start the Flask server: python app.py")
        sys.exit(1)
    
    # Test 3: Authentication
    token = test_authentication()
    if not token:
        print("\n⚠️  Authentication failed. Cannot test AI endpoints.")
        sys.exit(1)
    
    # Test 4: Summarization
    summarize_ok = test_summarize(token)
    
    # Test 5: Flashcards
    flashcards_ok = test_flashcards(token)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"API Key: ✅")
    print(f"Backend: ✅")
    print(f"Authentication: ✅")
    print(f"Summarization: {'✅' if summarize_ok else '❌'}")
    print(f"Flashcards: {'✅' if flashcards_ok else '❌'}")
    
    if summarize_ok and flashcards_ok:
        print("\n🎉 All tests passed! Gemini is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)

