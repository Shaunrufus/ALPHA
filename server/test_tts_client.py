import requests
import json
from pathlib import Path

def test_tts_endpoint():
    """Test the TTS endpoint with different languages."""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test data
    test_cases = [
        {
            "user_id": "user1",
            "text": "Hello, I am your AI assistant. How can I help you today?",
            "language": "en",
            "description": "English TTS"
        },
        {
            "user_id": "user1", 
            "text": "नमस्ते! मैं आपकी AI सहायिका हूं। आज मैं आपकी कैसे मदद कर सकती हूं?",
            "language": "hi",
            "description": "Hindi TTS"
        },
        {
            "user_id": "user1",
            "text": "నమస్కారం! నేను మీ AI సహాయకుడిని. ఈరోజు నేను మీకు ఎలా సహాయపడగలను?",
            "language": "te", 
            "description": "Telugu TTS"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['description']}")
        print(f"📝 Text: {test_case['text'][:50]}...")
        
        try:
            # Make TTS request
            response = requests.post(
                f"{base_url}/tts",
                data={
                    "user_id": test_case["user_id"],
                    "text": test_case["text"],
                    "language": test_case["language"]
                }
            )
            
            if response.status_code == 200:
                # Save the audio file
                filename = f"tts_output_{test_case['language']}_{i}.wav"
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"✅ Success! Audio saved as: {filename}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

def test_multilingual_voice_cloning():
    """Test voice cloning with different language audio files."""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test with different language audio files
    test_files = [
        "base_text_1.wav",  # English
        "base_text_2.wav",  # English  
        "base_text_3.wav",  # English
        "base_text_4.wav"   # English
    ]
    
    print(f"\n🎯 Testing Voice Cloning with Different Audio Files:")
    
    for i, filename in enumerate(test_files, 1):
        print(f"\n🧪 Test {i}: Cloning {filename}")
        
        try:
            # Check if file exists
            file_path = f"../OpenVoice/OpenVoice/outputs/{filename}"
            if not Path(file_path).exists():
                print(f"⚠️ File not found: {file_path}")
                continue
                
            # Clone voice
            with open(file_path, "rb") as f:
                files = {"file": f}
                data = {"user_id": "user1"}
                
                response = requests.post(f"{base_url}/clone", data=data, files=files)
                
                if response.status_code == 200:
                    # Save cloned output
                    output_filename = f"cloned_{filename}"
                    with open(output_filename, "wb") as f:
                        f.write(response.content)
                    print(f"✅ Success! Cloned audio saved as: {output_filename}")
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 Testing Voice Cloning TTS System")
    print("=" * 50)
    
    # Test TTS endpoint
    test_tts_endpoint()
    
    # Test voice cloning
    test_multilingual_voice_cloning()
    
    print("\n🎉 Testing Complete!")
    print("\n📋 Next Steps:")
    print("1. Check the generated audio files")
    print("2. Compare original vs cloned voices")
    print("3. Test with your main application")
    print("4. Experiment with different languages and parameters")
