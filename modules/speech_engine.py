import os, io, threading
import sounddevice as sd
import soundfile as sf
import numpy as np
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

KOKORO_MODEL  = os.environ.get("KOKORO_MODEL",  "kokoro-v0_19.onnx")
KOKORO_VOICES = os.environ.get("KOKORO_VOICES", "voices.bin")

_lock = threading.Lock()

def speak(text):
    with _lock:
        try:
            from kokoro_onnx import Kokoro
            kokoro = Kokoro(KOKORO_MODEL, KOKORO_VOICES)
            samples, sample_rate = kokoro.create(text, voice="af_sarah", speed=1.0, lang="en-us")
            print(f"[Alpha speaks]: {text}")
            sd.play(samples, sample_rate)
            sd.wait()
        except Exception as e:
            print(f"[Kokoro failed, using pyttsx3]: {e}")
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 165)
            engine.setProperty('volume', 1.0)
            print(f"[Alpha speaks]: {text}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()
