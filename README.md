# ALPHA — Personal AI Voice Assistant

> A locally-running, voice-first AI assistant powered by Groq LLM, Kokoro TTS, and Whisper STT.
> Works on desktop and mobile browser. Integrates with MightyLion for PC control via voice.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What ALPHA Can Do

- 🎙️ Listen to your voice via mobile browser or desktop mic
- 🧠 Understand and respond intelligently using Groq (llama-3.3-70b)
- 🔊 Speak back using Kokoro neural TTS (natural voice)
- 📱 Work from your phone via a Siri-style mobile web UI
- 🖥️ Trigger PC actions (screenshot, open apps) via MightyLion integration
- 💬 Remember conversation context across a session

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Speech-to-Text | faster-whisper |
| Wake Word | openwakeword (hey_jarvis) |
| LLM Brain | Groq — llama-3.3-70b-versatile |
| Text-to-Speech | Kokoro ONNX (af_sarah voice) |
| Fallback TTS | pyttsx3 |
| API Server | Flask + Flask-CORS |
| Mobile UI | Vanilla HTML/JS (Siri-style dark UI) |
| PC Control | MightyLion PC Bridge (port 8765) |

---

## Project Structure
```
ALPHA/
├── alpha_server.py          # Flask API server (port 8766)
├── alpha_mobile.html        # Mobile web UI
├── app/
│   └── main.py              # Desktop voice mode (wakeword + mic)
├── modules/
│   ├── brain.py             # Groq LLM integration
│   ├── speech_engine.py     # Kokoro TTS + pyttsx3 fallback
│   ├── voice_listener.py    # Microphone input handler
│   └── wakeword_listener.py # Hey Jarvis wakeword detection
├── kokoro-v0_19.onnx        # TTS model (download separately)
├── voices.bin               # TTS voices (download separately)
├── .env                     # Your config (never committed)
├── .env.example             # Template for setup
└── requirements.txt         # Python dependencies
```

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Shaunrufus/ALPHA.git
cd ALPHA
```

### 2. Create virtual environment
```bash
python -m venv venv_new
venv_new\Scripts\activate
pip install -r requirements.txt
```

### 3. Download TTS model files
```bash
curl -L -o kokoro-v0_19.onnx https://huggingface.co/thewh1teagle/Kokoro/resolve/main/kokoro-v0_19.onnx
curl -L -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

### 4. Configure environment
```bash
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 5. Start ALPHA
```bash
venv_new\Scripts\python.exe alpha_server.py
```

Open http://localhost:8766 in your browser.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | Your Groq API key (get free at console.groq.com) |
| PC_BRIDGE_URL | MightyLion PC Bridge URL (default: http://localhost:8765) |
| KOKORO_MODEL | Path to kokoro-v0_19.onnx |
| KOKORO_VOICES | Path to voices.bin |
| ALPHA_PORT | Server port (default: 8766) |

---

## Mobile Access

To use ALPHA from your phone:

1. Run the server
2. Create a tunnel: `cloudflared tunnel --url http://localhost:8766`
3. Open the tunnel URL on your phone
4. Press the mic button and speak

HTTPS is required for microphone access on mobile — the Cloudflare tunnel handles this automatically.

---

## MightyLion Integration

ALPHA connects to [MightyLion](https://github.com/Shaunrufus/mightylion) for PC control.
Say commands like:
- *"Take a screenshot"*
- *"What's on my screen?"*
- *"Open Chrome"*

ALPHA detects the intent and forwards it to the MightyLion PC Bridge.

---

## Roadmap

- [x] Voice input via browser mic
- [x] Groq LLM brain
- [x] Kokoro neural TTS
- [x] Mobile web UI
- [x] MightyLion PC control integration
- [ ] Continuous voice mode (no push-to-talk)
- [ ] Android lock screen widget
- [ ] Oracle Cloud deployment (always-on)
- [ ] Multi-user support
- [ ] WhatsApp integration

---

## License

MIT License — free to use, modify, and distribute.

---

Built by [Shaun Rufus](https://github.com/Shaunrufus)
