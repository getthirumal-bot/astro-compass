"""
Environment Configuration Loader
Loads API keys and secrets from .env file (NOT from config.json)
"""

import os
from pathlib import Path

def load_env_file(env_path='.env'):
    """Load environment variables from .env file"""
    if not os.path.exists(env_path):
        raise FileNotFoundError(
            f".env file not found at {env_path}\n"
            f"Please create .env file with your API key.\n"
            f"See .env.example for template."
        )
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def get_api_key():
    """Get Gemini API key from .env file"""
    env_vars = load_env_file()
    
    api_key = env_vars.get('GEMINI_API_KEY')
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        raise ValueError(
            "Please set your Gemini API key in .env file\n"
            "Get it from: https://aistudio.google.com/app/apikey\n"
            "Then add to .env file: GEMINI_API_KEY=your_key_here"
        )
    
    return api_key

def get_email_config():
    """Get email configuration from .env"""
    env_vars = load_env_file()
    
    return {
        'smtp_server': env_vars.get('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(env_vars.get('SMTP_PORT', 587)),
        'smtp_email': env_vars.get('SMTP_EMAIL'),
        'smtp_password': env_vars.get('SMTP_PASSWORD'),
    }


if __name__ == "__main__":
    # Test
    try:
        api_key = get_api_key()
        print(f"✅ API Key loaded: {api_key[:20]}...")
        
        email_config = get_email_config()
        print(f"✅ Email config loaded: {email_config['smtp_email']}")
    except Exception as e:
        print(f"❌ Error: {e}")
