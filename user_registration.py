"""
User Registration System
Handles phone authentication and birth data storage
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

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
                'dob': 'YYYY-MM-DD',
                'tob': 'HH:MM',
                'place': str,
                'lat': float,
                'lon': float
            }
        
        Returns:
            True if successful, False if user already exists
        """
        if self.user_exists(phone):
            return False
        
        with open(self.db_path, 'r') as f:
            users = json.load(f)
        
        # Store user with metadata
        users[phone] = {
            'name': user_data['name'],
            'birth_details': {
                'dob': user_data['dob'],
                'tob': user_data['tob'],
                'place': user_data['place'],
                'lat': user_data['lat'],
                'lon': user_data['lon']
            },
            'subscription': 'FREE',
            'lifetime_questions': 0,
            'registered_at': datetime.now().isoformat(),
            'language': 'English',
            'custom_systems': []
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
        """Increment lifetime question counter"""
        user = self.get_user(phone)
        if user:
            user['lifetime_questions'] += 1
            self.update_user(phone, user)


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
