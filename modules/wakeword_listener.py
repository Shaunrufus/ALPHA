# 📂 File: modules/wakeword_listener.py

import threading
import time
from .speech_engine import speak

# ✅ This is the actual wake word detection logic
def detect_wakeword():
    """
    Simulated wake word detection using text input.
    You can later replace this with actual audio-based detection.
    """
    print("🎧 Listening for wake word... (type your input)")
    user_input = input("You: ").lower()
    return "alpha" in user_input  # Change 'alpha' to your desired wake word

# ✅ Wakeword thread controller
wakeword_active = True
wakeword_thread = None

def _wakeword_loop(trigger_callback):
    global wakeword_active
    while wakeword_active:
        if detect_wakeword():
            speak("Yes, I'm listening.")
            trigger_callback()
        time.sleep(0.5)

def start_wake_word_detection(trigger_callback):
    global wakeword_thread, wakeword_active
    wakeword_active = True
    wakeword_thread = threading.Thread(target=_wakeword_loop, args=(trigger_callback,))
    wakeword_thread.daemon = True
    wakeword_thread.start()

def stop_wake_word_detection():
    global wakeword_active
    wakeword_active = False
