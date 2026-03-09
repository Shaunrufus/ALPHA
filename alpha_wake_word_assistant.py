#!/usr/bin/env python3
"""
ALPHA Wake Word Voice Assistant
Listens for "ALPHA" and then activates your cloned voice assistant!
"""

import speech_recognition as sr
import requests
import tempfile
import os
import sounddevice as sd
import soundfile as sf
import time
import threading
import numpy as np
from pathlib import Path

class AlphaWakeWordAssistant:
    """Wake word activated voice assistant using your cloned voice."""
    
    def __init__(self, server_url="http://127.0.0.1:8000", user_id="user1"):
        self.server_url = server_url
        self.user_id = user_id
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.is_active = False
        
        # Wake word settings
        self.WAKE_WORD = "alpha"
        self.WAKE_WORD_ALIASES = ["alpha", "alfa", "alpa", "alpaa"]
        
        # Adjust microphone sensitivity for wake word detection
        self.recognizer.energy_threshold = 4000  # Higher threshold = less sensitive
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Longer pause = more accurate
        
    def listen_for_wake_word(self):
        """Continuously listen for the wake word 'ALPHA'."""
        print(f"🎧 Listening for wake word: '{self.WAKE_WORD.upper()}'...")
        print("💡 Say 'ALPHA' to activate me!")
        print("🛑 Say 'quit' or 'exit' to stop completely!")
        
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while self.is_listening:
                    try:
                        print("🔇 Listening for wake word...")
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        
                        # Try to recognize the wake word
                        try:
                            text = self.recognizer.recognize_google(audio).lower()
                            print(f"🎯 Heard: {text}")
                            
                            # Check for quit commands first
                            if any(word in text for word in ["quit", "exit", "stop", "bye"]):
                                print("🛑 Quit command detected! Stopping ALPHA...")
                                self.is_listening = False
                                return
                            
                            # Check if wake word is detected (with debouncing)
                            if any(alias in text for alias in self.WAKE_WORD_ALIASES):
                                # Debounce: prevent multiple activations
                                if not self.is_active:
                                    print(f"🚀 WAKE WORD DETECTED: {text.upper()}")
                                    self.is_active = True
                                    self.activate_assistant()
                                    # Wait before allowing next activation
                                    time.sleep(3)
                                    self.is_active = False
                                else:
                                    print("⏳ Already active, ignoring wake word...")
                                
                        except sr.UnknownValueError:
                            pass  # No speech detected, continue listening
                        except sr.RequestError as e:
                            print(f"❌ Speech recognition error: {e}")
                            
                    except sr.WaitTimeoutError:
                        continue  # No timeout, keep listening
                        
        except Exception as e:
            print(f"❌ Microphone error: {e}")
    
    def activate_assistant(self):
        """Activate the voice assistant after wake word detection."""
        print("🎤 ALPHA activated! I'm listening for your command...")
        
        # Play activation sound (optional)
        self.play_activation_sound()
        
        # Listen for command
        command = self.listen_for_command()
        
        if command:
            # Process the command
            self.process_command(command)
        
        # Return to wake word listening
        print("🔇 Returning to wake word listening...")
    
    def listen_for_command(self):
        """Listen for user command after wake word activation."""
        try:
            with sr.Microphone() as source:
                print("🎤 Speak your command now...")
                print("💡 Say 'quit' to exit completely, or give me a command!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                print("🔄 Processing command...")
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ Command: {text}")
                
                # Check for quit commands in the command
                if any(word in text.lower() for word in ["quit", "exit", "stop", "bye", "goodbye"]):
                    print("🛑 Quit command detected in command! Stopping ALPHA...")
                    self.is_listening = False
                    return "quit"
                
                return text.lower()
                
        except sr.WaitTimeoutError:
            print("⏰ No command detected, returning to sleep")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand command")
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
    
    def play_activation_sound(self):
        """Play a professional activation sound like Siri."""
        try:
            # Create a more sophisticated activation sound
            sample_rate = 44100
            duration = 0.6
            
            # Create time array
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Multi-frequency chord for rich sound
            freq1 = 523.25  # C5
            freq2 = 659.25  # E5
            freq3 = 783.99  # G5
            
            # Create chord with fade in/out
            chord = (np.sin(2 * np.pi * freq1 * t) * 0.2 + 
                    np.sin(2 * np.pi * freq2 * t) * 0.15 + 
                    np.sin(2 * np.pi * freq3 * t) * 0.1)
            
            # Apply fade in/out
            fade_samples = int(0.1 * sample_rate)
            chord[:fade_samples] *= np.linspace(0, 1, fade_samples)
            chord[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            print("🔔 Playing professional activation sound...")
            sd.play(chord, sample_rate)
            sd.wait()
            
        except Exception as e:
            print(f"❌ Activation sound error: {e}")
    
    def process_command(self, user_input):
        """Process user command and generate response."""
        # Check if this is a quit command
        if user_input == "quit":
            print("🛑 Quitting ALPHA...")
            self.is_listening = False
            return False
        
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
    
    def start(self):
        """Start the wake word detection system."""
        print("🚀 ALPHA Wake Word Assistant Starting...")
        print("=" * 60)
        print(f"🎧 Wake Word: '{self.WAKE_WORD.upper()}'")
        print("💡 Say 'ALPHA' to activate me!")
        print("🛑 Say 'quit' or 'exit' to stop")
        print("=" * 60)
        
        self.is_listening = True
        
        try:
            # Start wake word detection
            self.listen_for_wake_word()
            
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user. Stopping...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.is_listening = False
            print("🎤 ALPHA assistant stopped.")

def main():
    """Main function to run the wake word assistant."""
    print("🚀 Starting ALPHA Wake Word Assistant")
    print("=" * 60)
    
    # Initialize the assistant
    assistant = AlphaWakeWordAssistant(user_id="user1")
    
    # Start the wake word detection
    assistant.start()

if __name__ == "__main__":
    main()
