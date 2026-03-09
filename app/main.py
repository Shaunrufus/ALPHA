#!/usr/bin/env python3
"""
ALPHA Voice Assistant - Main Application
Now with Groq brain — intelligent responses like Siri/Alexa
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.speech_engine import speak
from modules.wakeword_listener import start_wake_word_detection, stop_wake_word_detection
from modules.voice_listener import listen_for_command
from modules.brain import think, get_friendly_greeting, clear_memory


def handle_action(action: dict):
    """
    Handle PC actions returned by the brain.
    For now these are placeholders — Phase 3 connects to PC Bridge.
    """
    action_type = action.get("action", "")

    if action_type == "screenshot":
        speak("Taking a screenshot for you.")
        # TODO Phase 3: call PC Bridge /screenshot
        print("[Action] Screenshot requested")

    elif action_type == "open_app":
        app = action.get("app", "that app")
        speak(f"Opening {app} for you.")
        # TODO Phase 3: call PC Bridge /shell
        print(f"[Action] Open app: {app}")

    elif action_type == "time":
        current_time = time.strftime("%I:%M %p")
        speak(f"It's {current_time}")

    elif action_type == "date":
        current_date = time.strftime("%B %d, %Y")
        speak(f"Today is {current_date}")

    else:
        speak("I understood the command but that action isn't set up yet.")
        print(f"[Action] Unknown action: {action}")


def process_command(command: str) -> bool:
    """
    Process a voice command through the Groq brain.
    Returns False to exit, True to keep running.
    """
    if not command or not command.strip():
        speak("Sorry, I didn't catch that. Try again.")
        return True

    command_lower = command.lower().strip()

    # Exit commands
    if any(word in command_lower for word in ["goodbye alpha", "bye alpha", "shut down", "stop alpha"]):
        speak("Goodbye Shaun! Talk soon.")
        return False

    # Clear memory command
    if "forget everything" in command_lower or "clear memory" in command_lower:
        clear_memory()
        speak("Done, I've cleared my memory. Fresh start!")
        return True

    print(f"[Alpha] Thinking about: {command}")

    # Send to Groq brain
    reply, action = think(command)

    if action:
        handle_action(action)
    elif reply:
        speak(reply)
    else:
        speak("I'm not sure what to do with that.")

    return True


def command_callback():
    """Called when wake word is detected"""
    # Friendly random greeting like Siri
    greeting = get_friendly_greeting()
    speak(greeting)

    # Listen for the actual command
    command = listen_for_command()

    # Process it
    result = process_command(command)
    return result


def main():
    """Main application loop"""
    print("=" * 50)
    print("   ALPHA Voice Assistant — Starting Up")
    print("=" * 50)

    speak("Hey Shaun! Alpha is ready. Just say Alpha to wake me up.")

    # Start wake word detection
    start_wake_word_detection(command_callback)

    try:
        print("\n🎧 Say 'Alpha' to activate... (Ctrl+C to quit)\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down ALPHA...")
        stop_wake_word_detection()
        speak("Goodbye Shaun!")
        sys.exit(0)


if __name__ == "__main__":
    main()