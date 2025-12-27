"""
Session Manager - Persistent Login System
Handles user sessions across devices with tier-based limits
"""

import json
import os
import secrets
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class SessionManager:
    """
    Manages user sessions with device limits based on subscription tier
    
    Features:
    - Forever login (no expiry unless manually logged out)
    - Device limits: FREE=1, PAID=2, PREMIUM=3, VIP=unlimited
    - Device fingerprinting
    - Remote logout capability
    """
    
    # Device limits by tier
    DEVICE_LIMITS = {
        'FREE': 1,
        'PAID': 2,
        'PREMIUM': 3,
        'VIP': 999  # Effectively unlimited
    }
    
    def __init__(self, sessions_path='data/sessions.json'):
        self.sessions_path = sessions_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create sessions storage file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.sessions_path), exist_ok=True)
        if not os.path.exists(self.sessions_path):
            with open(self.sessions_path, 'w') as f:
                json.dump({}, f)
    
    def _generate_session_token(self) -> str:
        """Generate a secure random session token"""
        return secrets.token_urlsafe(32)
    
    def _generate_device_id(self, user_agent: str, ip_address: str) -> str:
        """Generate device fingerprint from user agent and IP"""
        fingerprint = f"{user_agent}:{ip_address}"
        return hashlib.md5(fingerprint.encode()).hexdigest()
    
    def _get_sessions(self, phone: str) -> List[Dict]:
        """Get all active sessions for a user"""
        with open(self.sessions_path, 'r') as f:
            all_sessions = json.load(f)
        return all_sessions.get(phone, [])
    
    def _save_sessions(self, phone: str, sessions: List[Dict]):
        """Save sessions for a user"""
        with open(self.sessions_path, 'r') as f:
            all_sessions = json.load(f)
        
        all_sessions[phone] = sessions
        
        with open(self.sessions_path, 'w') as f:
            json.dump(all_sessions, f, indent=2)
    
    def get_device_limit(self, tier: str) -> int:
        """Get device limit for subscription tier"""
        return self.DEVICE_LIMITS.get(tier, 1)
    
    def create_session(
        self, 
        phone: str, 
        tier: str,
        user_agent: str = "Unknown",
        ip_address: str = "0.0.0.0"
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Create a new session for user
        
        Args:
            phone: User's phone number
            tier: Subscription tier (FREE/PAID/PREMIUM/VIP)
            user_agent: Browser user agent
            ip_address: Client IP address
        
        Returns:
            (success: bool, message: str, session_token: str | None)
        """
        # Get current sessions
        sessions = self._get_sessions(phone)
        
        # Get device limit
        max_devices = self.get_device_limit(tier)
        
        # Generate device fingerprint
        device_id = self._generate_device_id(user_agent, ip_address)
        
        # Check if this device already has a session
        existing_session = None
        for session in sessions:
            if session['device_id'] == device_id:
                existing_session = session
                break
        
        if existing_session:
            # Update last active time
            existing_session['last_active'] = datetime.now().isoformat()
            self._save_sessions(phone, sessions)
            return True, "Session resumed", existing_session['session_token']
        
        # Check device limit
        if len(sessions) >= max_devices:
            return False, f"Device limit reached ({max_devices} devices for {tier} tier)", None
        
        # Create new session
        session_token = self._generate_session_token()
        
        new_session = {
            'session_token': session_token,
            'device_id': device_id,
            'device_info': self._parse_user_agent(user_agent),
            'created_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'ip_address': ip_address
        }
        
        sessions.append(new_session)
        self._save_sessions(phone, sessions)
        
        return True, "Session created", session_token
    
    def verify_session(self, phone: str, session_token: str) -> bool:
        """
        Verify if a session token is valid
        
        Args:
            phone: User's phone number
            session_token: Session token to verify
        
        Returns:
            True if session is valid
        """
        sessions = self._get_sessions(phone)
        
        for session in sessions:
            if session['session_token'] == session_token:
                # Update last active time
                session['last_active'] = datetime.now().isoformat()
                self._save_sessions(phone, sessions)
                return True
        
        return False
    
    def get_active_sessions(self, phone: str) -> List[Dict]:
        """Get list of active sessions with device info"""
        sessions = self._get_sessions(phone)
        
        # Return user-friendly session info
        active_sessions = []
        for session in sessions:
            active_sessions.append({
                'device_info': session['device_info'],
                'last_active': session['last_active'],
                'created_at': session['created_at'],
                'session_token': session['session_token']  # For logout
            })
        
        return active_sessions
    
    def logout_session(self, phone: str, session_token: str) -> bool:
        """
        Logout a specific session
        
        Args:
            phone: User's phone number
            session_token: Session token to logout
        
        Returns:
            True if session was found and removed
        """
        sessions = self._get_sessions(phone)
        
        updated_sessions = [s for s in sessions if s['session_token'] != session_token]
        
        if len(updated_sessions) < len(sessions):
            self._save_sessions(phone, updated_sessions)
            return True
        
        return False
    
    def logout_all_sessions(self, phone: str):
        """Logout all sessions for a user"""
        self._save_sessions(phone, [])
    
    def _parse_user_agent(self, user_agent: str) -> str:
        """Parse user agent to friendly device name"""
        ua_lower = user_agent.lower()
        
        # Detect device type
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            device_type = "📱 Mobile"
        elif 'tablet' in ua_lower or 'ipad' in ua_lower:
            device_type = "📱 Tablet"
        else:
            device_type = "💻 Desktop"
        
        # Detect browser
        if 'chrome' in ua_lower and 'edg' not in ua_lower:
            browser = "Chrome"
        elif 'firefox' in ua_lower:
            browser = "Firefox"
        elif 'safari' in ua_lower and 'chrome' not in ua_lower:
            browser = "Safari"
        elif 'edg' in ua_lower:
            browser = "Edge"
        else:
            browser = "Browser"
        
        # Detect OS
        if 'windows' in ua_lower:
            os_name = "Windows"
        elif 'mac' in ua_lower or 'darwin' in ua_lower:
            os_name = "macOS"
        elif 'linux' in ua_lower:
            os_name = "Linux"
        elif 'android' in ua_lower:
            os_name = "Android"
        elif 'iphone' in ua_lower or 'ipad' in ua_lower:
            os_name = "iOS"
        else:
            os_name = "Unknown"
        
        return f"{device_type} ({browser} on {os_name})"
    
    def cleanup_user_sessions(self, phone: str, new_tier: str):
        """
        Clean up excess sessions when user downgrades tier
        
        Args:
            phone: User's phone number
            new_tier: New subscription tier
        """
        sessions = self._get_sessions(phone)
        max_devices = self.get_device_limit(new_tier)
        
        if len(sessions) > max_devices:
            # Keep only the most recently active sessions
            sessions.sort(key=lambda x: x['last_active'], reverse=True)
            sessions = sessions[:max_devices]
            self._save_sessions(phone, sessions)


# Singleton instance
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get session manager singleton"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
