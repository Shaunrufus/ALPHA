# 📂 modules/voice_listener.py

import queue
import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from modules.speech_engine import speak

# 🧠 Load Whisper model (only once)
MODEL_SIZE = "base.en"
model = WhisperModel(MODEL_SIZE, compute_type="auto")

# 🎧 Recording settings
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 5  # seconds

# Queue to hold audio chunks
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"[!] Audio Input Status: {status}")
    audio_queue.put(indata.copy())

def record_audio():
    """Records audio for a fixed duration and returns as NumPy array"""
    print("🎤 Listening...")
    audio_data = []

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
        for _ in range(int(SAMPLE_RATE / 1024 * CHUNK_DURATION)):
            audio_chunk = audio_queue.get()
            audio_data.append(audio_chunk)

    full_audio = np.concatenate(audio_data, axis=0)
    return full_audio.squeeze()

def transcribe_audio(audio_np):
    """Transcribes NumPy audio input using faster-whisper"""
    segments, _ = model.transcribe(audio_np, beam_size=5)
    full_text = " ".join([seg.text for seg in segments])
    return full_text.strip()

def listen_for_command():
    """Main callable function to capture, transcribe, and return voice input"""
    try:
        audio_np = record_audio()
        command_text = transcribe_audio(audio_np)

        if command_text:
            print(f"🗣️ You said: {command_text}")
            speak(f"You said: {command_text}")
        else:
            speak("Sorry, I didn't catch that.")
        
        return command_text
    except Exception as e:
        print(f"[❌ ERROR] Voice listening failed: {e}")
        speak("Something went wrong while listening.")
        return ""
