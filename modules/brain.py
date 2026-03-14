import os
from groq import Groq
from dotenv import load_dotenv
import random, json

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

GREETINGS = [
    "Hmm?", "Hi Shaun!", "Hey, what's up?",
    "Yeah?", "I'm here!", "Hello! How can I help?", "Hi! What do you need?",
]

SYSTEM_PROMPT = """You are ALPHA, a personal AI voice assistant.
You are friendly, smart, and concise - like Siri or Google Assistant.
Rules:
- Keep responses SHORT (1-3 sentences max) - this is voice, not text
- Be warm and friendly, use the user's name occasionally
- Vary your responses - don't always start the same way
- For greetings like 'hi' or 'good morning' - respond naturally and warmly
- For questions - answer directly and clearly
- For tasks (open app, set timer, etc.) - confirm what you're doing
- Never say 'As an AI...' or long disclaimers
- Sound like a helpful friend, not a robot
If the user asks for PC control (screenshot, open app, check files), reply with JSON:
{"action": "screenshot"} or {"action": "open_app", "app": "chrome"}
Otherwise reply naturally in plain text."""

conversation_history = []

def get_friendly_greeting():
    return random.choice(GREETINGS)

def think(user_input):
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            max_tokens=150,
            temperature=0.8,
        )
        reply = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": reply})
        if reply.startswith("{") and reply.endswith("}"):
            try:
                action = json.loads(reply)
                return None, action
            except:
                pass
        return reply, None
    except Exception as e:
        print(f"[Brain Error] {e}")
        return "Sorry, I'm having trouble thinking right now.", None

def clear_memory():
    global conversation_history
    conversation_history = []
    print("[Brain] Memory cleared.")
