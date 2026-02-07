#!/usr/bin/env python3
"""
Smart Personal Life Assistant Chatbot
Enhanced version with multiple daily life features
"""

import json
import re
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Any
import sqlite3
import os

class ContextManager:
    """Manages conversation context and user preferences"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.current_context = {}
        self.session_data = {}
    
    def add_to_history(self, user_input: str, bot_response: str):
        """Add conversation to history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'bot': bot_response
        })
        
        # Keep only last 10 conversations
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)
    
    def get_context(self, key: str):
        """Get context value"""
        return self.current_context.get(key)
    
    def set_context(self, key: str, value: Any):
        """Set context value"""
        self.current_context[key] = value

class DatabaseManager:
    """Manages SQLite database for persistent storage"""
    
    def __init__(self, db_path="smart_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Schedule table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date_time DATETIME NOT NULL,
                category TEXT,
                priority INTEGER DEFAULT 1,
                completed BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date DATE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Study sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                duration INTEGER NOT NULL,
                date DATE NOT NULL,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

class ScheduleManager:
    """Manages daily schedule and reminders"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_schedule(self, title: str, date_time: str, description: str = "", category: str = "general"):
        """Add new schedule item"""
        try:
            # Parse date time
            dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO schedule (title, description, date_time, category)
                VALUES (?, ?, ?, ?)
            ''', (title, description, dt, category))
            
            conn.commit()
            conn.close()
            
            return f"✅ Schedule added: {title} on {dt.strftime('%d %B %Y at %I:%M %p')}"
            
        except ValueError:
            return "❌ Invalid date format. Use: YYYY-MM-DD HH:MM"
        except Exception as e:
            return f"❌ Error adding schedule: {str(e)}"
    
    def get_today_schedule(self):
        """Get today's schedule"""
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, description, date_time, category
            FROM schedule
            WHERE DATE(date_time) = ?
            ORDER BY date_time
        ''', (today,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "📅 No schedule for today. You're free!"
        
        schedule_text = "📅 **Today's Schedule:**\n\n"
        for title, desc, dt_str, category in results:
            dt = datetime.fromisoformat(dt_str)
            time_str = dt.strftime('%I:%M %p')
            schedule_text += f"🕐 **{time_str}** - {title}"
            if category != "general":
                schedule_text += f" ({category})"
            if desc:
                schedule_text += f"\n   📝 {desc}"
            schedule_text += "\n\n"
        
        return schedule_text
    
    def get_upcoming_schedule(self, days: int = 7):
        """Get upcoming schedule for next few days"""
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, description, date_time, category
            FROM schedule
            WHERE DATE(date_time) BETWEEN ? AND ?
            ORDER BY date_time
        ''', (start_date, end_date))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"📅 No upcoming schedule for next {days} days."
        
        schedule_text = f"📅 **Upcoming Schedule (Next {days} days):**\n\n"
        current_date = None
        
        for title, desc, dt_str, category in results:
            dt = datetime.fromisoformat(dt_str)
            date_str = dt.strftime('%d %B %Y')
            time_str = dt.strftime('%I:%M %p')
            
            if current_date != date_str:
                current_date = date_str
                schedule_text += f"📆 **{date_str}**\n"
            
            schedule_text += f"  🕐 {time_str} - {title}"
            if category != "general":
                schedule_text += f" ({category})"
            schedule_text += "\n"
        
        return schedule_text

