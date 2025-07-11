#!/usr/bin/env python3
"""
Test script to verify that the main app can be imported correctly.
This helps debug Docker import issues.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")

        # Test basic imports
        import fastapi
        print("✓ FastAPI imported successfully")

        import uvicorn
        print("✓ Uvicorn imported successfully")

        # Test local imports
        import main
        print("✓ Main module imported successfully")

        # Test that the app exists
        app = main.app
        print("✓ FastAPI app instance found")

        # Test other local modules
        import spotdl_runner
        print("✓ SpotDL runner imported successfully")

        import add_to_playlist
        print("✓ Add to playlist module imported successfully")

        print("\n✅ All imports successful!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_environment():
    """Check the current environment setup."""
    print("Environment check:")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")

    # Check if required files exist
    required_files = ['main.py', 'spotdl_runner.py', 'add_to_playlist.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"❌ {file} missing")

if __name__ == "__main__":
    print("=== SpotDL Web App Import Test ===\n")

    check_environment()
    print()

    success = test_imports()

    if success:
        print("\n🎉 Ready to run the application!")
        sys.exit(0)
    else:
        print("\n💥 Import test failed!")
        sys.exit(1)
