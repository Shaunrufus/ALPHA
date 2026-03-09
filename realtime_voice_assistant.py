#!/usr/bin/env python3
"""
Real-Time Voice Assistant with Cloned Voice
This turns your voice cloning system into a live AI assistant!
"""

import speech_recognition as sr
import requests
import tempfile
import os
import sounddevice as sd
import soundfile as sf
import time
from pathlib import Path

class RealtimeVoiceAssistant:
    """Real-time voice assistant using your cloned voice."""
    
    def __init__(self, server_url="http://127.0.0.1:8000", user_id="user1"):
        self.server_url = server_url
        self.user_id = user_id
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Adjust microphone sensitivity
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def listen_for_speech(self):
        """Listen to microphone and convert to text."""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (speak now)")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                print("🔄 Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ You said: {text}")
                return text.lower()
                
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_ai_response(self, user_input):
        """Get AI response using the realtime endpoint."""
        try:
            response = requests.post(
                f"{self.server_url}/realtime",
                data={
                    "user_id": self.user_id,
                    "text": user_input
                }
            )
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request error: {e}")
            return None
    
    def play_audio(self, audio_data):
        """Play audio response."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name
            
            # Load and play audio
            audio, sr = sf.read(tmp_file_path)
            print("🔊 Playing response...")
            sd.play(audio, sr)
            sd.wait()  # Wait until audio finishes
            
            # Clean up
            os.unlink(tmp_file_path)
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
    def process_command(self, user_input):
        """Process user input and generate response."""
        print(f"\n🧠 Processing: {user_input}")
        
        # Get AI response with cloned voice
        audio_response = self.get_ai_response(user_input)
        
        if audio_response:
            # Play the response
            self.play_audio(audio_response)
            return True
        else:
            print("❌ Failed to get response")
            return False
    
    def start_conversation(self):
        """Start the real-time conversation loop."""
        print("🎤 Real-Time Voice Assistant Started!")
        print("=" * 50)
        print("Commands:")
        print("- Say 'hello' to start")
        print("- Ask 'how are you'")
        print("- Ask 'what can you do'")
        print("- Say anything else for a response")
        print("- Say 'quit' to exit")
        print("=" * 50)
        
        self.is_listening = True
        
        while self.is_listening:
            try:
                # Listen for speech
                user_input = self.listen_for_speech()
                
                if user_input:
                    # Check for quit command
                    if "quit" in user_input or "exit" in user_input or "stop" in user_input:
                        print("👋 Goodbye! Stopping voice assistant.")
                        self.is_listening = False
                        break
                    
                    # Process the command
                    success = self.process_command(user_input)
                    
                    if success:
                        print("\n✅ Response completed. Listening for next command...")
                    else:
                        print("\n⚠️ Response failed. Listening for next command...")
                    
                    # Small delay before next listen
                    time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user. Stopping...")
                self.is_listening = False
                break
            except Exception as e:
                print(f"❌ Error in conversation loop: {e}")
                continue
        
        print("🎤 Voice assistant stopped.")

def main():
    """Main function to run the voice assistant."""
    print("🚀 Starting Real-Time Voice Assistant")
    print("=" * 50)
    
    # Initialize the assistant
    assistant = RealtimeVoiceAssistant(user_id="user1")
    
    # Start the conversation
    assistant.start_conversation()

if __name__ == "__main__":
    main()
