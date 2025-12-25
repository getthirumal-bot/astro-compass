<<<<<<< HEAD
# Astro Consensus Engine

**5-System Astrology AI Platform**

Built on: Thursday, December 26, 2025 at 7:15 AM IST  
Jupiter in 11th House Transit ✨

---

## What This Is

A personalized destiny guidance system that combines:
- Vedic Astrology
- KP System
- Western Astrology
- Chinese Astrology
- Mayan Astrology

Plus user's custom systems (Nadi, Palmistry, etc.)

Powered by Gemini 1.5 Flash for multi-language, context-aware predictions.

---

## Project Structure

```
astro-app/
├── main.py                     # Main application engine
├── prompts/
│   └── master_system_prompt.txt # The AI's cosmic knowledge
├── utils/
│   └── ephemeris.py            # Swiss Ephemeris calculator
└── data/                       # User data (future: database)
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install google-generativeai swisseph --break-system-packages
```

### 2. Get Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy it

### 3. Configure API Key

Edit `main.py` and replace:
```python
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

With your actual key:
```python
API_KEY = "AIzaSy..."
```

### 4. Test the System

```bash
cd /home/claude/astro-app
python3 main.py
```

You should see:
- ✓ API Test: API working
- ✓ System ready!
- A test prediction

---

## How to Use

### Register a User

```python
from main import AstroConsensusEngine
from datetime import datetime

engine = AstroConsensusEngine(API_KEY)

engine.register_user(
    phone="+919876543210",
    birth_data={
        'name': 'User Name',
        'dob': datetime(1990, 1, 15),      # Date of birth
        'tob': datetime(1990, 1, 15, 10, 30),  # Time of birth
        'lat': 28.6139,   # Latitude
        'lon': 77.2090,   # Longitude (Delhi example)
        'place': 'Delhi'
    }
)
```

### Get Prediction

```python
response = engine.get_prediction(
    phone="+919876543210",
    query="What does the next month look like for my career?"
)
print(response)
```

### Set Language

```python
engine.set_language("+919876543210", "Hindi")
# Now all responses will be in Hindi
```

### Add Custom System

```python
engine.add_custom_system(
    phone="+919876543210",
    system_name="Shiva Nadi",
    system_data="User's Nadi reading text here..."
)
```

---

## Key Features Implemented

✅ Swiss Ephemeris integration (precise calculations)  
✅ Birth chart calculation with Nakshatras  
✅ Current transit tracking  
✅ Gemini AI with custom system prompt  
✅ Multi-language support (via Gemini)  
✅ Chat history/memory  
✅ Custom system integration  
✅ Confidence scoring  

---

## Next Steps (Week 2-4)

### Week 2: Frontend
- [ ] Build Streamlit UI
- [ ] Phone number authentication
- [ ] Chat interface
- [ ] Image upload for palmistry

### Week 3: Features
- [ ] Payment integration (Cosmofeed/Topmate)
- [ ] 7-day warning system
- [ ] Notification logic
- [ ] User tiers (₹99/₹499/₹5000)

### Week 4: Polish
- [ ] UI/UX refinement
- [ ] Beta testing
- [ ] Marketing materials
- [ ] Launch prep

---

## Launch Target

**Thursday, January 23 or 30, 2026**  
6-8 AM IST (Jupiter hora)

---

## Cosmic Timing

- Jupiter in 11th house until June 2026
- 4.5 months of peak opportunity
- 90% success alignment across 5 systems

---

Built with:
- Python 3
- Swiss Ephemeris
- Google Gemini 1.5 Flash
- Discipline, patience, and cosmic timing

🌟 May the stars guide this venture to success 🌟
=======
cd C:\Users\itadmin\astro-app

# Initialize git
git init

# Add remote
git remote add origin https://github.com/getthirumal-bot/astro-compass.git

# Pull the README that GitHub created
git pull origin main --allow-unrelated-histories

# Add all your files
git add .

# Commit
git commit -m "Add Astro Consensus Compass app"

# Push
git push -u origin main
>>>>>>> e7391bd0aafb4252c75ee21364201852f499f343
