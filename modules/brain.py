"""
ALPHA Brain — powered by Groq
Handles all intelligent responses + intent detection
"""

from groq import Groq
import random

GROQ_API_KEY = "os.environ.get("GROQ_API_KEY", "")"

client = Groq(api_key=GROQ_API_KEY)

# Friendly greeting variations — like Siri/Alexa
GREETINGS = [
    "Hmm?",
    "Hi Shaun!",
    "Hey, what's up?",
    "Yeah?",
    "I'm here!",
    "Hello! How can I help?",
    "Hi! What do you need?",
]

SYSTEM_PROMPT = """You are ALPHA, a personal AI voice assistant for Shaun.
You are friendly, smart, and concise — like Siri or Google Assistant.

Rules:
- Keep responses SHORT (1-3 sentences max) — this is voice, not text
- Be warm and friendly, use the user's name "Shaun" occasionally
- Vary your responses — don't always start the same way
- For greetings like "hi" or "good morning" — respond naturally and warmly
- For questions — answer directly and clearly
- For tasks (open app, set timer, etc.) — confirm what you're doing
- Never say "As an AI..." or long disclaimers
- Sound like a helpful friend, not a robot

If the user asks you to do something that needs PC control (take screenshot, 
open app, check files), reply with JSON like:
{"action": "screenshot"} or {"action": "open_app", "app": "chrome"}
Otherwise just reply naturally in plain text."""

# Conversation memory (keeps last 10 exchanges)
conversation_history = []

def get_friendly_greeting():
    """Returns a random friendly activation response"""
    return random.choice(GREETINGS)

def think(user_input):
    """
    Send user input to Groq and get intelligent response.
    Returns (response_text, action_dict_or_None)
    """
    global conversation_history

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Keep only last 10 messages (5 exchanges) to avoid token bloat
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + conversation_history,
            max_tokens=150,
            temperature=0.8,
        )

        reply = response.choices[0].message.content.strip()

        # Add assistant reply to history
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        # Check if it's a JSON action command
        if reply.startswith("{") and reply.endswith("}"):
            import json
            try:
                action = json.loads(reply)
                return None, action  # No speech, just action
            except:
                pass

        return reply, None

    except Exception as e:
        print(f"[Brain Error] {e}")
        return "Sorry, I'm having trouble thinking right now.", None


def clear_memory():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    print("[Brain] Memory cleared.")
