"""
Token Tracking & Usage Management
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict

class TokenTracker:
    def __init__(self, tracker_file='data/token_usage.json'):
        self.tracker_file = tracker_file
        self.DAILY_REQUEST_LIMIT = 1500
        self.DAILY_TOKEN_LIMIT = 1000000
        self.MINUTE_REQUEST_LIMIT = 15
        self._ensure_tracker_exists()
    
    def _ensure_tracker_exists(self):
        os.makedirs(os.path.dirname(self.tracker_file), exist_ok=True)
        if not os.path.exists(self.tracker_file):
            self._reset_daily_tracker()
    
    def _reset_daily_tracker(self):
        tracker_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_requests_today': 0,
            'total_tokens_today': 0,
            'free_requests_today': 0,
            'paid_requests_today': 0,
            'reset_time': (datetime.now() + timedelta(days=1)).replace(
                hour=0, minute=0, second=0
            ).isoformat(),
            'minute_tracker': []
        }
        with open(self.tracker_file, 'w') as f:
            json.dump(tracker_data, f, indent=2)
    
    def _get_tracker_data(self) -> Dict:
        with open(self.tracker_file, 'r') as f:
            data = json.load(f)
        
        if data['date'] != datetime.now().strftime('%Y-%m-%d'):
            self._reset_daily_tracker()
            with open(self.tracker_file, 'r') as f:
                data = json.load(f)
        
        return data
    
    def _clean_minute_tracker(self, tracker_data: Dict):
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        tracker_data['minute_tracker'] = [
            ts for ts in tracker_data['minute_tracker']
            if datetime.fromisoformat(ts) > one_minute_ago
        ]
    
    def can_make_request(self, is_paid_user: bool = False) -> Dict:
        tracker_data = self._get_tracker_data()
        self._clean_minute_tracker(tracker_data)
        
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
        
        if tracker_data['total_requests_today'] >= self.DAILY_REQUEST_LIMIT:
            reset_time = datetime.fromisoformat(tracker_data['reset_time'])
            hours_until_reset = int((reset_time - datetime.now()).total_seconds() / 3600)
            
            return {
                'allowed': False,
                'reason': 'daily_request_limit',
                'message': f"🌙 Free tier daily limit reached. Resets in ~{hours_until_reset} hours.\n\nUpgrade to $1/month for unlimited access!"
            }
        
        if tracker_data['total_tokens_today'] >= self.DAILY_TOKEN_LIMIT:
            reset_time = datetime.fromisoformat(tracker_data['reset_time'])
            hours_until_reset = int((reset_time - datetime.now()).total_seconds() / 3600)
            
            return {
                'allowed': False,
                'reason': 'daily_token_limit',
                'message': f"🔥 Server capacity reached. Resets in ~{hours_until_reset} hours.\n\n$1/month = Unlimited predictions!"
            }
        
        requests_this_minute = len(tracker_data['minute_tracker'])
        if requests_this_minute >= self.MINUTE_REQUEST_LIMIT:
            return {
                'allowed': False,
                'reason': 'rate_limit',
                'message': "⏱️ Slow down! Wait 30 seconds and try again.\n\nUpgrade to $1/month for no rate limits!"
            }
        
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
        tracker_data = self._get_tracker_data()
        tracker_data['total_requests_today'] += 1
        tracker_data['total_tokens_today'] += (input_tokens + output_tokens)
        
        if is_paid_user:
            tracker_data['paid_requests_today'] += 1
        else:
            tracker_data['free_requests_today'] += 1
        
        tracker_data['minute_tracker'].append(datetime.now().isoformat())
        self._clean_minute_tracker(tracker_data)
        
        with open(self.tracker_file, 'w') as f:
            json.dump(tracker_data, f, indent=2)
    
    def get_usage_stats(self) -> Dict:
        tracker_data = self._get_tracker_data()
        return {
            'date': tracker_data['date'],
            'requests_used': tracker_data['total_requests_today'],
            'requests_limit': self.DAILY_REQUEST_LIMIT,
            'tokens_used': tracker_data['total_tokens_today'],
            'tokens_limit': self.DAILY_TOKEN_LIMIT,
            'reset_time': tracker_data['reset_time']
        }