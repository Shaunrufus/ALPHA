#!/usr/bin/env python3
"""
ALPHA Voice Assistant
Stays active until silence - like Siri/Alexa
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.speech_engine import speak
from modules.wakeword_listener import start_wake_word_detection, stop_wake_word_detection
from modules.voice_listener import listen_for_command
from modules.brain import think, get_friendly_greeting, clear_memory

# Go to sleep after this many seconds of silence
SILENCE_TIMEOUT = 45

is_in_conversation = False


def handle_action(action: dict):
    action_type = action.get("action", "")
    if action_type == "screenshot":
        speak("Taking a screenshot for you.")
        print("[Action] Screenshot requested")
    elif action_type == "open_app":
        app = action.get("app", "that")
        speak(f"Opening {app} for you.")
    elif action_type == "time":
        speak(f"It's {time.strftime('%I:%M %p')}")
    elif action_type == "date":
        speak(f"Today is {time.strftime('%B %d, %Y')}")
    else:
        speak("I understood but that action isn't set up yet.")


def process_command(command: str) -> bool:
    """Returns False to sleep, True to keep listening"""
    if not command or not command.strip():
        return True  # silence — don't reply, just keep waiting

    command_lower = command.lower().strip()

    # Sleep commands
    if any(p in command_lower for p in ["goodbye alpha", "bye alpha", "stop alpha", "go to sleep", "goodbye", "bye"]):
        speak("Going to sleep. Say Hey Jarvis when you need me!")
        return False

    # Clear memory
    if "forget everything" in command_lower or "clear memory" in command_lower:
        clear_memory()
        speak("Done, fresh start!")
        return True

    print(f"[Alpha] Thinking: {command}")
    reply, action = think(command)

    if action:
        handle_action(action)
    elif reply:
        speak(reply)

    return True


def conversation_mode():
    """Stay active until silence timeout or goodbye"""
    global is_in_conversation
    is_in_conversation = True

    speak(get_friendly_greeting())

    last_spoke = time.time()

    while is_in_conversation:
        # Check silence timeout
        silence_duration = time.time() - last_spoke
        remaining = int(SILENCE_TIMEOUT - silence_duration)

        if silence_duration > SILENCE_TIMEOUT:
            speak("Going to sleep. Say Hey Jarvis when you need me!")
            break

        print(f"[Alpha] Listening... (sleeping in {remaining}s of silence)")
        command = listen_for_command()

        if command and command.strip():
            last_spoke = time.time()  # reset timer when user speaks
            should_continue = process_command(command)
            if not should_continue:
                break
        # if empty/silence - just loop back, timer keeps counting

    is_in_conversation = False
    print("[Alpha] Sleeping. Say 'Hey Jarvis' to wake me.")


def main():
    print("=" * 50)
    print("   ALPHA Voice Assistant")
    print("=" * 50)

    speak("Hey Shaun! Alpha is ready. Say Hey Jarvis to wake me up.")
    start_wake_word_detection(conversation_mode)

    try:
        print("\n🎧 Say 'Hey Jarvis' to activate... (Ctrl+C to quit)\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down ALPHA...")
        stop_wake_word_detection()
        speak("Goodbye Shaun!")
        sys.exit(0)


if __name__ == "__main__":
    main()