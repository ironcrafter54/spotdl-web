import os

class Settings:
    URL = os.getenv("SECRET_KEY", "default")
    USERNAME = os.getenv("USERNAME", "default")
    PASSWORD = os.getenv("PASSWORD", "passwords")
    PORT = os.getenv("PORT", "4533")

settings = Settings()
