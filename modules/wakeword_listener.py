"""
ALPHA Wakeword Listener
Real audio-based wake word detection using faster-whisper
Listens in short 2-second chunks, triggers when "alpha" is detected
No extra packages needed — reuses Whisper already installed
"""

import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Use tiny model for wakeword — very fast, low resource
print("[Wakeword] Loading tiny Whisper model for wake detection...")
_wake_model = WhisperModel("tiny.en", compute_type="int8")
print("[Wakeword] Ready.")

SAMPLE_RATE = 16000
WAKE_CHUNK_SECONDS = 2  # Listen in 2-second chunks

wakeword_active = False
wakeword_thread = None


def _record_chunk(seconds=WAKE_CHUNK_SECONDS):
    """Record a short audio chunk and return as numpy array"""
    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    return audio.squeeze()


def _contains_wakeword(audio_np):
    """Check if audio contains the wake word 'alpha'"""
    segments, _ = _wake_model.transcribe(
        audio_np,
        beam_size=1,        # Fast
        language="en",
        condition_on_previous_text=False
    )
    text = " ".join([s.text for s in segments]).lower().strip()
    if text:
        print(f"[Wakeword heard]: {text}")
    return "alpha" in text


def _wakeword_loop(trigger_callback):
    """Continuously listen for wake word in background"""
    global wakeword_active
    print("[Wakeword] Listening for 'Alpha'...")

    while wakeword_active:
        try:
            audio = _record_chunk()

            # Skip silent chunks (saves processing)
            if np.abs(audio).mean() < 0.001:
                continue

            if _contains_wakeword(audio):
                print("[Wakeword] Detected! Triggering...")
                wakeword_active = False  # Pause wakeword while processing
                trigger_callback()
                wakeword_active = True   # Resume after command handled
                print("[Wakeword] Back to listening for 'Alpha'...")

        except Exception as e:
            print(f"[Wakeword Error] {e}")
            continue


def start_wake_word_detection(trigger_callback):
    """Start listening for wake word in background thread"""
    global wakeword_thread, wakeword_active
    wakeword_active = True
    wakeword_thread = threading.Thread(
        target=_wakeword_loop,
        args=(trigger_callback,),
        daemon=True
    )
    wakeword_thread.start()


def stop_wake_word_detection():
    """Stop wake word detection"""
    global wakeword_active
    wakeword_active = False
    print("[Wakeword] Stopped.")