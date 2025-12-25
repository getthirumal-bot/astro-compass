"""
Country Code & Language Mapping
Maps phone country codes to countries and languages
"""

COUNTRY_CODES = {
    # Core 5 + India regional
    '+91': {'country': 'India', 'languages': ['Hindi', 'English', 'Telugu', 'Tamil', 'Kannada', 'Malayalam', 'Bengali', 'Marathi', 'Gujarati', 'Punjabi', 'Urdu', 'Odia']},
    
    # Americas
    '+1': {'country': 'United States/Canada', 'languages': ['English', 'Spanish', 'French']},
    '+52': {'country': 'Mexico', 'languages': ['Spanish', 'English']},
    '+55': {'country': 'Brazil', 'languages': ['Portuguese', 'English']},
    '+54': {'country': 'Argentina', 'languages': ['Spanish', 'English']},
    '+57': {'country': 'Colombia', 'languages': ['Spanish', 'English']},
    '+56': {'country': 'Chile', 'languages': ['Spanish', 'English']},
    '+51': {'country': 'Peru', 'languages': ['Spanish', 'English']},
    '+58': {'country': 'Venezuela', 'languages': ['Spanish', 'English']},
    
    # Europe
    '+44': {'country': 'United Kingdom', 'languages': ['English']},
    '+49': {'country': 'Germany', 'languages': ['German', 'English']},
    '+33': {'country': 'France', 'languages': ['French', 'English']},
    '+39': {'country': 'Italy', 'languages': ['Italian', 'English']},
    '+34': {'country': 'Spain', 'languages': ['Spanish', 'Catalan', 'English']},
    '+7': {'country': 'Russia', 'languages': ['Russian', 'English']},
    '+31': {'country': 'Netherlands', 'languages': ['Dutch', 'English']},
    '+48': {'country': 'Poland', 'languages': ['Polish', 'English']},
    '+46': {'country': 'Sweden', 'languages': ['Swedish', 'English']},
    '+47': {'country': 'Norway', 'languages': ['Norwegian', 'English']},
    '+45': {'country': 'Denmark', 'languages': ['Danish', 'English']},
    '+358': {'country': 'Finland', 'languages': ['Finnish', 'Swedish', 'English']},
    '+41': {'country': 'Switzerland', 'languages': ['German', 'French', 'Italian', 'English']},
    '+43': {'country': 'Austria', 'languages': ['German', 'English']},
    '+32': {'country': 'Belgium', 'languages': ['Dutch', 'French', 'German', 'English']},
    '+353': {'country': 'Ireland', 'languages': ['English', 'Irish']},
    '+351': {'country': 'Portugal', 'languages': ['Portuguese', 'English']},
    '+30': {'country': 'Greece', 'languages': ['Greek', 'English']},
    
    # Middle East
    '+971': {'country': 'UAE', 'languages': ['Arabic', 'English', 'Urdu', 'Hindi']},
    '+966': {'country': 'Saudi Arabia', 'languages': ['Arabic', 'English']},
    '+974': {'country': 'Qatar', 'languages': ['Arabic', 'English']},
    '+965': {'country': 'Kuwait', 'languages': ['Arabic', 'English']},
    '+968': {'country': 'Oman', 'languages': ['Arabic', 'English']},
    '+973': {'country': 'Bahrain', 'languages': ['Arabic', 'English']},
    '+20': {'country': 'Egypt', 'languages': ['Arabic', 'English']},
    '+212': {'country': 'Morocco', 'languages': ['Arabic', 'French', 'English']},
    '+213': {'country': 'Algeria', 'languages': ['Arabic', 'French', 'English']},
    '+216': {'country': 'Tunisia', 'languages': ['Arabic', 'French', 'English']},
    
    # Asia Pacific
    '+86': {'country': 'China', 'languages': ['Chinese', 'English']},
    '+81': {'country': 'Japan', 'languages': ['Japanese', 'English']},
    '+82': {'country': 'South Korea', 'languages': ['Korean', 'English']},
    '+852': {'country': 'Hong Kong', 'languages': ['Chinese', 'English']},
    '+886': {'country': 'Taiwan', 'languages': ['Chinese', 'English']},
    '+65': {'country': 'Singapore', 'languages': ['English', 'Chinese', 'Malay', 'Tamil']},
    '+60': {'country': 'Malaysia', 'languages': ['Malay', 'English', 'Chinese', 'Tamil']},
    '+66': {'country': 'Thailand', 'languages': ['Thai', 'English']},
    '+62': {'country': 'Indonesia', 'languages': ['Indonesian', 'English', 'Javanese']},
    '+63': {'country': 'Philippines', 'languages': ['Filipino', 'English']},
    '+84': {'country': 'Vietnam', 'languages': ['Vietnamese', 'English']},
    '+95': {'country': 'Myanmar', 'languages': ['Burmese', 'English']},
    '+855': {'country': 'Cambodia', 'languages': ['Khmer', 'English']},
    '+856': {'country': 'Laos', 'languages': ['Lao', 'English']},
    
    # South Asia
    '+92': {'country': 'Pakistan', 'languages': ['Urdu', 'English', 'Punjabi', 'Sindhi']},
    '+880': {'country': 'Bangladesh', 'languages': ['Bengali', 'English']},
    '+94': {'country': 'Sri Lanka', 'languages': ['Sinhala', 'Tamil', 'English']},
    '+977': {'country': 'Nepal', 'languages': ['Nepali', 'English']},
    
    # Oceania
    '+61': {'country': 'Australia', 'languages': ['English']},
    '+64': {'country': 'New Zealand', 'languages': ['English', 'Maori']},
    
    # Africa
    '+27': {'country': 'South Africa', 'languages': ['English', 'Afrikaans', 'Zulu', 'Xhosa']},
    '+234': {'country': 'Nigeria', 'languages': ['English', 'Yoruba', 'Igbo', 'Hausa']},
    '+254': {'country': 'Kenya', 'languages': ['English', 'Swahili']},
    '+233': {'country': 'Ghana', 'languages': ['English', 'Akan', 'Ewe']},
    '+256': {'country': 'Uganda', 'languages': ['English', 'Swahili', 'Luganda']},
    '+255': {'country': 'Tanzania', 'languages': ['Swahili', 'English']},
    '+251': {'country': 'Ethiopia', 'languages': ['Amharic', 'English']},
    '+263': {'country': 'Zimbabwe', 'languages': ['English', 'Shona', 'Ndebele']},
    '+260': {'country': 'Zambia', 'languages': ['English', 'Bemba']},
    '+267': {'country': 'Botswana', 'languages': ['English', 'Setswana']},
    '+264': {'country': 'Namibia', 'languages': ['English', 'Afrikaans']},
    '+230': {'country': 'Mauritius', 'languages': ['English', 'French', 'Creole']},
}

