#!/usr/bin/env python3
"""
ALPHA Voice Assistant - Main Application
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.speech_engine import speak
from modules.wakeword_listener import start_wake_word_detection, stop_wake_word_detection
from modules.voice_listener import listen_for_command
import time

def process_command(command):
    """Process voice commands"""
    if not command:
        return
    
    command = command.lower()
    
    # Simple command processing
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
    elif "time" in command:
        current_time = time.strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = time.strftime("%B %d, %Y")
        speak(f"Today is {current_date}")
    elif "goodbye" in command or "bye" in command:
        speak("Goodbye! Have a great day!")
        return False  # Signal to exit
    else:
        speak(f"I heard you say: {command}")
    
    return True

def main():
    """Main application loop"""
    print("🎧 ALPHA Voice Assistant Starting...")
    speak("Hello! I am Alpha. Your voice assistant is now ready.")
    
    def command_callback():
        """Called when wake word is detected"""
        speak("Yes, I'm listening.")
        command = listen_for_command()
        return process_command(command)
    
    # Start wake word detection
    start_wake_word_detection(command_callback)
    
    try:
        print("🎧 Listening for wake word... (Press Ctrl+C to exit)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down ALPHA...")
        stop_wake_word_detection()
        speak("Goodbye!")

if __name__ == "__main__":
    main()
