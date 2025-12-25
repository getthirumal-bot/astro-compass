"""
Astro Consensus Engine - Integrated Main System
Combines: Registration + Quota + Ephemeris + Gemini AI + Token Tracking
"""

import sys
from datetime import datetime
from typing import Dict, Optional
from google import genai

# Import our modules
from user_registration import UserDatabase, geocode_place
from quota_checker import QuotaChecker
from token_tracker import TokenTracker
from env_loader import get_api_key
sys.path.append('utils')
from ephemeris import calculate_chart, calculate_transits, format_chart_for_ai


class AstroEngine:
    """Complete Astro Consensus Engine"""
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        
        # Load master system prompt
        with open('prompts/master_system_prompt.txt', 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
        
        # Initialize subsystems
        self.db = UserDatabase('data/users.json')
        self.quota = QuotaChecker('data/daily_quota.json')
        self.token_tracker = TokenTracker('data/token_usage.json')
    
    def register_user(self, phone: str, name: str, dob: str, tob: str, 
                     place: str) -> Dict:
        """
        Register new user
        
        Args:
            phone: +919876543210
            name: User's name
            dob: YYYY-MM-DD
            tob: HH:MM
            place: City name
        
        Returns:
            {'success': bool, 'message': str}
        """
        # Check if already exists
        if self.db.user_exists(phone):
            return {
                'success': False,
                'message': 'User already registered! Please login.'
            }
        
        # Get coordinates
        lat, lon = geocode_place(place)
        
        # Register
        success = self.db.register_user(phone, {
            'name': name,
            'dob': dob,
            'tob': tob,
            'place': place,
            'lat': lat,
            'lon': lon
        })
        
        if success:
            return {
                'success': True,
                'message': f"Welcome {name}! 🌟 Your cosmic profile is ready.\n\n"
                          f"You have 15 free questions to explore your destiny."
            }
        else:
            return {
                'success': False,
                'message': 'Registration failed. Please try again.'
            }
    
    def ask_question(self, phone: str, question: str, conversation_history: list = None) -> Dict:
        """
        Main function: User asks a question
        
        Args:
            phone: User's phone number
            question: The question to ask
        
        Returns:
            {
                'success': bool,
                'response': str,
                'usage_info': str (optional)
            }
        """
        # Check if user exists
        user = self.db.get_user(phone)
        if not user:
            return {
                'success': False,
                'response': 'Please register first with your birth details.'
            }
        
        # Check quota
        quota_check = self.quota.can_user_ask(user)
        
        if not quota_check['allowed']:
            return {
                'success': False,
                'response': quota_check['message']
            }
        
        # Check token limits (global)
        is_paid = user['subscription'] in ['PAID', 'PREMIUM', 'VIP']
        token_check = self.token_tracker.can_make_request(is_paid_user=is_paid)
        
        if not token_check['allowed']:
            return {
                'success': False,
                'response': token_check['message'],
                'retry_available': True  # Signal that retry might work
            }
        
        # Calculate birth chart
        birth_datetime = datetime.strptime(
            f"{user['birth_details']['dob']} {user['birth_details']['tob']}", 
            "%Y-%m-%d %H:%M"
        )
        
        chart = calculate_chart(
            birth_datetime,
            user['birth_details']['lat'],
            user['birth_details']['lon']
        )
        
        # Get current transits
        transits = calculate_transits()
        
        # Format for AI
        chart_data = format_chart_for_ai(chart, transits)
        
        # Build prompt with system instructions
        custom_systems_text = ""
        if user.get('custom_systems') and len(user['custom_systems']) > 0:
            custom_systems_text = f"\n\nADDITIONAL SYSTEMS REQUESTED:\n{', '.join(user['custom_systems'])}\n(Please incorporate insights from these systems as well)"
        
        # Response length control based on user tier and question quality
        response_guidance = ""
        if user['subscription'] == 'FREE':
            response_guidance = """

RESPONSE LENGTH RULES FOR FREE USERS:
- For vague/unclear questions (like "tell me about tomorrow", "what about X again"): Give 2-3 sentences maximum, then suggest they upgrade for detailed analysis
- For specific questions with clear context: Provide full analysis
- Don't waste tokens on nonsense queries from free users
"""
        
        # CRITICAL: Pass current date explicitly IN USER'S TIMEZONE
        from country_utils import get_user_current_datetime
        
        user_now = get_user_current_datetime(phone)
        current_date_str = user_now.strftime("%B %d, %Y")  # e.g., "December 25, 2025"
        current_time_str = user_now.strftime("%I:%M %p")   # e.g., "02:30 PM"
        timezone_name = user_now.tzinfo.tzname(user_now)
        
        # Build conversation context (last 5 exchanges max)
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            # Get last 10 messages (5 exchanges)
            recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
            
            conversation_context = "\n\nRECENT CONVERSATION HISTORY:\n"
            for msg in recent_history:
                role = "USER" if msg['role'] == 'user' else "ASSISTANT"
                conversation_context += f"{role}: {msg['content'][:200]}...\n"  # Truncate long messages
            
            conversation_context += "\nUse this conversation context when answering the current query. If the user says 'it', 'that', 'this', refer back to what was discussed above.\n"
        
        full_prompt = f"""
{self.system_prompt}

{response_guidance}

---

CRITICAL INFORMATION:
TODAY'S DATE (USER'S LOCAL TIME): {current_date_str}
CURRENT TIME (USER'S LOCAL): {current_time_str} {timezone_name}
CURRENT YEAR: {user_now.year}
CURRENT MONTH: {user_now.strftime("%B")}
CURRENT DAY: {user_now.day}

When user asks about "tomorrow", "next week", "next 5 days", calculate dates from TODAY ({current_date_str}), NOT from any other date.
This is the user's LOCAL time in their timezone, use this for all date calculations.

---

USER: {user['name']}
LANGUAGE PREFERENCE: {user['language']}

{chart_data}{custom_systems_text}

{conversation_context}

CURRENT QUERY: {question}
"""
        
        # Call Gemini API
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt
            )
            
            ai_response = response.text
            
            # Extract token usage from response
            usage_metadata = response.usage_metadata
            input_tokens = usage_metadata.prompt_token_count if hasattr(usage_metadata, 'prompt_token_count') else 0
            output_tokens = usage_metadata.candidates_token_count if hasattr(usage_metadata, 'candidates_token_count') else 0
            
            # Record token usage
            self.token_tracker.record_usage(input_tokens, output_tokens, is_paid_user=is_paid)
            
            # Update counters
            if quota_check['api_tier'] == 'free':
                self.quota.process_free_query()
            
            self.db.increment_question_count(phone)
            
            # Get updated user for stats
            user = self.db.get_user(phone)
            
            usage_msg = ""
            if user['subscription'] == 'FREE':
                remaining = 15 - user['lifetime_questions']
                usage_msg = f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 {remaining} free questions remaining"
            
            return {
                'success': True,
                'response': ai_response + usage_msg
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': f'Error: {str(e)}'
            }
    
    def upgrade_to_paid(self, phone: str) -> Dict:
        """Upgrade user to paid subscription"""
        user = self.db.get_user(phone)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        self.db.update_user(phone, {'subscription': 'PAID'})
        
        return {
            'success': True,
            'message': '🎉 Upgraded to PAID! Unlimited questions unlocked!'
        }
    
    def get_stats(self, phone: str) -> str:
        """Get user statistics"""
        user = self.db.get_user(phone)
        if not user:
            return "User not found"
        
        return self.quota.get_usage_stats(user)


# Command-line interface for testing
if __name__ == "__main__":
    print("=" * 70)
    print("ASTRO CONSENSUS ENGINE - INTEGRATED TEST")
    print("=" * 70)
    
    # Load API key from config.json
    try:
        API_KEY = get_api_key()
        print("\n✅ API key loaded from config.json")
    except Exception as e:
        print(f"\n❌ {e}")
        exit()
    
    # Initialize engine
    engine = AstroEngine(API_KEY)
    
    # Test registration
    print("\n[Test 1] Registering new user...")
    result = engine.register_user(
        phone="+919999888877",
        name="Ravi Kumar",
        dob="1985-03-20",
        tob="14:30",
        place="Mumbai"
    )
    print(result['message'])
    
    # Test asking question
    print("\n[Test 2] Asking first question...")
    result = engine.ask_question(
        phone="+919999888877",
        question="What does my birth chart say about career success?"
    )
    
    if result['success']:
        print("\n✅ AI RESPONSE:")
        print("-" * 70)
        print(result['response'])
    else:
        print(f"\n❌ {result['response']}")
    
    # Test stats
    print("\n[Test 3] Checking usage stats...")
    stats = engine.get_stats("+919999888877")
    print(stats)
