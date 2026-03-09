from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
from voice_clone import clone_voice, enroll_user

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Voice cloning server running"}

@app.post("/enroll")
async def enroll(user_id: str = Form(...), file: UploadFile = File(...)):
    input_path = UPLOAD_DIR / file.filename
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    enroll_user(user_id, input_path)
    return {"status": "enrolled", "user_id": user_id}

@app.post("/clone")
async def clone(user_id: str = Form(...), file: UploadFile = File(...)):
    input_path = UPLOAD_DIR / file.filename
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    output_path = clone_voice(user_id, input_path)
    return FileResponse(output_path, media_type="audio/wav", filename="cloned.wav")

@app.post("/tts")
async def text_to_speech(user_id: str = Form(...), text: str = Form(...), language: str = Form("en")):
    """Convert text to speech using cloned voice."""
    try:
        # Check if user is enrolled
        ref_path = Path(f"C:/ALPHA/OpenVoice/recording_{user_id}.wav")
        if not ref_path.exists():
            return JSONResponse(status_code=400, content={"error": f"No enrollment found for user {user_id}"})
        
        # Generate TTS audio using base speaker
        from openvoice.api import BaseSpeakerTTS
        base_tts = BaseSpeakerTTS('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/config.json', device="cpu")
        base_tts.load_ckpt('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/checkpoint.pth')
        
        # Create temporary TTS file
        tts_temp = Path(f"C:/ALPHA/OpenVoice/tts_temp_{user_id}.wav")
        
        # Handle different languages
        if language in ["te", "te-IN", "telugu"]:
            # For Telugu, we'll use English TTS but can add transliteration later
            print(f"🌍 Processing Telugu text: {text[:50]}...")
            # Use English TTS for now (Telugu text will be processed as English phonemes)
            base_tts.tts(text, str(tts_temp), speaker='default', language='English', speed=1.0)
        elif language in ["hi", "hi-IN", "hindi"]:
            # For Hindi, same approach
            print(f"🌍 Processing Hindi text: {text[:50]}...")
            base_tts.tts(text, str(tts_temp), speaker='default', language='English', speed=1.0)
        else:
            # Default to English
            base_tts.tts(text, str(tts_temp), speaker='default', language='English', speed=1.0)
        
        # Clone the TTS output to user's voice
        output_path = clone_voice(user_id, tts_temp)
        
        # Clean up temp file
        tts_temp.unlink(missing_ok=True)
        
        return FileResponse(output_path, media_type="audio/wav", filename="tts_output.wav")
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/speak")
async def speak_text(user_id: str = Form(...), text: str = Form(...), language: str = Form("en")):
    """Simple text-to-speech endpoint for quick testing."""
    return await text_to_speech(user_id, text, language)

@app.post("/realtime")
async def realtime_assistant(user_id: str = Form(...), text: str = Form(...)):
    """Real-time voice assistant endpoint with intelligent LLM responses."""
    try:
        # Check if user is enrolled
        ref_path = Path(f"C:/ALPHA/OpenVoice/recording_{user_id}.wav")
        if not ref_path.exists():
            return JSONResponse(status_code=400, content={"error": f"No enrollment found for user {user_id}"})
        
        # Import Groq LLM for intelligent responses
        import sys
        sys.path.append(str(Path(__file__).parent.parent))
        from groq_integration import GroqLLM
        
        # Initialize LLM and get intelligent response
        llm = GroqLLM()
        response = llm.get_intelligent_response(text)
        
        # Generate TTS with the response
        from openvoice.api import BaseSpeakerTTS
        base_tts = BaseSpeakerTTS('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/config.json', device="cpu")
        base_tts.load_ckpt('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/checkpoint.pth')
        
        # Create temporary TTS file
        tts_temp = Path(f"C:/ALPHA/OpenVoice/tts_temp_{user_id}.wav")
        base_tts.tts(response, str(tts_temp), speaker='default', language='English', speed=1.0)
        
        # Clone the TTS output to user's voice
        output_path = clone_voice(user_id, tts_temp)
        
        # Clean up temp file
        tts_temp.unlink(missing_ok=True)
        
        return FileResponse(output_path, media_type="audio/wav", filename="realtime_response.wav")
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.exception_handler(Exception)
async def error_handler(_, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})
