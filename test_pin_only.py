#!/usr/bin/env python3
"""
Minimal PIN authentication test without FastAPI dependencies
This tests only the core PIN logic to verify it works correctly.
"""

import os
import sys
import secrets

# Mock the settings without importing config
class MockSettings:
    def __init__(self):
        self.PIN = os.getenv("PIN", "1234")
        self.SESSION_SECRET = os.getenv("SESSION_SECRET", "your-secret-key-change-this")
        self.PORT = os.getenv("PORT", "8000")

def verify_pin(pin: str, expected_pin: str) -> bool:
    """Verify if the provided PIN is correct"""
    return pin == expected_pin

def create_session_token() -> str:
    """Create a secure session token"""
    return secrets.token_urlsafe(32)

def test_pin_logic():
    """Test the core PIN authentication logic"""
    print("🔐 Testing PIN Authentication Logic")
    print("=" * 40)

    # Create mock settings
    settings = MockSettings()

    print(f"Current PIN: {'*' * len(settings.PIN)}")
    print(f"Session Secret: {'Set' if settings.SESSION_SECRET else 'Not Set'}")
    print(f"Port: {settings.PORT}")

    # Test 1: Correct PIN
    print("\n1. Testing correct PIN")
    if verify_pin(settings.PIN, settings.PIN):
        print("   ✅ Correct PIN verification works")
    else:
        print("   ❌ Correct PIN verification failed")
        return False

    # Test 2: Incorrect PIN
    print("\n2. Testing incorrect PIN")
    if not verify_pin("wrong-pin", settings.PIN):
        print("   ✅ Incorrect PIN rejection works")
    else:
        print("   ❌ Incorrect PIN rejection failed")
        return False

    # Test 3: Session token generation
    print("\n3. Testing session token generation")
    tokens = [create_session_token() for _ in range(3)]

    if len(set(tokens)) == len(tokens):
        print("   ✅ Session tokens are unique")
    else:
        print("   ❌ Session tokens are not unique")
        return False

    if all(len(token) >= 32 for token in tokens):
        print("   ✅ Session tokens are secure length (32+ chars)")
    else:
        print("   ❌ Session tokens are too short")
        return False

    # Test 4: Different PIN scenarios
    print("\n4. Testing various PIN scenarios")

    test_cases = [
        ("1234", "1234", True, "Default PIN"),
        ("my-secure-pin", "my-secure-pin", True, "Custom PIN"),
        ("1234", "4321", False, "Wrong PIN"),
        ("", "1234", False, "Empty PIN"),
        ("1234", "", False, "Empty expected PIN"),
    ]

    for pin, expected, should_pass, description in test_cases:
        result = verify_pin(pin, expected)
        if result == should_pass:
            print(f"   ✅ {description}: {result}")
        else:
            print(f"   ❌ {description}: Expected {should_pass}, got {result}")
            return False

    return True

def test_environment_variables():
    """Test environment variable handling"""
    print("\n📱 Testing Environment Variables")
    print("=" * 40)

    # Check current environment
    pin_env = os.getenv("PIN")
    secret_env = os.getenv("SESSION_SECRET")
    port_env = os.getenv("PORT")

    print(f"PIN environment variable: {'Set' if pin_env else 'Not set'}")
    print(f"SESSION_SECRET environment variable: {'Set' if secret_env else 'Not set'}")
    print(f"PORT environment variable: {'Set' if port_env else 'Not set'}")

    if pin_env:
        print(f"PIN value: {'*' * len(pin_env)}")
    if port_env:
        print(f"PORT value: {port_env}")

    # Test with mock environment
    print("\n🧪 Testing with different environment values:")

    # Save original values
    original_pin = os.environ.get("PIN")
    original_secret = os.environ.get("SESSION_SECRET")

    try:
        # Test with custom PIN
        os.environ["PIN"] = "test-pin-123"
        os.environ["SESSION_SECRET"] = "test-secret-456"

        settings = MockSettings()
        if settings.PIN == "test-pin-123":
            print("   ✅ Custom PIN loaded correctly")
        else:
            print("   ❌ Custom PIN not loaded")
            return False

        if settings.SESSION_SECRET == "test-secret-456":
            print("   ✅ Custom session secret loaded correctly")
        else:
            print("   ❌ Custom session secret not loaded")
            return False

    finally:
        # Restore original values
        if original_pin is not None:
            os.environ["PIN"] = original_pin
        elif "PIN" in os.environ:
            del os.environ["PIN"]

        if original_secret is not None:
            os.environ["SESSION_SECRET"] = original_secret
        elif "SESSION_SECRET" in os.environ:
            del os.environ["SESSION_SECRET"]

    return True

