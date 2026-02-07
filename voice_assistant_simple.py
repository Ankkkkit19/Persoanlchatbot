#!/usr/bin/env python3
"""
Enhanced Smart Personal Assistant with Voice Recognition
Features: Voice commands, Text-to-Speech (without face recognition for now)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import os
import json

# Try to import chatbot functionality
try:
    from chatbot import get_response
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("⚠️ Original chatbot not available, using fallback responses")

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.setup_voice_engine()
        self.setup_window()
        self.create_widgets()
        self.is_listening = False
        
    def setup_voice_engine(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to set female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
            
            print("✅ Text-to-Speech engine initialized")
            
        except Exception as e:
            print(f"⚠️ TTS engine error: {e}")
            self.tts_engine = None
    
    def setup_window(self):
        """Setup main window"""
        self.root.title("🎤 Voice Assistant Chatbot")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
    
    def create_widgets(self):
        """Create GUI widgets"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#34495e', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🎤 VOICE ASSISTANT CHATBOT",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#34495e'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Speak • Listen • Interact",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#34495e'
        )
        subtitle_label.pack()
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Panel - Voice Controls
        left_panel = tk.Frame(main_frame, bg='#34495e', width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Voice Controls Frame
        voice_frame = tk.LabelFrame(
            left_panel,
            text="🎤 Voice Assistant",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#34495e'
        )
        voice_frame.pack(fill='x', padx=10, pady=10)
        
        # Voice Status
        self.voice_status = tk.Label(
            voice_frame,
            text="🔴 Voice: Ready",
            font=('Arial', 12, 'bold'),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.voice_status.pack(pady=10)
        
        # Voice Controls
        voice_controls = tk.Frame(voice_frame, bg='#34495e')
        voice_controls.pack(pady=10)
        
        self.listen_btn = tk.Button(
            voice_controls,
            text="🎤 Start Listening",
            command=self.toggle_listening,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            width=15
        )
        self.listen_btn.pack(pady=5)
        
        self.speak_btn = tk.Button(
            voice_controls,
            text="🔊 Test Speech",
            command=self.test_speech,
            font=('Arial', 12, 'bold'),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=10,
            width=15
        )
        self.speak_btn.pack(pady=5)
        
        # Voice Commands Help
        help_frame = tk.LabelFrame(
            left_panel,
            text="💡 Voice Commands",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e'
        )
        help_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        help_text = """Try saying:

🎤 "Hello assistant"
🎤 "What time is it?"
🎤 "Weather update"
🎤 "Add expense 50 for food"
🎤 "Today's schedule"
🎤 "Tell me a joke"
🎤 "Motivate me"
🎤 "What can you do?"
🎤 "Stop listening"

📝 Or type normally in chat!"""
        
        help_label = tk.Label(
            help_frame,
            text=help_text,
            font=('Arial', 10),
            fg='white',
            bg='#34495e',
            justify='left',
            anchor='nw'
        )
        help_label.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Right Panel - Chat
        right_panel = tk.Frame(main_frame, bg='#ecf0f1')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            width=50,
            height=25,
            font=('Arial', 11),
            bg='#ffffff',
            fg='#2c3e50',
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configure text tags
        self.chat_display.tag_configure("user", foreground="#3498db", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("assistant", foreground="#27ae60", font=('Arial', 11))
        self.chat_display.tag_configure("system", foreground="#e74c3c", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("voice", foreground="#9b59b6", font=('Arial', 11, 'italic'))
        
        # Input Frame
        input_frame = tk.Frame(right_panel, bg='#ecf0f1')
        input_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        self.message_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='white'
        )
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=8)
        self.message_entry.bind('<Return>', self.send_text_message)
        
        self.send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.send_text_message,
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8
        )
        self.send_btn.pack(side='right')
        
        # Add welcome message
        self.add_welcome_message()
    
    def add_welcome_message(self):
        """Add welcome message"""
        welcome = """🎉 Welcome to Voice Assistant Chatbot!

🚀 NEW VOICE FEATURES:
🎤 Voice Recognition - Speak your commands
🔊 Text-to-Speech - Assistant speaks back
🗣️ Natural Conversation - Talk naturally

📋 VOICE COMMANDS:
• "Hello assistant" - Greet the assistant
• "What time is it?" - Get current time
• "Weather update" - Get weather information
• "Add expense 50 for food" - Voice expense tracking
• "Today's schedule" - Voice schedule management
• "Tell me a joke" - Get programming humor
• "Motivate me" - Get inspirational quotes

💡 GETTING STARTED:
1. Click "Start Listening" to enable voice
2. Speak clearly into your microphone
3. Or type messages normally

🎯 Try saying: "Hello assistant, what can you do?"
"""
        
        self.add_message("System", welcome, "system")
        
        # Speak welcome message
        if self.tts_engine:
            threading.Thread(
                target=self.speak_text,
                args=("Welcome to your voice assistant chatbot! Click start listening to begin.",),
                daemon=True
            ).start()
    
    def add_message(self, sender, message, tag=""):
        """Add message to chat display"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: ", "")
            self.chat_display.insert(tk.END, f"{message}\n\n", "user")
        elif sender == "Voice":
            self.chat_display.insert(tk.END, f"[{timestamp}] 🎤 Voice: ", "")
            self.chat_display.insert(tk.END, f"{message}\n\n", "voice")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] Assistant: ", "")
            self.chat_display.insert(tk.END, f"{message}\n\n", tag or "assistant")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_btn.config(text="🔴 Stop Listening", bg='#27ae60')
            self.voice_status.config(text="🟢 Voice: Listening...", fg='#27ae60')
            threading.Thread(target=self.voice_loop, daemon=True).start()
            self.add_message("System", "🎤 Voice listening started! Speak now...", "system")
        else:
            self.is_listening = False
            self.listen_btn.config(text="🎤 Start Listening", bg='#e74c3c')
            self.voice_status.config(text="🔴 Voice: Ready", fg='#e74c3c')
            self.add_message("System", "🔴 Voice listening stopped.", "system")
    
    def voice_loop(self):
        """Voice recognition loop"""
        recognizer = sr.Recognizer()
        
        try:
            microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.root.after(0, self.add_message, "System", "🎤 Microphone ready! Listening for commands...", "system")
            
            while self.is_listening:
                try:
                    with microphone as source:
                        # Listen for audio with timeout
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Recognize speech
                    text = recognizer.recognize_google(audio)
                    
                    if text:
                        self.root.after(0, self.process_voice_command, text)
                    
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    self.root.after(0, self.add_message, "System", f"❌ Voice recognition error: {e}", "system")
                    break
                    
        except Exception as e:
            self.root.after(0, self.add_message, "System", f"❌ Microphone error: {e}", "system")
    
    def process_voice_command(self, text):
        """Process voice command"""
        self.add_message("Voice", text, "voice")
        
        # Get response
        response = self.get_response(text)
        self.add_message("Assistant", response, "assistant")
        
        # Speak response
        threading.Thread(target=self.speak_text, args=(response,), daemon=True).start()
    
    def test_speech(self):
        """Test text-to-speech"""
        test_message = "Hello! I am your voice assistant chatbot. I can understand your speech and speak back to you!"
        self.speak_text(test_message)
        self.add_message("Assistant", "🔊 Testing speech synthesis... Listen to my voice!", "assistant")
    
    def speak_text(self, text):
        """Convert text to speech"""
        if self.tts_engine:
            try:
                # Clean text for speech (remove emojis and special characters)
                clean_text = ''.join(char for char in text if char.isalnum() or char.isspace() or char in '.,!?-')
                
                # Limit text length for speech
                if len(clean_text) > 200:
                    clean_text = clean_text[:200] + "..."
                
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def send_text_message(self, event=None):
        """Send text message"""
        message = self.message_entry.get().strip()
        if message:
            self.message_entry.delete(0, tk.END)
            self.add_message("You", message)
            
            # Get response
            response = self.get_response(message)
            self.add_message("Assistant", response)
            
            # Speak response if voice is active
            if self.is_listening:
                threading.Thread(target=self.speak_text, args=(response,), daemon=True).start()
    
    def get_response(self, user_input):
        """Get response from chatbot or voice commands"""
        text_lower = user_input.lower()
        
        # Voice-specific commands
        if any(word in text_lower for word in ['hello assistant', 'hi assistant', 'hey assistant']):
            return "Hello! I'm your voice assistant chatbot. How can I help you today?"
        
        elif 'what time' in text_lower or 'current time' in text_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif 'what can you do' in text_lower or 'your features' in text_lower:
            return ("I can understand voice commands, speak responses, manage your schedule, "
                   "track expenses, get weather updates, tell jokes, and provide motivation. "
                   "Try asking about weather, expenses, or schedule!")
        
        elif 'stop listening' in text_lower:
            self.root.after(0, self.toggle_listening)
            return "Voice listening stopped."
        
        elif 'start listening' in text_lower:
            if not self.is_listening:
                self.root.after(0, self.toggle_listening)
            return "Voice listening started."
        
        # Use original chatbot if available
        elif CHATBOT_AVAILABLE:
            return get_response(user_input)
        
        else:
            return ("I heard you say: " + user_input + 
                   ". I can understand voice commands and speak back. Try asking about time, weather, or my features!")

def main():
    """Main function"""
    print("🚀 Starting Voice Assistant Chatbot...")
    
    # Check dependencies
    try:
        import speech_recognition
        import pyttsx3
        print("✅ Voice dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Install with: pip install SpeechRecognition pyttsx3")
        return
    
    try:
        root = tk.Tk()
        app = VoiceAssistant(root)
        
        print("✅ Voice Assistant Chatbot loaded!")
        print("🎤 Voice commands ready")
        print("🔊 Text-to-speech ready")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        messagebox.showerror("Error", f"Failed to start: {e}")

if __name__ == "__main__":
    main()