"""
Token Tracking & Usage Management
Tracks both request counts and token usage to prevent mid-conversation failures
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict

class TokenTracker:
    """
    Manages token usage and request limits
    Google's free tier limits:
    - 1,500 requests/day
    - 1,000,000 tokens/day (input + output combined)
    - 15 requests/minute
    """
    
    def __init__(self, tracker_file='data/token_usage.json'):
        self.tracker_file = tracker_file
        self.DAILY_REQUEST_LIMIT = 1500
        self.DAILY_TOKEN_LIMIT = 1000000
        self.MINUTE_REQUEST_LIMIT = 15
        self._ensure_tracker_exists()
    
    def _ensure_tracker_exists(self):
        """Create tracker file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.tracker_file), exist_ok=True)
        if not os.path.exists(self.tracker_file):
            self._reset_daily_tracker()
    
    def _reset_daily_tracker(self):
        """Reset daily counters"""
        tracker_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_requests_today': 0,
            'total_tokens_today': 0,
            'free_requests_today': 0,
            'paid_requests_today': 0,
            'reset_time': (datetime.now() + timedelta(days=1)).replace(
                hour=0, minute=0, second=0
            ).isoformat(),
            'minute_tracker': []  # List of timestamps for rate limiting
        }
        with open(self.tracker_file, 'w') as f:
            json.dump(tracker_data, f, indent=2)
    
    def _get_tracker_data(self) -> Dict:
        """Get current tracker data, reset if new day"""
        with open(self.tracker_file, 'r') as f:
            data = json.load(f)
        
        # Check if we need to reset (new day)
        if data['date'] != datetime.now().strftime('%Y-%m-%d'):
            self._reset_daily_tracker()
            with open(self.tracker_file, 'r') as f:
                data = json.load(f)
        
        return data
    
    def _clean_minute_tracker(self, tracker_data: Dict):
        """Remove timestamps older than 1 minute"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        tracker_data['minute_tracker'] = [
            ts for ts in tracker_data['minute_tracker']
            if datetime.fromisoformat(ts) > one_minute_ago
        ]
    
    def can_make_request(self, is_paid_user: bool = False) -> Dict:
        """
        Check if request can be made
        
        Returns:
            {
                'allowed': bool,
                'reason': str (if not allowed),
                'message': str,
                'limits': {
                    'requests_remaining': int,
                    'tokens_remaining': int,
                    'requests_per_minute_remaining': int
                }
            }
        """
        tracker_data = self._get_tracker_data()
        self._clean_minute_tracker(tracker_data)
        
        # Paid users bypass all limits
        if is_paid_user:
            return {
                'allowed': True,
                'message': 'Unlimited access',
                'limits': {
                    'requests_remaining': 'unlimited',
                    'tokens_remaining': 'unlimited',
                    'requests_per_minute_remaining': 'unlimited'
                }
            }
        
        # Check daily request limit
        if tracker_data['total_requests_today'] >= self.DAILY_REQUEST_LIMIT:
            reset_time = datetime.fromisoformat(tracker_data['reset_time'])
            hours_until_reset = int((reset_time - datetime.now()).total_seconds() / 3600)
            
            return {
                'allowed': False,
                'reason': 'daily_request_limit',
                'message': (
                    f"🌙 **Free tier daily limit reached**\n\n"
                    f"Our servers are experiencing high demand today. Free quota resets in ~{hours_until_reset} hours.\n\n"
                    f"**Can't wait?**\n"
                    f"✨ Upgrade to $1/month for unlimited access\n"
                    f"💎 Never wait for quota resets\n"
                    f"🚀 Priority processing\n\n"
                    f"[Upgrade Now] or try again in {hours_until_reset} hours"
                )
            }
        
        # Check daily token limit
        if tracker_data['total_tokens_today'] >= self.DAILY_TOKEN_LIMIT:
            reset_time = datetime.fromisoformat(tracker_data['reset_time'])
            hours_until_reset = int((reset_time - datetime.now()).total_seconds() / 3600)
            
            return {
                'allowed': False,
                'reason': 'daily_token_limit',
                'message': (
                    f"🔥 **Server capacity reached**\n\n"
                    f"We've processed a lot of detailed predictions today! Our free servers need to cool down.\n\n"
                    f"Resets in ~{hours_until_reset} hours.\n\n"
                    f"**Skip the wait:**\n"
                    f"💫 $1/month = Unlimited predictions\n"
                    f"⚡ Instant responses, no waiting\n\n"
                    f"[Upgrade to Premium]"
                )
            }
        
        # Check requests per minute (rate limiting)
        requests_this_minute = len(tracker_data['minute_tracker'])
        if requests_this_minute >= self.MINUTE_REQUEST_LIMIT:
            return {
                'allowed': False,
                'reason': 'rate_limit',
                'message': (
                    f"⏱️ **Slow down there!**\n\n"
                    f"Our free servers can handle {self.MINUTE_REQUEST_LIMIT} requests per minute.\n\n"
                    f"Please wait 30 seconds and try again.\n\n"
                    f"**Pro tip:** Upgrade to $1/month for priority processing with no rate limits!"
                )
            }
        
        # All checks passed
        requests_remaining = self.DAILY_REQUEST_LIMIT - tracker_data['total_requests_today']
        tokens_remaining = self.DAILY_TOKEN_LIMIT - tracker_data['total_tokens_today']
        rpm_remaining = self.MINUTE_REQUEST_LIMIT - requests_this_minute
        
        return {
            'allowed': True,
            'message': 'Request allowed',
            'limits': {
                'requests_remaining': requests_remaining,
                'tokens_remaining': tokens_remaining,
                'requests_per_minute_remaining': rpm_remaining
            }
        }
    
    def record_usage(self, input_tokens: int, output_tokens: int, is_paid_user: bool = False):
        """
        Record API usage
        
        Args:
            input_tokens: Tokens in the prompt
            output_tokens: Tokens in the response
            is_paid_user: Whether user is on paid plan
        """
        tracker_data = self._get_tracker_data()
        
        # Update counters
        tracker_data['total_requests_today'] += 1
        tracker_data['total_tokens_today'] += (input_tokens + output_tokens)
        
        if is_paid_user:
            tracker_data['paid_requests_today'] += 1
        else:
            tracker_data['free_requests_today'] += 1
        
        # Add to minute tracker
        tracker_data['minute_tracker'].append(datetime.now().isoformat())
        self._clean_minute_tracker(tracker_data)
        
        # Save
        with open(self.tracker_file, 'w') as f:
            json.dump(tracker_data, f, indent=2)
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        tracker_data = self._get_tracker_data()
        
        return {
            'date': tracker_data['date'],
            'requests_used': tracker_data['total_requests_today'],
            'requests_limit': self.DAILY_REQUEST_LIMIT,
            'requests_remaining': self.DAILY_REQUEST_LIMIT - tracker_data['total_requests_today'],
            'tokens_used': tracker_data['total_tokens_today'],
            'tokens_limit': self.DAILY_TOKEN_LIMIT,
            'tokens_remaining': self.DAILY_TOKEN_LIMIT - tracker_data['total_tokens_today'],
            'free_requests': tracker_data['free_requests_today'],
            'paid_requests': tracker_data['paid_requests_today'],
            'reset_time': tracker_data['reset_time']
        }


if __name__ == "__main__":
    # Test the tracker
    print("=" * 60)
    print("TOKEN TRACKER TEST")
    print("=" * 60)
    
    tracker = TokenTracker('data/token_usage.json')
    
    # Check if request allowed
    print("\n[Test 1] Checking if request allowed...")
    result = tracker.can_make_request(is_paid_user=False)
    print(f"Allowed: {result['allowed']}")
    print(f"Limits: {result['limits']}")
    
    # Simulate usage
    print("\n[Test 2] Recording usage (5000 input, 2000 output tokens)...")
    tracker.record_usage(5000, 2000, is_paid_user=False)
    
    # Get stats
    print("\n[Test 3] Getting usage stats...")
    stats = tracker.get_usage_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n✅ Token tracker working!")
