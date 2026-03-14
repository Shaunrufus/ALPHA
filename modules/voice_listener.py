import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

model = WhisperModel("base.en", device="cpu", compute_type="int8")

SAMPLE_RATE = 16000
CHUNK_DURATION = 5

HALLUCINATIONS = [
    "thank you", "thanks for watching", "thanks for watching!",
    "thank you for watching", "we'll see you in a minute",
    "you", "bye", "the", "a", "uh", "um", "hmm", "."
]

def listen_for_command():
    try:
        print("Listening...")
        audio = sd.rec(int(CHUNK_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        audio_np = audio.squeeze()

        rms = float(np.sqrt(np.mean(audio_np**2)))
        print(f"[RMS: {rms:.4f}]")
        if rms < 0.01:
            print("No speech detected.")
            return ""

        segments, _ = model.transcribe(audio_np, beam_size=5, language="en", no_speech_threshold=0.6)
        text = " ".join([s.text for s in segments]).strip()

        if text.lower().strip(" .!?,") in HALLUCINATIONS:
            print(f"Filtered: '{text}'")
            return ""

        if text:
            print(f"You said: {text}")
        return text

    except Exception as e:
        print(f"[Voice Error] {e}")
        return ""
