"""
User Registration System
Handles phone authentication and birth data storage
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple

class UserDatabase:
    """Simple JSON-based user database (will upgrade to Firebase later)"""
    
    def __init__(self, db_path='data/users.json'):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({}, f)
    
    def user_exists(self, phone: str) -> bool:
        """Check if user is already registered"""
        with open(self.db_path, 'r') as f:
            users = json.load(f)
        return phone in users
    
    def register_user(self, phone: str, user_data: Dict) -> bool:
        """
        Register new user
        
        Args:
            phone: Phone number (unique ID)
            user_data: {
                'name': str,
                'email': str (optional),
                'country_code': str,
                'country_name': str,
                
                # Birth data quality
                'birth_data_quality': 'exact' | 'approximate' | 'none',
                
                # For exact birth data
                'dob': 'YYYY-MM-DD',
                'tob': 'HH:MM',
                'birth_city': str,
                'birth_state': str,
                'birth_country': str,
                'birth_timezone': str,
                'lat': float,
                'lon': float,
                
                # For approximate birth data
                'birth_year_range': [start, end] (optional),
                'birth_month_range': [start, end] (optional),
                'birth_time_range': str (optional - morning/afternoon/evening),
                
                'language': str
            }
        
        Returns:
            True if successful, False if user already exists
        """
        if self.user_exists(phone):
            return False
        
        with open(self.db_path, 'r') as f:
            users = json.load(f)
        
        birth_data_quality = user_data.get('birth_data_quality', 'exact')
        
        # Build birth details based on quality
        birth_details = {
            'quality': birth_data_quality
        }
        
        if birth_data_quality == 'exact':
            birth_details.update({
                'dob': user_data.get('dob'),
                'tob': user_data.get('tob'),
                'city': user_data.get('birth_city'),
                'state': user_data.get('birth_state'),
                'country': user_data.get('birth_country'),
                'timezone': user_data.get('birth_timezone'),
                'lat': user_data.get('lat'),
                'lon': user_data.get('lon')
            })
        elif birth_data_quality == 'approximate':
            birth_details.update({
                'year_range': user_data.get('birth_year_range'),
                'month_range': user_data.get('birth_month_range'),
                'time_range': user_data.get('birth_time_range'),
                'city': user_data.get('birth_city'),
                'state': user_data.get('birth_state'),
                'country': user_data.get('birth_country')
            })
        # 'none' quality has minimal birth data
        
        # Store user with enhanced metadata
        users[phone] = {
            'name': user_data.get('name'),
            'email': user_data.get('email', ''),
            'country_code': user_data.get('country_code'),
            'country_name': user_data.get('country_name'),
            
            'birth_details': birth_details,
            
            'tier': 'FREE',  # FREE, PAID, PREMIUM, VIP
            'subscription': 'FREE',  # For app.py compatibility
            'questions_asked': 0,
            'questions_limit': 7,  # 7 for FREE, None for paid tiers
            'lifetime_questions': 0,  # NEW: Track all questions ever asked
            'questions_left': 7,  # NEW: Remaining questions for this tier
            
            'otp_verified': True,  # Set to True after OTP verification
            
            'language': user_data.get('language', 'English'),
            'custom_systems': [],
            
            'registered_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            
            'pwa_installed': False
        }
        
        with open(self.db_path, 'w') as f:
            json.dump(users, f, indent=2)
        
        return True
    
    def get_user(self, phone: str) -> Optional[Dict]:
        """Get user data"""
        with open(self.db_path, 'r') as f:
            users = json.load(f)
        return users.get(phone)
    
    def update_user(self, phone: str, updates: Dict):
        """Update user data"""
        with open(self.db_path, 'r') as f:
            users = json.load(f)
        
        if phone in users:
            users[phone].update(updates)
            
            with open(self.db_path, 'w') as f:
                json.dump(users, f, indent=2)
    
    def increment_question_count(self, phone: str):
        """Increment lifetime question counter and decrement questions_left"""
        user = self.get_user(phone)
        if user:
            user['questions_asked'] = user.get('questions_asked', 0) + 1
            user['lifetime_questions'] = user.get('lifetime_questions', 0) + 1
            user['questions_left'] = max(0, user.get('questions_left', 7) - 1)
            user['updated_at'] = datetime.now().isoformat()
            self.update_user(phone, user)
    
    def can_ask_question(self, phone: str) -> Tuple[bool, str]:
        """
        Check if user can ask a question based on their tier and limit
        
        Returns:
            (can_ask: bool, message: str)
        """
        user = self.get_user(phone)
        if not user:
            return False, "User not found"
        
        tier = user.get('tier', 'FREE')
        questions_asked = user.get('questions_asked', 0)
        questions_limit = user.get('questions_limit')
        
        # Paid tiers have unlimited questions
        if tier in ['PAID', 'PREMIUM', 'VIP'] or questions_limit is None:
            return True, "OK"
        
        # FREE tier has limit
        if questions_asked >= questions_limit:
            return False, f"Free tier limit reached ({questions_limit} questions). Please upgrade to continue."
        
        remaining = questions_limit - questions_asked
        return True, f"{remaining} free questions remaining"
    
    def upgrade_tier(self, phone: str, new_tier: str):
        """
        Upgrade user to a new tier
        
        Args:
            phone: User phone number
            new_tier: PAID, PREMIUM, or VIP
        """
        user = self.get_user(phone)
        if user:
            user['tier'] = new_tier
            
            # Set questions limit based on tier
            if new_tier in ['PAID', 'PREMIUM', 'VIP']:
                user['questions_limit'] = None  # Unlimited
            else:
                user['questions_limit'] = 7  # FREE tier
            
            user['updated_at'] = datetime.now().isoformat()
            self.update_user(phone, user)
    
    def get_user_tier(self, phone: str) -> str:
        """Get user's subscription tier"""
        user = self.get_user(phone)
        return user.get('tier', 'FREE') if user else 'FREE'


