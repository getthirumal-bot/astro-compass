"""
Astro Consensus Engine - Main Application
Uses Gemini 1.5 Flash for 5-system astrology synthesis
"""

import os
from datetime import datetime
from typing import Optional, Dict
import google.generativeai as genai

# Import our ephemeris calculator
import sys
sys.path.append('/home/claude/astro-app/utils')
from ephemeris import calculate_chart, calculate_transits, format_chart_for_ai


class AstroConsensusEngine:
    """Main application class for the Astro Consensus Engine"""
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        genai.configure(api_key=api_key)
        
        # Load master system prompt
        with open('/home/claude/astro-app/prompts/master_system_prompt.txt', 'r') as f:
            self.system_prompt = f.read()
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=self.system_prompt
        )
        
        # Store user data (in production, this would be database)
        self.user_data = {}
    
    def register_user(self, phone: str, birth_data: Dict) -> str:
        """
        Register a new user with birth details
        
        Args:
            phone: Phone number (unique identifier)
            birth_data: {
                'name': str,
                'dob': datetime,
                'tob': datetime (time of birth),
                'lat': float,
                'lon': float,
                'place': str
            }
        """
        # Calculate birth chart
        birth_datetime = datetime.combine(
            birth_data['dob'].date(),
            birth_data['tob'].time()
        )
        
        chart = calculate_chart(
            birth_datetime,
            birth_data['lat'],
            birth_data['lon']
        )
        
        # Store user data
        self.user_data[phone] = {
            'name': birth_data['name'],
            'birth_chart': chart,
            'birth_details': birth_data,
            'chat_history': [],
            'language': 'English',  # Default, can be changed
            'custom_systems': []  # User can add Nadi, etc.
        }
        
        return f"Welcome {birth_data['name']}! Your cosmic profile is ready."
    
    def get_prediction(self, phone: str, query: str) -> str:
        """
        Get prediction for user query
        
        Args:
            phone: User's phone number
            query: Question or topic
        
        Returns:
            AI-generated response from 5-system consensus
        """
        if phone not in self.user_data:
            return "Please register first with your birth details."
        
        user = self.user_data[phone]
        
        # Get current transits
        transits = calculate_transits()
        
        # Format chart data
        chart_text = format_chart_for_ai(user['birth_chart'], transits)
        
        # Build context for AI
        context = f"""
USER: {user['name']}
LANGUAGE PREFERENCE: {user['language']}

{chart_text}

QUERY: {query}
"""
        
        # Add chat history if exists
        if user['chat_history']:
            context += "\nPREVIOUS CONVERSATION:\n"
            for msg in user['chat_history'][-5:]:  # Last 5 messages
                context += f"User: {msg['query']}\nAssistant: {msg['response']}\n\n"
        
        # Get AI response
        response = self.model.generate_content(context)
        
        # Store in chat history
        user['chat_history'].append({
            'query': query,
            'response': response.text,
            'timestamp': datetime.now()
        })
        
        return response.text
    
    def set_language(self, phone: str, language: str):
        """Set user's preferred language"""
        if phone in self.user_data:
            self.user_data[phone]['language'] = language
            return f"Language set to {language}"
        return "User not found"
    
    def add_custom_system(self, phone: str, system_name: str, system_data: str):
        """
        Add user's custom prediction system (Nadi, Palmistry, etc.)
        
        Args:
            phone: User phone
            system_name: Name of system (e.g., "Shiva Nadi")
            system_data: Text description of their profile in that system
        """
        if phone in self.user_data:
            self.user_data[phone]['custom_systems'].append({
                'name': system_name,
                'data': system_data
            })
            return f"{system_name} added to your profile"
        return "User not found"


def test_api_connection(api_key: str) -> bool:
    """Test if Gemini API key works"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'API working' if you can read this.")
        print(f"✓ API Test: {response.text}")
        return True
    except Exception as e:
        print(f"✗ API Test Failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("ASTRO CONSENSUS ENGINE - INITIALIZATION")
    print("=" * 60)
    
    # You'll need to add your Gemini API key here
    # Get it from: https://makersuite.google.com/app/apikey
    
    API_KEY = "YOUR_GEMINI_API_KEY_HERE"
    
    if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n⚠️  Please set your Gemini API key in the code")
        print("Get it from: https://makersuite.google.com/app/apikey")
    else:
        print("\nTesting API connection...")
        if test_api_connection(API_KEY):
            print("\n✓ System ready!")
            
            # Example usage
            engine = AstroConsensusEngine(API_KEY)
            
            # Register test user (you)
            engine.register_user(
                phone="+919876543210",
                birth_data={
                    'name': 'Thiru',
                    'dob': datetime(1976, 7, 31),
                    'tob': datetime(1976, 7, 31, 8, 12),
                    'lat': 15.5057,
                    'lon': 80.0499,
                    'place': 'Ongole'
                }
            )
            
            # Test query
            response = engine.get_prediction(
                "+919876543210",
                "Will my new app be successful?"
            )
            
            print("\n" + "=" * 60)
            print("TEST PREDICTION:")
            print("=" * 60)
            print(response)
