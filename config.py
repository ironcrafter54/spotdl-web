import os

class Settings:
    URL = os.getenv("SECRET_KEY", "default")
    USERNAME = os.getenv("USERNAME", "default")
    PASSWORD = os.getenv("PASSWORD", "passwords")
    NAVIDROME_PORT = os.getenv("PORT", "8000")
    PIN = os.getenv("PIN", "1234")  # Default PIN, should be changed via environment variable
    SESSION_SECRET = os.getenv("SESSION_SECRET", "your-secret-key-change-this")

settings = Settings()
