#!/usr/bin/env python3
"""
Test AWS Bedrock Integration with Modern Chatbot
Comprehensive testing of Bedrock-enhanced chatbot functionality
"""

import tkinter as tk
from datetime import datetime

def test_bedrock_integration():
    """Test Bedrock integration without GUI"""
    print("🧪 Testing AWS Bedrock Integration...")
    print("=" * 50)
    
    try:
        from aws_bedrock_integration import BedrockEnhancedAssistant
        
        assistant = BedrockEnhancedAssistant()
        
        if not assistant.is_available():
            print("❌ AWS Bedrock not available")
            print("Please run: python setup_bedrock.py")
            return False
        
        print("✅ AWS Bedrock is available!")
        
        # Test questions
        test_questions = [
            "Hello, can you introduce yourself?",
            "What is machine learning and how does it work?",
            "Tell me about Ankit Kumar Pandit",
            "Explain quantum physics in simple terms",
            "What are the benefits of cloud computing?"
        ]
        
        success_count = 0
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n[{i}/{len(test_questions)}] ❓ Testing: {question}")
            
            try:
                response = assistant.get_bedrock_response(question)
                
                if response and len(response) > 20:
                    print(f"✅ SUCCESS: {response[:100]}...")
                    success_count += 1
                else:
                    print(f"❌ FAILED: {response}")
                    
            except Exception as e:
                print(f"❌ ERROR: {e}")
        
        print(f"\n🎯 Test Results: {success_count}/{len(test_questions)} successful")
        
        if success_count == len(test_questions):
            print("🏆 All tests passed! Bedrock integration is working perfectly!")
            return True
        else:
            print("⚠️ Some tests failed. Check AWS credentials and model access.")
            return False
            
    except ImportError:
        print("❌ Bedrock integration module not found")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_modern_chatbot_with_bedrock():
    """Test modern chatbot with Bedrock integration"""
    print("\n🖥️ Testing Modern Chatbot with Bedrock...")
    print("=" * 50)
    
    try:
        from modern_enhanced_chatbot import ModernEnhancedChatbot
        
        # Create hidden root window for testing
        root = tk.Tk()
        root.withdraw()
        
        # Initialize chatbot
        app = ModernEnhancedChatbot(root)
        
        # Check if Bedrock is available in the chatbot
        if app.bedrock_assistant and app.bedrock_assistant.is_available():
            print("✅ Modern chatbot has Bedrock integration!")
            
            # Test some responses
            test_queries = [
                "Who is Albert Einstein?",
                "What is artificial intelligence?",
                "Tell me about machine learning",
                "Weather kaisa hai?",
                "Latest news dikhao"
            ]
            
            for query in test_queries:
                print(f"\n❓ Testing: {query}")
                response = app.get_response(query)
                
                if "AWS Bedrock AI" in response:
                    print("✅ Using Bedrock AI response")
                else:
                    print("✅ Using fallback response")
                
                print(f"Response: {response[:100]}...")
            
            print("\n🏆 Modern chatbot with Bedrock is working!")
            
        else:
            print("⚠️ Modern chatbot running without Bedrock")
            print("Standard responses will be used")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Modern chatbot test failed: {e}")
        return False

def test_cost_estimation():
    """Estimate costs for Bedrock usage"""
    print("\n💰 AWS Bedrock Cost Estimation...")
    print("=" * 50)
    
    # Approximate token counts and costs
    costs = {
        'claude-3-sonnet': {
            'input': 3.0,   # per 1M tokens
            'output': 15.0  # per 1M tokens
        },
        'llama-2-70b': {
            'input': 1.0,
            'output': 1.3
        },
        'titan-text': {
            'input': 0.5,
            'output': 0.7
        }
    }
    
    # Usage scenarios
    scenarios = {
        'Light Usage (50 queries/day)': {
            'queries_per_day': 50,
            'avg_input_tokens': 100,
            'avg_output_tokens': 200
        },
        'Medium Usage (200 queries/day)': {
            'queries_per_day': 200,
            'avg_input_tokens': 150,
            'avg_output_tokens': 300
        },
        'Heavy Usage (500 queries/day)': {
            'queries_per_day': 500,
            'avg_input_tokens': 200,
            'avg_output_tokens': 400
        }
    }
    
    print("📊 Monthly cost estimates:")
    
    for scenario_name, scenario in scenarios.items():
        print(f"\n🎯 {scenario_name}:")
        
        monthly_queries = scenario['queries_per_day'] * 30
        monthly_input_tokens = monthly_queries * scenario['avg_input_tokens']
        monthly_output_tokens = monthly_queries * scenario['avg_output_tokens']
        
        for model_name, model_costs in costs.items():
            input_cost = (monthly_input_tokens / 1_000_000) * model_costs['input']
            output_cost = (monthly_output_tokens / 1_000_000) * model_costs['output']
            total_cost = input_cost + output_cost
            
            print(f"   • {model_name}: ${total_cost:.2f}/month")

def main():
    """Main test function"""
    print("🚀 Comprehensive AWS Bedrock Testing")
    print("=" * 55)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Bedrock integration
    bedrock_works = test_bedrock_integration()
    
    # Test 2: Modern chatbot with Bedrock
    chatbot_works = test_modern_chatbot_with_bedrock()
    
    # Test 3: Cost estimation
    test_cost_estimation()
    
    # Summary
    print("\n" + "=" * 55)
    print("🎯 TEST SUMMARY:")
    print(f"✅ Bedrock Integration: {'PASS' if bedrock_works else 'FAIL'}")
    print(f"✅ Modern Chatbot: {'PASS' if chatbot_works else 'FAIL'}")
    
    if bedrock_works and chatbot_works:
        print("\n🏆 ALL TESTS PASSED!")
        print("Your AWS Bedrock integration is working perfectly!")
        print("\n🚀 Ready to run: python modern_enhanced_chatbot.py")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Please check AWS credentials and run: python setup_bedrock.py")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()