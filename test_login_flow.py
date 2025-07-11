#!/usr/bin/env python3
"""
Test script to simulate browser login flow and debug session issues
This script mimics what a browser does when logging in to help identify the problem.
"""

import requests
import sys
import os
from urllib.parse import urljoin

def test_login_flow():
    """Test the complete login flow"""

    # Configuration
    base_url = "http://localhost:8000"
    pin = os.getenv("PIN", "1234")

    print("🧪 Testing spotDL Web Login Flow")
    print("=" * 50)
    print(f"Base URL: {base_url}")
    print(f"PIN: {'*' * len(pin)}")

    # Create a session to maintain cookies
    session = requests.Session()

    try:
        # Step 1: Test if server is running
        print("\n1. 🌐 Testing server connection...")
        response = session.get(base_url, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")

        if response.status_code == 302:
            print(f"   ✅ Redirected to: {response.headers.get('Location')}")
        elif response.status_code == 200:
            print("   ⚠️  Got 200 instead of redirect - session might already exist")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            return False

        # Step 2: Access login page
        print("\n2. 🔑 Accessing login page...")
        login_url = urljoin(base_url, "/login")
        response = session.get(login_url)
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.content)}")

        if response.status_code != 200:
            print(f"   ❌ Login page not accessible: {response.status_code}")
            return False

        if "Enter PIN" in response.text:
            print("   ✅ Login page loaded correctly")
        else:
            print("   ❌ Login page content unexpected")
            return False

        # Step 3: Submit PIN
        print("\n3. 🔐 Submitting PIN...")
        login_data = {"pin": pin}
        response = session.post(login_url, data=login_data, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")

        if response.status_code == 302:
            print(f"   ✅ PIN accepted, redirecting to: {response.headers.get('Location')}")

            # Check if cookie was set
            cookies = session.cookies.get_dict()
            print(f"   🍪 Cookies after login: {cookies}")

            if "session_token" in cookies:
                print(f"   ✅ Session cookie set: {cookies['session_token'][:20]}...")
            else:
                print("   ❌ No session cookie found")
                return False

        elif response.status_code == 401:
            print("   ❌ PIN rejected - check PIN configuration")
            return False
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            print(f"   Response content: {response.text[:500]}...")
            return False

        # Step 4: Access main page with session
        print("\n4. 🏠 Accessing main page with session...")
        response = session.get(base_url, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("   ✅ Main page accessible - authentication working!")
            if "spotDL Downloader" in response.text:
                print("   ✅ Main page content correct")
            else:
                print("   ⚠️  Main page content unexpected")
        elif response.status_code == 302:
            print(f"   ❌ Still being redirected to: {response.headers.get('Location')}")
            print("   This indicates session validation is failing")
            return False
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            return False

        # Step 5: Test debug endpoint
        print("\n5. 🐛 Testing debug endpoint...")
        debug_url = urljoin(base_url, "/debug")
        response = session.get(debug_url)

        if response.status_code == 200:
            debug_info = response.json()
            print("   ✅ Debug info:")
            for key, value in debug_info.items():
                print(f"     {key}: {value}")
        else:
            print(f"   ❌ Debug endpoint failed: {response.status_code}")

        # Step 6: Test logout
        print("\n6. 🚪 Testing logout...")
        logout_url = urljoin(base_url, "/logout")
        response = session.post(logout_url, allow_redirects=False)
        print(f"   Status: {response.status_code}")

        if response.status_code == 302:
            print("   ✅ Logout successful")

            # Try accessing main page again
            response = session.get(base_url, allow_redirects=False)
            if response.status_code == 302:
                print("   ✅ Properly redirected to login after logout")
            else:
                print("   ❌ Still have access after logout")

        return True

    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed - is the server running?")
        print("   💡 Try: python3 run.py")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_direct_endpoints():
    """Test individual endpoints"""
    print("\n" + "=" * 50)
    print("🔍 Testing Individual Endpoints")
    print("=" * 50)

    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "Main page"),
        ("/login", "Login page"),
        ("/debug", "Debug endpoint"),
    ]

    for endpoint, description in endpoints:
        try:
            print(f"\n📍 Testing {description}: {endpoint}")
            response = requests.get(urljoin(base_url, endpoint), allow_redirects=False)
            print(f"   Status: {response.status_code}")

            if response.status_code == 302:
                print(f"   Redirects to: {response.headers.get('Location')}")
            elif response.status_code == 200:
                print(f"   Content length: {len(response.content)}")

        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection failed")
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    print("🎵 spotDL Web Login Flow Test")
    print("This script simulates what a browser does when logging in")
    print("Use this to debug session/cookie issues")
    print()

    # Test environment
    pin = os.getenv("PIN", "1234")
    if pin == "1234":
        print("⚠️  Using default PIN (1234)")
    else:
        print(f"✅ Using custom PIN ({'*' * len(pin)})")

    success = test_login_flow()

    if not success:
        print("\n🔍 Running individual endpoint tests...")
        test_direct_endpoints()

    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed!")
        print("The login flow is working correctly via HTTP requests.")
        print("If you're still having browser issues, try:")
        print("1. Clear browser cookies and cache")
        print("2. Try incognito/private browsing mode")
        print("3. Check browser developer tools for errors")
        print("4. Try a different browser")
    else:
        print("❌ Some tests failed.")
        print("Check the output above for specific issues.")
        print("Common fixes:")
        print("1. Make sure server is running: python3 run.py")
        print("2. Check PIN configuration: echo $PIN")
        print("3. Verify port is accessible: curl http://localhost:8000")
        print("4. Install dependencies: pip install -r requirements.txt")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