# Simple geocoding helper (for getting lat/lon from place name)
def geocode_place(place_name: str) -> tuple:
    """
    Convert place name to coordinates
    For now, returns hardcoded common cities
    Later: integrate with Google Maps API
    """
    
    cities = {
        'hyderabad': (17.3850, 78.4867),
        'bangalore': (12.9716, 77.5946),
        'mumbai': (19.0760, 72.8777),
        'delhi': (28.7041, 77.1025),
        'chennai': (13.0827, 80.2707),
        'kolkata': (22.5726, 88.3639),
        'pune': (18.5204, 73.8567),
        'ongole': (15.5057, 80.0499),
    }
    
    place_lower = place_name.lower().strip()
    
    if place_lower in cities:
        return cities[place_lower]
    
    # Default to Hyderabad if not found
    print(f"Warning: '{place_name}' not in database, using Hyderabad coordinates")
    return cities['hyderabad']


if __name__ == "__main__":
    # Test the system
    print("=" * 60)
    print("USER REGISTRATION SYSTEM TEST")
    print("=" * 60)
    
    db = UserDatabase('data/users.json')
    
    # Register test user
    test_phone = "+919876543210"
    
    if not db.user_exists(test_phone):
        lat, lon = geocode_place("Hyderabad")
        
        success = db.register_user(test_phone, {
            'name': 'Test User',
            'dob': '1990-01-15',
            'tob': '10:30',
            'place': 'Hyderabad',
            'lat': lat,
            'lon': lon
        })
        
        if success:
            print(f"\n✅ User registered: {test_phone}")
        else:
            print(f"\n❌ User already exists")
    else:
        print(f"\n✅ User already exists: {test_phone}")
    
    # Get user
    user = db.get_user(test_phone)
    print(f"\nUser data:")
    print(json.dumps(user, indent=2))
    
    # Test question counter
    db.increment_question_count(test_phone)
    user = db.get_user(test_phone)
    print(f"\nQuestions asked: {user['lifetime_questions']}/15")
