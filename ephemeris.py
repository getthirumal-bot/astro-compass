"""
Astro-App Ephemeris Calculator (Astropy version)
Works on Windows without C++ compiler
"""

from astropy.time import Time
from astropy.coordinates import get_body, solar_system_ephemeris, EarthLocation
import astropy.units as u
from datetime import datetime
import pytz
from typing import Dict

# Ayanamsa for Vedic calculations (Lahiri)
LAHIRI_AYANAMSA_2000 = 23.85  # degrees at J2000 epoch
AYANAMSA_RATE = 0.0138889  # degrees per year (approx 50" per year)

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]


def get_ayanamsa(year):
    """Calculate Lahiri ayanamsa for given year"""
    years_since_2000 = year - 2000
    return LAHIRI_AYANAMSA_2000 + (AYANAMSA_RATE * years_since_2000)


def tropical_to_sidereal(tropical_lon, year):
    """Convert tropical longitude to sidereal (Vedic)"""
    ayanamsa = get_ayanamsa(year)
    sidereal = tropical_lon - ayanamsa
    if sidereal < 0:
        sidereal += 360
    return sidereal


def get_planet_position(planet_name, time_obj):
    """Get tropical position of planet"""
    solar_system_ephemeris.set('builtin')
    
    # Map planet names
    planet_map = {
        'Sun': 'sun',
        'Moon': 'moon',
        'Mercury': 'mercury',
        'Venus': 'venus',
        'Mars': 'mars',
        'Jupiter': 'jupiter',
        'Saturn': 'saturn'
    }
    
    if planet_name in planet_map:
        body = get_body(planet_map[planet_name], time_obj, ephemeris='builtin')
        # Get ecliptic longitude
        lon = body.geocentrictrueecliptic.lon.degree
        return lon
    
    return None


def calculate_ascendant(dt, lat, lon):
    """Calculate Ascendant (simplified)"""
    time_obj = Time(dt)
    sun_tropical = get_planet_position('Sun', time_obj)
    hour_angle = (dt.hour + dt.minute/60) * 15
    asc_tropical = (sun_tropical + hour_angle) % 360
    asc_sidereal = tropical_to_sidereal(asc_tropical, dt.year)
    return asc_sidereal


def calculate_chart(birth_date: datetime, lat: float, lon: float) -> Dict:
    """Calculate complete birth chart"""
    if birth_date.tzinfo is None:
        birth_date = pytz.utc.localize(birth_date)
    
    time_obj = Time(birth_date)
    planets = {}
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    
    for planet_name in planet_names:
        tropical_long = get_planet_position(planet_name, time_obj)
        
        if tropical_long is not None:
            sidereal_long = tropical_to_sidereal(tropical_long, birth_date.year)
            sign_num = int(sidereal_long / 30)
            degree_in_sign = sidereal_long % 30
            nak_num = int(sidereal_long / 13.333333)
            nak_pada = int((sidereal_long % 13.333333) / 3.333333) + 1
            
            planets[planet_name] = {
                'longitude': round(sidereal_long, 2),
                'sign': SIGNS[sign_num],
                'sign_num': sign_num + 1,
                'degree': round(degree_in_sign, 2),
                'nakshatra': NAKSHATRAS[nak_num],
                'pada': nak_pada
            }
    
    # Calculate Rahu
    if 'Moon' in planets:
        moon_long = planets['Moon']['longitude']
        rahu_long = (moon_long + 180) % 360
        sign_num = int(rahu_long / 30)
        degree_in_sign = rahu_long % 30
        nak_num = int(rahu_long / 13.333333)
        nak_pada = int((rahu_long % 13.333333) / 3.333333) + 1
        
        planets['Rahu'] = {
            'longitude': round(rahu_long, 2),
            'sign': SIGNS[sign_num],
            'sign_num': sign_num + 1,
            'degree': round(degree_in_sign, 2),
            'nakshatra': NAKSHATRAS[nak_num],
            'pada': nak_pada
        }
    
    # Calculate Ascendant
    asc_sidereal = calculate_ascendant(birth_date, lat, lon)
    asc_sign_num = int(asc_sidereal / 30)
    
    return {
        'planets': planets,
        'ascendant': {
            'longitude': round(asc_sidereal, 2),
            'sign': SIGNS[asc_sign_num],
            'degree': round(asc_sidereal % 30, 2)
        },
        'ayanamsa': round(get_ayanamsa(birth_date.year), 4)
    }


def calculate_transits(dt: datetime = None) -> Dict:
    """Calculate current planetary transits"""
    if dt is None:
        dt = datetime.now(pytz.utc)
    elif dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    
    time_obj = Time(dt)
    transits = {}
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    
    for planet_name in planet_names:
        tropical_long = get_planet_position(planet_name, time_obj)
        
        if tropical_long is not None:
            sidereal_long = tropical_to_sidereal(tropical_long, dt.year)
            sign_num = int(sidereal_long / 30)
            
            transits[planet_name] = {
                'sign': SIGNS[sign_num],
                'degree': round(sidereal_long % 30, 2)
            }
    
    # Add Rahu
    if 'Moon' in transits:
        moon_long_tropical = get_planet_position('Moon', time_obj)
        rahu_long = tropical_to_sidereal((moon_long_tropical + 180) % 360, dt.year)
        sign_num = int(rahu_long / 30)
        
        transits['Rahu'] = {
            'sign': SIGNS[sign_num],
            'degree': round(rahu_long % 30, 2)
        }
    
    return transits


def format_chart_for_ai(chart: Dict, transits: Dict) -> str:
    """Format chart data for AI prompt"""
    output = "BIRTH CHART DATA:\n"
    output += f"Ascendant: {chart['ascendant']['sign']} {chart['ascendant']['degree']}°\n\n"
    
    output += "PLANETARY POSITIONS:\n"
    for planet, data in chart['planets'].items():
        output += f"{planet}: {data['sign']} {data['degree']}° ({data['nakshatra']} Pada {data['pada']})\n"
    
    output += "\nCURRENT TRANSITS:\n"
    for planet, data in transits.items():
        output += f"{planet}: {data['sign']} {data['degree']}°\n"
    
    return output


if __name__ == "__main__":
    print("Testing Astropy-based ephemeris...")
    birth = datetime(1976, 7, 31, 8, 12)
    birth_utc = pytz.utc.localize(birth)
    
    chart = calculate_chart(birth_utc, 15.5057, 80.0499)
    transits = calculate_transits()
    
    print("\n" + "="*60)
    print(format_chart_for_ai(chart, transits))
    print("="*60)
    print("\n✅ Astropy ephemeris working!")
