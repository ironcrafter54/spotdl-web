#!/usr/bin/env python3
"""
Startup script for spotDL Web Application
This script reads configuration from config.py and starts the server accordingly.
"""

import uvicorn
from config import settings

if __name__ == "__main__":
    print("🎵 Starting spotDL Web Application...")
    print("=" * 50)

    # Configuration display
    print(f"📌 PIN Authentication: {'Enabled' if settings.PIN != '1234' else 'Using Default PIN (Change recommended!)'}")
    print(f"🌐 Server will run on port: 8000")
    print(f"🔐 Session secret configured: {'Yes' if settings.SESSION_SECRET != 'your-secret-key-change-this' else 'Using default (Change recommended!)'}")

    # Security warnings
    if settings.PIN == "1234":
        print("⚠️  WARNING: Using default PIN! Change with: export PIN='your-secure-pin'")

    if settings.SESSION_SECRET == "your-secret-key-change-this":
        print("⚠️  WARNING: Using default session secret! Change with: export SESSION_SECRET='your-secret'")

    print()
    print(f"🚀 Access your app at: http://localhost:8000")
    print("🔑 Login with your PIN to start downloading music")
    print("=" * 50)
    print()

    # Start the FastAPI server
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port="8000",
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("💡 Try:")
        print(f"   1. Check if port 8000 is available")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Try a different port: export PORT='8080'")
