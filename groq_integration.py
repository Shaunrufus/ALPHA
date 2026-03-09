#!/usr/bin/env python3
"""
Groq LLM Integration for ALPHA Voice Assistant
Provides ChatGPT-level intelligence for voice responses
"""

import requests
import json
import os
from typing import Optional

class GroqLLM:
    """Groq LLM integration for intelligent voice assistant responses."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"  # Fast and intelligent model
        
        if not self.api_key:
            print("⚠️  No Groq API key found!")
            print("💡 Get your free API key from: https://console.groq.com/")
            print("💡 Set it as environment variable: GROQ_API_KEY")
    
    def get_intelligent_response(self, user_input: str, context: str = "") -> str:
        """Get intelligent response from Groq LLM."""
        if not self.api_key:
            return self._get_fallback_response(user_input)
        
        try:
            # Create a voice assistant prompt
            system_prompt = """You are ALPHA, a helpful and intelligent voice assistant. 
            Respond naturally and conversationally, as if you're having a friendly chat.
            Keep responses concise (1-2 sentences) since this is for voice output.
            Be helpful, friendly, and engaging."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"❌ Groq API Error: {response.status_code}")
                return self._get_fallback_response(user_input)
                
        except Exception as e:
            print(f"❌ Groq request error: {e}")
            return self._get_fallback_response(user_input)
    
    def _get_fallback_response(self, user_input: str) -> str:
        """Fallback responses when Groq is not available."""
        input_lower = user_input.lower()
        
        # Greetings
        if any(word in input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            return "Hello! How can I help you today?"
        
        # Goodbyes
        if any(word in input_lower for word in ["bye", "goodbye", "see you", "later"]):
            return "Goodbye! Have a great day!"
        
        # Thanks
        if any(word in input_lower for word in ["thank", "thanks"]):
            return "You're welcome! Is there anything else I can help you with?"
        
        # Weather
        if "weather" in input_lower:
            return "I'd be happy to help with weather information, but I need internet access for that."
        
        # Time
        if "time" in input_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        # Default response
        return "I understand you said that. How can I assist you further?"

def test_groq_integration():
    """Test the Groq integration."""
    print("🧠 Testing Groq LLM Integration...")
    print("=" * 50)
    
    llm = GroqLLM()
    
    test_inputs = [
        "Good morning!",
        "What's the weather like?",
        "Tell me a joke",
        "How are you doing?",
        "What time is it?",
        "Thank you for your help"
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        response = llm.get_intelligent_response(user_input)
        print(f"🤖 ALPHA: {response}")
        print("-" * 30)

if __name__ == "__main__":
    test_groq_integration()
