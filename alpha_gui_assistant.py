#!/usr/bin/env python3
"""
ALPHA Voice Assistant - Beautiful GUI Interface
Modern design with visual feedback and professional look!
"""

import tkinter as tk
from tkinter import ttk, messagebox
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
import json

class AlphaGUI:
    """Beautiful GUI interface for ALPHA voice assistant."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ALPHA - AI Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize voice assistant
        self.server_url = "http://127.0.0.1:8000"
        self.user_id = "user1"
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.is_active = False
        
        # Wake word settings
        self.WAKE_WORD = "alpha"
        self.WAKE_WORD_ALIASES = ["alpha", "alfa", "alpa", "alpaa"]
        
        # Configure microphone
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Status variables (must be created BEFORE widgets)
        self.status_var = tk.StringVar(value="Ready")
        self.wake_word_var = tk.StringVar(value="ALPHA")
        
        # Create GUI
        self.create_styles()
        self.create_widgets()
        
    def create_styles(self):
        """Create custom styles for the GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#00ff88', 
                       font=('Helvetica', 24, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#1a1a1a', 
                       foreground='#ffffff', 
                       font=('Helvetica', 12))
        
        style.configure('Info.TLabel', 
                       background='#1a1a1a', 
                       foreground='#cccccc', 
                       font=('Helvetica', 10))
        
        style.configure('Start.TButton', 
                       background='#00ff88', 
                       foreground='#000000', 
                       font=('Helvetica', 12, 'bold'))
        
        style.configure('Stop.TButton', 
                       background='#ff4444', 
                       foreground='#ffffff', 
                       font=('Helvetica', 12, 'bold'))
        
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="ALPHA", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="AI Voice Assistant", 
                                  style='Info.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Status display
        status_frame = tk.Frame(main_frame, bg='#1a1a1a')
        status_frame.pack(pady=20)
        
        status_label = ttk.Label(status_frame, 
                                text="Status:", 
                                style='Status.TLabel')
        status_label.pack(side='left', padx=(0, 10))
        
        self.status_display = ttk.Label(status_frame, 
                                       textvariable=self.status_var, 
                                       style='Status.TLabel')
        self.status_display.pack(side='left')
        
        # Wake word display
        wake_frame = tk.Frame(main_frame, bg='#1a1a1a')
        wake_frame.pack(pady=20)
        
        wake_label = ttk.Label(wake_frame, 
                              text="Wake Word:", 
                              style='Status.TLabel')
        wake_label.pack(side='left', padx=(0, 10))
        
        self.wake_display = ttk.Label(wake_frame, 
                                     textvariable=self.wake_word_var, 
                                     style='Status.TLabel')
        self.wake_display.pack(side='left')
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(pady=30)
        
        self.start_button = ttk.Button(button_frame, 
                                      text="Start Listening", 
                                      style='Start.TButton',
                                      command=self.start_listening)
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = ttk.Button(button_frame, 
                                     text="Stop", 
                                     style='Stop.TButton',
                                     command=self.stop_listening,
                                     state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        # Activity indicator
        self.activity_canvas = tk.Canvas(main_frame, 
                                        width=200, 
                                        height=200, 
                                        bg='#1a1a1a', 
                                        highlightthickness=0)
        self.activity_canvas.pack(pady=30)
        
        # Draw initial circle
        self.draw_status_circle('#333333')
        
        # Log display
        log_frame = tk.Frame(main_frame, bg='#1a1a1a')
        log_frame.pack(expand=True, fill='both', pady=20)
        
        log_label = ttk.Label(log_frame, 
                             text="Activity Log:", 
                             style='Status.TLabel')
        log_label.pack(anchor='w')
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(log_frame, bg='#1a1a1a')
        text_frame.pack(expand=True, fill='both', pady=(10, 0))
        
        self.log_text = tk.Text(text_frame, 
                                height=8, 
                                bg='#2a2a2a', 
                                fg='#00ff88', 
                                font=('Consolas', 9),
                                insertbackground='#00ff88')
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Instructions
        instructions = """
        🎧 Say "ALPHA" to activate me!
        💡 I'll respond with your cloned voice
        🛑 Say "quit" to stop completely
        """
        
        instructions_label = ttk.Label(main_frame, 
                                     text=instructions, 
                                     style='Info.TLabel',
                                     justify='center')
        instructions_label.pack(pady=20)
        
    def draw_status_circle(self, color):
        """Draw status circle with given color."""
        self.activity_canvas.delete("all")
        
        # Draw outer circle
        self.activity_canvas.create_oval(20, 20, 180, 180, 
                                        outline=color, 
                                        width=8, 
                                        fill='#1a1a1a')
        
        # Draw inner circle
        self.activity_canvas.create_oval(40, 40, 160, 160, 
                                        outline=color, 
                                        width=4, 
                                        fill='#1a1a1a')
        
        # Draw center dot
        self.activity_canvas.create_oval(70, 70, 130, 130, 
                                        outline=color, 
                                        width=2, 
                                        fill=color)
        
    def log_message(self, message):
        """Add message to log display."""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limit log size
        if int(self.log_text.index('end-1c').split('.')[0]) > 100:
            self.log_text.delete('1.0', '2.0')
    
    def start_listening(self):
        """Start the wake word detection system."""
        self.is_listening = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("Listening for ALPHA...")
        self.draw_status_circle('#00ff88')
        
        self.log_message("🚀 ALPHA started listening...")
        
        # Start listening in separate thread
        self.listen_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop the wake word detection system."""
        self.is_listening = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Stopped")
        self.draw_status_circle('#ff4444')
        
        self.log_message("🛑 ALPHA stopped listening")
    
    def listen_for_wake_word(self):
        """Listen for wake word in background thread."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        
                        try:
                            text = self.recognizer.recognize_google(audio).lower()
                            self.root.after(0, self.log_message, f"🎯 Heard: {text}")
                            
                            # Check for quit commands
                            if any(word in text for word in ["quit", "exit", "stop", "bye"]):
                                self.root.after(0, self.log_message, "🛑 Quit command detected!")
                                self.root.after(0, self.stop_listening)
                                return
                            
                            # Check for wake word
                            if any(alias in text for alias in self.WAKE_WORD_ALIASES):
                                if not self.is_active:
                                    self.root.after(0, self.wake_word_detected, text)
                                else:
                                    self.root.after(0, self.log_message, "⏳ Already active, ignoring...")
                                    
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            self.root.after(0, self.log_message, f"❌ Speech recognition error: {e}")
                            
                    except sr.WaitTimeoutError:
                        continue
                        
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Microphone error: {e}")
    
    def wake_word_detected(self, text):
        """Handle wake word detection."""
        self.is_active = True
        self.status_var.set("ALPHA Activated!")
        self.draw_status_circle('#ffff00')
        
        self.log_message(f"🚀 WAKE WORD DETECTED: {text.upper()}")
        self.play_activation_sound()
        
        # Listen for command
        self.listen_for_command()
    
    def listen_for_command(self):
        """Listen for user command."""
        self.status_var.set("Listening for command...")
        self.draw_status_circle('#ffff00')
        
        self.log_message("🎤 Speak your command now...")
        
        # Start command listening in separate thread
        command_thread = threading.Thread(target=self._listen_command_thread, daemon=True)
        command_thread.start()
    
    def _listen_command_thread(self):
        """Listen for command in background thread."""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    self.root.after(0, self.log_message, f"🗣️ Command: {text}")
                    
                    # Check for quit
                    if any(word in text for word in ["quit", "exit", "stop", "bye", "goodbye"]):
                        self.root.after(0, self.log_message, "🛑 Quit command detected!")
                        self.root.after(0, self.stop_listening)
                        return
                    
                    # Process command
                    self.root.after(0, self.process_command, text)
                    
                except sr.UnknownValueError:
                    self.root.after(0, self.log_message, "❌ Could not understand command")
                    self.root.after(0, self.return_to_listening)
                except sr.RequestError as e:
                    self.root.after(0, self.log_message, f"❌ Speech recognition error: {e}")
                    self.root.after(0, self.return_to_listening)
                    
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Command listening error: {e}")
            self.root.after(0, self.return_to_listening)
    
    def process_command(self, user_input):
        """Process user command."""
        self.status_var.set("Processing command...")
        self.draw_status_circle('#00ffff')
        
        self.log_message(f"🧠 Processing: {user_input}")
        
        # Get AI response
        response_thread = threading.Thread(target=self._get_response_thread, args=(user_input,), daemon=True)
        response_thread.start()
    
    def _get_response_thread(self, user_input):
        """Get AI response in background thread."""
        try:
            response = requests.post(
                f"{self.server_url}/realtime",
                data={
                    "user_id": self.user_id,
                    "text": user_input
                }
            )
            
            if response.status_code == 200:
                self.root.after(0, self.log_message, "✅ Got response, playing audio...")
                self.root.after(0, self.play_response, response.content)
            else:
                self.root.after(0, self.log_message, f"❌ API Error: {response.status_code}")
                self.root.after(0, self.return_to_listening)
                
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Request error: {e}")
            self.root.after(0, self.return_to_listening)
    
    def play_response(self, audio_data):
        """Play audio response."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_data)
                tmp_file_path = tmp_file.name
            
            # Play audio
            audio, sr = sf.read(tmp_file_path)
            sd.play(audio, sr)
            sd.wait()
            
            # Clean up
            os.unlink(tmp_file_path)
            
            self.root.after(0, self.log_message, "🔊 Response played successfully!")
            self.root.after(0, self.return_to_listening)
            
        except Exception as e:
            self.root.after(0, self.log_message, f"❌ Audio playback error: {e}")
            self.root.after(0, self.return_to_listening)
    
    def return_to_listening(self):
        """Return to wake word listening mode."""
        self.is_active = False
        self.status_var.set("Listening for ALPHA...")
        self.draw_status_circle('#00ff88')
        
        self.log_message("🔇 Returning to wake word listening...")
    
    def play_activation_sound(self):
        """Play professional activation sound."""
        try:
            # Create sophisticated activation sound
            sample_rate = 44100
            duration = 0.6
            
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Multi-frequency chord
            freq1 = 523.25  # C5
            freq2 = 659.25  # E5
            freq3 = 783.99  # G5
            
            chord = (np.sin(2 * np.pi * freq1 * t) * 0.2 + 
                    np.sin(2 * np.pi * freq2 * t) * 0.15 + 
                    np.sin(2 * np.pi * freq3 * t) * 0.1)
            
            # Apply fade in/out
            fade_samples = int(0.1 * sample_rate)
            chord[:fade_samples] *= np.linspace(0, 1, fade_samples)
            chord[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            sd.play(chord, sample_rate)
            sd.wait()
            
        except Exception as e:
            self.log_message(f"❌ Activation sound error: {e}")

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = AlphaGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"800x600+{x}+{y}")
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
