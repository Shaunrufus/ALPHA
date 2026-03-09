#!/usr/bin/env python3
"""
Direct Test: Groq Intelligence + Voice Cloning
Bypasses server to test the full pipeline directly
"""

import os
import sys
import tempfile
import sounddevice as sd
import soundfile as sf
from pathlib import Path

# Add server directory to path
sys.path.append(str(Path(__file__).parent / "server"))

def test_groq_voice_direct():
    """Test Groq intelligence with voice cloning directly."""
    print("🧠 Testing Groq Intelligence + Voice Cloning Directly...")
    print("=" * 60)
    
    # Set API key
    os.environ['GROQ_API_KEY'] = "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"
    
    # Import Groq LLM
    from groq_integration import GroqLLM
    
    # Initialize LLM
    llm = GroqLLM()
    
    # Test inputs
    test_inputs = [
        "Good morning!",
        "Tell me a joke",
        "What's the weather like?",
        "How are you doing?",
        "What time is it?"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        
        # Get intelligent response from Groq
        response = llm.get_intelligent_response(user_input)
        print(f"🤖 ALPHA (Intelligent): {response}")
        
        # Test if we can generate voice (optional)
        try:
            # Try to import voice cloning
            from voice_clone import clone_voice
            from openvoice.api import BaseSpeakerTTS
            
            print("🎵 Generating voice...")
            
            # Generate TTS
            base_tts = BaseSpeakerTTS('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/config.json', device="cpu")
            base_tts.load_ckpt('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/checkpoint.pth')
            
            # Create temp file
            tts_temp = Path("temp_tts.wav")
            base_tts.tts(response, str(tts_temp), speaker='default', language='English', speed=1.0)
            
            # Clone voice
            output_path = clone_voice("user1", tts_temp)
            
            # Play the audio
            print("🔊 Playing intelligent response...")
            audio, sr = sf.read(output_path)
            sd.play(audio, sr)
            sd.wait()
            
            # Clean up
            tts_temp.unlink(missing_ok=True)
            print("✅ Voice response played!")
            
        except Exception as e:
            print(f"⚠️ Voice generation failed: {e}")
            print("💡 This is expected if voice cloning isn't fully set up")
        
        print("-" * 40)
        input("Press Enter to continue...")

if __name__ == "__main__":
    test_groq_voice_direct()
