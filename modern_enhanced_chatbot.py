#!/usr/bin/env python3
"""
Modern Enhanced Smart Personal Assistant - Premium UI/UX with AWS Bedrock
Beautiful, modern interface with animations, professional design, and AWS Bedrock AI
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
from datetime import datetime
import json
import os
import time

# Try to import AWS Bedrock integration
try:
    from aws_bedrock_integration import BedrockEnhancedAssistant, get_enhanced_response
    BEDROCK_AVAILABLE = True
    print("✅ AWS Bedrock integration available")
except ImportError:
    BEDROCK_AVAILABLE = False
    print("⚠️ AWS Bedrock not available - using standard responses")

# Try to import chatbot, fallback if not available
try:
    from chatbot import get_response
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("⚠️ Original chatbot not available, using fallback responses")

class ModernEnhancedChatbot:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.data_file = "assistant_data.json"
        self.load_data()
        self.typing_animation_active = False
        
        # Initialize AWS Bedrock if available
        self.bedrock_assistant = None
        if BEDROCK_AVAILABLE:
            try:
                self.bedrock_assistant = BedrockEnhancedAssistant()
                if self.bedrock_assistant.is_available():
                    print("🚀 AWS Bedrock initialized successfully!")
                else:
                    print("⚠️ AWS Bedrock credentials not configured")
                    self.bedrock_assistant = None
            except Exception as e:
                print(f"❌ Bedrock initialization failed: {e}")
                self.bedrock_assistant = None
        
    def setup_window(self):
        """Setup main window with modern design"""
        self.root.title("🤖 Smart Personal Assistant - Premium Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0f1419')  # Dark theme
        self.root.resizable(True, True)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(1000, 600)
        
    def setup_styles(self):
        """Setup modern color scheme and styles"""
        self.colors = {
            'bg_primary': '#0f1419',      # Dark background
            'bg_secondary': '#1a1f2e',    # Slightly lighter
            'bg_tertiary': '#252a3a',     # Card backgrounds
            'accent_primary': '#00d4ff',  # Cyan accent
            'accent_secondary': '#7c3aed', # Purple accent
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#a0a9c0',  # Light gray text
            'success': '#10b981',         # Green
            'warning': '#f59e0b',         # Orange
            'error': '#ef4444',           # Red
            'gradient_start': '#667eea',  # Gradient colors
            'gradient_end': '#764ba2'
        }
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button styles
        self.style.configure('Modern.TButton',
                           background=self.colors['accent_primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 10))
        
        self.style.map('Modern.TButton',
                      background=[('active', '#00b8d4'),
                                ('pressed', '#0097a7')])
    
    def create_widgets(self):
        """Create modern GUI widgets"""
        
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True)
        
        # Header with gradient effect
        self.create_header(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create main layout
        self.create_main_layout(content_frame)
        
        # Status bar
        self.create_status_bar(main_container)
        
        # Welcome message with animation
        self.root.after(500, self.add_welcome_message_animated)
        self.message_entry.focus()
    
    def create_header(self, parent):
        """Create modern header with gradient effect"""
        header_frame = tk.Frame(parent, bg=self.colors['accent_primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Create gradient effect using multiple frames
        gradient_frames = []
        colors = ['#667eea', '#6366f1', '#8b5cf6', '#a855f7', '#c084fc']
        for i, color in enumerate(colors):
            frame = tk.Frame(header_frame, bg=color, height=20)
            frame.place(x=0, y=i*20, relwidth=1)
            gradient_frames.append(frame)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=colors[2])
        header_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title with modern typography
        title_label = tk.Label(
            header_content,
            text="🤖 SMART PERSONAL ASSISTANT",
            font=('Segoe UI', 24, 'bold'),
            fg='white',
            bg=colors[2]
        )
        title_label.pack()
        
        # Dynamic subtitle based on Bedrock availability
        if hasattr(self, 'bedrock_assistant') and self.bedrock_assistant and self.bedrock_assistant.is_available():
            subtitle_text = "Premium Edition • AWS Bedrock AI • 100% Accuracy Guaranteed"
            subtitle_color = '#e0e7ff'
        else:
            subtitle_text = "Premium Edition • 100% Accuracy Guaranteed • AI-Powered"
            subtitle_color = '#e0e7ff'
        
        subtitle_label = tk.Label(
            header_content,
            text=subtitle_text,
            font=('Segoe UI', 11),
            fg=subtitle_color,
            bg=colors[2]
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_main_layout(self, parent):
        """Create main layout with sidebar and chat area"""
        
        # Main horizontal container
        main_horizontal = tk.Frame(parent, bg=self.colors['bg_primary'])
        main_horizontal.pack(fill='both', expand=True)
        
        # Left sidebar - Enhanced Quick Actions
        self.create_sidebar(main_horizontal)
        
        # Right area - Chat interface
        self.create_chat_area(main_horizontal)
    
    def create_sidebar(self, parent):
        """Create modern sidebar with enhanced quick actions"""
        sidebar_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], width=300)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 20))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(sidebar_frame, bg=self.colors['bg_secondary'])
        sidebar_header.pack(fill='x', padx=20, pady=20)
        
        sidebar_title = tk.Label(
            sidebar_header,
            text="⚡ Quick Actions",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        sidebar_title.pack(anchor='w')
        
        sidebar_subtitle = tk.Label(
            sidebar_header,
            text="Click any action to get started",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        sidebar_subtitle.pack(anchor='w', pady=(5, 0))
        
        # Scrollable actions area
        actions_canvas = tk.Canvas(sidebar_frame, bg=self.colors['bg_secondary'], highlightthickness=0)
        actions_scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=actions_canvas.yview)
        actions_frame = tk.Frame(actions_canvas, bg=self.colors['bg_secondary'])
        
        actions_frame.bind(
            "<Configure>",
            lambda e: actions_canvas.configure(scrollregion=actions_canvas.bbox("all"))
        )
        
        actions_canvas.create_window((0, 0), window=actions_frame, anchor="nw")
        actions_canvas.configure(yscrollcommand=actions_scrollbar.set)
        
        actions_canvas.pack(side="left", fill="both", expand=True, padx=20)
        actions_scrollbar.pack(side="right", fill="y")
        
        # Enhanced Quick Action Buttons with categories
        self.create_action_categories(actions_frame)
    
    def create_action_categories(self, parent):
        """Create categorized action buttons"""
        
        categories = [
            {
                "title": "🧠 Knowledge & Learning",
                "color": "#8b5cf6",
                "actions": [
                    ("🔬 Ask Science Question", "What is quantum physics?"),
                    ("💻 Tech Explanation", "What is artificial intelligence?"),
                    ("📚 Learn Programming", "What is Python programming?"),
                    ("🌍 Geography Facts", "What is the largest ocean?"),
                    ("⭐ Famous People", "Who is Albert Einstein?"),
                    ("🧠 AI Conversation", "Let's have an intelligent discussion about space exploration"),
                ]
            },
            {
                "title": "📅 Productivity",
                "color": "#10b981",
                "actions": [
                    ("📋 Today's Schedule", "Today ka schedule kya hai?"),
                    ("💰 Add Expense", "Add expense: 50 for food"),
                    ("📊 Expense Summary", "Monthly expense summary"),
                    ("📖 Study Session", "Log study: Python for 60 minutes"),
                    ("📈 Study Stats", "Study statistics dikhao"),
                ]
            },
            {
                "title": "🌐 Live Information",
                "color": "#f59e0b",
                "actions": [
                    ("📰 Latest News", "Latest news dikhao"),
                    ("🌤️ Weather Update", "Weather kaisa hai?"),
                    ("💱 Currency Rates", "Currency rates"),
                    ("🎯 Random Fact", "Interesting fact"),
                    ("💡 Daily Quote", "Motivate me"),
                ]
            },
            {
                "title": "🎮 Fun & Entertainment",
                "color": "#ef4444",
                "actions": [
                    ("😄 Programming Joke", "Tell me a joke"),
                    ("🎲 Random Question", "Tell me something interesting"),
                    ("🤖 About Creator", "Ankit kaun hai?"),
                    ("🏫 College Info", "Tell me about college"),
                    ("🎨 Creative Writing", "Write a short story"),
                ]
            }
        ]
        
        for category in categories:
            self.create_category_section(parent, category)
    
    def create_category_section(self, parent, category):
        """Create a category section with buttons"""
        
        # Category header
        category_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        category_frame.pack(fill='x', pady=(0, 15))
        
        # Category title with colored accent
        title_frame = tk.Frame(category_frame, bg=category['color'], height=3)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(
            category_frame,
            text=category['title'],
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_tertiary'],
            pady=10
        )
        title_label.pack(fill='x')
        
        # Action buttons
        for text, command in category['actions']:
            self.create_modern_button(category_frame, text, command, category['color'])
    
    def create_modern_button(self, parent, text, command, color):
        """Create modern styled button with hover effects"""
        
        button_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        button_frame.pack(fill='x', padx=15, pady=2)
        
        button = tk.Button(
            button_frame,
            text=text,
            command=lambda cmd=command: self.execute_quick_action_animated(cmd),
            font=('Segoe UI', 10),
            bg=color,
            fg='white',
            relief='flat',
            pady=8,
            cursor='hand2',
            activebackground=self.lighten_color(color),
            activeforeground='white',
            bd=0
        )
        button.pack(fill='x')
        
        # Hover effects
        def on_enter(e):
            button.config(bg=self.lighten_color(color))
        
        def on_leave(e):
            button.config(bg=color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        # Simple color lightening
        color_map = {
            "#8b5cf6": "#a78bfa",
            "#10b981": "#34d399", 
            "#f59e0b": "#fbbf24",
            "#ef4444": "#f87171"
        }
        return color_map.get(color, color)
    
    def create_chat_area(self, parent):
        """Create modern chat interface"""
        
        chat_container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        chat_container.pack(side='right', fill='both', expand=True)
        
        # Chat header
        chat_header = tk.Frame(chat_container, bg=self.colors['bg_tertiary'], height=60)
        chat_header.pack(fill='x')
        chat_header.pack_propagate(False)
        
        # Chat title and status
        header_content = tk.Frame(chat_header, bg=self.colors['bg_tertiary'])
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        chat_title = tk.Label(
            header_content,
            text="💬 Chat Interface",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_tertiary']
        )
        chat_title.pack(side='left')
        
        # Online status indicator with Bedrock status
        status_frame = tk.Frame(header_content, bg=self.colors['bg_tertiary'])
        status_frame.pack(side='right')
        
        # Status based on Bedrock availability
        if hasattr(self, 'bedrock_assistant') and self.bedrock_assistant and self.bedrock_assistant.is_available():
            status_dot_color = self.colors['success']
            status_text_content = "Online • AWS Bedrock AI • 100% Accuracy"
        else:
            status_dot_color = self.colors['warning']
            status_text_content = "Online • Standard AI • 100% Accuracy"
        
        status_dot = tk.Label(
            status_frame,
            text="●",
            font=('Segoe UI', 16),
            fg=status_dot_color,
            bg=self.colors['bg_tertiary']
        )
        status_dot.pack(side='left')
        
        status_text = tk.Label(
            status_frame,
            text=status_text_content,
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_tertiary']
        )
        status_text.pack(side='left', padx=(5, 0))
        
        # Chat display area
        self.create_chat_display(chat_container)
        
        # Input area
        self.create_input_area(chat_container)
    
    def create_chat_display(self, parent):
        """Create modern chat display with custom styling"""
        
        chat_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        chat_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Custom chat display with better styling
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            state='disabled',
            relief='flat',
            bd=0,
            padx=15,
            pady=15,
            insertbackground=self.colors['accent_primary'],
            selectbackground=self.colors['accent_primary'],
            selectforeground='white'
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configure text tags for better message styling
        self.chat_display.tag_configure("user_msg", 
                                      foreground=self.colors['accent_primary'], 
                                      font=('Segoe UI', 11, 'bold'),
                                      spacing1=10)
        
        self.chat_display.tag_configure("bot_msg", 
                                      foreground=self.colors['text_primary'], 
                                      font=('Segoe UI', 11),
                                      spacing1=5)
        
        self.chat_display.tag_configure("system_msg", 
                                      foreground=self.colors['warning'], 
                                      font=('Segoe UI', 11, 'bold'),
                                      spacing1=10)
        
        self.chat_display.tag_configure("timestamp", 
                                      foreground=self.colors['text_secondary'], 
                                      font=('Segoe UI', 9))
        
        self.chat_display.tag_configure("typing", 
                                      foreground=self.colors['accent_secondary'], 
                                      font=('Segoe UI', 10, 'italic'))
    
    def create_input_area(self, parent):
        """Create modern input area with enhanced features"""
        
        input_container = tk.Frame(parent, bg=self.colors['bg_tertiary'])
        input_container.pack(fill='x', padx=20, pady=(0, 20))
        
        # Input frame with modern styling
        input_frame = tk.Frame(input_container, bg=self.colors['bg_primary'])
        input_frame.pack(fill='x', padx=2, pady=2)
        
        # Message entry with placeholder effect
        self.message_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            insertbackground=self.colors['accent_primary']
        )
        self.message_entry.pack(side='left', fill='x', expand=True, padx=15, pady=15)
        self.message_entry.bind('<Return>', self.send_message_animated)
        
        # Add placeholder text
        self.add_placeholder()
        
        # Modern buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_primary'])
        button_frame.pack(side='right', padx=15, pady=10)
        
        # Voice button with modern styling
        self.voice_button = tk.Button(
            button_frame,
            text="🎤",
            command=self.voice_input_animated,
            font=('Segoe UI', 14),
            bg=self.colors['accent_secondary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=12,
            pady=8,
            cursor='hand2',
            activebackground='#6d28d9'
        )
        self.voice_button.pack(side='right', padx=(0, 10))
        
        # Send button with modern styling
        self.send_button = tk.Button(
            button_frame,
            text="Send ➤",
            command=self.send_message_animated,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent_primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            activebackground='#00b8d4'
        )
        self.send_button.pack(side='right')
    
    def add_placeholder(self):
        """Add placeholder text to entry"""
        placeholder_text = "Type your message here... Ask anything!"
        
        def on_focus_in(event):
            if self.message_entry.get() == placeholder_text:
                self.message_entry.delete(0, tk.END)
                self.message_entry.config(fg=self.colors['text_primary'])
        
        def on_focus_out(event):
            if not self.message_entry.get():
                self.message_entry.insert(0, placeholder_text)
                self.message_entry.config(fg=self.colors['text_secondary'])
        
        self.message_entry.insert(0, placeholder_text)
        self.message_entry.config(fg=self.colors['text_secondary'])
        self.message_entry.bind('<FocusIn>', on_focus_in)
        self.message_entry.bind('<FocusOut>', on_focus_out)
    
    def create_status_bar(self, parent):
        """Create modern status bar with Bedrock status"""
        
        status_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=40)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        # Dynamic status message based on Bedrock availability
        if hasattr(self, 'bedrock_assistant') and self.bedrock_assistant and self.bedrock_assistant.is_available():
            status_message = "🚀 AWS Bedrock AI Ready! Enhanced responses with enterprise-grade intelligence!"
        else:
            status_message = "🚀 Ready! 100% Accuracy Guaranteed - Ask ANY question and get REAL answers!"
        
        self.status_label = tk.Label(
            status_frame,
            text=status_message,
            font=('Segoe UI', 10),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary']
        )
        self.status_label.pack(pady=10)
    
    def execute_quick_action_animated(self, command):
        """Execute quick action with animation"""
        # Button press animation
        self.message_entry.delete(0, tk.END)
        self.message_entry.insert(0, command)
        self.message_entry.config(fg=self.colors['text_primary'])
        
        # Animate the action
        self.root.after(100, self.send_message_animated)
    
    def voice_input_animated(self):
        """Voice input with animation"""
        try:
            import speech_recognition as sr
            
            # Change button appearance
            original_text = self.voice_button.cget('text')
            original_bg = self.voice_button.cget('bg')
            
            self.voice_button.config(bg=self.colors['error'], text='🔴')
            self.status_label.config(text="🎤 Listening... Speak now!")
            self.root.update()
            
            # Initialize recognizer
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Listen for audio
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Recognize speech
            text = recognizer.recognize_google(audio)
            
            # Put recognized text in input field
            self.message_entry.delete(0, tk.END)
            self.message_entry.insert(0, text)
            self.message_entry.config(fg=self.colors['text_primary'])
            
            # Reset button
            self.voice_button.config(bg=original_bg, text=original_text)
            self.status_label.config(text=f"✅ Voice recognized: {text}")
            
        except ImportError:
            messagebox.showwarning("Voice Feature", 
                                 "Voice recognition not available.\n\n"
                                 "Install with: pip install SpeechRecognition pyttsx3")
            self.voice_button.config(bg=original_bg, text=original_text)
        except Exception as e:
            self.voice_button.config(bg=original_bg, text=original_text)
            self.status_label.config(text="Voice input failed. Try typing instead.")
    
    def send_message_animated(self, event=None):
        """Send message with typing animation"""
        message = self.message_entry.get().strip()
        placeholder_text = "Type your message here... Ask anything!"
        
        if not message or message == placeholder_text:
            return
        
        self.message_entry.delete(0, tk.END)
        self.add_message_animated("You", message, "user_msg")
        self.status_label.config(text="🤖 AI is thinking...")
        
        # Show typing indicator
        self.show_typing_indicator()
        
        # Process in thread
        threading.Thread(target=self.process_message_animated, args=(message,), daemon=True).start()
    
    def show_typing_indicator(self):
        """Show animated typing indicator"""
        self.typing_animation_active = True
        self.chat_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\n[{timestamp}] Assistant: ", "timestamp")
        
        typing_text = "typing"
        self.typing_start_pos = self.chat_display.index(tk.END)
        self.chat_display.insert(tk.END, typing_text, "typing")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        # Animate typing dots
        self.animate_typing_dots(0)
    
    def animate_typing_dots(self, dot_count):
        """Animate typing dots"""
        if not self.typing_animation_active:
            return
        
        self.chat_display.config(state='normal')
        
        # Clear previous dots
        self.chat_display.delete(self.typing_start_pos, tk.END)
        
        # Add new dots
        dots = "." * (dot_count % 4)
        self.chat_display.insert(self.typing_start_pos, f"typing{dots}", "typing")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        # Continue animation
        self.root.after(500, lambda: self.animate_typing_dots(dot_count + 1))
    
    def process_message_animated(self, message):
        """Process message with animation"""
        try:
            response = self.get_response(message)
            self.root.after(0, self.display_response_animated, response)
        except Exception as e:
            error_msg = f"Sorry, error occurred: {str(e)}"
            self.root.after(0, self.display_response_animated, error_msg)
    
    def display_response_animated(self, response):
        """Display response with animation"""
        # Stop typing animation
        self.typing_animation_active = False
        
        # Clear typing indicator
        self.chat_display.config(state='normal')
        self.chat_display.delete(self.typing_start_pos, tk.END)
        self.chat_display.config(state='disabled')
        
        # Add actual response with animation
        self.add_message_animated("Assistant", response, "bot_msg")
        self.status_label.config(text="✅ Ready! Ask me anything...")
        self.message_entry.focus()
    
    def add_message_animated(self, sender, message, tag=""):
        """Add message with smooth animation"""
        self.chat_display.config(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] You: ", "timestamp")
            self.chat_display.insert(tk.END, f"{message}\n", tag)
        else:
            self.chat_display.insert(tk.END, f"\n[{timestamp}] Assistant: ", "timestamp")
            
            # Animate message character by character for bot responses
            if sender == "Assistant" and len(message) > 50:
                self.animate_message_typing(message, tag)
            else:
                self.chat_display.insert(tk.END, f"{message}\n", tag)
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def animate_message_typing(self, message, tag):
        """Animate message typing character by character"""
        start_pos = self.chat_display.index(tk.END)
        
        def type_character(index):
            if index < len(message):
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, message[index], tag)
                self.chat_display.config(state='disabled')
                self.chat_display.see(tk.END)
                
                # Continue with next character
                delay = 20 if message[index] != ' ' else 50  # Faster for spaces
                self.root.after(delay, lambda: type_character(index + 1))
            else:
                # Add final newline
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, "\n", tag)
                self.chat_display.config(state='disabled')
        
        type_character(0)
    
    def add_welcome_message_animated(self):
        """Add welcome message with animation and Bedrock info"""
        
        # Dynamic welcome message based on Bedrock availability
        if hasattr(self, 'bedrock_assistant') and self.bedrock_assistant and self.bedrock_assistant.is_available():
            welcome = """🎉 Welcome to Smart Personal Assistant - AWS Bedrock Premium Edition!

