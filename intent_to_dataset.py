#!/usr/bin/env python3
"""
Intent to Dataset Converter
Converts intents.json format to question-answer pairs
"""

import json

def load_intents_as_qa(intents_path):
    """
    Load intents.json and convert to question-answer pairs
    """
    try:
        with open(intents_path, 'r', encoding='utf-8') as f:
            intents_data = json.load(f)
        
        questions = []
        answers = []
        
        # Extract from intents format
        if 'intents' in intents_data:
            for intent in intents_data['intents']:
                if 'patterns' in intent and 'responses' in intent:
                    # Use first response for each pattern
                    response = intent['responses'][0] if intent['responses'] else "I don't understand."
                    
                    for pattern in intent['patterns']:
                        questions.append(pattern.lower())
                        answers.append(response)
        
        print(f"✅ Loaded {len(questions)} intent patterns")
        return questions, answers
        
    except FileNotFoundError:
        print(f"⚠️ Intents file not found: {intents_path}")
        return [], []
    except Exception as e:
        print(f"❌ Error loading intents: {e}")
        return [], []

if __name__ == "__main__":
    # Test the function
    questions, answers = load_intents_as_qa("intents.json")
    print(f"Loaded {len(questions)} questions from intents")
    if questions:
        print(f"Sample: {questions[0]} -> {answers[0]}")