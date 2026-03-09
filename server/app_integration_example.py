"""
Example: How to integrate Voice Cloning TTS into your main application
This replaces pyttsx3 or other TTS engines with your cloned voice
"""

import requests
import tempfile
import os
from pathlib import Path
import sounddevice as sd
import soundfile as sf

class ClonedVoiceTTS:
    """Voice Cloning TTS client for your application."""
    
    def __init__(self, server_url="http://127.0.0.1:8000", user_id="user1"):
        self.server_url = server_url
        self.user_id = user_id
        
    def speak(self, text, language="en", save_to_file=None):
        """
        Convert text to speech using your cloned voice.
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (en, hi, te, etc.)
            save_to_file (str, optional): File path to save audio
            
        Returns:
            bytes: Audio data in WAV format
        """
        try:
            # Make TTS request to your voice cloning server
            response = requests.post(
                f"{self.server_url}/tts",
                data={
                    "user_id": self.user_id,
                    "text": text,
                    "language": language
                }
            )
            
            if response.status_code == 200:
                audio_data = response.content
                
                # Save to file if requested
                if save_to_file:
                    with open(save_to_file, "wb") as f:
                        f.write(audio_data)
                    print(f"✅ Audio saved to: {save_to_file}")
                
                return audio_data
            else:
                print(f"❌ TTS Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ TTS Exception: {e}")
            return None
    
    def play_audio(self, audio_data):
        """Play audio data using sounddevice."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name
            
            # Load and play audio
            audio, sr = sf.read(tmp_file_path)
            sd.play(audio, sr)
            sd.wait()  # Wait until audio finishes
            
            # Clean up
            os.unlink(tmp_file_path)
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
    def speak_and_play(self, text, language="en"):
        """Convert text to speech and play it immediately."""
        audio_data = self.speak(text, language)
        if audio_data:
            self.play_audio(audio_data)
        return audio_data

# Example usage in your main application
def main():
    """Example of how to use ClonedVoiceTTS in your app."""
    
    # Initialize the cloned voice TTS
    tts = ClonedVoiceTTS(user_id="user1")
    
    print("🎤 Testing Cloned Voice TTS Integration")
    print("=" * 50)
    
    # Test 1: English TTS
    print("\n🇺🇸 English TTS:")
    english_text = "Hello! I am your AI assistant with a cloned voice. How can I help you today?"
    tts.speak_and_play(english_text, "en")
    
    # Test 2: Hindi TTS
    print("\n🇮🇳 Hindi TTS:")
    hindi_text = "नमस्ते! मैं आपकी AI सहायिका हूं। मेरी आवाज क्लोन की गई है। आज मैं आपकी कैसे मदद कर सकती हूं?"
    tts.speak_and_play(hindi_text, "hi")
    
    # Test 3: Telugu TTS
    print("\n🇮🇳 Telugu TTS:")
    telugu_text = "నమస్కారం! నేను మీ AI సహాయకుడిని. నా స్వరం క్లోన్ చేయబడింది. ఈరోజు నేను మీకు ఎలా సహాయపడగలను?"
    tts.speak_and_play(telugu_text, "te")
    
    # Test 4: Save audio to file
    print("\n💾 Saving Audio to File:")
    save_text = "This is a test of saving cloned voice audio to a file."
    audio_data = tts.speak(save_text, "en", save_to_file="cloned_voice_output.wav")
    
    if audio_data:
        print(f"✅ Audio saved successfully! Size: {len(audio_data)} bytes")
    
    print("\n🎉 Integration Test Complete!")

# Example: Integration with your existing voice assistant
class VoiceAssistant:
    """Example voice assistant using cloned voice."""
    
    def __init__(self):
        self.tts = ClonedVoiceTTS(user_id="user1")
    
    def respond(self, user_input):
        """Generate response and speak it using cloned voice."""
        
        # Your AI logic here
        if "hello" in user_input.lower():
            response = "Hello! Nice to meet you. I'm your AI assistant with a cloned voice."
        elif "help" in user_input.lower():
            response = "I can help you with various tasks. Just ask me anything!"
        else:
            response = "I understand you said: " + user_input + ". How can I help you?"
        
        # Speak response using cloned voice
        print(f"🤖 Assistant: {response}")
        self.tts.speak_and_play(response, "en")
        
        return response

if __name__ == "__main__":
    # Test basic functionality
    main()
    
    # Test voice assistant integration
    print("\n" + "="*50)
    print("🤖 Testing Voice Assistant Integration")
    print("="*50)
    
    assistant = VoiceAssistant()
    assistant.respond("Hello, can you help me?")
    assistant.respond("What can you do?")
