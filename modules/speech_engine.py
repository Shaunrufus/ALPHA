import pyttsx3
import threading

engine = pyttsx3.init()
lock = threading.Lock()  # 🔐 Lock to prevent simultaneous access

def list_voices():
    voices = engine.getProperty('voices')
    print("🔊 Available Voices:")
    for idx, voice in enumerate(voices):
        print(f"{idx}: {voice.name} - {voice.languages} - {voice.id}")

def speak(text):
    with lock:  # ⛓️ Ensures only one thread uses the engine at a time
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()

# Optional testing
if __name__ == "__main__":
    list_voices()
    speak("Hello. This is a test of the voice engine.")
