"""
Quota Checker System
Validates user requests against free/paid limits
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict

class QuotaChecker:
    """Manages free tier limits and paid subscriptions"""
    
    def __init__(self, quota_file='data/daily_quota.json'):
        self.quota_file = quota_file
        self.FREE_LIFETIME_LIMIT = 15
        self.FREE_DAILY_TOKEN_LIMIT = 1500  # Gemini free tier limit
        self._ensure_quota_file()
    
    def _ensure_quota_file(self):
        """Create quota tracking file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.quota_file), exist_ok=True)
        if not os.path.exists(self.quota_file):
            self._reset_daily_quota()
    
    def _reset_daily_quota(self):
        """Reset daily quota counter"""
        quota_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'free_queries_today': 0,
            'reset_time': (datetime.now() + timedelta(days=1)).replace(
                hour=0, minute=0, second=0
            ).isoformat()
        }
        with open(self.quota_file, 'w') as f:
            json.dump(quota_data, f, indent=2)
    
    def _get_quota_data(self) -> Dict:
        """Get current quota data, reset if new day"""
        with open(self.quota_file, 'r') as f:
            data = json.load(f)
        
        # Check if we need to reset (new day)
        if data['date'] != datetime.now().strftime('%Y-%m-%d'):
            self._reset_daily_quota()
            with open(self.quota_file, 'r') as f:
                data = json.load(f)
        
        return data
    
    def _increment_daily_quota(self):
        """Increment today's free query count"""
        data = self._get_quota_data()
        data['free_queries_today'] += 1
        
        with open(self.quota_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def can_user_ask(self, user: Dict) -> Dict:
        """
        Check if user can ask a question
        
        Args:
            user: User dict from database
        
        Returns:
            {
                'allowed': bool,
                'reason': str,
                'message': str,
                'api_tier': 'free' or 'paid'
            }
        """
        
        # Step 1: Check if paid subscriber
        if user['subscription'] in ['PAID', 'PREMIUM', 'VIP']:
            return {
                'allowed': True,
                'api_tier': 'paid',
                'message': f"Welcome back, {user['name']}! 🌟"
            }
        
        # Step 2: Check lifetime question limit (FREE users)
        if user['lifetime_questions'] >= self.FREE_LIFETIME_LIMIT:
            return {
                'allowed': False,
                'reason': 'lifetime_limit',
                'message': (
                    f"🙏 You've used all {self.FREE_LIFETIME_LIMIT} free questions.\n\n"
                    f"Support our mission for just $1/month:\n"
                    f"✓ Unlimited questions\n"
                    f"✓ Chat history & memory\n"
                    f"✓ Custom systems (Nadi, Palmistry)\n"
                    f"✓ Multi-language support\n\n"
                    f"[Subscribe for $1/month]"
                )
            }
        
        # Step 3: Check daily free quota
        quota_data = self._get_quota_data()
        
        if quota_data['free_queries_today'] >= self.FREE_DAILY_TOKEN_LIMIT:
            reset_time = datetime.fromisoformat(quota_data['reset_time'])
            hours_until_reset = int((reset_time - datetime.now()).total_seconds() / 3600)
            
            return {
                'allowed': False,
                'reason': 'daily_quota',
                'message': (
                    f"🌙 Free daily quota reached.\n\n"
                    f"Resets in: ~{hours_until_reset} hours\n"
                    f"Your questions: {user['lifetime_questions']}/{self.FREE_LIFETIME_LIMIT}\n\n"
                    f"Can't wait? Subscribe for $1/month!\n\n"
                    f"[Subscribe Now] [Ask Tomorrow]"
                )
            }
        
        # Step 4: All checks passed - allow free query
        remaining = self.FREE_LIFETIME_LIMIT - user['lifetime_questions']
        quota_data = self._get_quota_data()
        reset_time = datetime.fromisoformat(quota_data['reset_time'])
        
        return {
            'allowed': True,
            'api_tier': 'free',
            'message': (
                f"✨ Question {user['lifetime_questions'] + 1}/{self.FREE_LIFETIME_LIMIT}\n"
                f"Free quota resets: {reset_time.strftime('%I:%M %p')}"
            )
        }
    
    def process_free_query(self):
        """Increment daily quota counter for free queries"""
        self._increment_daily_quota()
    
    def get_usage_stats(self, user: Dict) -> str:
        """Get formatted usage statistics"""
        quota_data = self._get_quota_data()
        
        stats = f"""
📊 YOUR USAGE STATS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subscription: {user['subscription']}
Lifetime Questions: {user['lifetime_questions']}/{self.FREE_LIFETIME_LIMIT}
Today's Free Queries: {quota_data['free_queries_today']}/{self.FREE_DAILY_TOKEN_LIMIT}
Reset Time: {datetime.fromisoformat(quota_data['reset_time']).strftime('%I:%M %p')}
"""
        return stats


if __name__ == "__main__":
    from user_registration import UserDatabase
    
    print("=" * 60)
    print("QUOTA CHECKER TEST")
    print("=" * 60)
    
    # Initialize
    db = UserDatabase('data/users.json')
    quota = QuotaChecker('data/daily_quota.json')
    
    # Test with free user
    test_phone = "+919876543210"
    user = db.get_user(test_phone)
    
    print(f"\n[Test 1] Checking quota for FREE user...")
    result = quota.can_user_ask(user)
    
    print(f"\nAllowed: {result['allowed']}")
    print(f"Message:\n{result['message']}")
    
    # Simulate asking a question
    if result['allowed']:
        print("\n[Test 2] Processing question...")
        quota.process_free_query()
        db.increment_question_count(test_phone)
        print("✅ Question processed")
    
    # Check stats
    user = db.get_user(test_phone)
    print(quota.get_usage_stats(user))
    
    # Test with paid user
    print("\n[Test 3] Simulating PAID user...")
    db.update_user(test_phone, {'subscription': 'PAID'})
    user = db.get_user(test_phone)
    
    result = quota.can_user_ask(user)
    print(f"Allowed: {result['allowed']}")
    print(f"Message: {result['message']}")
    
    # Reset for next test
    db.update_user(test_phone, {'subscription': 'FREE'})
