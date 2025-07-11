# 🔧 Troubleshooting Guide - spotDL Web PIN Authentication

This guide addresses common issues when setting up and using PIN authentication with spotDL Web.

## 🚨 Common Issues & Solutions

### Issue 1: "Font download failed" Error in Browser Console

**Error Message:**
```
downloadable font: download failed (font-family: "Roboto" style:normal weight:700 stretch:100 src index:0): status=2152398850
```

**Solution:**
This is a harmless warning. The app has been updated to use system fonts as fallback. You can ignore this error, or to completely fix it:

1. **Quick Fix:** The app now uses system fonts, so this won't affect functionality
2. **Complete Fix:** Clear your browser cache and refresh the page

### Issue 2: PIN Authentication Not Working / Not Proceeding to Main Interface

**Symptoms:**
- Enter PIN, but page doesn't redirect to main application
- Form submits but stays on login page
- No error messages shown

**Solutions:**

#### A. Check Application Status
```bash
# Make sure the app is running
python3 run.py

# You should see output like:
# 🎵 Starting spotDL Web Application...
# 📌 PIN Authentication: Enabled
# 🌐 Server will run on port: 8000
```

#### B. Verify PIN Configuration
```bash
# Check your current PIN
echo $PIN

# If empty, set your PIN
export PIN="your-secure-pin"
```

#### C. Check Browser Developer Tools
1. Open browser developer tools (F12)
2. Go to Console tab
3. Look for error messages
4. Go to Network tab
5. Try logging in again
6. Check if the POST request to `/login` is successful

#### D. Verify Port Access
```bash
# Check if port 8000 is accessible
curl http://localhost:8000

# Or try a different port
export PORT="8080"
python3 run.py
```

### Issue 3: Port 4533 Error (Wrong Port)

**Error Message:**
```
GET http://127.0.0.1:4533/favicon.ico [HTTP/1.1 404 Not Found 0ms]
```

**Solution:**
This happens when the app tries to access the wrong port. 

```bash
# Set correct port
export PORT="8000"

# Or edit config.py to ensure PORT defaults to 8000
# PORT = os.getenv("PORT", "8000")  # Should be 8000, not 4533
```

### Issue 4: Dependencies Not Installed

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
Install the required dependencies:

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn websockets python-multipart
```

### Issue 5: Session/Cookie Issues

**Symptoms:**
- Login successful but immediately redirected back to login
- WebSocket connection fails
- Session not persisting

**Solutions:**

#### A. Clear Browser Data
1. Clear cookies for localhost:8000
2. Clear browser cache
3. Try incognito/private browsing mode

#### B. Check Session Secret
```bash
# Set a proper session secret
export SESSION_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

#### C. Verify Cookie Settings
The app uses HTTP-only cookies. Make sure:
- You're accessing via `http://localhost:8000` (not `https://`)
- No browser extensions are blocking cookies
- Cookies are enabled in your browser

### Issue 6: WebSocket Connection Fails

**Error Message:**
```
WebSocket connection failed
Authentication required
```

**Solution:**
This happens when the session token isn't properly passed to WebSocket.

```bash
# Check browser console for session token
# Should see: "session_token=..." in cookies

# If missing, try:
# 1. Logout and login again
# 2. Clear browser cookies
# 3. Restart the application
```

## 🔍 Debugging Steps

### Step 1: Basic Configuration Test
```bash
# Test without starting the web server
python3 test_pin_only.py

# Should show all tests passing except security warnings
```

### Step 2: Check Application Logs
```bash
# Start with debug logging
python3 run.py

# Look for these messages:
# 🔑 Login page requested
# 🔐 PIN authentication attempt
# ✅ Authentication successful
# 🌐 Main page access attempt
```

### Step 3: Test with curl
```bash
# Test login endpoint
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pin=1234" \
  -v

# Should return 302 redirect with Set-Cookie header
```

### Step 4: Browser Network Analysis
1. Open Developer Tools (F12)
2. Go to Network tab
3. Clear network log
4. Try logging in
5. Check:
   - POST to `/login` returns 302
   - Response has `Set-Cookie` header
   - Browser follows redirect to `/`

## 🛠️ Complete Reset Instructions

If nothing works, try this complete reset:

```bash
# 1. Stop the application (Ctrl+C)

# 2. Clear environment
unset PIN
unset SESSION_SECRET
unset PORT

# 3. Set fresh configuration
export PIN="my-secure-pin-2024"
export SESSION_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
export PORT="8000"

# 4. Clear browser data
# - Clear cookies for localhost
# - Clear cache
# - Close all browser tabs

# 5. Restart application
python3 run.py

# 6. Test with fresh browser window
# Visit: http://localhost:8000
```

## 🔐 Security Checklist

Before reporting issues, verify:

- [ ] Changed default PIN from "1234"
- [ ] Set secure session secret
- [ ] Using correct port (8000)
- [ ] No browser extensions blocking cookies
- [ ] Accessing via HTTP (not HTTPS) for local development
- [ ] Firewall not blocking the port

## 📱 Browser-Specific Issues

### Chrome/Chromium
- Clear Site Data: Developer Tools → Application → Storage → Clear Site Data
- Check: Settings → Privacy → Cookies → Allow all cookies

### Firefox
- Clear Cookies: Developer Tools → Storage → Cookies → Delete All
- Check: about:preferences#privacy → Cookies and Site Data

### Safari
- Clear Cookies: Develop → Empty Caches
- Check: Preferences → Privacy → Cookies and website data

## 🆘 Getting Help

If you're still having issues:

1. **Check the console output** when starting the app
2. **Note the exact error messages** in browser console
3. **Test with curl** to isolate browser issues
4. **Try a different browser** to rule out browser-specific problems
5. **Check if other localhost services work** on different ports

### Information to Collect:
- Operating system
- Browser and version
- Python version
- Complete error messages
- Steps to reproduce
- Console output from the application

## 🎯 Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Font errors | Ignore - app uses system fonts |
| Wrong port | `export PORT="8000"` |
| No dependencies | `pip install -r requirements.txt` |
| PIN not working | Check `echo $PIN` and browser console |
| Session issues | Clear cookies, restart app |
| WebSocket fails | Login again, check session token |

## 📋 Verification Commands

```bash
# Check configuration
python3 -c "from config import settings; print(f'PIN: {len(settings.PIN)} chars, Port: {settings.PORT}')"

# Test authentication logic
python3 test_pin_only.py

# Check if port is available
netstat -an | grep 8000

# Test basic connectivity
curl http://localhost:8000/login
```

Remember: The authentication is working correctly in most cases. Issues are usually related to:
1. Browser cookies/cache
2. Port configuration
3. Environment variables
4. Network connectivity

Start with the simplest solutions first!