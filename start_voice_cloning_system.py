#!/usr/bin/env python3
"""
Voice Cloning System Startup Script
This script will help you start the voice cloning system and test it
"""

import subprocess
import time
import sys
import os

def start_server():
    """Start the voice cloning server."""
    print("🚀 Starting Voice Cloning Server...")
    print("=" * 50)
    
    # Change to server directory
    os.chdir("server")
    
    # Start the server
    try:
        print("📡 Starting server on http://localhost:8000")
        print("💡 Keep this terminal open - the server is running here")
        print("=" * 50)
        
        # Start uvicorn server
        subprocess.run([
            "python", "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def show_testing_instructions():
    """Show testing instructions."""
    print("\n" + "="*60)
    print("🧪 TESTING INSTRUCTIONS")
    print("="*60)
    
    print("\n📋 STEP 1: Start the Server")
    print("   Run this script to start the server")
    print("   Server will be available at: http://localhost:8000")
    
    print("\n📋 STEP 2: Test in Swagger UI")
    print("   Open: http://localhost:8000/docs")
    print("   Test these endpoints:")
    print("   - /enroll: Upload your voice (recording.wav)")
    print("   - /clone: Clone voice from audio files")
    print("   - /tts: Text-to-speech with cloned voice")
    
    print("\n📋 STEP 3: Test Programmatically")
    print("   In a NEW terminal (keep server running):")
    print("   cd server")
    print("   python test_tts_client.py")
    print("   python app_integration_example.py")
    
    print("\n📋 STEP 4: Test Main Application")
    print("   In another NEW terminal:")
    print("   python main.py")
    print("   Commands:")
    print("   - 'test voice': Test multilingual voice")
    print("   - 'alpha' + math: Test math with voice")
    print("   - 'quit': Exit")
    
    print("\n🌍 MULTILINGUAL SUPPORT:")
    print("   - English (en): Full support")
    print("   - Hindi (hi): Basic support")
    print("   - Telugu (te): Basic support")
    
    print("\n💡 PRO TIPS:")
    print("   - Keep server terminal open")
    print("   - Use different terminals for testing")
    print("   - Check audio output files")
    print("   - Compare original vs cloned voices")

if __name__ == "__main__":
    print("🎤 VOICE CLONING SYSTEM")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        show_testing_instructions()
    else:
        print("Choose an option:")
        print("1. Start server (recommended)")
        print("2. Show testing instructions")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            start_server()
        elif choice == "2":
            show_testing_instructions()
        else:
            print("Invalid choice. Showing instructions...")
            show_testing_instructions()