class ExpenseTracker:
    """Tracks daily expenses and provides insights"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.categories = [
            "food", "transport", "entertainment", "study", 
            "shopping", "bills", "health", "other"
        ]
    
    def add_expense(self, amount: float, category: str, description: str = ""):
        """Add new expense"""
        try:
            if category.lower() not in self.categories:
                return f"❌ Invalid category. Use: {', '.join(self.categories)}"
            
            today = datetime.now().date()
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO expenses (amount, category, description, date)
                VALUES (?, ?, ?, ?)
            ''', (amount, category.lower(), description, today))
            
            conn.commit()
            conn.close()
            
            return f"💰 Expense added: ₹{amount} for {category}"
            
        except Exception as e:
            return f"❌ Error adding expense: {str(e)}"
    
    def get_today_expenses(self):
        """Get today's expenses"""
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT amount, category, description
            FROM expenses
            WHERE date = ?
            ORDER BY created_at DESC
        ''', (today,))
        
        results = cursor.fetchall()
        
        # Get total
        cursor.execute('''
            SELECT SUM(amount) FROM expenses WHERE date = ?
        ''', (today,))
        
        total = cursor.fetchone()[0] or 0
        conn.close()
        
        if not results:
            return "💰 No expenses recorded for today."
        
        expense_text = f"💰 **Today's Expenses (Total: ₹{total}):**\n\n"
        for amount, category, desc in results:
            expense_text += f"• ₹{amount} - {category.title()}"
            if desc:
                expense_text += f" ({desc})"
            expense_text += "\n"
        
        return expense_text
    
    def get_monthly_summary(self):
        """Get monthly expense summary"""
        # Get current month data
        now = datetime.now()
        start_date = now.replace(day=1).date()
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Total this month
        cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE date >= ?
        ''', (start_date,))
        
        total = cursor.fetchone()[0] or 0
        
        # Category wise breakdown
        cursor.execute('''
            SELECT category, SUM(amount) FROM expenses 
            WHERE date >= ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (start_date,))
        
        categories = cursor.fetchall()
        conn.close()
        
        summary = f"📊 **Monthly Expense Summary (₹{total}):**\n\n"
        
        for category, amount in categories:
            percentage = (amount / total * 100) if total > 0 else 0
            summary += f"• {category.title()}: ₹{amount} ({percentage:.1f}%)\n"
        
        return summary

class StudyAssistant:
    """Manages study sessions and provides insights"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def log_study_session(self, subject: str, duration: int, notes: str = ""):
        """Log a study session"""
        try:
            today = datetime.now().date()
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO study_sessions (subject, duration, date, notes)
                VALUES (?, ?, ?, ?)
            ''', (subject, duration, today, notes))
            
            conn.commit()
            conn.close()
            
            return f"📚 Study session logged: {subject} for {duration} minutes"
            
        except Exception as e:
            return f"❌ Error logging study session: {str(e)}"
    
    def get_study_stats(self):
        """Get study statistics"""
        today = datetime.now().date()
        week_start = today - timedelta(days=7)
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Today's study time
        cursor.execute('''
            SELECT SUM(duration) FROM study_sessions WHERE date = ?
        ''', (today,))
        
        today_minutes = cursor.fetchone()[0] or 0
        
        # This week's study time
        cursor.execute('''
            SELECT SUM(duration) FROM study_sessions 
            WHERE date >= ?
        ''', (week_start,))
        
        week_minutes = cursor.fetchone()[0] or 0
        
        # Subject wise breakdown (this week)
        cursor.execute('''
            SELECT subject, SUM(duration) FROM study_sessions 
            WHERE date >= ?
            GROUP BY subject
            ORDER BY SUM(duration) DESC
        ''', (week_start,))
        
        subjects = cursor.fetchall()
        conn.close()
        
        stats = f"📚 **Study Statistics:**\n\n"
        stats += f"📅 Today: {today_minutes} minutes ({today_minutes//60}h {today_minutes%60}m)\n"
        stats += f"📊 This Week: {week_minutes} minutes ({week_minutes//60}h {week_minutes%60}m)\n\n"
        
        if subjects:
            stats += "📖 **Subject-wise (This Week):**\n"
            for subject, minutes in subjects:
                stats += f"• {subject}: {minutes} min ({minutes//60}h {minutes%60}m)\n"
        
        return stats

class WeatherService:
    """Provides weather information and suggestions"""
    
    def __init__(self):
        # Using a free weather API (you can replace with your preferred service)
        self.api_key = "your_weather_api_key"  # Replace with actual API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_suggestion(self, city: str = "Dehradun"):
        """Get weather-based suggestions"""
        try:
            # For demo purposes, returning mock data
            # In real implementation, use actual weather API
            
            suggestions = {
                "sunny": "☀️ Sunny day! Perfect for outdoor activities. Don't forget sunscreen!",
                "rainy": "🌧️ Rainy day! Carry umbrella and avoid bike. Bus is safer today.",
                "cloudy": "☁️ Cloudy weather. Good day for studying indoors.",
                "cold": "🥶 Cold weather! Wear warm clothes and carry jacket."
            }
            
            # Mock weather condition (replace with actual API call)
            import random
            condition = random.choice(list(suggestions.keys()))
            
            return f"🌤️ **Weather Update for {city}:**\n{suggestions[condition]}"
            
        except Exception as e:
            return "❌ Unable to fetch weather information."

