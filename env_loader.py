"""
Environment Configuration Loader
Loads API keys from .env file (local) or Streamlit secrets (cloud)
"""

import os

def get_api_key():
    """Get Gemini API key from .env file or Streamlit secrets"""
    
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']
            if api_key and api_key != 'your-api-key-here':
                return api_key
    except:
        pass
    
    # Fall back to .env file (for local development)
    if os.path.exists('.env'):
        env_vars = load_env_file()
        api_key = env_vars.get('GEMINI_API_KEY')
        
        if api_key and api_key != 'YOUR_API_KEY_HERE':
            return api_key
    
    raise ValueError(
        "API key not found!\n"
        "Local: Add GEMINI_API_KEY to .env file\n"
        "Cloud: Add GEMINI_API_KEY to Streamlit secrets"
    )

def load_env_file(env_path='.env'):
    """Load environment variables from .env file"""
    if not os.path.exists(env_path):
        return {}
    
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
        print(f"✓ API Key loaded: {api_key[:20]}...")
        
        email_config = get_email_config()
        print(f"✓ Email config loaded: {email_config['smtp_email']}")
    except Exception as e:
        print(f"✗ Error: {e}")
