#!/usr/bin/env python3
"""
Enhanced Smart Personal Assistant with Voice and Face Recognition
Features: Voice commands, Text-to-Speech, Face recognition, Camera capture
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
import os
import json
from PIL import Image, ImageTk
import face_recognition

# Try to import chatbot functionality
try:
    from chatbot import get_response
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("⚠️ Original chatbot not available, using fallback responses")

class VoiceFaceAssistant:
    def __init__(self, root):
        self.root = root
        self.setup_voice_engine()
        self.setup_face_recognition()
        self.setup_window()
        self.create_widgets()
        self.is_listening = False
        self.camera_active = False
        self.user_authenticated = False
        
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
    
    def setup_face_recognition(self):
        """Initialize face recognition"""
        try:
            self.known_faces = []
            self.known_names = []
            self.face_data_file = "face_data.json"
            
            # Load existing face data
            self.load_face_data()
            
            print("✅ Face recognition initialized")
            
        except Exception as e:
            print(f"⚠️ Face recognition error: {e}")
    
    def setup_window(self):
        """Setup main window"""
        self.root.title("🤖 Voice & Face Recognition Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
    
    def create_widgets(self):
        """Create GUI widgets"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#34495e', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🤖 VOICE & FACE RECOGNITION ASSISTANT",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#34495e'
        )
        title_label.pack(pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Speak • Recognize • Interact",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#34495e'
        )
        subtitle_label.pack()
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Panel - Camera & Controls
        left_panel = tk.Frame(main_frame, bg='#34495e', width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Camera Frame
        camera_frame = tk.LabelFrame(
            left_panel,
            text="📷 Face Recognition",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e'
        )
        camera_frame.pack(fill='x', padx=10, pady=10)
        
        # Camera Display
        self.camera_label = tk.Label(
            camera_frame,
            text="Camera will appear here",
            width=50,
            height=20,
            bg='black',
            fg='white'
        )
        self.camera_label.pack(pady=10)
        
        # Camera Controls
        camera_controls = tk.Frame(camera_frame, bg='#34495e')
        camera_controls.pack(pady=5)
        
        self.start_camera_btn = tk.Button(
            camera_controls,
            text="📷 Start Camera",
            command=self.start_camera,
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=15,
            pady=5
        )
        self.start_camera_btn.pack(side='left', padx=5)
        
        self.capture_face_btn = tk.Button(
            camera_controls,
            text="👤 Capture Face",
            command=self.capture_face,
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            padx=15,
            pady=5
        )
        self.capture_face_btn.pack(side='left', padx=5)
        
        # Voice Controls Frame
        voice_frame = tk.LabelFrame(
            left_panel,
            text="🎤 Voice Assistant",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e'
        )
        voice_frame.pack(fill='x', padx=10, pady=10)
        
        # Voice Status
        self.voice_status = tk.Label(
            voice_frame,
            text="🔴 Voice: Ready",
            font=('Arial', 11),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.voice_status.pack(pady=5)
        
        # Voice Controls
        voice_controls = tk.Frame(voice_frame, bg='#34495e')
        voice_controls.pack(pady=5)
        
        self.listen_btn = tk.Button(
            voice_controls,
            text="🎤 Start Listening",
            command=self.toggle_listening,
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=15,
            pady=5
        )
        self.listen_btn.pack(side='left', padx=5)
        
        self.speak_btn = tk.Button(
            voice_controls,
            text="🔊 Test Speech",
            command=self.test_speech,
            font=('Arial', 10, 'bold'),
            bg='#9b59b6',
            fg='white',
            padx=15,
            pady=5
        )
        self.speak_btn.pack(side='left', padx=5)
        
        # Authentication Status
        auth_frame = tk.LabelFrame(
            left_panel,
            text="🔐 Authentication",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e'
        )
        auth_frame.pack(fill='x', padx=10, pady=10)
        
        self.auth_status = tk.Label(
            auth_frame,
            text="❌ Not Authenticated",
            font=('Arial', 11, 'bold'),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.auth_status.pack(pady=10)
        
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
        welcome = """🎉 Welcome to Voice & Face Recognition Assistant!

🚀 NEW FEATURES:
📷 Face Recognition - Capture and recognize your face
🎤 Voice Commands - Speak to interact
🔊 Text-to-Speech - Assistant speaks back
🔐 Authentication - Secure access with face recognition

📋 VOICE COMMANDS:
• "Hello assistant" - Greet the assistant
• "What time is it?" - Get current time
• "Weather update" - Get weather information
• "Add expense 50 for food" - Voice expense tracking
• "Today's schedule" - Voice schedule management

💡 GETTING STARTED:
1. Click "Start Camera" to enable face recognition
2. Click "Capture Face" to register your face
3. Click "Start Listening" for voice commands
4. Or type messages normally

🎯 Try saying: "Hello assistant, what can you do?"
"""
        
        self.add_message("System", welcome, "system")
        
        # Speak welcome message
        if self.tts_engine:
            threading.Thread(
                target=self.speak_text,
                args=("Welcome to your voice and face recognition assistant!",),
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
    
    def start_camera(self):
        """Start camera for face recognition"""
        if not self.camera_active:
            self.camera_active = True
            self.start_camera_btn.config(text="📷 Stop Camera", bg='#e74c3c')
            threading.Thread(target=self.camera_loop, daemon=True).start()
            self.add_message("System", "📷 Camera started! Face recognition active.", "system")
        else:
            self.camera_active = False
            self.start_camera_btn.config(text="📷 Start Camera", bg='#27ae60')
            self.add_message("System", "📷 Camera stopped.", "system")
    
    def camera_loop(self):
        """Camera capture loop"""
        try:
            cap = cv2.VideoCapture(0)
            
            while self.camera_active:
                ret, frame = cap.read()
                if ret:
                    # Flip frame horizontally for mirror effect
                    frame = cv2.flip(frame, 1)
                    
                    # Face recognition
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rgb_frame)
                    
                    # Draw rectangles around faces
                    for (top, right, bottom, left) in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        
                        # Check if face matches known faces
                        if self.known_faces:
                            face_encoding = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])
                            if face_encoding:
                                matches = face_recognition.compare_faces(self.known_faces, face_encoding[0])
                                if True in matches:
                                    name = self.known_names[matches.index(True)]
                                    cv2.putText(frame, f"Welcome {name}!", (left, top-10), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                                    
                                    if not self.user_authenticated:
                                        self.user_authenticated = True
                                        self.auth_status.config(text=f"✅ Authenticated: {name}", fg='#27ae60')
                                        self.root.after(0, self.on_face_recognized, name)
                    
                    # Convert to PhotoImage and display
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_pil = Image.fromarray(frame_rgb)
                    frame_pil = frame_pil.resize((380, 280), Image.Resampling.LANCZOS)
                    frame_tk = ImageTk.PhotoImage(frame_pil)
                    
                    self.camera_label.config(image=frame_tk)
                    self.camera_label.image = frame_tk
                
                time.sleep(0.1)
            
            cap.release()
            
        except Exception as e:
            print(f"Camera error: {e}")
            self.add_message("System", f"❌ Camera error: {str(e)}", "system")
    
    def capture_face(self):
        """Capture and save user's face"""
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            
            if ret:
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                if face_locations:
                    # Get face encoding
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    
                    if face_encodings:
                        # Ask for name
                        name = tk.simpledialog.askstring("Face Registration", "Enter your name:")
                        
                        if name:
                            # Save face encoding
                            self.known_faces.append(face_encodings[0])
                            self.known_names.append(name)
                            self.save_face_data()
                            
                            self.add_message("System", f"✅ Face registered for {name}!", "system")
                            self.speak_text(f"Face registered successfully for {name}")
                        else:
                            self.add_message("System", "❌ Face registration cancelled.", "system")
                    else:
                        self.add_message("System", "❌ Could not encode face. Try again.", "system")
                else:
                    self.add_message("System", "❌ No face detected. Please face the camera.", "system")
            
            cap.release()
            
        except Exception as e:
            self.add_message("System", f"❌ Face capture error: {str(e)}", "system")
    
    def on_face_recognized(self, name):
        """Called when face is recognized"""
        self.add_message("System", f"👋 Welcome back, {name}! Face authentication successful.", "system")
        self.speak_text(f"Welcome back, {name}!")
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_btn.config(text="🔴 Stop Listening", bg='#27ae60')
            self.voice_status.config(text="🟢 Voice: Listening...", fg='#27ae60')
            threading.Thread(target=self.voice_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.listen_btn.config(text="🎤 Start Listening", bg='#e74c3c')
            self.voice_status.config(text="🔴 Voice: Ready", fg='#e74c3c')
    
    def voice_loop(self):
        """Voice recognition loop"""
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
        
        while self.is_listening:
            try:
                with microphone as source:
                    # Listen for audio
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
    
    def process_voice_command(self, text):
        """Process voice command"""
        self.add_message("Voice", text, "voice")
        
        # Get response
        response = self.get_response(text)
        self.add_message("Assistant", response, "assistant")
        
        # Speak response
        self.speak_text(response)
    
    def test_speech(self):
        """Test text-to-speech"""
        test_message = "Hello! I am your voice and face recognition assistant. I can speak and recognize your face!"
        self.speak_text(test_message)
        self.add_message("Assistant", "🔊 Testing speech synthesis...", "assistant")
    
    def speak_text(self, text):
        """Convert text to speech"""
        if self.tts_engine:
            try:
                # Clean text for speech (remove emojis and special characters)
                clean_text = ''.join(char for char in text if char.isalnum() or char.isspace() or char in '.,!?')
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
                self.speak_text(response)
    
    def get_response(self, user_input):
        """Get response from chatbot or voice commands"""
        text_lower = user_input.lower()
        
        # Voice-specific commands
        if any(word in text_lower for word in ['hello assistant', 'hi assistant', 'hey assistant']):
            return "Hello! I'm your voice and face recognition assistant. How can I help you today?"
        
        elif 'what time' in text_lower or 'current time' in text_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif 'what can you do' in text_lower or 'your features' in text_lower:
            return ("I can recognize your face, understand voice commands, speak responses, "
                   "manage your schedule, track expenses, and answer questions. "
                   "Try asking about weather, expenses, or schedule!")
        
        elif 'stop listening' in text_lower:
            self.root.after(0, self.toggle_listening)
            return "Voice listening stopped."
        
        # Use original chatbot if available
        elif CHATBOT_AVAILABLE:
            return get_response(user_input)
        
        else:
            return ("I heard you say: " + user_input + 
                   ". I'm still learning! Try asking about time, weather, or my features.")
    
    def load_face_data(self):
        """Load saved face data"""
        try:
            if os.path.exists(self.face_data_file):
                with open(self.face_data_file, 'r') as f:
                    data = json.load(f)
                    
                self.known_names = data.get('names', [])
                
                # Load face encodings
                encodings_data = data.get('encodings', [])
                self.known_faces = [np.array(encoding) for encoding in encodings_data]
                
                print(f"✅ Loaded {len(self.known_faces)} known faces")
                
        except Exception as e:
            print(f"⚠️ Could not load face data: {e}")
    
    def save_face_data(self):
        """Save face data"""
        try:
            data = {
                'names': self.known_names,
                'encodings': [encoding.tolist() for encoding in self.known_faces]
            }
            
            with open(self.face_data_file, 'w') as f:
                json.dump(data, f)
                
            print("✅ Face data saved")
            
        except Exception as e:
            print(f"⚠️ Could not save face data: {e}")

def main():
    """Main function"""
    print("🚀 Starting Voice & Face Recognition Assistant...")
    
    # Check dependencies
    try:
        import cv2
        import speech_recognition
        import pyttsx3
        import face_recognition
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Install with: pip install opencv-python speechrecognition pyttsx3 face-recognition pillow")
        return
    
    try:
        root = tk.Tk()
        app = VoiceFaceAssistant(root)
        
        print("✅ Voice & Face Recognition Assistant loaded!")
        print("🎤 Voice commands ready")
        print("📷 Face recognition ready")
        print("🔊 Text-to-speech ready")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        messagebox.showerror("Error", f"Failed to start: {e}")

if __name__ == "__main__":
    main()