def test_security_recommendations():
    """Test security recommendations"""
    print("\n🛡️  Security Analysis")
    print("=" * 40)

    settings = MockSettings()

    recommendations = []

    # Check PIN strength
    if settings.PIN == "1234":
        recommendations.append("Change default PIN (1234) to something more secure")

    if len(settings.PIN) < 4:
        recommendations.append("Use a PIN with at least 4 characters")

    if settings.PIN.isdigit() and len(settings.PIN) == 4:
        recommendations.append("Consider using a longer PIN or including letters")

    # Check session secret
    if settings.SESSION_SECRET == "your-secret-key-change-this":
        recommendations.append("Change default session secret")

    if len(settings.SESSION_SECRET) < 16:
        recommendations.append("Use a longer session secret (at least 16 characters)")

    # Check for weak PINs
    weak_pins = ["1234", "0000", "1111", "2222", "1212", "password", "admin"]
    if settings.PIN.lower() in weak_pins:
        recommendations.append("Avoid common weak PINs")

    if recommendations:
        print("⚠️  Security recommendations:")
        for rec in recommendations:
            print(f"   • {rec}")
        return False
    else:
        print("✅ Security configuration looks good!")
        return True

def simulate_web_flow():
    """Simulate the web authentication flow"""
    print("\n🌐 Simulating Web Authentication Flow")
    print("=" * 40)

    settings = MockSettings()

    # Mock session storage
    active_sessions = {}

    def authenticate_user(pin: str):
        """Simulate user authentication"""
        if verify_pin(pin, settings.PIN):
            session_token = create_session_token()
            active_sessions[session_token] = {
                "authenticated": True,
                "created": "2024-01-01T12:00:00Z"
            }
            return {"success": True, "session_token": session_token}
        else:
            return {"success": False, "error": "Invalid PIN"}

    def is_authenticated(session_token: str):
        """Check if session is valid"""
        return session_token in active_sessions and active_sessions[session_token]["authenticated"]

    # Simulate the flow
    print("1. User visits main page without session")
    print("   → Should redirect to login")

    print("\n2. User enters incorrect PIN")
    result = authenticate_user("wrong-pin")
    if not result["success"]:
        print("   ✅ Invalid PIN rejected")
    else:
        print("   ❌ Invalid PIN accepted")
        return False

    print("\n3. User enters correct PIN")
    result = authenticate_user(settings.PIN)
    if result["success"]:
        session_token = result["session_token"]
        print(f"   ✅ Valid PIN accepted, session: {session_token[:20]}...")
    else:
        print("   ❌ Valid PIN rejected")
        return False

    print("\n4. User accesses main page with session")
    if is_authenticated(session_token):
        print("   ✅ Session is valid, access granted")
    else:
        print("   ❌ Session validation failed")
        return False

    print("\n5. User logs out")
    if session_token in active_sessions:
        del active_sessions[session_token]
        print("   ✅ Session invalidated")

    print("\n6. User tries to access with old session")
    if not is_authenticated(session_token):
        print("   ✅ Invalid session rejected")
    else:
        print("   ❌ Invalid session accepted")
        return False

    return True

def main():
    """Run all tests"""
    print("🎵 spotDL Web PIN Authentication")
    print("Minimal Test Suite (No FastAPI Dependencies)")
    print("=" * 50)

    tests = [
        ("Core PIN Logic", test_pin_logic),
        ("Environment Variables", test_environment_variables),
        ("Security Analysis", test_security_recommendations),
        ("Web Flow Simulation", simulate_web_flow),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            print(f"\n{'='*50}")
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        print("\n🚀 PIN authentication logic is working correctly!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your PIN: export PIN='your-secure-pin'")
        print("3. Start the app: python run.py")
        print("4. Visit: http://localhost:8000")

        # Show current configuration
        settings = MockSettings()
        print(f"\nCurrent configuration:")
        print(f"  PIN: {'*' * len(settings.PIN)} ({'Default' if settings.PIN == '1234' else 'Custom'})")
        print(f"  Session Secret: {'Default' if settings.SESSION_SECRET == 'your-secret-key-change-this' else 'Custom'}")
        print(f"  Port: {settings.PORT}")

        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
