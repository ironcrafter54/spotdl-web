#!/usr/bin/env python3
"""
Simple test for PIN authentication functionality
This test verifies that the PIN authentication system works correctly.
"""

import os
import sys
import tempfile
import subprocess
import time

from config import settings

def test_pin_authentication():
    """Test PIN authentication functionality"""
    print("🔐 Testing PIN authentication...")

    # Test 1: Verify PIN configuration
    print(f"   📌 Current PIN: {'*' * len(settings.PIN)}")
    print(f"   🔑 Session secret configured: {'Yes' if settings.SESSION_SECRET else 'No'}")

    # Test 2: Verify PIN validation function
    try:
        from main import verify_pin, create_session_token

        # Test correct PIN
        if verify_pin(settings.PIN):
            print("   ✅ PIN verification works correctly")
        else:
            print("   ❌ PIN verification failed")
            return False

        # Test incorrect PIN
        if not verify_pin("wrong-pin"):
            print("   ✅ Invalid PIN rejection works correctly")
        else:
            print("   ❌ Invalid PIN rejection failed")
            return False

        # Test session token generation
        token = create_session_token()
        if token and len(token) > 10:
            print("   ✅ Session token generation works")
        else:
            print("   ❌ Session token generation failed")
            return False

    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Authentication test failed: {e}")
        return False

    return True

def test_environment_variables():
    """Test environment variable configuration"""
    print("🌍 Testing environment variables...")

    # Check if PIN is set to default
    if settings.PIN == "1234":
        print("   ⚠️  WARNING: Using default PIN (1234) - change this for security!")
    else:
        print("   ✅ Custom PIN configured")

    # Check if session secret is set to default
    if settings.SESSION_SECRET == "your-secret-key-change-this":
        print("   ⚠️  WARNING: Using default session secret - change this for security!")
    else:
        print("   ✅ Custom session secret configured")

    # Check port configuration
    try:
        port = int(settings.PORT)
        if 1024 <= port <= 65535:
            print(f"   ✅ Valid port configured: {port}")
        else:
            print(f"   ⚠️  Port {port} may not be valid")
    except ValueError:
        print(f"   ❌ Invalid port configuration: {settings.PORT}")
        return False

    return True

def test_security_recommendations():
    """Test security recommendations"""
    print("🛡️  Security recommendations:")

    recommendations = []

    # Check PIN strength
    if len(settings.PIN) < 4:
        recommendations.append("Use a PIN with at least 4 characters")
    elif settings.PIN.isdigit() and len(settings.PIN) == 4:
        recommendations.append("Consider using a longer PIN or include letters")

    # Check session secret strength
    if len(settings.SESSION_SECRET) < 16:
        recommendations.append("Use a longer session secret (at least 16 characters)")

    # Check for common weak PINs
    weak_pins = ["1234", "0000", "1111", "2222", "1212", "1010"]
    if settings.PIN in weak_pins:
        recommendations.append("Avoid common PINs like 1234, 0000, etc.")

    if recommendations:
        print("   ⚠️  Security recommendations:")
        for rec in recommendations:
            print(f"     • {rec}")
    else:
        print("   ✅ Basic security checks passed")

    return len(recommendations) == 0

def test_imports():
    """Test that all authentication-related imports work"""
    print("📦 Testing imports...")

    try:
        from main import (
            verify_pin, create_session_token, get_session_token,
            is_authenticated, active_sessions
        )
        print("   ✅ All authentication functions imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("🧪 spotDL Web Authentication Tests")
    print("=" * 40)

    tests = [
        ("Import Test", test_imports),
        ("Environment Variables", test_environment_variables),
        ("PIN Authentication", test_pin_authentication),
        ("Security Recommendations", test_security_recommendations),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"   ✅ {test_name} passed")
            else:
                print(f"   ❌ {test_name} failed")
        except Exception as e:
            print(f"   ❌ {test_name} failed with error: {e}")

    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All authentication tests passed!")
        print("\n🚀 Your spotDL Web app is ready to use securely!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
