"""
ALPHA Speech Engine - Kokoro TTS (natural voice)
Falls back to pyttsx3 if Kokoro fails
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
import io
import threading

_lock = threading.Lock()

def speak(text):
    with _lock:
        try:
            from kokoro_onnx import Kokoro
            kokoro = Kokoro("kokoro-v0_19.onnx", "voices.bin")
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