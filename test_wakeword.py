# test_wakeword.py

from modules.wakeword_listener import start_wake_word_detection
import time

def trigger_action():
    print("🔊 Wake word detected! Ready for command.")

start_wake_word_detection(trigger_action)

# Keep the main program alive so the background thread runs
try:
    while True:
        time.sleep(3)
except KeyboardInterrupt:
    print("\n👋 Exiting wakeword test.")
