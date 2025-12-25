"""
Environment Configuration Loader
Loads API keys from .env file
"""

import os

def load_env_file(env_path='.env'):
    """Load environment variables from .env file"""
    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env file not found at {env_path}")
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def get_api_key():
    """Get Gemini API key from .env file"""
    env_vars = load_env_file()
    
    api_key = env_vars.get('GEMINI_API_KEY')
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        raise ValueError("Please set your Gemini API key in .env file")
    
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