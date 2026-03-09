#!/usr/bin/env python3
"""
Test Intelligent Voice Assistant with Groq Integration
"""

import requests
import tempfile
import os
import sounddevice as sd
import soundfile as sf

def test_intelligent_voice():
    """Test the intelligent voice assistant."""
    print("🧠 Testing Intelligent Voice Assistant...")
    print("=" * 50)
    
    server_url = "http://127.0.0.1:8000"
    user_id = "user1"
    
    # Test inputs
    test_inputs = [
        "Good morning!",
        "Tell me a joke",
        "What's the weather like?",
        "How are you doing?",
        "What time is it?",
        "Thank you for your help"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        
        try:
            # Call the intelligent voice assistant
            response = requests.post(
                f"{server_url}/realtime",
                data={
                    "user_id": user_id,
                    "text": user_input
                }
            )
            
            if response.status_code == 200:
                # Save and play the audio
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name
                
                print(f"🎵 Playing intelligent response...")
                
                # Play the audio
                audio, sr = sf.read(tmp_file_path)
                sd.play(audio, sr)
                sd.wait()
                
                # Clean up
                os.unlink(tmp_file_path)
                
                print("✅ Response played successfully!")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print("-" * 30)
        input("Press Enter to continue to next test...")

if __name__ == "__main__":
    test_intelligent_voice()
