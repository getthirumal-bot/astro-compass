"""
OTP Service - Firebase Phone Authentication
Handles sending and verifying OTP codes via SMS
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import hashlib
import secrets

# Note: Firebase Admin SDK will be added when Firebase is configured
# For now, this is a mock implementation that will work locally
# and can be easily replaced with real Firebase later

class OTPService:
    """
    OTP Service using Firebase Phone Authentication
    
    Features:
    - Send 6-digit OTP via SMS
    - Verify OTP codes
    - Rate limiting (1 OTP per phone per minute)
    - Expiry (5 minutes)
    - Max attempts (3)
    """
    
    def __init__(self, otp_storage_path='data/otp_codes.json'):
        self.storage_path = otp_storage_path
        self._ensure_storage_exists()
        
        # Firebase configuration (will be loaded from environment)
        self.firebase_configured = self._check_firebase_config()
    
    def _ensure_storage_exists(self):
        """Create OTP storage file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)
    
    def _check_firebase_config(self) -> bool:
        """Check if Firebase is properly configured"""
        # Check for Firebase credentials in environment
        # For MVP, we'll use mock OTP (development mode)
        return os.getenv('FIREBASE_CONFIGURED') == 'true'
    
    def _generate_otp(self) -> str:
        """Generate a 6-digit OTP code"""
        return f"{secrets.randbelow(1000000):06d}"
    
    def _hash_otp(self, otp: str) -> str:
        """Hash OTP for secure storage"""
        return hashlib.sha256(otp.encode()).hexdigest()
    
    def _get_otp_data(self, phone: str) -> Optional[Dict]:
        """Get stored OTP data for a phone number"""
        with open(self.storage_path, 'r') as f:
            otp_data = json.load(f)
        return otp_data.get(phone)
    
    def _save_otp_data(self, phone: str, data: Dict):
        """Save OTP data"""
        with open(self.storage_path, 'r') as f:
            otp_data = json.load(f)
        
        otp_data[phone] = data
        
        with open(self.storage_path, 'w') as f:
            json.dump(otp_data, f, indent=2)
    
    def _clear_otp_data(self, phone: str):
        """Clear OTP data after successful verification"""
        with open(self.storage_path, 'r') as f:
            otp_data = json.load(f)
        
        if phone in otp_data:
            del otp_data[phone]
            
            with open(self.storage_path, 'w') as f:
                json.dump(otp_data, f, indent=2)
    
    def can_send_otp(self, phone: str) -> Tuple[bool, str]:
        """
        Check if OTP can be sent (rate limiting)
        
        Returns:
            (can_send: bool, message: str)
        """
        data = self._get_otp_data(phone)
        
        if not data:
            return True, "OK"
        
        last_sent = datetime.fromisoformat(data['sent_at'])
        time_since_last = datetime.now() - last_sent
        
        if time_since_last < timedelta(minutes=1):
            wait_seconds = 60 - int(time_since_last.total_seconds())
            return False, f"Please wait {wait_seconds} seconds before requesting another OTP"
        
        return True, "OK"
    
    def send_otp(self, phone: str, country_code: str) -> Tuple[bool, str, Optional[str]]:
        """
        Send OTP code via SMS
        
        Args:
            phone: Phone number (with country code, e.g., +919876543210)
            country_code: Country code (e.g., +91)
        
        Returns:
            (success: bool, message: str, otp: str | None)
            Note: otp is returned only in development mode for testing
        """
        # Check rate limit
        can_send, message = self.can_send_otp(phone)
        if not can_send:
            return False, message, None
        
        # Generate OTP
        otp_code = self._generate_otp()
        otp_hash = self._hash_otp(otp_code)
        
        # Save OTP data
        self._save_otp_data(phone, {
            'otp_hash': otp_hash,
            'sent_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=5)).isoformat(),
            'attempts': 0,
            'verified': False
        })
        
        if self.firebase_configured:
            # Send via Firebase Phone Authentication
            try:
                # TODO: Implement Firebase phone auth
                # firebase_admin.auth.send_sms(phone, otp_code)
                return True, "OTP sent successfully", None
            except Exception as e:
                return False, f"Failed to send OTP: {str(e)}", None
        else:
            # Development mode - return OTP for testing
            print(f"\n{'='*50}")
            print(f"DEVELOPMENT MODE - OTP for {phone}: {otp_code}")
            print(f"{'='*50}\n")
            return True, f"OTP sent (DEV MODE: {otp_code})", otp_code
    
    def verify_otp(self, phone: str, otp_code: str) -> Tuple[bool, str]:
        """
        Verify OTP code
        
        Args:
            phone: Phone number
            otp_code: 6-digit OTP entered by user
        
        Returns:
            (success: bool, message: str)
        """
        data = self._get_otp_data(phone)
        
        if not data:
            return False, "No OTP request found. Please request a new OTP."
        
        # Check if already verified
        if data.get('verified'):
            return False, "OTP already used. Please request a new OTP."
        
        # Check expiry
        expires_at = datetime.fromisoformat(data['expires_at'])
        if datetime.now() > expires_at:
            self._clear_otp_data(phone)
            return False, "OTP expired. Please request a new OTP."
        
        # Check attempts
        if data['attempts'] >= 3:
            self._clear_otp_data(phone)
            return False, "Maximum attempts exceeded. Please request a new OTP."
        
        # Verify OTP
        otp_hash = self._hash_otp(otp_code)
        
        if otp_hash != data['otp_hash']:
            # Increment attempts
            data['attempts'] += 1
            self._save_otp_data(phone, data)
            
            remaining = 3 - data['attempts']
            if remaining > 0:
                return False, f"Invalid OTP. {remaining} attempts remaining."
            else:
                self._clear_otp_data(phone)
                return False, "Invalid OTP. Maximum attempts exceeded."
        
        # Success - mark as verified and clear data
        data['verified'] = True
        self._save_otp_data(phone, data)
        
        # Clear OTP data after successful verification
        self._clear_otp_data(phone)
        
        return True, "Phone number verified successfully!"
    
    def cleanup_expired_otps(self):
        """Remove expired OTP entries (run periodically)"""
        with open(self.storage_path, 'r') as f:
            otp_data = json.load(f)
        
        now = datetime.now()
        cleaned_data = {}
        
        for phone, data in otp_data.items():
            expires_at = datetime.fromisoformat(data['expires_at'])
            if now <= expires_at:
                cleaned_data[phone] = data
        
        with open(self.storage_path, 'w') as f:
            json.dump(cleaned_data, f, indent=2)


# Singleton instance
_otp_service = None

def get_otp_service() -> OTPService:
    """Get OTP service singleton"""
    global _otp_service
    if _otp_service is None:
        _otp_service = OTPService()
    return _otp_service
