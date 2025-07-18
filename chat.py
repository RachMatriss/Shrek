#!/usr/bin/env python3
"""
Shrek AI Chat Bot using Mistral AI APIs
An improved version with better security, error handling, and user experience
"""

import os
import sys
import json
from typing import Optional, Dict, Any
import requests
from datetime import datetime

class ShrekChatBot:
    """Main chat bot class using Mistral AI"""
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-large-latest"
        self.conversation_history = []
        self.max_history = 10
        
    def _get_api_key(self) -> str:
        """Securely get API key from environment variable"""
        #api_key = os.getenv("MISTRAL_API_KEY")
        api_key = "wAXWy1eeUpdccaTA8pgFPhk24PEr0gV6"
        if not api_key:
            print("❌ Error: MISTRAL_API_KEY environment variable not found")
            print("Please set your Mistral API key: export MISTRAL_API_KEY='your-key-here'")
            sys.exit(1)
        return api_key
    
    def _make_request(self, messages: list) -> Optional[str]:
        """Make API request to Mistral AI"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 1.0,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except requests.exceptions.Timeout:
            return "⏰ Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"❌ Network error: {str(e)}"
        except KeyError:
            return "❌ Invalid response format from API"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def _format_message(self, role: str, content: str) -> Dict[str, str]:
        """Format message for API"""
        return {"role": role, "content": content}
    
    def _add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append(self._format_message(role, content))
        
        # Keep only recent messages
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def _get_context_messages(self) -> list:
        """Get formatted messages including system prompt"""
        system_prompt = {
            "role": "system",
            "content": """You are Shrek, the friendly ogre from the swamp. 
            You speak with Scottish accent and have a grumpy but lovable personality. 
            You're protective of your swamp and love your family. 
            Keep responses conversational, humorous, and in character as Shrek."""
        }
        
        messages = [system_prompt]
        messages.extend(self.conversation_history)
        return messages
    
    def chat(self, user_input: str) -> str:
        """Process user input and get AI response"""
        if not user_input.strip():
            return "Oi! Say somethin', will ya?"
        
        # Add user message to history
        self._add_to_history("user", user_input)
        
        # Get messages with context
        messages = self._get_context_messages()
        
        # Get AI response
        response = self._make_request(messages)
        
        if response and not response.startswith("❌") and not response.startswith("⏰"):
            self._add_to_history("assistant", response)
        
        return response
    
    def save_conversation(self, filename: Optional[str] = None):
        """Save conversation history to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shrek_chat_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Could not save conversation: {e}")
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🧹 Conversation history cleared!")

def display_banner():
    """Display welcome banner"""
    banner = """
    🏰  Welcome to Shrek's Swamp Chat!  🏰
    
    I'm Shrek, your friendly neighborhood ogre!
    Ask me anything, and I'll give you my honest ogre opinion.
    
    Commands:
    • Type 'save' to save this conversation
    • Type 'clear' to clear chat history
    • Type 'quit', 'exit', or 'q' to leave the swamp
    
    Let's have a chat, shall we?
    """
    print(banner)

def main():
    """Main chat loop"""
    display_banner()
    
    try:
        bot = ShrekChatBot()
    except SystemExit:
        return
    
    print("\n🗣️  Shrek is ready to chat!\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("\n👋 Shrek: Farewell, traveler! Don't forget to visit the swamp again!")
                break
            
            elif user_input.lower() == 'save':
                bot.save_conversation()
                continue
            
            elif user_input.lower() == 'clear':
                bot.clear_history()
                continue
            
            # Get AI response
            response = bot.chat(user_input)
            print(f"\n🟢 Shrek: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Shrek: Oi! No need to be rude! See ya later!")
            break
        except EOFError:
            print("\n\n👋 Shrek: Looks like you left without sayin' goodbye!")
            break
    
    # Save conversation on exit
    save_on_exit = input("\n💾 Save this conversation before leaving? (y/n): ").strip().lower()
    if save_on_exit in ['y', 'yes']:
        bot.save_conversation()

if __name__ == "__main__":
    main()