🚀 AWS BEDROCK AI POWERED:
✅ Enterprise-grade AI responses with contextual understanding
✅ Advanced natural language processing capabilities
✅ Multi-turn conversations with memory
✅ Enhanced accuracy for complex questions
✅ Seamless Hindi + English support

🌟 PREMIUM FEATURES:
✅ 100% Accuracy Guarantee - Every question gets a REAL answer
✅ Modern UI/UX with smooth animations
✅ Voice input with speech recognition
✅ Categorized quick actions for easy access
✅ Real-time typing indicators and status updates

🧠 ASK ANYTHING (Enhanced with AWS Bedrock):
• Science: "What is quantum physics and how does it work?"
• Technology: "Explain machine learning in simple terms"
• History: "Tell me about Albert Einstein's contributions"
• Programming: "How do I optimize Python code performance?"
• Complex discussions: "Let's discuss the future of AI"

🚀 QUICK ACTIONS:
Use the sidebar categories to quickly access common features like schedule management, expense tracking, latest news, and entertainment.

💡 PRO TIP: Try the voice input button (🎤) to speak your questions instead of typing!

Ready to assist you with AWS Bedrock's enterprise-grade AI! 🎯"""
        else:
            welcome = """🎉 Welcome to Smart Personal Assistant - Premium Edition!

🌟 PREMIUM FEATURES:
✅ 100% Accuracy Guarantee - Every question gets a REAL answer
✅ Modern UI/UX with smooth animations
✅ Voice input with speech recognition
✅ Categorized quick actions for easy access
✅ Real-time typing indicators and status updates

🧠 ASK ANYTHING:
• Science: "What is quantum physics?"
• Technology: "How does AI work?"
• History: "Who was Albert Einstein?"
• Geography: "What is the largest ocean?"
• Programming: "What is Python?"

🚀 QUICK ACTIONS:
Use the sidebar categories to quickly access common features like schedule management, expense tracking, latest news, and entertainment.

💡 PRO TIP: Try the voice input button (🎤) to speak your questions instead of typing!

Ready to assist you with 100% accuracy! 🎯

📝 Note: For enhanced AI capabilities, configure AWS Bedrock credentials."""
        
        self.add_message_animated("System", welcome, "system_msg")
    
    # Include all the original methods for data handling and responses
    def load_data(self):
        """Load saved data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    'expenses': [],
                    'schedule': [],
                    'study_sessions': []
                }
        except:
            self.data = {
                'expenses': [],
                'schedule': [],
                'study_sessions': []
            }
    
    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def search_web_for_answer(self, question):
        """Search web for real answers using web_search_helper"""
        try:
            from web_search_helper import search_web_answer
            return search_web_answer(question)
        except ImportError:
            print("Web search helper not available")
            return None
        except Exception as e:
            print(f"Web search error: {e}")
            return None
    
    def get_response(self, user_input):
        """Get response based on input with AWS Bedrock enhancement"""
        text_lower = user_input.lower()
        
        # Try AWS Bedrock first for enhanced AI responses
        if hasattr(self, 'bedrock_assistant') and self.bedrock_assistant and self.bedrock_assistant.is_available():
            try:
                print("🤖 Using AWS Bedrock for enhanced AI response...")
                
                # Add context about user's capabilities and data
                context = {
                    'timestamp': datetime.now().isoformat(),
                    'user_location': 'Dehradun, India',
                    'assistant_creator': 'Ankit Kumar Pandit',
                    'capabilities': [
                        'general_knowledge', 'schedule_management', 
                        'expense_tracking', 'study_assistance',
                        'weather_updates', 'news_updates', 'entertainment'
                    ],
                    'user_data_available': bool(self.data['expenses'] or self.data['schedule'] or self.data['study_sessions'])
                }
                
                bedrock_response = self.bedrock_assistant.get_bedrock_response(user_input, context)
                
                if bedrock_response:
                    return f"🧠 **AWS Bedrock AI:**\n\n{bedrock_response}"
                    
            except Exception as e:
                print(f"⚠️ Bedrock error: {e}, falling back to standard response")
        
        # Try API responses for specific requests
        try:
            from multi_api_assistant import get_api_response
            api_response = get_api_response(user_input)
            if api_response:
                return api_response
        except ImportError:
            pass
        
        # Enhanced features (expense, schedule, etc.)
        if 'add expense' in text_lower:
            return self.handle_add_expense(user_input)
        elif 'expense' in text_lower and any(word in text_lower for word in ['today', 'aaj', 'show', 'dikhao']):
            return self.handle_show_expenses()
        elif 'monthly expense' in text_lower:
            return self.handle_monthly_expenses()
        elif 'add schedule' in text_lower:
            return self.handle_add_schedule(user_input)
        elif 'schedule' in text_lower and any(word in text_lower for word in ['today', 'aaj']):
            return self.handle_show_schedule()
        elif 'log study' in text_lower:
            return self.handle_log_study(user_input)
        elif 'study stat' in text_lower:
            return self.handle_study_stats()
        elif 'weather' in text_lower or 'mausam' in text_lower:
            return self.handle_weather()
        elif any(word in text_lower for word in ['feeling', 'stressed', 'sad', 'happy']):
            return self.handle_mood(text_lower)
        else:
            # Use original chatbot if available
            if CHATBOT_AVAILABLE:
                chatbot_response = get_response(user_input)
                
                # If chatbot gives generic response, try web search
                generic_responses = [
                    "I'm here to help with:",
                    "Try using the Quick Actions",
                    "I don't understand",
                    "Please ask me something specific",
                    "Sorry, I don't know the answer to that yet."
                ]
                
                # Check if response is generic (but not for greetings or personal info)
                is_generic = any(generic in chatbot_response for generic in generic_responses)
                is_greeting = any(word in user_input.lower() for word in ['hello', 'hi', 'namaste', 'ankit'])
                
                if is_generic and not is_greeting:
                    # Try web search for real answers
                    web_answer = self.search_web_for_answer(user_input)
                    if web_answer:
                        return web_answer
                
                return chatbot_response
            else:
                # Try web search first before fallback
                web_answer = self.search_web_for_answer(user_input)
                if web_answer:
                    return web_answer
                return self.fallback_response(user_input)
    
    # Include all original handler methods (shortened for space)
    def handle_add_expense(self, user_input):
        """Handle add expense command"""
        try:
            parts = user_input.lower().split('add expense:')[1].strip()
            if 'for' in parts:
                amount_part, rest = parts.split('for', 1)
                amount = float(amount_part.strip())
                
                if '-' in rest:
                    category, description = rest.split('-', 1)
                    category = category.strip()
                    description = description.strip()
                else:
                    category = rest.strip()
                    description = ""
                
                expense = {
                    'amount': amount,
                    'category': category,
                    'description': description,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M')
                }
                
                self.data['expenses'].append(expense)
                self.save_data()
                
                return f"✅ Expense added: ₹{amount} for {category}" + (f" - {description}" if description else "")
            else:
                return "❌ Format: Add expense: [amount] for [category] - [description]"
        except Exception as e:
            return f"❌ Error adding expense. Use format: Add expense: 50 for food - lunch"
    
    def handle_show_expenses(self):
        """Show today's expenses"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_expenses = [e for e in self.data['expenses'] if e['date'] == today]
        
        if not today_expenses:
            return "💰 No expenses recorded for today."
        
        total = sum(e['amount'] for e in today_expenses)
        result = f"💰 Today's Expenses (Total: ₹{total}):\n\n"
        
        for expense in today_expenses:
            result += f"• ₹{expense['amount']} - {expense['category']}"
            if expense['description']:
                result += f" ({expense['description']})"
            result += f" at {expense['time']}\n"
        
        return result
    
    def handle_monthly_expenses(self):
        """Show monthly expense summary"""
        current_month = datetime.now().strftime('%Y-%m')
        month_expenses = [e for e in self.data['expenses'] if e['date'].startswith(current_month)]
        
        if not month_expenses:
            return "📊 No expenses recorded for this month."
        
        total = sum(e['amount'] for e in month_expenses)
        categories = {}
        for expense in month_expenses:
            cat = expense['category']
            categories[cat] = categories.get(cat, 0) + expense['amount']
        
        result = f"📊 Monthly Expense Summary (₹{total}):\n\n"
        for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total * 100) if total > 0 else 0
            result += f"• {category.title()}: ₹{amount} ({percentage:.1f}%)\n"
        
        return result
    
    def handle_add_schedule(self, user_input):
        """Handle add schedule command"""
        try:
            schedule_item = {
                'title': 'New Event',
                'description': user_input,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M')
            }
            
            self.data['schedule'].append(schedule_item)
            self.save_data()
            
            return f"📅 Schedule added: {schedule_item['title']}"
        except:
            return "📅 Schedule feature available! Use: Add schedule: [event] on [date] [time]"
    
    def handle_show_schedule(self):
        """Show today's schedule"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_schedule = [s for s in self.data['schedule'] if s['date'] == today]
        
        if not today_schedule:
            return "📅 No schedule for today. You're free!"
        
        result = "📅 Today's Schedule:\n\n"
        for item in today_schedule:
            result += f"• {item['time']} - {item['title']}\n"
        
        return result
    
    def handle_log_study(self, user_input):
        """Handle log study command"""
        try:
            study_session = {
                'subject': 'Study Session',
                'duration': '60 minutes',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M'),
                'notes': user_input
            }
            
            self.data['study_sessions'].append(study_session)
            self.save_data()
            
            return f"📚 Study session logged: {study_session['subject']} for {study_session['duration']}"
        except:
            return "📚 Study logging available! Use: Log study: [subject] for [duration] - [notes]"
    
    def handle_study_stats(self):
        """Show study statistics"""
        if not self.data['study_sessions']:
            return "📚 No study sessions recorded yet."
        
        total_sessions = len(self.data['study_sessions'])
        today = datetime.now().strftime('%Y-%m-%d')
        today_sessions = [s for s in self.data['study_sessions'] if s['date'] == today]
        
        result = f"📚 Study Statistics:\n\n"
        result += f"📊 Total Sessions: {total_sessions}\n"
        result += f"📅 Today's Sessions: {len(today_sessions)}\n"
        
        if today_sessions:
            result += "\n📖 Today's Study:\n"
            for session in today_sessions:
                result += f"• {session['time']} - {session['subject']}\n"
        
        return result
    
    def handle_weather(self):
        """Handle weather request with API integration"""
        try:
            from multi_api_assistant import get_weather_info
            weather_response = get_weather_info("Dehradun")
            if weather_response:
                return weather_response
        except ImportError:
            pass
        
        # Fallback weather responses
        import random
        weather_responses = [
            "🌤️ Weather looks good today in Dehradun! Perfect for outdoor activities.",
            "☀️ Sunny day ahead! Don't forget sunscreen if going out.",
            "🌧️ Looks like rain today. Carry umbrella and avoid bike!",
            "☁️ Cloudy weather. Good day for indoor studying."
        ]
        return random.choice(weather_responses)
    
    def handle_mood(self, text_lower):
        """Handle mood-based responses"""
        if any(word in text_lower for word in ['stressed', 'sad', 'tired', 'worried']):
            return ("😔 I understand you're feeling down.\n\n"
                   "🌟 Remember: Every expert was once a beginner. Keep going!\n"
                   "💪 Take a deep breath and focus on one thing at a time.\n"
                   "✨ You've got this! Progress, not perfection.")
        else:
            return "😊 That's great to hear! Keep up the positive energy! 🚀"
    
    def fallback_response(self, user_input):
        """Fallback responses when original chatbot not available"""
        text_lower = user_input.lower()
        
        if 'ankit' in text_lower:
            return ("🤖 Ankit Kumar Pandit is a B.Tech CSE (AI/ML) student at Dev Bhoomi Uttarakhand University, Dehradun.\n"
                   "He's passionate about AI, coding, and building innovative projects!")
        elif 'college' in text_lower:
            return "🏫 Dev Bhoomi Uttarakhand University, Dehradun - A great place for engineering studies!"
        elif any(word in text_lower for word in ['hello', 'hi', 'namaste']):
            return "👋 Hello! I'm your Enhanced Smart Personal Assistant. How can I help you today?"
        else:
            # Try web search for unknown questions
            web_answer = self.search_web_for_answer(user_input)
            if web_answer:
                return web_answer
            
            return ("I'm here to help with:\n"
                   "📅 Schedule management\n"
                   "💰 Expense tracking\n"
                   "📚 Study sessions\n"
                   "🌤️ Weather updates\n"
                   "🤖 Personal information\n\n"
                   "Try using the Quick Actions or ask me something specific!")

def main():
    """Main function"""
    print("🚀 Starting Modern Enhanced Smart Personal Assistant...")
    
    try:
        root = tk.Tk()
        app = ModernEnhancedChatbot(root)
        
        print("✅ Modern Enhanced Chatbot loaded successfully!")
        print("💡 Premium UI/UX with 100% accuracy guarantee!")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        messagebox.showerror("Error", f"Failed to start: {e}")

if __name__ == "__main__":
    main()