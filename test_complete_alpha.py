#!/usr/bin/env python3
"""
Complete ALPHA Test: Groq Intelligence + Voice Cloning
Tests the full pipeline with proper error handling
"""

import os
import sys
import requests
import tempfile
import sounddevice as sd
import soundfile as sf
from pathlib import Path

def test_groq_intelligence():
    """Test Groq intelligence separately."""
    print("🧠 Testing Groq Intelligence...")
    print("=" * 40)
    
    # Set API key
    os.environ['GROQ_API_KEY'] = "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"
    
    # Import and test Groq
    from groq_integration import GroqLLM
    llm = GroqLLM()
    
    test_inputs = [
        "Good morning!",
        "Tell me a joke",
        "What's the weather like?",
        "How are you doing?",
        "What time is it?"
    ]
    
    for user_input in test_inputs:
        response = llm.get_intelligent_response(user_input)
        print(f"👤 User: {user_input}")
        print(f"🤖 ALPHA: {response}")
        print("-" * 30)
    
    return True

def test_voice_cloning():
    """Test voice cloning separately."""
    print("\n🎵 Testing Voice Cloning...")
    print("=" * 40)
    
    try:
        # Test basic TTS
        from openvoice.api import BaseSpeakerTTS
        print("✅ OpenVoice imported successfully")
        
        # Test TTS generation
        base_tts = BaseSpeakerTTS('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/config.json', device="cpu")
        base_tts.load_ckpt('../OpenVoice/OpenVoice/checkpoints/base_speakers/EN/checkpoint.pth')
        print("✅ TTS model loaded successfully")
        
        # Test voice cloning
        from voice_clone import clone_voice
        print("✅ Voice cloning imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice cloning test failed: {e}")
        return False

def test_server_integration():
    """Test the full server integration."""
    print("\n🌐 Testing Server Integration...")
    print("=" * 40)
    
    server_url = "http://127.0.0.1:8000"
    user_id = "user1"
    
    # Test server connection
    try:
        response = requests.get(f"{server_url}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Test intelligent voice assistant
    test_inputs = [
        "Good morning!",
        "Tell me a joke",
        "How are you doing?"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        
        try:
            response = requests.post(
                f"{server_url}/realtime",
                data={
                    "user_id": user_id,
                    "text": user_input
                },
                timeout=30
            )
            
            if response.status_code == 200:
                # Save and play the audio
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name
                
                print("🎵 Playing intelligent voice response...")
                
                # Play the audio
                audio, sr = sf.read(tmp_file_path)
                sd.play(audio, sr)
                sd.wait()
                
                # Clean up
                os.unlink(tmp_file_path)
                print("✅ Voice response played successfully!")
                
            else:
                print(f"❌ Server error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        print("-" * 30)
        input("Press Enter to continue...")
    
    return True

def main():
    """Run all tests."""
    print("🚀 ALPHA Complete System Test")
    print("=" * 50)
    
    # Test 1: Groq Intelligence
    groq_working = test_groq_intelligence()
    
    # Test 2: Voice Cloning
    voice_working = test_voice_cloning()
    
    # Test 3: Server Integration (if both above work)
    if groq_working and voice_working:
        print("\n🎯 Both components working! Testing full integration...")
        server_working = test_server_integration()
    else:
        print("\n⚠️ Some components not working. Skipping server test.")
        server_working = False
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"🧠 Groq Intelligence: {'✅ Working' if groq_working else '❌ Failed'}")
    print(f"🎵 Voice Cloning: {'✅ Working' if voice_working else '❌ Failed'}")
    print(f"🌐 Server Integration: {'✅ Working' if server_working else '❌ Failed'}")
    
    if groq_working and voice_working and server_working:
        print("\n🎉 ALPHA is fully operational!")
    else:
        print("\n🔧 Some components need attention.")

if __name__ == "__main__":
    main()
