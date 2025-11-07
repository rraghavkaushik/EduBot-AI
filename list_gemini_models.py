#!/usr/bin/env python3
"""List available Gemini models"""
import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not set")
    exit(1)

genai.configure(api_key=api_key)

print("Available Gemini Models:\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print()
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying common model names directly...")
    
    # Try common model names
    common_models = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-latest",
    ]
    
    for model_name in common_models:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✅ {model_name} - Available")
        except Exception as err:
            print(f"❌ {model_name} - {err}")

