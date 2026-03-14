"""
ALPHA API Server - Flask
Accepts text/voice commands from:
1. Mobile web app
2. MightyLion Telegram bot
Returns text reply + audio (base64)
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys, os, io, base64, tempfile, threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.brain import think, clear_memory
from modules.speech_engine import speak as local_speak

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_file('alpha_mobile.html')
CORS(app)

def text_to_audio_base64(text):
    """Convert text to audio and return as base64"""
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
        import numpy as np

        kokoro = Kokoro("kokoro-v0_19.onnx", "voices.bin")
        samples, sample_rate = kokoro.create(text, voice="af_sarah", speed=1.0, lang="en-us")

        buf = io.BytesIO()
        sf.write(buf, samples, sample_rate, format='WAV')
        buf.seek(0)
        audio_b64 = base64.b64encode(buf.read()).decode('utf-8')
        return audio_b64
    except Exception as e:
        print(f"[TTS Error] {e}")
        return None


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "name": "ALPHA"})


@app.route('/chat', methods=['POST'])
def chat():
    """
    Accept text message, return text + audio reply
    Used by mobile web app and MightyLion
    """
    data = request.json
    user_text = data.get('message', '').strip()
    source = data.get('source', 'unknown')  # 'mobile' or 'telegram'

    if not user_text:
        return jsonify({"error": "No message provided"}), 400

    print(f"[API] [{source}] {user_text}")

    reply, action = think(user_text)

    if action:
        action_type = action.get('action', '')
        reply = f"Action triggered: {action_type}"

    if not reply:
        reply = "I'm not sure how to respond to that."

    # Generate audio for mobile
    audio_b64 = None
    if source == 'mobile':
        audio_b64 = text_to_audio_base64(reply)

    return jsonify({
        "reply": reply,
        "audio": audio_b64,  # base64 WAV, None for telegram
        "action": action
    })


@app.route('/clear', methods=['POST'])
def clear():
    clear_memory()
    return jsonify({"status": "memory cleared"})


@app.route('/pc', methods=['POST'])
def pc_command():
    import requests
    data = request.json
    try:
        res = requests.post('http://192.168.29.3:8765/' + data.get('endpoint','screenshot'), json=data.get('payload',{}), timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("   ALPHA API Server starting on port 8766")
    print("   Mobile: http://192.168.29.3:8766")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8766, debug=False)

