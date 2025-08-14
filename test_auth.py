#!/usr/bin/env python3
"""
Test script for the AI Finance Advisor authentication system
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_FULL_NAME = "Test User"

def test_authentication():
    """Test the complete authentication flow"""
    print("🧪 Testing AI Finance Advisor Authentication System")
    print("=" * 60)
    
    # Test 1: Register a new user
    print("\n1. Testing User Registration...")
    register_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "full_name": TEST_FULL_NAME
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Name: {user_data['full_name']}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return False
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"   Token type: {token_data['token_type']}")
            print(f"   Expires in: {token_data['expires_in']} seconds")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    # Test 3: Get current user info
    print("\n3. Testing Get Current User...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("✅ Get current user successful!")
            user_info = response.json()
            print(f"   User ID: {user_info['id']}")
            print(f"   Email: {user_info['email']}")
            print(f"   Name: {user_info['full_name']}")
            print(f"   Role: {user_info['role']}")
        else:
            print(f"❌ Get current user failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get current user error: {str(e)}")
        return False
    
    # Test 4: Test protected endpoint (chat)
    print("\n4. Testing Protected Endpoint (Chat)...")
    chat_data = {
        "message": "Hello, how can I save money?",
        "document_ids": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/chat/", json=chat_data, headers=headers)
        if response.status_code == 200:
            print("✅ Protected endpoint access successful!")
            chat_response = response.json()
            print(f"   Response received: {len(chat_response['message'])} characters")
        else:
            print(f"❌ Protected endpoint access failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {str(e)}")
        return False
    
    # Test 5: Test unauthorized access
    print("\n5. Testing Unauthorized Access...")
    try:
        response = requests.post(f"{BASE_URL}/api/chat/", json=chat_data)
        if response.status_code == 401:
            print("✅ Unauthorized access properly blocked!")
        else:
            print(f"❌ Unauthorized access not blocked: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Unauthorized access test error: {str(e)}")
        return False
    
    # Test 6: Update user profile
    print("\n6. Testing User Profile Update...")
    update_data = {
        "full_name": "Updated Test User"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/auth/me", json=update_data, headers=headers)
        if response.status_code == 200:
            print("✅ Profile update successful!")
            updated_user = response.json()
            print(f"   Updated name: {updated_user['full_name']}")
        else:
            print(f"❌ Profile update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile update error: {str(e)}")
        return False
    
    # Test 7: Change password
    print("\n7. Testing Password Change...")
    password_change_data = {
        "current_password": TEST_PASSWORD,
        "new_password": "newpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/change-password", json=password_change_data, headers=headers)
        if response.status_code == 200:
            print("✅ Password change successful!")
        else:
            print(f"❌ Password change failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Password change error: {str(e)}")
        return False
    
    # Test 8: Test login with new password
    print("\n8. Testing Login with New Password...")
    new_login_data = {
        "email": TEST_EMAIL,
        "password": "newpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=new_login_data)
        if response.status_code == 200:
            print("✅ Login with new password successful!")
        else:
            print(f"❌ Login with new password failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login with new password error: {str(e)}")
        return False
    
    # Test 9: Forgot password
    print("\n9. Testing Forgot Password...")
    forgot_password_data = {
        "email": TEST_EMAIL
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json=forgot_password_data)
        if response.status_code == 200:
            print("✅ Forgot password request successful!")
            print("   (Check server logs for reset token)")
        else:
            print(f"❌ Forgot password failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Forgot password error: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All authentication tests passed!")
    print("✅ Authentication system is working correctly")
    return True

def test_health_check():
    """Test if the server is running"""
    print("🏥 Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is healthy and running!")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not accessible: {str(e)}")
        print("   Make sure the backend server is running on http://localhost:8000")
        return False

if __name__ == "__main__":
    print("🚀 AI Finance Advisor Authentication Test Suite")
    print("=" * 60)
    
    # First check if server is running
    if not test_health_check():
        print("\n❌ Cannot proceed with tests - server is not accessible")
        exit(1)
    
    # Run authentication tests
    success = test_authentication()
    
    if success:
        print("\n🎯 Test Summary:")
        print("   ✅ User Registration")
        print("   ✅ User Login")
        print("   ✅ Get Current User")
        print("   ✅ Protected Endpoint Access")
        print("   ✅ Unauthorized Access Blocking")
        print("   ✅ Profile Update")
        print("   ✅ Password Change")
        print("   ✅ Forgot Password")
        print("\n🚀 Authentication system is ready for production!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        exit(1)
