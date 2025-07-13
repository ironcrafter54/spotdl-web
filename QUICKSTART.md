# 🚀 Quick Start Guide - PIN Authentication

This guide will help you set up PIN authentication for your spotDL Web application in just a few minutes.

## 📋 Prerequisites

- Python 3.11+ installed
- Basic terminal/command line knowledge
- Port 8000 available (or choose a different port)

## 🔧 Quick Setup (5 minutes)

### Step 1: Configure Your PIN

**Option A: Environment Variables (Recommended)**
```bash
# Set your custom PIN (change from default 1234)
export PIN="your-secure-pin"

# Set a secure session secret
export SESSION_SECRET="your-random-secret-key"

# Optional: Set custom port (default is 8000)
export PORT="8000"
```

**Option B: Create .env File**
```bash
# Copy the example file
cp .env.example .env

# Edit the file and change the values
# PIN=your-secure-pin
# SESSION_SECRET=your-random-secret-key
```

### Step 2: Generate Secure Session Secret

```bash
# Generate a secure session secret
python3 -c "import secrets; print('SESSION_SECRET=' + secrets.token_urlsafe(32))"
```

### Step 3: Start the Application

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the application
python3 run.py
```

### Step 4: Access the Application

1. Open your browser and go to: **http://localhost:8000**
2. You'll see the PIN login page
3. Enter your PIN (default: `1234`)
4. Click "Access spotDL" to continue
5. You're now in the main application!

## 🐳 Docker Quick Start

```bash
# Build and run with custom PIN
docker build -t spotdl-web .
docker run -p 8000:8000 \
  -e PIN="your-secure-pin" \
  -e SESSION_SECRET="your-random-secret" \
  -v ./downloads:/app/downloads \
  spotdl-web
```

## 🔐 Security Checklist

Before using in production, make sure you:

- [ ] **Change the default PIN** from `1234` to something secure
- [ ] **Set a strong session secret** (at least 32 characters)
- [ ] **Use HTTPS** in production environments
- [ ] **Regularly rotate** your PIN and session secret
- [ ] **Monitor access logs** for suspicious activity

## 🎯 PIN Security Tips

### Good PINs:
- `MyMusic2024!` (mix of letters, numbers, symbols)
- `spotDL-secure-789` (descriptive but unique)
- `Music$Download$2024` (themed and secure)

### Avoid:
- `1234` (default - too common)
- `0000` (too simple)
- `password` (too obvious)
- Your birthday or personal info

## 🔄 Usage Flow

1. **First Visit**: Enter PIN → Access granted for 24 hours
2. **Return Visits**: Automatic access (session remembered)
3. **After 24 Hours**: Re-enter PIN for new session
4. **Logout**: Click "Logout" to end session immediately

## 🛠️ Troubleshooting

### "Invalid PIN" Error
- Check your PIN configuration: `echo $PIN`
- Verify you're using the correct PIN
- Try restarting the application

### "Connection Failed" Error
- Check if the application is running: `python3 run.py`
- Verify the port is available: `netstat -an | grep 8000`
- Try a different port: `export PORT="8080"`

### Session Not Working
- Clear browser cookies and try again
- Check session secret is set: `echo $SESSION_SECRET`
- Restart the application

## 📱 Mobile Access

The PIN authentication works on mobile devices too:
- Same URL: `http://your-server:8000`
- Mobile-friendly login page
- Touch-friendly interface

## 🔧 Advanced Configuration

### Custom Session Duration
Edit `main.py` and change the cookie `max_age`:
```python
response.set_cookie(
    key="session_token",
    value=session_token,
    max_age=3600 * 12,  # 12 hours instead of 24
    httponly=True,
    secure=False,
    samesite="lax"
)
```

### Multiple PINs (for teams)
You can extend the PIN verification to support multiple PINs:
```python
def verify_pin(pin: str) -> bool:
    allowed_pins = ["admin-pin", "user-pin", "guest-pin"]
    return pin in allowed_pins
```

## 🆘 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your configuration with: `python3 test_auth.py`
3. Try the demo: `python3 demo_auth.py`
4. Check the main README.md for detailed documentation

## 🎉 You're Ready!

Your spotDL Web application is now secured with PIN authentication. Users will need to enter the PIN to access the downloader, keeping your service protected from unauthorized access.

**Next Steps:**
- Share the URL and PIN with authorized users
- Monitor usage through the application logs
- Consider setting up HTTPS for production use
- Regularly update your PIN and session secret

---

*Happy downloading! 🎵*