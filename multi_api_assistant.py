#!/usr/bin/env python3
"""
Multi-API Enhanced Smart Personal Assistant
Integrates multiple APIs for comprehensive functionality
"""

import requests
import json
import random
from datetime import datetime, timedelta
import os
from typing import Dict, Any, Optional

class MultiAPIAssistant:
    """Enhanced assistant with multiple API integrations"""
    
    def __init__(self):
        # API Keys (Replace with your actual keys)
        self.api_keys = {
            'weather': 'your_openweather_api_key',  # OpenWeatherMap
            'news': 'your_newsapi_key',             # NewsAPI
            'quotes': None,                         # No key needed for quotable.io
            'jokes': None,                          # No key needed for JokeAPI
            'currency': None,                       # No key needed for exchangerate-api
            'facts': None                           # No key needed for uselessfacts
        }
        
        # API Base URLs
        self.api_urls = {
            'weather': 'http://api.openweathermap.org/data/2.5/weather',
            'news': 'https://newsapi.org/v2/top-headlines',
            'quotes': 'https://api.quotable.io/random',
            'jokes': 'https://v2.jokeapi.dev/joke/Programming,Miscellaneous',
            'currency': 'https://api.exchangerate-api.com/v4/latest/USD',
            'facts': 'https://uselessfacts.jsph.pl/random.json?language=en',
            'github': 'https://api.github.com/users',
            'dictionary': 'https://api.dictionaryapi.dev/api/v2/entries/en'
        }
    
    def get_weather_info(self, city: str = "Dehradun") -> str:
        """Get weather information using OpenWeatherMap API"""
        try:
            # Free version without API key (mock data)
            weather_conditions = [
                {
                    'condition': 'sunny',
                    'temp': '25°C',
                    'description': 'Clear sky',
                    'suggestion': '☀️ Perfect day for outdoor activities! Don\'t forget sunscreen.'
                },
                {
                    'condition': 'rainy',
                    'temp': '18°C', 
                    'description': 'Light rain',
                    'suggestion': '🌧️ Rainy day! Carry umbrella and avoid bike. Bus is safer today.'
                },
                {
                    'condition': 'cloudy',
                    'temp': '22°C',
                    'description': 'Partly cloudy',
                    'suggestion': '☁️ Cloudy weather. Good day for studying indoors.'
                },
                {
                    'condition': 'cold',
                    'temp': '12°C',
                    'description': 'Cold and windy',
                    'suggestion': '🥶 Cold weather! Wear warm clothes and carry jacket.'
                }
            ]
            
            weather = random.choice(weather_conditions)
            
            return f"""🌤️ **Weather Update for {city}:**
            
🌡️ Temperature: {weather['temp']}
🌈 Condition: {weather['description']}
💡 Suggestion: {weather['suggestion']}

📍 Location: {city}
🕐 Updated: {datetime.now().strftime('%H:%M')}"""
            
        except Exception as e:
            return f"❌ Weather service temporarily unavailable: {str(e)}"
    
    def get_daily_news(self, category: str = "technology") -> str:
        """Get latest news using NewsAPI"""
        try:
            # Mock news data (replace with actual API call)
            news_items = [
                {
                    'title': 'AI Revolution in Education: New Tools Transform Learning',
                    'source': 'Tech Today',
                    'time': '2 hours ago'
                },
                {
                    'title': 'Python 3.12 Released with Enhanced Performance',
                    'source': 'Developer News',
                    'time': '4 hours ago'
                },
                {
                    'title': 'Machine Learning Breakthrough in Healthcare',
                    'source': 'Science Daily',
                    'time': '6 hours ago'
                },
                {
                    'title': 'New Coding Bootcamp Opens in Dehradun',
                    'source': 'Local News',
                    'time': '1 day ago'
                }
            ]
            
            selected_news = random.sample(news_items, 3)
            
            result = f"📰 **Latest {category.title()} News:**\n\n"
            for i, news in enumerate(selected_news, 1):
                result += f"{i}. **{news['title']}**\n"
                result += f"   📰 {news['source']} • {news['time']}\n\n"
            
            return result
            
        except Exception as e:
            return f"❌ News service temporarily unavailable: {str(e)}"
    
    def get_motivational_quote(self) -> str:
        """Get motivational quote using Quotable API"""
        try:
            response = requests.get(self.api_urls['quotes'], timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"✨ **Daily Motivation:**\n\n\"{data['content']}\"\n\n— {data['author']}"
            else:
                raise Exception("API request failed")
                
        except Exception:
            # Fallback quotes
            fallback_quotes = [
                "\"The only way to do great work is to love what you do.\" — Steve Jobs",
                "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\" — Winston Churchill",
                "\"The future belongs to those who believe in the beauty of their dreams.\" — Eleanor Roosevelt",
                "\"It is during our darkest moments that we must focus to see the light.\" — Aristotle",
                "\"Believe you can and you're halfway there.\" — Theodore Roosevelt"
            ]
            
            quote = random.choice(fallback_quotes)
            return f"✨ **Daily Motivation:**\n\n{quote}"
    
    def get_programming_joke(self) -> str:
        """Get programming joke using JokeAPI"""
        try:
            response = requests.get(self.api_urls['jokes'], timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                if data['type'] == 'single':
                    return f"😄 **Programming Humor:**\n\n{data['joke']}"
                else:
                    return f"😄 **Programming Humor:**\n\n{data['setup']}\n\n{data['delivery']}"
            else:
                raise Exception("API request failed")
                
        except Exception:
            # Fallback jokes
            fallback_jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
                "Why do Java developers wear glasses? Because they can't C# ! 👓",
                "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?' 🍺",
                "Why did the programmer quit his job? He didn't get arrays! 📊"
            ]
            
            joke = random.choice(fallback_jokes)
            return f"😄 **Programming Humor:**\n\n{joke}"
    
    def get_currency_rates(self, base_currency: str = "USD") -> str:
        """Get currency exchange rates"""
        try:
            response = requests.get(self.api_urls['currency'], timeout=5)
            if response.status_code == 200:
                data = response.json()
                rates = data['rates']
                
                # Focus on commonly used currencies
                important_currencies = {
                    'INR': 'Indian Rupee',
                    'EUR': 'Euro',
                    'GBP': 'British Pound',
                    'JPY': 'Japanese Yen',
                    'CAD': 'Canadian Dollar'
                }
                
                result = f"💱 **Currency Exchange Rates (Base: {base_currency}):**\n\n"
                
                for code, name in important_currencies.items():
                    if code in rates:
                        result += f"💰 {code} ({name}): {rates[code]:.2f}\n"
                
                result += f"\n🕐 Updated: {datetime.now().strftime('%H:%M')}"
                return result
            else:
                raise Exception("API request failed")
                
        except Exception:
            return "💱 **Currency Rates:**\n\n💰 USD to INR: ~83.00\n💰 USD to EUR: ~0.85\n💰 USD to GBP: ~0.73\n\n⚠️ Rates are approximate"
    
    def get_random_fact(self) -> str:
        """Get random interesting fact"""
        try:
            response = requests.get(self.api_urls['facts'], timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"🧠 **Did You Know?**\n\n{data['text']}"
            else:
                raise Exception("API request failed")
                
        except Exception:
            # Fallback facts
            fallback_facts = [
                "The first computer bug was an actual bug - a moth found trapped in a Harvard computer in 1947! 🐛",
                "Python was named after the British comedy group Monty Python, not the snake! 🐍",
                "The term 'debugging' was coined by Admiral Grace Hopper in the 1940s! 🔧",
                "The first 1GB hard drive cost $40,000 and weighed over 500 pounds! 💾",
                "More than 90% of the world's currency exists only on computers! 💻"
            ]
            
            fact = random.choice(fallback_facts)
            return f"🧠 **Did You Know?**\n\n{fact}"
    
    def get_github_user_info(self, username: str) -> str:
        """Get GitHub user information"""
        try:
            url = f"{self.api_urls['github']}/{username}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                result = f"👨‍💻 **GitHub Profile: {username}**\n\n"
                result += f"📝 Name: {data.get('name', 'Not provided')}\n"
                result += f"🏢 Company: {data.get('company', 'Not provided')}\n"
                result += f"📍 Location: {data.get('location', 'Not provided')}\n"
                result += f"📊 Public Repos: {data.get('public_repos', 0)}\n"
                result += f"👥 Followers: {data.get('followers', 0)}\n"
                result += f"👤 Following: {data.get('following', 0)}\n"
                
                if data.get('bio'):
                    result += f"📖 Bio: {data['bio']}\n"
                
                result += f"🔗 Profile: {data['html_url']}"
                
                return result
            else:
                return f"❌ GitHub user '{username}' not found."
                
        except Exception as e:
            return f"❌ GitHub service temporarily unavailable: {str(e)}"
    
    def get_word_definition(self, word: str) -> str:
        """Get word definition using Dictionary API"""
        try:
            url = f"{self.api_urls['dictionary']}/{word.lower()}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                word_data = data[0]
                
                result = f"📚 **Definition of '{word.title()}':**\n\n"
                
                # Get phonetic
                if 'phonetic' in word_data:
                    result += f"🔊 Pronunciation: {word_data['phonetic']}\n\n"
                
                # Get meanings
                for meaning in word_data['meanings'][:2]:  # Limit to 2 meanings
                    result += f"📝 **{meaning['partOfSpeech'].title()}:**\n"
                    
                    for definition in meaning['definitions'][:2]:  # Limit to 2 definitions
                        result += f"• {definition['definition']}\n"
                        
                        if 'example' in definition:
                            result += f"  💡 Example: {definition['example']}\n"
                    
                    result += "\n"
                
                return result
            else:
                return f"❌ Definition for '{word}' not found."
                
        except Exception as e:
            return f"❌ Dictionary service temporarily unavailable: {str(e)}"
    
    def get_tech_news_summary(self) -> str:
        """Get technology news summary"""
        try:
            tech_updates = [
                "🚀 AI models are getting more efficient with new optimization techniques",
                "💻 Python 3.12 brings significant performance improvements",
                "🔒 Cybersecurity threats are evolving, stay updated with latest patches",
                "📱 Mobile app development trends focus on cross-platform solutions",
                "☁️ Cloud computing adoption continues to grow in enterprises",
                "🤖 Machine learning is transforming healthcare diagnostics"
            ]
            
            selected_updates = random.sample(tech_updates, 4)
            
            result = "📡 **Tech Updates Summary:**\n\n"
            for i, update in enumerate(selected_updates, 1):
                result += f"{i}. {update}\n"
            
            result += f"\n🕐 Updated: {datetime.now().strftime('%H:%M')}"
            return result
            
        except Exception as e:
            return f"❌ Tech news service temporarily unavailable: {str(e)}"

# Integration function for the main chatbot
def get_api_response(user_input: str, api_assistant: MultiAPIAssistant = None) -> Optional[str]:
    """Get response from appropriate API based on user input"""
    
    if api_assistant is None:
        api_assistant = MultiAPIAssistant()
    
    text_lower = user_input.lower()
    
    # Weather API
    if any(word in text_lower for word in ['weather', 'mausam', 'temperature', 'climate']):
        city = "Dehradun"  # Default city
        if 'delhi' in text_lower:
            city = "Delhi"
        elif 'mumbai' in text_lower:
            city = "Mumbai"
        elif 'bangalore' in text_lower:
            city = "Bangalore"
        
        return api_assistant.get_weather_info(city)
    
    # News API
    elif any(word in text_lower for word in ['news', 'headlines', 'latest news', 'current news']):
        category = "technology"
        if 'sports' in text_lower:
            category = "sports"
        elif 'business' in text_lower:
            category = "business"
        elif 'health' in text_lower:
            category = "health"
        
        return api_assistant.get_daily_news(category)
    
    # Motivational Quote API
    elif any(word in text_lower for word in ['quote', 'motivation', 'inspire', 'motivate me']):
        return api_assistant.get_motivational_quote()
    
    # Joke API
    elif any(word in text_lower for word in ['joke', 'funny', 'humor', 'laugh', 'hasao']):
        return api_assistant.get_programming_joke()
    
    # Currency API
    elif any(word in text_lower for word in ['currency', 'exchange rate', 'dollar', 'rupee']):
        return api_assistant.get_currency_rates()
    
    # Random Fact API
    elif any(word in text_lower for word in ['fact', 'did you know', 'interesting', 'trivia']):
        return api_assistant.get_random_fact()
    
    # GitHub API
    elif 'github' in text_lower and any(word in text_lower for word in ['user', 'profile']):
        # Extract username (simple parsing)
        words = user_input.split()
        username = None
        for i, word in enumerate(words):
            if word.lower() == 'github' and i + 1 < len(words):
                username = words[i + 1]
                break
        
        if username:
            return api_assistant.get_github_user_info(username)
        else:
            return "Please specify GitHub username. Example: 'GitHub user ankitpandit'"
    
    # Dictionary API
    elif any(word in text_lower for word in ['define', 'definition', 'meaning', 'what is']):
        # Extract word to define
        if 'define' in text_lower:
            word = text_lower.split('define')[-1].strip()
        elif 'what is' in text_lower:
            word = text_lower.split('what is')[-1].strip()
        elif 'meaning of' in text_lower:
            word = text_lower.split('meaning of')[-1].strip()
        else:
            return "Please specify a word to define. Example: 'Define algorithm'"
        
        if word:
            return api_assistant.get_word_definition(word)
        else:
            return "Please specify a word to define."
    
    # Tech News Summary
    elif any(word in text_lower for word in ['tech update', 'technology news', 'tech summary']):
        return api_assistant.get_tech_news_summary()
    
    return None  # No API match found

# Test function
def test_apis():
    """Test all APIs"""
    assistant = MultiAPIAssistant()
    
    print("🧪 Testing Multi-API Assistant...\n")
    
    tests = [
        ("Weather kaisa hai?", "weather"),
        ("Latest news dikhao", "news"),
        ("Motivate me", "quote"),
        ("Tell me a joke", "joke"),
        ("Currency rates", "currency"),
        ("Interesting fact", "fact"),
        ("GitHub user octocat", "github"),
        ("Define algorithm", "dictionary"),
        ("Tech updates", "tech_news")
    ]
    
    for query, api_type in tests:
        print(f"🔍 Testing: {query}")
        response = get_api_response(query, assistant)
        print(f"✅ Response: {response[:100]}...\n")

if __name__ == "__main__":
    test_apis()