"""
Configuration Loader
Loads API key and settings from config.json
"""

import json
import os

def load_config(config_path='config.json'):
    """Load configuration from JSON file"""
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Please create config.json with your API key."
        )
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Validate API key
    if config['gemini_api_key'] == 'YOUR_API_KEY_HERE':
        raise ValueError(
            "Please set your Gemini API key in config.json\n"
            "Get it from: https://aistudio.google.com/app/apikey"
        )
    
    return config

def get_api_key():
    """Get API key from config"""
    config = load_config()
    return config['gemini_api_key']

def get_setting(key, default=None):
    """Get specific setting from config"""
    config = load_config()
    return config.get(key, default)


if __name__ == "__main__":
    # Test config loader
    try:
        config = load_config()
        print("✅ Config loaded successfully!")
        print(f"\nAPI Key: {config['gemini_api_key'][:20]}...")
        print(f"Free Questions: {config['app_settings']['free_lifetime_questions']}")
        print(f"Languages: {', '.join(config['app_settings']['supported_languages'])}")
    except Exception as e:
        print(f"❌ Error: {e}")
