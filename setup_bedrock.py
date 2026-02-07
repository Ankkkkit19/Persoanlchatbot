#!/usr/bin/env python3
"""
AWS Bedrock Setup and Configuration Script
Helps set up AWS Bedrock integration for the Smart Personal Assistant
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def check_python_packages():
    """Check and install required Python packages"""
    print("🔍 Checking Python packages...")
    
    required_packages = ['boto3', 'awscli']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    print("\n🔑 Checking AWS credentials...")
    
    # Check for AWS credentials file
    aws_credentials_path = Path.home() / '.aws' / 'credentials'
    aws_config_path = Path.home() / '.aws' / 'config'
    
    if aws_credentials_path.exists() or aws_config_path.exists():
        print("✅ AWS credentials file found")
        
        # Try to test credentials
        try:
            import boto3
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"✅ AWS credentials are valid for account: {identity.get('Account', 'Unknown')}")
            return True
        except Exception as e:
            print(f"⚠️ AWS credentials found but may be invalid: {e}")
            return False
    else:
        print("❌ AWS credentials not found")
        return False

def setup_aws_credentials():
    """Guide user through AWS credentials setup"""
    print("\n🛠️ AWS Credentials Setup")
    print("=" * 40)
    
    print("To use AWS Bedrock, you need:")
    print("1. AWS Account with Bedrock access")
    print("2. AWS Access Key ID and Secret Access Key")
    print("3. Bedrock model access enabled")
    
    choice = input("\nDo you want to configure AWS credentials now? (y/n): ").lower()
    
    if choice == 'y':
        print("\nPlease run the following command in your terminal:")
        print("aws configure")
        print("\nYou'll need to provide:")
        print("- AWS Access Key ID")
        print("- AWS Secret Access Key")
        print("- Default region name (recommended: us-east-1)")
        print("- Default output format (recommended: json)")
        
        input("\nPress Enter after you've configured AWS credentials...")
        return check_aws_credentials()
    else:
        print("⚠️ AWS Bedrock features will not be available without credentials")
        return False

def test_bedrock_access():
    """Test AWS Bedrock access"""
    print("\n🧪 Testing AWS Bedrock access...")
    
    try:
        import boto3
        
        # Test Bedrock client
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        
        # List available models
        response = bedrock.list_foundation_models()
        models = response.get('modelSummaries', [])
        
        if models:
            print(f"✅ Bedrock access confirmed! Found {len(models)} available models")
            
            # Show some available models
            print("\n📋 Available models:")
            for model in models[:5]:  # Show first 5 models
                print(f"   • {model.get('modelName', 'Unknown')} ({model.get('modelId', 'Unknown')})")
            
            return True
        else:
            print("⚠️ Bedrock access granted but no models available")
            print("Please enable model access in AWS Bedrock console")
            return False
            
    except Exception as e:
        print(f"❌ Bedrock access test failed: {e}")
        print("\nPossible issues:")
        print("- AWS credentials not configured")
        print("- Bedrock not available in your region")
        print("- Insufficient permissions")
        print("- Bedrock models not enabled")
        return False

def create_bedrock_config():
    """Create Bedrock configuration file"""
    print("\n📝 Creating Bedrock configuration...")
    
    config = {
        "bedrock_settings": {
            "region": "us-east-1",
            "default_model": "anthropic.claude-3-sonnet-20240229-v1:0",
            "max_tokens": 1000,
            "temperature": 0.7,
            "fallback_enabled": True
        },
        "cost_controls": {
            "max_monthly_cost": 50.0,
            "alert_threshold": 80.0,
            "token_limit_per_request": 1000
        }
    }
    
    config_file = "bedrock_config.json"
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration saved to {config_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def run_integration_test():
    """Run integration test"""
    print("\n🚀 Running integration test...")
    
    try:
        from aws_bedrock_integration import BedrockEnhancedAssistant
        
        assistant = BedrockEnhancedAssistant()
        
        if assistant.is_available():
            print("✅ Bedrock integration test passed!")
            
            # Test a simple query
            test_query = "Hello, can you introduce yourself?"
            print(f"\n🧪 Testing query: {test_query}")
            
            response = assistant.get_bedrock_response(test_query)
            
            if response:
                print(f"✅ Response received: {response[:100]}...")
                return True
            else:
                print("❌ No response received")
                return False
        else:
            print("❌ Bedrock integration not available")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AWS Bedrock Setup for Smart Personal Assistant")
    print("=" * 55)
    
    # Step 1: Check Python packages
    if not check_python_packages():
        print("❌ Setup failed at package installation")
        return
    
    # Step 2: Check AWS credentials
    if not check_aws_credentials():
        if not setup_aws_credentials():
            print("❌ Setup failed at AWS credentials")
            return
    
    # Step 3: Test Bedrock access
    if not test_bedrock_access():
        print("⚠️ Bedrock access test failed, but continuing setup...")
    
    # Step 4: Create configuration
    create_bedrock_config()
    
    # Step 5: Run integration test
    if run_integration_test():
        print("\n🎉 AWS Bedrock setup completed successfully!")
        print("\n🚀 You can now run the enhanced chatbot:")
        print("python modern_enhanced_chatbot.py")
    else:
        print("\n⚠️ Setup completed with warnings")
        print("Bedrock features may not work until credentials are properly configured")
    
    print("\n📚 For detailed setup instructions, see: bedrock_setup_guide.md")

if __name__ == "__main__":
    main()