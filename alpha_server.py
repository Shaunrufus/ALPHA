"""
ALPHA API Server
Accepts commands from mobile web app and MightyLion
Returns text reply + audio (base64)
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import sys, os, io, base64

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.brain import think, clear_memory
from modules.speech_engine import speak as local_speak

app = Flask(__name__, static_folder='.')
CORS(app)

KOKORO_MODEL  = os.environ.get("KOKORO_MODEL",  "kokoro-v0_19.onnx")
KOKORO_VOICES = os.environ.get("KOKORO_VOICES", "voices.bin")
PC_BRIDGE_URL = os.environ.get("PC_BRIDGE_URL", "http://localhost:8765")
ALPHA_PORT    = int(os.environ.get("ALPHA_PORT", "8766"))

@app.route('/')
def index():
    return send_file('alpha_mobile.html')

def text_to_audio_base64(text):
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
        kokoro = Kokoro(KOKORO_MODEL, KOKORO_VOICES)
        samples, sample_rate = kokoro.create(text, voice="af_sarah", speed=1.0, lang="en-us")
        buf = io.BytesIO()
        sf.write(buf, samples, sample_rate, format='WAV')
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception as e:
        print(f"[TTS Error] {e}")
        return None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "name": "ALPHA"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get('message', '').strip()
    source    = data.get('source', 'unknown')
    if not user_text:
        return jsonify({"error": "No message provided"}), 400
    print(f"[API] [{source}] {user_text}")
    reply, action = think(user_text)
    if action:
        reply = f"Action triggered: {action.get('action','')}"
    if not reply:
        reply = "I'm not sure how to respond to that."
    audio_b64 = text_to_audio_base64(reply) if source == 'mobile' else None
    return jsonify({"reply": reply, "audio": audio_b64, "action": action})

@app.route('/clear', methods=['POST'])
def clear():
    clear_memory()
    return jsonify({"status": "memory cleared"})

@app.route('/pc', methods=['POST'])
def pc_command():
    import requests
    data = request.json
    try:
        res = requests.post(
            PC_BRIDGE_URL + '/' + data.get('endpoint', 'screenshot'),
            json=data.get('payload', {}),
            timeout=10
        )
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print(f"   ALPHA API Server starting on port {ALPHA_PORT}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=ALPHA_PORT, debug=False)
