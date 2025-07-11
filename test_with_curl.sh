#!/bin/bash
# Test script to debug spotDL Web login flow using curl
# This script simulates browser behavior to identify session/cookie issues

echo "🧪 Testing spotDL Web Login Flow with curl"
echo "=================================================="

# Configuration
BASE_URL="http://localhost:8000"
PIN="${PIN:-1234}"
COOKIE_JAR="/tmp/spotdl_cookies.txt"

echo "Base URL: $BASE_URL"
echo "PIN: $(echo $PIN | sed 's/./*/g')"
echo "Cookie jar: $COOKIE_JAR"
echo ""

# Clean up any existing cookies
rm -f "$COOKIE_JAR"

# Test 1: Check server connection
echo "1. 🌐 Testing server connection..."
RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -o /dev/null "$BASE_URL")
HTTP_STATUS=$(echo $RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "   ✅ Server responding (200 OK)"
elif [ "$HTTP_STATUS" -eq 302 ]; then
    echo "   ✅ Server redirecting to login (302 Found)"
elif [ "$HTTP_STATUS" -eq 000 ]; then
    echo "   ❌ Server not responding - is it running?"
    echo "   💡 Try: python3 run.py"
    exit 1
else
    echo "   ⚠️  Unexpected status: $HTTP_STATUS"
fi

# Test 2: Access login page
echo ""
echo "2. 🔑 Accessing login page..."
LOGIN_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -c "$COOKIE_JAR" "$BASE_URL/login")
LOGIN_STATUS=$(echo $LOGIN_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
LOGIN_CONTENT=$(echo $LOGIN_RESPONSE | sed -e 's/HTTPSTATUS:.*//')

if [ "$LOGIN_STATUS" -eq 200 ]; then
    echo "   ✅ Login page accessible (200 OK)"
    if echo "$LOGIN_CONTENT" | grep -q "Enter PIN"; then
        echo "   ✅ Login page content correct"
    else
        echo "   ❌ Login page content unexpected"
        echo "   First 200 chars: $(echo "$LOGIN_CONTENT" | head -c 200)"
    fi
else
    echo "   ❌ Login page not accessible: $LOGIN_STATUS"
    exit 1
fi

# Test 3: Submit PIN
echo ""
echo "3. 🔐 Submitting PIN..."
LOGIN_POST_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -c "$COOKIE_JAR" -b "$COOKIE_JAR" \
    -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "pin=$PIN" \
    "$BASE_URL/login")
