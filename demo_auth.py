#!/usr/bin/env python3
"""
Demo script for PIN authentication in spotDL Web
This script demonstrates how the PIN authentication system works.
"""

import os
import sys
import secrets
import hashlib
from datetime import datetime, timedelta

# Mock the authentication functions to demonstrate functionality
class MockAuthDemo:
    def __init__(self):
        self.PIN = "1234"  # Default PIN
        self.SESSION_SECRET = "demo-secret-key"
        self.active_sessions = {}

    def verify_pin(self, pin: str) -> bool:
        """Verify if the provided PIN is correct"""
        return pin == self.PIN

    def create_session_token(self) -> str:
        """Create a secure session token"""
        return secrets.token_urlsafe(32)

    def authenticate_user(self, pin: str) -> dict:
        """Authenticate user with PIN and return session info"""
        if self.verify_pin(pin):
            session_token = self.create_session_token()
            self.active_sessions[session_token] = {
                "created": datetime.now(),
                "expires": datetime.now() + timedelta(hours=24),
                "authenticated": True
            }
            return {
                "success": True,
                "session_token": session_token,
                "expires_in": "24 hours"
            }
        else:
            return {
                "success": False,
                "error": "Invalid PIN"
            }

    def is_authenticated(self, session_token: str) -> bool:
        """Check if session token is valid and not expired"""
        if session_token not in self.active_sessions:
            return False

        session = self.active_sessions[session_token]
        if datetime.now() > session["expires"]:
            # Session expired, remove it
            del self.active_sessions[session_token]
            return False

        return session["authenticated"]

    def logout(self, session_token: str) -> bool:
        """Logout and invalidate session"""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return True
        return False

def demo_authentication_flow():
    """Demonstrate the complete authentication flow"""
    print("🎵 spotDL Web Authentication Demo")
    print("=" * 50)

    # Create authentication instance
    auth = MockAuthDemo()

    print("\n1. 🔐 PIN Authentication Setup")
    print(f"   Default PIN: {auth.PIN}")
    print(f"   Session Secret: {auth.SESSION_SECRET[:10]}...")

    print("\n2. 🚫 Testing Invalid PIN")
    result = auth.authenticate_user("wrong-pin")
    print(f"   Result: {result}")

    print("\n3. ✅ Testing Valid PIN")
    result = auth.authenticate_user("1234")
    if result["success"]:
        session_token = result["session_token"]
        print(f"   ✅ Authentication successful!")
        print(f"   📄 Session token: {session_token[:20]}...")
        print(f"   ⏰ Expires in: {result['expires_in']}")

        print("\n4. 🔍 Testing Session Validation")
        if auth.is_authenticated(session_token):
            print("   ✅ Session is valid and active")
        else:
            print("   ❌ Session validation failed")

        print("\n5. 🔒 Testing Logout")
        if auth.logout(session_token):
            print("   ✅ Logout successful")
        else:
            print("   ❌ Logout failed")

        print("\n6. 🔍 Testing Session After Logout")
        if not auth.is_authenticated(session_token):
            print("   ✅ Session properly invalidated after logout")
        else:
            print("   ❌ Session still active after logout")
    else:
        print(f"   ❌ Authentication failed: {result['error']}")

