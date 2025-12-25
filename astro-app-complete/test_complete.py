"""
TEST SCRIPT - Run this on your local machine
"""

import google.generativeai as genai
from datetime import datetime

# Your API Key
API_KEY = "AIzaSyDSS3asd2mFDs5AykDLSBtTUV2rsEHJw1Y"

print("=" * 70)
print("ASTRO APP - API TEST")
print("=" * 70)

# Test 1: Basic Connection
print("\n[Test 1] Testing API connection...")
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'API working!' if you can read this.")
    print(f"✅ SUCCESS: {response.text}")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit()

# Test 2: Astrology Response
print("\n[Test 2] Testing astrology knowledge...")
try:
    prompt = """
    You are an astrology expert. 
    
    Birth Chart:
    - Sun: Cancer
    - Moon: Virgo
    - Ascendant: Leo
    - Jupiter: Taurus (10th house)
    
    Question: What does Jupiter in 10th house mean for career?
    
    Give a 2-sentence answer.
    """
    
    response = model.generate_content(prompt)
    print(f"✅ Response: {response.text}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 3: Multi-language
print("\n[Test 3] Testing Hindi language support...")
try:
    response = model.generate_content("Say 'Hello, I can speak Hindi' in Hindi")
    print(f"✅ Response: {response.text}")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 70)
print("ALL TESTS COMPLETE!")
print("=" * 70)
print("\nYour API key is working. Ready to build the app!")
