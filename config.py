import os

class Settings:
    URL = os.getenv("URL", "default")
    NAVIDROME_USERNAME = os.getenv("NAVIDROME_USERNAME", "default")
    PASSWORD = os.getenv("PASSWORD", "passwords")
    NAVIDROME_PORT = os.getenv("NAVIDROME_PORT", "8000")
    PIN = os.getenv("PIN", "1234")  # Default PIN, should be changed via environment variable
    SESSION_SECRET = os.getenv("SESSION_SECRET", "your-secret-key-change-this")

settings = Settings()
