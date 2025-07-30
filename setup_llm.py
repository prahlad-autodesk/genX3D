#!/usr/bin/env python3
"""
LLM Setup Script for GenX3D
This script helps you configure your LLM API keys and test the connection.
"""

import os
import sys
from pathlib import Path

def print_banner():
    print("🤖 GenX3D LLM Setup")
    print("=" * 50)

def check_env_file():
    """Check if .env file exists and create one if needed"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        create_env = input("Would you like to create one? (y/n): ").lower().strip()
        
        if create_env == 'y':
            # Copy from example
            example_file = Path("env.example")
            if example_file.exists():
                with open(example_file, 'r') as f:
                    content = f.read()
                
                with open(env_file, 'w') as f:
                    f.write(content)
                
                print("✅ Created .env file from env.example")
                print("📝 Please edit .env file with your API keys")
                return True
            else:
                print("❌ env.example file not found")
                return False
        else:
            return False

def get_llm_choice():
    """Get user's LLM choice"""
    print("\n🔧 Choose your LLM provider:")
    print("1. Groq (Recommended - Fast & Free tier)")
    print("2. OpenAI (Requires paid API key)")
    print("3. Anthropic Claude (Requires paid API key)")
    print("4. Local Ollama (Free, requires installation)")
    print("5. Skip for now (use mock LLM)")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("❌ Invalid choice. Please enter 1-5.")

def setup_groq():
    """Setup Groq API key"""
    print("\n🚀 Setting up Groq...")
    print("1. Go to https://console.groq.com/")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    
    api_key = input("\nEnter your Groq API key: ").strip()
    
    if api_key and api_key != "your_groq_api_key_here":
        # Update .env file
        update_env_file("GROQ_API_KEY", api_key)
        print("✅ Groq API key configured!")
        return True
    else:
        print("❌ Invalid API key")
        return False

def setup_openai():
    """Setup OpenAI API key"""
    print("\n🤖 Setting up OpenAI...")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Create an account and add payment method")
    print("3. Generate an API key")
    
    api_key = input("\nEnter your OpenAI API key: ").strip()
    
    if api_key and api_key != "your_openai_api_key_here":
        # Update .env file
        update_env_file("OPENAI_API_KEY", api_key)
        print("✅ OpenAI API key configured!")
        return True
    else:
        print("❌ Invalid API key")
        return False

def setup_anthropic():
    """Setup Anthropic API key"""
    print("\n🧠 Setting up Anthropic Claude...")
    print("1. Go to https://console.anthropic.com/")
    print("2. Create an account and add payment method")
    print("3. Generate an API key")
    
    api_key = input("\nEnter your Anthropic API key: ").strip()
    
    if api_key and api_key != "your_anthropic_api_key_here":
        # Update .env file
        update_env_file("ANTHROPIC_API_KEY", api_key)
        print("✅ Anthropic API key configured!")
        return True
    else:
        print("❌ Invalid API key")
        return False

def setup_ollama():
    """Setup Ollama"""
    print("\n🦙 Setting up Ollama...")
    print("1. Install Ollama from https://ollama.ai/")
    print("2. Run: ollama pull llama3.2:3b")
    print("3. Start Ollama service")
    
    confirm = input("\nHave you installed and started Ollama? (y/n): ").lower().strip()
    
    if confirm == 'y':
        # Update .env file
        update_env_file("USE_OLLAMA", "true")
        print("✅ Ollama configured!")
        return True
    else:
        print("❌ Please install Ollama first")
        return False

def update_env_file(key, value):
    """Update .env file with new key-value pair"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        return
    
    # Read current content
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update or add the key
    key_found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_found = True
            break
    
    if not key_found:
        lines.append(f"{key}={value}\n")
    
    # Write back
    with open(env_file, 'w') as f:
        f.writelines(lines)

def test_llm_connection():
    """Test LLM connection"""
    print("\n🧪 Testing LLM connection...")
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Import and test LLM
        import sys
        sys.path.append('backend')
        
        from langgraph_app import llm
        
        # Test with a simple message
        from langchain_core.messages import HumanMessage
        
        print("Sending test message...")
        response = llm.ainvoke([HumanMessage(content="Say 'Hello from GenX3D!'")])
        
        print(f"✅ LLM Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def main():
    print_banner()
    
    # Check .env file
    if not check_env_file():
        print("❌ Setup cancelled")
        return
    
    # Get LLM choice
    choice = get_llm_choice()
    
    success = False
    if choice == '1':
        success = setup_groq()
    elif choice == '2':
        success = setup_openai()
    elif choice == '3':
        success = setup_anthropic()
    elif choice == '4':
        success = setup_ollama()
    elif choice == '5':
        print("⏭️  Skipping LLM setup - will use mock LLM")
        success = True
    
    if success:
        print("\n🎉 LLM setup completed!")
        
        # Test connection
        test_connection = input("\nWould you like to test the LLM connection? (y/n): ").lower().strip()
        if test_connection == 'y':
            test_llm_connection()
        
        print("\n📋 Next steps:")
        print("1. Start the backend: poetry run uvicorn backend.main:app --reload --port 8000")
        print("2. Test the chat functionality")
        print("3. Enjoy your AI-powered CAD assistant!")
    else:
        print("\n❌ LLM setup failed. You can still use the mock LLM for testing.")

if __name__ == "__main__":
    main() 