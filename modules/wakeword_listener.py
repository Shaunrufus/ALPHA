"""
ALPHA Wakeword Listener
Uses openwakeword with hey_jarvis model - free forever, no API key
Say "Hey Jarvis" to activate Alpha
"""

import threading
import numpy as np
import sounddevice as sd
import openwakeword
from openwakeword.model import Model

print("[Wakeword] Loading Hey Jarvis model...")
_oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
print("[Wakeword] Ready. Say 'Hey Jarvis' to activate Alpha.")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80ms chunks - openwakeword requirement

wakeword_active = False
wakeword_thread = None


def _wakeword_loop(trigger_callback):
    global wakeword_active

    print("[Wakeword] Listening for 'Hey Jarvis'...")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                        dtype='int16', blocksize=CHUNK_SIZE) as stream:
        while wakeword_active:
            try:
                audio_chunk, _ = stream.read(CHUNK_SIZE)
                audio_np = audio_chunk.squeeze()

                # Feed to openwakeword
                prediction = _oww_model.predict(audio_np)

                # Check if hey_jarvis confidence is high enough
                for model_name, score in prediction.items():
                    if score > 0.5:
                        print(f"[Wakeword] ✅ Detected! (score: {score:.2f})")
                        wakeword_active = False
                        _oww_model.reset()
                        trigger_callback()
                        wakeword_active = True
                        print("[Wakeword] Back to listening for 'Hey Jarvis'...")
                        break

            except Exception as e:
                print(f"[Wakeword Error] {e}")
                continue


def start_wake_word_detection(trigger_callback):
    global wakeword_thread, wakeword_active
    wakeword_active = True
    wakeword_thread = threading.Thread(
        target=_wakeword_loop,
        args=(trigger_callback,),
        daemon=True
    )
    wakeword_thread.start()


def stop_wake_word_detection():
    global wakeword_active
    wakeword_active = False
    print("[Wakeword] Stopped.")