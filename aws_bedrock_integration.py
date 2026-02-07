#!/usr/bin/env python3
"""
AWS Bedrock Integration for Smart Personal Assistant
Enhances the chatbot with advanced AI capabilities
"""

import boto3
import json
from typing import Optional, Dict, Any
import logging
from datetime import datetime

class BedrockEnhancedAssistant:
    """Enhanced assistant using AWS Bedrock"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize Bedrock client"""
        try:
            # Initialize AWS Bedrock client
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name=region_name
            )
            
            # Available models in Bedrock
            self.models = {
                'claude': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'llama': 'meta.llama2-70b-chat-v1',
                'titan': 'amazon.titan-text-express-v1'
            }
            
            self.current_model = self.models['claude']  # Default to Claude
            self.conversation_history = []
            
            print("✅ AWS Bedrock initialized successfully!")
            
        except Exception as e:
            print(f"❌ Bedrock initialization failed: {e}")
            self.bedrock_client = None
    
    def is_available(self) -> bool:
        """Check if Bedrock is available"""
        return self.bedrock_client is not None
    
    def enhance_prompt(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Enhance user prompt with context and instructions"""
        
        system_prompt = """You are a Smart Personal Assistant created by Ankit Kumar Pandit, a B.Tech CSE (AI/ML) student. 

Your capabilities include:
- Answering general knowledge questions with accuracy
- Helping with schedule management and expense tracking
- Providing weather updates and latest news
- Assisting with study sessions and productivity
- Offering programming help and technical explanations
- Giving motivational quotes and entertainment

Guidelines:
- Be helpful, friendly, and accurate
- Use emojis appropriately for better engagement
- For technical questions, provide detailed explanations
- For personal questions about Ankit, mention he's a B.Tech CSE (AI/ML) student at Dev Bhoomi Uttarakhand University, Dehradun
- If you don't know something specific, be honest about it
- Keep responses concise but informative
"""
        
        # Add conversation history for context
        conversation_context = ""
        if self.conversation_history:
            conversation_context = "\n\nRecent conversation:\n"
            for entry in self.conversation_history[-3:]:  # Last 3 exchanges
                conversation_context += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n"
        
        # Add current context if provided
        current_context = ""
        if context:
            current_context = f"\n\nCurrent context: {json.dumps(context, indent=2)}"
        
        enhanced_prompt = f"{system_prompt}{conversation_context}{current_context}\n\nUser: {user_input}\nAssistant:"
        
        return enhanced_prompt
    
    def get_bedrock_response(self, user_input: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Get response from AWS Bedrock"""
        
        if not self.is_available():
            return None
        
        try:
            # Enhance the prompt
            enhanced_prompt = self.enhance_prompt(user_input, context)
            
            # Prepare request body based on model
            if 'claude' in self.current_model:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": enhanced_prompt
                        }
                    ]
                }
            elif 'llama' in self.current_model:
                body = {
                    "prompt": enhanced_prompt,
                    "max_gen_len": 1000,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            else:  # Titan
                body = {
                    "inputText": enhanced_prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 1000,
                        "temperature": 0.7,
                        "topP": 0.9
                    }
                }
            
            # Make request to Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.current_model,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model
            if 'claude' in self.current_model:
                ai_response = response_body['content'][0]['text']
            elif 'llama' in self.current_model:
                ai_response = response_body['generation']
            else:  # Titan
                ai_response = response_body['results'][0]['outputText']
            
            # Update conversation history
            self.conversation_history.append({
                'user': user_input,
                'assistant': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return ai_response.strip()
            
        except Exception as e:
            print(f"❌ Bedrock API error: {e}")
            return None
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to different Bedrock model"""
        if model_name in self.models:
            self.current_model = self.models[model_name]
            print(f"✅ Switched to {model_name} model")
            return True
        else:
            print(f"❌ Model {model_name} not available")
            return False
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✅ Conversation history cleared")

# Integration with existing chatbot
def get_enhanced_response(user_input: str, bedrock_assistant: BedrockEnhancedAssistant = None) -> str:
    """Get enhanced response using Bedrock with fallback to original system"""
    
    # Initialize Bedrock assistant if not provided
    if bedrock_assistant is None:
        bedrock_assistant = BedrockEnhancedAssistant()
    
    # Try Bedrock first
    if bedrock_assistant.is_available():
        print("🤖 Using AWS Bedrock for enhanced response...")
        
        # Add context about user's data if relevant
        context = {
            'timestamp': datetime.now().isoformat(),
            'user_location': 'Dehradun, India',
            'assistant_creator': 'Ankit Kumar Pandit',
            'capabilities': ['general_knowledge', 'schedule_management', 'expense_tracking', 'study_assistance']
        }
        
        bedrock_response = bedrock_assistant.get_bedrock_response(user_input, context)
        
        if bedrock_response:
            return f"🧠 **Enhanced AI Response:**\n\n{bedrock_response}"
    
    # Fallback to original system
    print("⚠️ Falling back to original response system...")
    
    try:
        # Import original response function
        from chatbot import get_response
        return get_response(user_input)
    except ImportError:
        # Final fallback
        from web_search_helper import search_web_answer
        web_response = search_web_answer(user_input)
        return web_response if web_response else "I'm here to help! Please try asking your question again."

# Test function
def test_bedrock_integration():
    """Test Bedrock integration"""
    print("🧪 Testing AWS Bedrock Integration...")
    print("=" * 50)
    
    assistant = BedrockEnhancedAssistant()
    
    if not assistant.is_available():
        print("❌ Bedrock not available. Check AWS credentials and region.")
        return
    
    test_questions = [
        "Who is Albert Einstein?",
        "What is machine learning?",
        "Tell me about Ankit Kumar Pandit",
        "How can I manage my daily expenses?",
        "What's the weather like today?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = get_enhanced_response(question, assistant)
        print(f"✅ Response: {response[:200]}...")
        print("-" * 30)

if __name__ == "__main__":
    test_bedrock_integration()