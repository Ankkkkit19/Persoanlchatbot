#!/usr/bin/env python3
"""
Enhanced Smart Personal Assistant Web App
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import re
from chatbot import get_response

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

@app.route("/", methods=["GET", "POST"])
def home():
    user = ""
    reply = ""

    if request.method == "POST":
        user = request.form.get("msg")
        reply = get_response(user)
        
        # Store in session for context
        if 'conversation' not in session:
            session['conversation'] = []
        
        session['conversation'].append({
            'user': user,
            'bot': reply,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 conversations
        if len(session['conversation']) > 10:
            session['conversation'] = session['conversation'][-10:]

    return render_template("enhanced_index.html", user=user, reply=reply)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """API endpoint for chat"""
    data = request.get_json()
    user_input = data.get('message', '')
    
    if not user_input.strip():
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        response = get_response(user_input)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/quick-actions", methods=["GET"])
def quick_actions():
    """Get quick action suggestions"""
    actions = [
        {
            'title': 'Today\'s Schedule',
            'command': 'Today ka schedule kya hai?',
            'icon': '📅'
        },
        {
            'title': 'Add Expense',
            'command': 'Add expense: 50 for food - Lunch',
            'icon': '💰'
        },
        {
            'title': 'Study Stats',
            'command': 'Study statistics dikhao',
            'icon': '📚'
        },
        {
            'title': 'Weather Update',
            'command': 'Weather kaisa hai?',
            'icon': '🌤️'
        },
        {
            'title': 'Monthly Expenses',
            'command': 'Monthly expense summary',
            'icon': '📊'
        },
        {
            'title': 'Add Schedule',
            'command': 'Add schedule: Meeting on 2024-01-15 14:00',
            'icon': '⏰'
        }
    ]
    
    return jsonify(actions)

@app.route("/dashboard")
def dashboard():
    """Dashboard with quick stats"""
    return render_template("dashboard.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)