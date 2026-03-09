#!/usr/bin/env python3
"""
ALPHA Test from Server Directory
Tests Groq Intelligence + Voice Cloning from server environment
"""

import os
import sys
import tempfile
import sounddevice as sd
import soundfile as sf
from pathlib import Path

# Add parent directory to path for groq_integration
sys.path.append(str(Path(__file__).parent.parent))

def test_alpha_complete():
    """Test complete ALPHA pipeline from server directory."""
    print("🚀 ALPHA Complete Test (Server Environment)")
    print("=" * 50)
    
    # Set API key
    os.environ['GROQ_API_KEY'] = "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"
    
    # Import Groq LLM
    from groq_integration import GroqLLM
    llm = GroqLLM()
    
    # Import voice cloning
    from voice_clone import clone_voice
    from openvoice.api import BaseSpeakerTTS
    
    # Initialize TTS
    base_tts = BaseSpeakerTTS('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/config.json', device="cpu")
    base_tts.load_ckpt('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/checkpoint.pth')
    
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
        
        # Generate voice
        print("🎵 Generating voice...")
        
        # Create temp TTS file
        tts_temp = Path("temp_tts.wav")
        base_tts.tts(response, str(tts_temp), speaker='default', language='English', speed=1.0)
        
        # Clone voice
        output_path = clone_voice("user1", tts_temp)
        
        # Play the audio
        print("🔊 Playing intelligent voice response...")
        audio, sr = sf.read(output_path)
        sd.play(audio, sr)
        sd.wait()
        
        # Clean up
        tts_temp.unlink(missing_ok=True)
        print("✅ Voice response played!")
        
        print("-" * 40)
        input("Press Enter to continue...")
    
    print("\n🎉 ALPHA Complete Test Finished!")

if __name__ == "__main__":
    test_alpha_complete()
