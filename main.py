import re
import requests
import speech_recognition as sr
import time
import sounddevice as sd
import numpy as np
import tempfile
import os
import soundfile as sf

recognizer = sr.Recognizer()

# === Voice Cloning TTS Settings ===
VOICE_SERVER_URL = "http://127.0.0.1:8000"
USER_ID = "user1"  # Change this for different users

# === Wake word settings ===
WAKE_WORD = "alpha"

def speak(text, language="en"):
    """Speak text using your cloned voice."""
    print(f"🧠 Speaking with cloned voice: {text}")
    
    try:
        # Make TTS request to voice cloning server
        # Note: Server currently only supports English for TTS
        response = requests.post(
            f"{VOICE_SERVER_URL}/tts",
            data={
                "user_id": USER_ID,
                "text": text,
                "language": "en"  # Force English for now
            }
        )
        
        if response.status_code == 200:
            audio_data = response.content
            
            # Play the audio
            play_cloned_audio(audio_data)
            
        else:
            print(f"❌ TTS Error: {response.status_code}")
            print(f"Response: {response.text}")
            # Fallback to simple text
            print(f"🔊 Fallback: {text}")
            
    except Exception as e:
        print(f"❌ TTS Exception: {e}")
        # Fallback to simple text
        print(f"🔊 Fallback: {text}")

def play_cloned_audio(audio_data):
    """Play cloned voice audio."""
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

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
    return ""

def evaluate_expression(text):
    # Replace words with symbols
    text = text.lower()
    replacements = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "times": "*",
        "multiplied by": "*",
        "multiply": "*",
        "x": "*",
        "divide by": "/",
        "divided by": "/",
        "divide": "/",
        "over": "/"
    }

    for word, symbol in replacements.items():
        text = text.replace(word, symbol)

    # Handle phrases like "multiply 5 and 6" or "add 5 and 6"
    match = re.search(r"(add|\+|subtract|\-|multiply|\*|divide|/)\s*(\d+)[^\d]+(\d+)", text)
    if match:
        op = match.group(1)
        num1 = float(match.group(2))
        num2 = float(match.group(3))
    else:
        # Try to extract simple expression like "5 + 6"
        try:
            result = eval(text)
            return result
        except:
            return None

    if op in ["add", "+"]:
        return num1 + num2
    elif op in ["subtract", "-"]:
        return num1 - num2
    elif op in ["multiply", "*"]:
        return num1 * num2
    elif op in ["divide", "/"]:
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"
    return None

def test_multilingual_voice():
    """Test multilingual voice cloning."""
    print("\n🌍 Testing Multilingual Voice Cloning")
    print("=" * 50)
    
    # Test English
    print("\n🇺🇸 English:")
    speak("Hello! I am your AI assistant with a cloned voice. How can I help you today?", "en")
    
    # Test Hindi
    print("\n🇮🇳 Hindi:")
    speak("नमस्ते! मैं आपकी AI सहायिका हूं। मेरी आवाज क्लोन की गई है।", "hi")
    
    # Test Telugu
    print("\n🇮🇳 Telugu:")
    speak("నమస్కారం! నేను మీ AI సహాయకుడిని. నా స్వరం క్లోన్ చేయబడింది.", "te")
    
    # Test Telugu with English transliteration
    print("\n🇮🇳 Telugu (Transliterated):")
    speak("Namaskaram! Nenu mee AI sahayakudini. Naa swaram clone cheyabadindi.", "te")
    
    print("\n✅ Multilingual test complete!")

def main():
    print("🎧 Voice Cloning AI Assistant")
    print("=" * 50)
    print("Commands:")
    print("- 'alpha' + math: Calculate math expressions")
    print("- 'test voice': Test multilingual voice cloning")
    print("- 'quit': Exit the program")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ").lower().strip()
        
        if "quit" in user_input:
            print("👋 Goodbye!")
            break
        elif "test voice" in user_input:
            test_multilingual_voice()
        elif WAKE_WORD in user_input:
            audio_text = listen()
            if not audio_text:
                continue
            result = evaluate_expression(audio_text)
            if result is not None:
                print(f"🧮 Result: {round(result, 2) if isinstance(result, float) else result}")
                speak(f"The answer is {round(result, 2)}")
            else:
                print("🤷 Sorry, I couldn't understand the math.")
                speak("Sorry, I couldn't understand that.")
        else:
            print("💡 Try: 'alpha' + math expression, 'test voice', or 'quit'")

if __name__ == "__main__":
    main()
