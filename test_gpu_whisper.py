from faster_whisper import WhisperModel

# Load the model (make sure you have the medium or large model if GPU is available)
model = WhisperModel("medium", device="cuda", compute_type="float16")

# Transcribe the audio
segments, _ = model.transcribe("output.wav", beam_size=5)

# Print each segment
for segment in segments:
    print(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text}")
