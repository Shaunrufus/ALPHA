import sounddevice as sd
import numpy as np
import wave, os

SAVE_DIR = r'C:\ALPHA\wakeword_training\positive'
SAMPLE_RATE = 16000
DURATION = 1.5

os.makedirs(SAVE_DIR, exist_ok=True)
print('Say ALPHA clearly when prompted. Recording 30 samples.')

for i in range(30):
    input(f'Press Enter for sample {i+1}/30...')
    print('Recording...')
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    path = os.path.join(SAVE_DIR, f'alpha_{i+1:03d}.wav')
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio.tobytes())
    print(f'Saved: alpha_{i+1:03d}.wav')

print('Done! All 30 samples recorded.')
