#!/usr/bin/env python3
"""
Simple test script to verify PIN authentication is working
"""

import sys
import os

def test_config():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")

    try:
        from config import settings
        print(f"   ✅ PIN: {'*' * len(settings.PIN)}")
        print(f"   ✅ Port: {settings.PORT}")
        print(f"   ✅ Session Secret: {'Set' if settings.SESSION_SECRET else 'Not Set'}")
        return True
    except Exception as e:
        print(f"   ❌ Config error: {e}")
        return False

def test_main_imports():
    """Test main application imports"""
    print("\n📦 Testing Main Application...")

    try:
        from main import verify_pin, create_session_token, active_sessions
        print("   ✅ Authentication functions imported")
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_pin_verification():
    """Test PIN verification function"""
    print("\n🔐 Testing PIN Verification...")

    try:
        from main import verify_pin
        from config import settings

        # Test correct PIN
        if verify_pin(settings.PIN):
            print("   ✅ Correct PIN verification works")
        else:
            print("   ❌ Correct PIN verification failed")
            return False

        # Test incorrect PIN
        if not verify_pin("wrong-pin"):
            print("   ✅ Incorrect PIN rejection works")
        else:
            print("   ❌ Incorrect PIN rejection failed")
            return False

        return True
    except Exception as e:
        print(f"   ❌ PIN verification error: {e}")
        return False

def test_session_tokens():
    """Test session token generation"""
    print("\n🎫 Testing Session Tokens...")

    try:
        from main import create_session_token

        # Generate multiple tokens
        tokens = [create_session_token() for _ in range(3)]

        # Check uniqueness
        if len(set(tokens)) == len(tokens):
            print("   ✅ Session tokens are unique")
        else:
            print("   ❌ Session tokens are not unique")
            return False

        # Check length
        if all(len(token) >= 32 for token in tokens):
            print("   ✅ Session tokens are secure length")
        else:
            print("   ❌ Session tokens are too short")
            return False

        return True
    except Exception as e:
        print(f"   ❌ Session token error: {e}")
        return False

def test_file_access():
    """Test file access"""
    print("\n📄 Testing File Access...")

    try:
        # Test frontend file
        with open("frontend/index.html", "r") as f:
            content = f.read()
            if "spotDL" in content:
                print("   ✅ Frontend file accessible")
            else:
                print("   ❌ Frontend file content invalid")
                return False

        return True
    except Exception as e:
        print(f"   ❌ File access error: {e}")
        return False

def print_debug_info():
    """Print debug information"""
    print("\n🔍 Debug Information:")
    print(f"   Python version: {sys.version}")
    print(f"   Current directory: {os.getcwd()}")
    print(f"   Files in current dir: {os.listdir('.')}")

    # Check environment variables
    print(f"   PIN env var: {'Set' if os.getenv('PIN') else 'Not set'}")
    print(f"   SESSION_SECRET env var: {'Set' if os.getenv('SESSION_SECRET') else 'Not set'}")
    print(f"   PORT env var: {'Set' if os.getenv('PORT') else 'Not set'}")

def main():
    """Run all tests"""
    print("🧪 spotDL Web Simple Test")
    print("=" * 40)

    tests = [
        ("Configuration", test_config),
        ("Main Imports", test_main_imports),
        ("PIN Verification", test_pin_verification),
        ("Session Tokens", test_session_tokens),
        ("File Access", test_file_access),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"   ❌ {test_name} failed")
        except Exception as e:
            print(f"   ❌ {test_name} failed with error: {e}")

    print_debug_info()

    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        print("\n🚀 Try starting the app:")
        print("   python run.py")
        print("   Then visit: http://localhost:8000")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