# Major Indian cities with coordinates
INDIAN_CITIES = {
    'Mumbai': (19.0760, 72.8777),
    'Delhi': (28.7041, 77.1025),
    'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567),
    'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873),
    'Lucknow': (26.8467, 80.9462),
    'Ongole': (15.5057, 80.0499),
    'Vijayawada': (16.5062, 80.6480),
    'Visakhapatnam': (17.6868, 83.2185),
    'Guntur': (16.3067, 80.4365),
    'Tirupati': (13.6288, 79.4192),
}

# Global major cities
GLOBAL_CITIES = {
    'New York': (40.7128, -74.0060),
    'London': (51.5074, -0.1278),
    'Paris': (48.8566, 2.3522),
    'Tokyo': (35.6762, 139.6503),
    'Dubai': (25.2048, 55.2708),
    'Singapore': (1.3521, 103.8198),
    'Los Angeles': (34.0522, -118.2437),
    'Sydney': (-33.8688, 151.2093),
    'Toronto': (43.6532, -79.3832),
    'Berlin': (52.5200, 13.4050),
}

ALL_CITIES = {**INDIAN_CITIES, **GLOBAL_CITIES}


def detect_country_from_phone(phone: str) -> dict:
    """
    Detect country and languages from phone number
    
    Args:
        phone: Phone number with country code (e.g., +919876543210)
    
    Returns:
        {
            'country': str,
            'languages': list,
            'code': str
        }
    """
    if not phone.startswith('+'):
        return None
    
    # Try longest codes first (e.g., +971 before +91)
    sorted_codes = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)
    
    for code in sorted_codes:
        if phone.startswith(code):
            return {
                'country': COUNTRY_CODES[code]['country'],
                'languages': COUNTRY_CODES[code]['languages'],
                'code': code
            }
    
    return None


def get_coordinates(city: str, country: str = None) -> tuple:
    """Get lat/lon for a city"""
    
    # Try exact match first
    if city in ALL_CITIES:
        return ALL_CITIES[city]
    
    # Try case-insensitive match
    for known_city, coords in ALL_CITIES.items():
        if known_city.lower() == city.lower():
            return coords
    
    # Default to Hyderabad if not found
    print(f"Warning: '{city}' not found, using Hyderabad coordinates")
    return INDIAN_CITIES['Hyderabad']


if __name__ == "__main__":
    # Test
    test_numbers = ['+919876543210', '+14155552671', '+447911123456']
    
    for number in test_numbers:
        result = detect_country_from_phone(number)
        if result:
            print(f"{number} → {result['country']}")
            print(f"  Languages: {', '.join(result['languages'])}\n")
