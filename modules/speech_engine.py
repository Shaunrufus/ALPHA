"""
ALPHA Speech Engine
Fixed: reinitializes engine each call to avoid threading crashes
"""

import pyttsx3

def speak(text):
    """Speak text out loud — thread-safe version"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        engine.setProperty('volume', 1.0)

        # Pick a better voice if available
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        print(f"[Alpha speaks]: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[Speech Error] {e}")

def list_voices():
    """List all available voices"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available Voices:")
    for idx, voice in enumerate(voices):
        print(f"  {idx}: {voice.name} — {voice.id}")
    engine.stop()

if __name__ == "__main__":
    list_voices()
    speak("Hello Shaun! Alpha speech engine is working correctly.")