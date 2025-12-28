"""
Razorpay Payment Handler
Manages subscription payments for Astro Compass
Supports both Indian (Razorpay) and International (Stripe) users
"""

import os
import json
from datetime import datetime
from typing import Dict, Optional, Tuple

# Razorpay will be imported when configured
# import razorpay

class PaymentHandler:
    """
    Handle payments via Razorpay (India) and Stripe (International)
    
    Tiers:
    - BASIC: ₹99/month (India), $2/month (International)
    - FAMILY: ₹499/month (India), $8/month (International)  
    - VIP: ₹4,000/month (India), $40/month (International)
    """
    
    # Pricing in paise (for Razorpay) and cents (for Stripe)
    PLANS = {
        'BASIC_IN': {
            'amount': 9900,  # ₹99 in paise
            'currency': 'INR',
            'name': 'BASIC Plan - India',
            'description': 'Unlimited questions, 1 birth chart',
            'period': 'monthly'
        },
        'FAMILY_IN': {
            'amount': 49900,  # ₹499 in paise
            'currency': 'INR',
            'name': 'FAMILY Plan - India',
            'description': 'Unlimited questions, 8 birth charts',
            'period': 'monthly'
        },
        'VIP_IN': {
            'amount': 400000,  # ₹4,000 in paise
            'currency': 'INR',
            'name': 'VIP Plan - India',
            'description': 'Unlimited everything, priority support',
            'period': 'monthly'
        },
        'BASIC_INTL': {
            'amount': 200,  # $2 in cents
            'currency': 'USD',
            'name': 'BASIC Plan - International',
            'description': 'Unlimited questions, 1 birth chart',
            'period': 'monthly'
        },
        'FAMILY_INTL': {
            'amount': 800,  # $8 in cents
            'currency': 'USD',
            'name': 'FAMILY Plan - International',
            'description': 'Unlimited questions, 8 birth charts',
            'period': 'monthly'
        },
        'VIP_INTL': {
            'amount': 4000,  # $40 in cents
            'currency': 'USD',
            'name': 'VIP Plan - International',
            'description': 'Unlimited everything, priority support',
            'period': 'monthly'
        }
    }
    
    def __init__(self, subscriptions_path='data/subscriptions.json'):
        self.subscriptions_path = subscriptions_path
        self._ensure_storage_exists()
        
        # Check if Razorpay/Stripe is configured
        self.razorpay_configured = self._check_razorpay_config()
        self.stripe_configured = self._check_stripe_config()
        
        if self.razorpay_configured:
            self._init_razorpay()
        if self.stripe_configured:
            self._init_stripe()
    
    def _ensure_storage_exists(self):
        """Create subscriptions storage if doesn't exist"""
        os.makedirs(os.path.dirname(self.subscriptions_path), exist_ok=True)
        if not os.path.exists(self.subscriptions_path):
            with open(self.subscriptions_path, 'w') as f:
                json.dump({}, f)
    
    def _check_razorpay_config(self) -> bool:
        """Check if Razorpay credentials are configured"""
        return (
            os.getenv('RAZORPAY_KEY_ID') is not None and
            os.getenv('RAZORPAY_KEY_SECRET') is not None
        )
    
    def _check_stripe_config(self) -> bool:
        """Check if Stripe credentials are configured"""
        return os.getenv('STRIPE_SECRET_KEY') is not None
    
    def _init_razorpay(self):
        """Initialize Razorpay client"""
        try:
            import razorpay
            self.razorpay_client = razorpay.Client(
                auth=(
                    os.getenv('RAZORPAY_KEY_ID'),
                    os.getenv('RAZORPAY_KEY_SECRET')
                )
            )
        except ImportError:
            print("Razorpay not installed. Run: pip install razorpay")
            self.razorpay_configured = False
    
    def _init_stripe(self):
        """Initialize Stripe client"""
        try:
            import stripe
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
            self.stripe = stripe
        except ImportError:
            print("Stripe not installed. Run: pip install stripe")
            self.stripe_configured = False
    
    def _get_subscription_data(self, phone: str) -> Optional[Dict]:
        """Get subscription data for user"""
        with open(self.subscriptions_path, 'r') as f:
            subscriptions = json.load(f)
        return subscriptions.get(phone)
    
    def _save_subscription_data(self, phone: str, data: Dict):
        """Save subscription data for user"""
        with open(self.subscriptions_path, 'r') as f:
            subscriptions = json.load(f)
        
        subscriptions[phone] = data
        
        with open(self.subscriptions_path, 'w') as f:
            json.dump(subscriptions, f, indent=2)
    
    def create_subscription(
        self, 
        phone: str, 
        plan_id: str,
        user_email: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Create a new subscription
        
        Args:
            phone: User's phone number
            plan_id: Plan ID (BASIC_IN, FAMILY_IN, etc.)
            user_email: Optional email for receipts
        
        Returns:
            (success: bool, message: str, payment_data: dict | None)
        """
        if plan_id not in self.PLANS:
            return False, "Invalid plan selected", None
        
        plan = self.PLANS[plan_id]
        is_indian = plan_id.endswith('_IN')
        
        # Check if payment gateway is configured
        if is_indian and not self.razorpay_configured:
            return False, "Payment system not configured. Please contact support.", None
        elif not is_indian and not self.stripe_configured:
            return False, "International payments not configured yet.", None
        
        try:
            if is_indian:
                # Create Razorpay subscription
                subscription_data = {
                    'plan_id': plan_id,
                    'customer_notify': 1,
                    'total_count': 12,  # 12 months
                    'notes': {
                        'phone': phone,
                        'plan': plan['name']
                    }
                }
                
                if user_email:
                    subscription_data['customer'] = {
                        'email': user_email,
                        'contact': phone
                    }
                
                # Create subscription via Razorpay
                subscription = self.razorpay_client.subscription.create(subscription_data)
                
                return True, "Subscription created", {
                    'subscription_id': subscription['id'],
                    'payment_url': f"https://razorpay.com/subscriptions/{subscription['id']}",
                    'plan_id': plan_id,
                    'amount': plan['amount'],
                    'currency': plan['currency']
                }
            
            else:
                # Create Stripe subscription (placeholder)
                # TODO: Implement Stripe subscription
                return False, "Stripe integration coming soon", None
        
        except Exception as e:
            return False, f"Payment error: {str(e)}", None
    
    def verify_payment(
        self,
        phone: str,
        payment_id: str,
        subscription_id: str
    ) -> Tuple[bool, str]:
        """
        Verify payment after user completes it
        
        Args:
            phone: User's phone number
            payment_id: Payment ID from Razorpay/Stripe
            subscription_id: Subscription ID
        
        Returns:
            (success: bool, message: str)
        """
        try:
            if self.razorpay_configured:
                # Fetch payment details
                payment = self.razorpay_client.payment.fetch(payment_id)
                
                if payment['status'] == 'captured':
                    # Payment successful - activate subscription
                    subscription_data = {
                        'subscription_id': subscription_id,
                        'payment_id': payment_id,
                        'status': 'active',
                        'activated_at': datetime.now().isoformat(),
                        'next_billing': payment.get('next_billing_at')
                    }
                    
                    self._save_subscription_data(phone, subscription_data)
                    return True, "Subscription activated successfully!"
                else:
                    return False, f"Payment status: {payment['status']}"
            
            return False, "Payment gateway not configured"
        
        except Exception as e:
            return False, f"Verification error: {str(e)}"
    
    def cancel_subscription(self, phone: str) -> Tuple[bool, str]:
        """Cancel user's subscription"""
        sub_data = self._get_subscription_data(phone)
        
        if not sub_data:
            return False, "No active subscription found"
        
        try:
            if self.razorpay_configured and 'subscription_id' in sub_data:
                # Cancel Razorpay subscription
                self.razorpay_client.subscription.cancel(sub_data['subscription_id'])
            
            # Update local data
            sub_data['status'] = 'cancelled'
            sub_data['cancelled_at'] = datetime.now().isoformat()
            self._save_subscription_data(phone, sub_data)
            
            return True, "Subscription cancelled successfully"
        
        except Exception as e:
            return False, f"Cancellation error: {str(e)}"
    
    def get_subscription_status(self, phone: str) -> Dict:
        """Get current subscription status for user"""
        sub_data = self._get_subscription_data(phone)
        
        if not sub_data:
            return {
                'tier': 'FREE',
                'status': 'none',
                'active': False
            }
        
        return {
            'tier': self._get_tier_from_plan(sub_data.get('plan_id', '')),
            'status': sub_data.get('status', 'unknown'),
            'active': sub_data.get('status') == 'active',
            'next_billing': sub_data.get('next_billing'),
            'subscription_id': sub_data.get('subscription_id')
        }
    
    def _get_tier_from_plan(self, plan_id: str) -> str:
        """Extract tier from plan ID"""
        if 'BASIC' in plan_id:
            return 'BASIC'
        elif 'FAMILY' in plan_id:
            return 'FAMILY'
        elif 'VIP' in plan_id:
            return 'VIP'
        return 'FREE'