LOGIN_POST_STATUS=$(echo $LOGIN_POST_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

if [ "$LOGIN_POST_STATUS" -eq 302 ]; then
    echo "   ✅ PIN accepted (302 Redirect)"

    # Check if cookies were set
    if [ -f "$COOKIE_JAR" ]; then
        echo "   🍪 Cookies after login:"
        cat "$COOKIE_JAR" | grep -v "^#" | while read line; do
            echo "      $line"
        done

        if grep -q "session_token" "$COOKIE_JAR"; then
            echo "   ✅ Session cookie found"
        else
            echo "   ❌ No session cookie found"
        fi
    else
        echo "   ❌ No cookie jar created"
    fi

elif [ "$LOGIN_POST_STATUS" -eq 401 ]; then
    echo "   ❌ PIN rejected (401 Unauthorized)"
    echo "   💡 Check PIN configuration: echo \$PIN"
    exit 1
elif [ "$LOGIN_POST_STATUS" -eq 200 ]; then
    echo "   ❌ PIN rejected (200 OK - error page)"
    echo "   Content preview: $(echo $LOGIN_POST_RESPONSE | sed -e 's/HTTPSTATUS:.*//' | head -c 200)"
    exit 1
else
    echo "   ❌ Unexpected response: $LOGIN_POST_STATUS"
    exit 1
fi

# Test 4: Access main page with session
echo ""
echo "4. 🏠 Accessing main page with session..."
MAIN_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -b "$COOKIE_JAR" "$BASE_URL")
MAIN_STATUS=$(echo $MAIN_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
MAIN_CONTENT=$(echo $MAIN_RESPONSE | sed -e 's/HTTPSTATUS:.*//')

if [ "$MAIN_STATUS" -eq 200 ]; then
    echo "   ✅ Main page accessible (200 OK)"
    if echo "$MAIN_CONTENT" | grep -q "spotDL Downloader"; then
        echo "   ✅ Main page content correct"
        echo "   🎉 Authentication is working!"
    else
        echo "   ⚠️  Main page content unexpected"
        echo "   First 200 chars: $(echo "$MAIN_CONTENT" | head -c 200)"
    fi
elif [ "$MAIN_STATUS" -eq 302 ]; then
    echo "   ❌ Still being redirected (302)"
    echo "   This indicates session validation is failing"

    # Get redirect location
    REDIRECT_LOCATION=$(curl -s -I -b "$COOKIE_JAR" "$BASE_URL" | grep -i "location:" | cut -d' ' -f2- | tr -d '\r\n')
    echo "   Redirect location: $REDIRECT_LOCATION"

    # This is the main issue - let's debug it
    echo ""
    echo "   🐛 DEBUGGING SESSION ISSUE:"
    echo "   This is likely your problem - the session isn't being validated correctly"

else
    echo "   ❌ Unexpected status: $MAIN_STATUS"
fi

# Test 5: Debug endpoint
echo ""
echo "5. 🐛 Testing debug endpoint..."
DEBUG_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -b "$COOKIE_JAR" "$BASE_URL/debug")
DEBUG_STATUS=$(echo $DEBUG_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
DEBUG_CONTENT=$(echo $DEBUG_RESPONSE | sed -e 's/HTTPSTATUS:.*//')

if [ "$DEBUG_STATUS" -eq 200 ]; then
    echo "   ✅ Debug endpoint accessible"
    echo "   Debug info:"
    echo "$DEBUG_CONTENT" | python3 -m json.tool 2>/dev/null || echo "$DEBUG_CONTENT"
else
    echo "   ❌ Debug endpoint failed: $DEBUG_STATUS"
fi

# Test 6: Test logout
echo ""
echo "6. 🚪 Testing logout..."
LOGOUT_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -b "$COOKIE_JAR" -X POST "$BASE_URL/logout")
LOGOUT_STATUS=$(echo $LOGOUT_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

if [ "$LOGOUT_STATUS" -eq 302 ]; then
    echo "   ✅ Logout successful (302 Redirect)"

    # Test access after logout
    AFTER_LOGOUT_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -b "$COOKIE_JAR" "$BASE_URL")
    AFTER_LOGOUT_STATUS=$(echo $AFTER_LOGOUT_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

    if [ "$AFTER_LOGOUT_STATUS" -eq 302 ]; then
        echo "   ✅ Properly redirected after logout"
    else
        echo "   ❌ Still have access after logout: $AFTER_LOGOUT_STATUS"
    fi
else
    echo "   ❌ Logout failed: $LOGOUT_STATUS"
fi

# Summary
echo ""
echo "=================================================="
echo "🎯 SUMMARY"
echo "=================================================="

if [ "$MAIN_STATUS" -eq 200 ]; then
    echo "✅ Authentication is working correctly!"
    echo ""
    echo "If you're still having browser issues, try:"
    echo "1. Clear browser cookies and cache"
    echo "2. Use incognito/private browsing mode"
    echo "3. Check browser developer tools for errors"
    echo "4. Try a different browser"
    echo ""
    echo "The server-side authentication is working fine."
else
    echo "❌ Authentication has issues."
    echo ""
    echo "Common fixes:"
    echo "1. Check server logs for error messages"
    echo "2. Verify PIN: export PIN='your-secure-pin'"
    echo "3. Restart the server: python3 run.py"
    echo "4. Check session secret: export SESSION_SECRET='your-secret'"
    echo ""
    echo "Debug info:"
    echo "- Login POST status: $LOGIN_POST_STATUS"
    echo "- Main page status: $MAIN_STATUS"
    echo "- Session cookie: $(grep -q 'session_token' "$COOKIE_JAR" 2>/dev/null && echo 'Present' || echo 'Missing')"
fi

# Clean up
rm -f "$COOKIE_JAR"

echo ""
echo "🔍 Next steps:"
echo "1. Check the server terminal for debug messages"
echo "2. Compare this output with your browser behavior"
echo "3. If curl works but browser doesn't, it's a browser issue"
echo "4. If both fail, it's a server configuration issue"