def demo_security_features():
    """Demonstrate security features"""
    print("\n" + "=" * 50)
    print("🛡️  Security Features Demo")
    print("=" * 50)

    auth = MockAuthDemo()

    print("\n1. 🔐 Session Token Security")
    tokens = [auth.create_session_token() for _ in range(3)]
    print("   Generated tokens are unique and secure:")
    for i, token in enumerate(tokens, 1):
        print(f"   Token {i}: {token[:30]}...")

    print(f"\n   ✅ All tokens are unique: {len(set(tokens)) == len(tokens)}")
    print(f"   ✅ All tokens are 32+ chars: {all(len(t) >= 32 for t in tokens)}")

    print("\n2. 🕐 Session Expiration")
    # Create a session
    result = auth.authenticate_user("1234")
    session_token = result["session_token"]

    # Check current status
    print(f"   📅 Session created: {auth.active_sessions[session_token]['created']}")
    print(f"   📅 Session expires: {auth.active_sessions[session_token]['expires']}")
    print(f"   ✅ Session valid: {auth.is_authenticated(session_token)}")

    print("\n3. 🔒 Multiple Sessions")
    # Create multiple sessions
    sessions = []
    for i in range(3):
        result = auth.authenticate_user("1234")
        sessions.append(result["session_token"])

    print(f"   ✅ Created {len(sessions)} concurrent sessions")
    print(f"   ✅ All sessions valid: {all(auth.is_authenticated(s) for s in sessions)}")

    # Logout one session
    auth.logout(sessions[0])
    print(f"   ✅ Logout affects only target session")
    print(f"   ❌ Session 1 valid: {auth.is_authenticated(sessions[0])}")
    print(f"   ✅ Session 2 valid: {auth.is_authenticated(sessions[1])}")
    print(f"   ✅ Session 3 valid: {auth.is_authenticated(sessions[2])}")

def demo_web_integration():
    """Demonstrate how this integrates with the web application"""
    print("\n" + "=" * 50)
    print("🌐 Web Integration Demo")
    print("=" * 50)

    print("\n1. 🔄 Web Application Flow")
    print("   User visits: http://localhost:8000/")
    print("   → No session cookie found")
    print("   → Redirect to: http://localhost:8000/login")
    print("   → User enters PIN on login page")
    print("   → POST to /login with PIN")
    print("   → Server validates PIN")
    print("   → Session token stored in HTTP-only cookie")
    print("   → Redirect to main application")
    print("   → WebSocket connection includes session token")
    print("   → User can now use the application")

    print("\n2. 📱 WebSocket Authentication")
    print("   WebSocket URL: ws://localhost:8000/ws?session_token=<token>")
    print("   → Server validates session token")
    print("   → Connection established if valid")
    print("   → Connection closed with code 4001 if invalid")

    print("\n3. 🔐 Session Management")
    print("   ✅ Sessions last 24 hours")
    print("   ✅ Sessions stored server-side")
    print("   ✅ HTTP-only cookies prevent XSS")
    print("   ✅ Secure logout invalidates sessions")

def demo_configuration():
    """Demonstrate configuration options"""
    print("\n" + "=" * 50)
    print("⚙️  Configuration Demo")
    print("=" * 50)

    print("\n1. 🌍 Environment Variables")
    print("   PIN=your-secure-pin")
    print("   SESSION_SECRET=your-random-secret")
    print("   PORT=8000")

    print("\n2. 🐳 Docker Configuration")
    print("   docker run -p 8000:8000 \\")
    print("     -e PIN=your-secure-pin \\")
    print("     -e SESSION_SECRET=your-secret \\")
    print("     spotdl-web")

    print("\n3. 📄 .env File")
    print("   # Copy .env.example to .env")
    print("   # Edit the values:")
    print("   PIN=your-secure-pin")
    print("   SESSION_SECRET=your-random-secret")

    print("\n4. 🔐 Security Best Practices")
    print("   ✅ Change default PIN (1234)")
    print("   ✅ Use strong session secret")
    print("   ✅ Use HTTPS in production")
    print("   ✅ Regularly rotate credentials")
    print("   ✅ Monitor access logs")

def main():
    """Run all demonstration functions"""
    print("🎵 spotDL Web PIN Authentication")
    print("Complete Demonstration")
    print("=" * 50)

    try:
        demo_authentication_flow()
        demo_security_features()
        demo_web_integration()
        demo_configuration()

        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("Your spotDL Web application now has PIN authentication!")
        print("\n🚀 Next steps:")
        print("1. Set your custom PIN: export PIN='your-secure-pin'")
        print("2. Set session secret: export SESSION_SECRET='your-secret'")
        print("3. Start the app: python run.py")
        print("4. Visit: http://localhost:8000")
        print("5. Enter your PIN to access the downloader")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
