#!/usr/bin/env python3
"""
Test script to check Google Gemini API connectivity
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

async def test_gemini_api():
    """Test Gemini API connectivity"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            print("❌ GOOGLE_GEMINI_API_KEY not found in environment variables")
            return False
            
        print(f"🔑 API Key found: {api_key[:10]}...")
        
        # Configure genai
        genai.configure(api_key=api_key)
        
        # Test different model names
        models_to_test = [
            "gemini-1.5-pro",
            "gemini-pro",
            "gemini-1.0-pro"
        ]
        
        for model_name in models_to_test:
            try:
                print(f"🧪 Testing model: {model_name}")
                model = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.7,
                    max_output_tokens=100,
                    convert_system_message_to_human=True
                )
                
                # Test a simple query
                from langchain_core.messages import HumanMessage
                response = await model.agenerate([[HumanMessage(content="Hello, how are you?")]])
                
                if response and response.generations:
                    print(f"✅ Model {model_name} is working!")
                    print(f"📝 Response: {response.generations[0][0].text[:100]}...")
                    return True
                    
            except Exception as e:
                print(f"❌ Model {model_name} failed: {str(e)}")
                continue
        
        print("❌ All models failed to initialize")
        return False
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure langchain-google-genai is installed")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    """Main function"""
    print("🧪 Testing Google Gemini API Connectivity")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('backend/.env'):
        print("❌ backend/.env file not found")
        print("Please run this script from the project root directory")
        return
    
    # Run the test
    success = asyncio.run(test_gemini_api())
    
    if success:
        print("\n🎉 Gemini API is working correctly!")
        print("You can now use the chat functionality in your application.")
    else:
        print("\n💥 Gemini API test failed!")
        print("Please check:")
        print("1. Your API key is correct")
        print("2. You have access to Gemini API")
        print("3. Your API key has the necessary permissions")
        print("4. You're not hitting rate limits")

if __name__ == "__main__":
    main()
