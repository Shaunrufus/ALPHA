# ALPHA Voice Assistant

A Python-based voice assistant with wake word detection, speech recognition, and text-to-speech capabilities.

## Features

- 🎧 **Wake Word Detection**: Listens for "alpha" to activate
- 🗣️ **Speech Recognition**: Uses faster-whisper for accurate transcription
- 🔊 **Text-to-Speech**: Natural voice output using pyttsx3
- 🧮 **Voice Commands**: Responds to basic commands like time, date, greetings
- 🎤 **Real-time Audio Processing**: Continuous listening with VAD

## Project Structure

```
ALPHA/
├── app/
│   ├── main.py              # Main application entry point
│   ├── agent/               # AI agent modules (future)
│   ├── llm/                 # Language model integration (future)
│   ├── tts/                 # Text-to-speech modules (future)
│   ├── stt/                 # Speech-to-text modules (future)
│   ├── vad/                 # Voice activity detection (future)
│   └── utils/               # Utility functions (future)
├── modules/
│   ├── speech_engine.py     # TTS functionality
│   ├── voice_listener.py    # STT with faster-whisper
│   └── wakeword_listener.py # Wake word detection
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. **Clone the repository** (if applicable)
2. **Activate virtual environment**:
   ```bash
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the main application:
```bash
python app/main.py
```

### Test individual components:
```bash
# Test speech synthesis
python test_speak.py

# Test wake word detection
python test_wakeword.py

# Test GPU-accelerated Whisper
python test_gpu_whisper.py
```

## How it Works

1. **Wake Word Detection**: Continuously listens for "alpha"
2. **Command Processing**: When wake word detected, listens for commands
3. **Speech Recognition**: Transcribes audio using faster-whisper
4. **Response Generation**: Processes commands and generates responses
5. **Text-to-Speech**: Converts responses to speech

## Dependencies

- `pyttsx3`: Text-to-speech engine
- `faster-whisper`: Fast speech recognition
- `sounddevice`: Audio input/output
- `numpy`: Numerical computing
- `torch`: PyTorch for ML models
- `librosa`: Audio processing

## Troubleshooting

### Import Issues
If you get import errors, make sure:
1. Virtual environment is activated
2. You're running from the project root directory
3. All dependencies are installed

### Audio Issues
- Check microphone permissions
- Ensure audio drivers are working
- Try different audio devices if available

### GPU Issues
- Install CUDA if using GPU acceleration
- Use CPU-only mode if GPU not available

## Future Enhancements

- [ ] Real wake word detection (currently simulated)
- [ ] AI agent integration
- [ ] More sophisticated command processing
- [ ] Voice cloning capabilities
- [ ] Multi-language support

## License

This project is for educational purposes.
