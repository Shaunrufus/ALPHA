#!/usr/bin/env python3
"""
Quick test to verify all imports work correctly
"""

def test_imports():
    """Test all the imports used in the project"""
    print("🧪 Testing imports...")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 - OK")
    except ImportError as e:
        print(f"❌ pyttsx3 - FAILED: {e}")
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition - OK")
    except ImportError as e:
        print(f"❌ speech_recognition - FAILED: {e}")
    
    try:
        import sounddevice as sd
        print("✅ sounddevice - OK")
    except ImportError as e:
        print(f"❌ sounddevice - FAILED: {e}")
    
    try:
        import numpy as np
        print("✅ numpy - OK")
    except ImportError as e:
        print(f"❌ numpy - FAILED: {e}")
    
    try:
        from faster_whisper import WhisperModel
        print("✅ faster_whisper - OK")
    except ImportError as e:
        print(f"❌ faster_whisper - FAILED: {e}")
    
    try:
        import torch
        print("✅ torch - OK")
    except ImportError as e:
        print(f"❌ torch - FAILED: {e}")
    
    try:
        import librosa
        print("✅ librosa - OK")
    except ImportError as e:
        print(f"❌ librosa - FAILED: {e}")
    
    print("\n🎯 Testing module imports...")
    
    try:
        from modules.speech_engine import speak
        print("✅ modules.speech_engine - OK")
    except ImportError as e:
        print(f"❌ modules.speech_engine - FAILED: {e}")
    
    try:
        from modules.wakeword_listener import start_wake_word_detection
        print("✅ modules.wakeword_listener - OK")
    except ImportError as e:
        print(f"❌ modules.wakeword_listener - FAILED: {e}")
    
    try:
        from modules.voice_listener import listen_for_command
        print("✅ modules.voice_listener - OK")
    except ImportError as e:
        print(f"❌ modules.voice_listener - FAILED: {e}")

if __name__ == "__main__":
    test_imports()