class MoodDetector:
    """Detects user mood and provides appropriate responses"""
    
    def __init__(self):
        self.positive_words = [
            "happy", "good", "great", "awesome", "excellent", "wonderful",
            "khush", "accha", "badhiya", "mast", "zabardast"
        ]
        
        self.negative_words = [
            "sad", "bad", "terrible", "awful", "stressed", "worried", "tired",
            "udaas", "bura", "pareshan", "tension", "thak gaya"
        ]
        
        self.motivational_quotes = [
            "🌟 Every expert was once a beginner. Keep going!",
            "💪 Success is not final, failure is not fatal. Keep trying!",
            "🚀 The only way to do great work is to love what you do.",
            "✨ Believe in yourself and all that you are!",
            "🎯 Focus on progress, not perfection."
        ]
    
    def detect_mood(self, text: str):
        """Detect mood from user input"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def get_mood_response(self, mood: str):
        """Get appropriate response based on mood"""
        if mood == "positive":
            return "😊 That's great to hear! Keep up the positive energy!"
        elif mood == "negative":
            import random
            return f"😔 I understand you're feeling down. {random.choice(self.motivational_quotes)}"
        else:
            return ""

class IntentClassifier:
    """Classifies user intent from input"""
    
    def __init__(self):
        self.intent_patterns = {
            "schedule": [
                r"schedule|reminder|meeting|class|appointment",
                r"kal|today|tomorrow|time|timing",
                r"add.*schedule|set.*reminder"
            ],
            "expense": [
                r"expense|money|spend|cost|price|rupees|₹",
                r"kharcha|paisa|kharch|bill"
            ],
            "study": [
                r"study|padhai|subject|exam|test|assignment",
                r"log.*study|study.*session"
            ],
            "weather": [
                r"weather|mausam|rain|sunny|temperature",
                r"umbrella|jacket|bike|bus"
            ],
            "mood": [
                r"feeling|mood|happy|sad|stressed|tired",
                r"khush|udaas|pareshan|thak"
            ]
        }
    
    def classify_intent(self, text: str):
        """Classify user intent"""
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        return "general"

class SmartPersonalAssistant:
    """Main Smart Personal Assistant class"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.context_manager = ContextManager()
        self.schedule_manager = ScheduleManager(self.db_manager)
        self.expense_tracker = ExpenseTracker(self.db_manager)
        self.study_assistant = StudyAssistant(self.db_manager)
        self.weather_service = WeatherService()
        self.mood_detector = MoodDetector()
        self.intent_classifier = IntentClassifier()
        
        # Load original chatbot functionality
        try:
            from chatbot import get_response as original_get_response
            self.original_chatbot = original_get_response
        except ImportError:
            self.original_chatbot = None
    
    def process_input(self, user_input: str):
        """Process user input and return appropriate response"""
        
        # Detect mood first
        mood = self.mood_detector.detect_mood(user_input)
        mood_response = self.mood_detector.get_mood_response(mood)
        
        # Classify intent
        intent = self.intent_classifier.classify_intent(user_input)
        
        response = ""
        
        # Handle different intents
        if intent == "schedule":
            response = self.handle_schedule_intent(user_input)
        elif intent == "expense":
            response = self.handle_expense_intent(user_input)
        elif intent == "study":
            response = self.handle_study_intent(user_input)
        elif intent == "weather":
            response = self.handle_weather_intent(user_input)
        else:
            # Use original chatbot for general queries
            if self.original_chatbot:
                response = self.original_chatbot(user_input)
            else:
                response = "I'm here to help! Try asking about schedule, expenses, study sessions, or weather."
        
        # Add mood response if applicable
        if mood_response:
            response = mood_response + "\n\n" + response
        
        # Add to conversation history
        self.context_manager.add_to_history(user_input, response)
        
        return response
    
    def handle_schedule_intent(self, user_input: str):
        """Handle schedule-related queries"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ["today", "aaj"]):
            return self.schedule_manager.get_today_schedule()
        elif any(word in text_lower for word in ["upcoming", "next", "kal", "future"]):
            return self.schedule_manager.get_upcoming_schedule()
        elif any(word in text_lower for word in ["add", "set", "create"]):
            return ("📅 To add schedule, use format:\n"
                   "Add schedule: [Title] on [YYYY-MM-DD HH:MM]\n"
                   "Example: Add schedule: Python class on 2024-01-15 10:00")
        else:
            return self.schedule_manager.get_today_schedule()
    
    def handle_expense_intent(self, user_input: str):
        """Handle expense-related queries"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ["today", "aaj"]):
            return self.expense_tracker.get_today_expenses()
        elif any(word in text_lower for word in ["month", "summary", "total"]):
            return self.expense_tracker.get_monthly_summary()
        elif any(word in text_lower for word in ["add", "spent", "spend"]):
            return ("💰 To add expense, use format:\n"
                   "Add expense: [Amount] for [Category] - [Description]\n"
                   "Categories: food, transport, entertainment, study, shopping, bills, health, other\n"
                   "Example: Add expense: 50 for food - Chai and samosa")
        else:
            return self.expense_tracker.get_today_expenses()
    
    def handle_study_intent(self, user_input: str):
        """Handle study-related queries"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ["stats", "statistics", "summary"]):
            return self.study_assistant.get_study_stats()
        elif any(word in text_lower for word in ["log", "add", "studied"]):
            return ("📚 To log study session, use format:\n"
                   "Log study: [Subject] for [Minutes] minutes - [Notes]\n"
                   "Example: Log study: Python for 60 minutes - Learned loops")
        else:
            return self.study_assistant.get_study_stats()
    
    def handle_weather_intent(self, user_input: str):
        """Handle weather-related queries"""
        return self.weather_service.get_weather_suggestion()

# Main function to get response (compatible with existing chatbot)
def get_smart_response(user_input: str):
    """Get response from Smart Personal Assistant"""
    if not hasattr(get_smart_response, 'assistant'):
        get_smart_response.assistant = SmartPersonalAssistant()
    
    return get_smart_response.assistant.process_input(user_input)

if __name__ == "__main__":
    # Test the assistant
    assistant = SmartPersonalAssistant()
    
    print("🤖 Smart Personal Assistant initialized!")
    print("Try commands like:")
    print("- 'Today ka schedule kya hai?'")
    print("- 'Add expense: 50 for food - Lunch'")
    print("- 'Log study: Python for 60 minutes'")
    print("- 'Weather kaisa hai?'")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        
        response = assistant.process_input(user_input)
        print(f"Bot: {response}")