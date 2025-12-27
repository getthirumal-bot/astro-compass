"""
Astro Consensus Engine - Streamlit Web Interface
Complete version with OTP authentication, session management, and enhanced features
"""

import streamlit as st
from datetime import datetime
import time
from astro_engine import AstroEngine
from env_loader import get_api_key
from country_utils import detect_country_from_phone, get_coordinates
from otp_service import OTPService
from session_manager import SessionManager
import pytz

# Initialize services
otp_service = OTPService()
session_manager = SessionManager()

# Shared country list
ALL_COUNTRIES = [
    ('🇮🇳 India', '+91'),
    ('🇺🇸 United States', '+1'),
    ('🇬🇧 United Kingdom', '+44'),
    # Middle East
    ('🇦🇪 UAE', '+971'),
    ('🇸🇦 Saudi Arabia', '+966'),
    ('🇶🇦 Qatar', '+974'),
    ('🇰🇼 Kuwait', '+965'),
    ('🇴🇲 Oman', '+968'),
    ('🇧🇭 Bahrain', '+973'),
    # Asia Pacific
    ('🇦🇺 Australia', '+61'),
    ('🇨🇦 Canada', '+1'),
    ('🇸🇬 Singapore', '+65'),
    ('🇲🇾 Malaysia', '+60'),
    ('🇹🇭 Thailand', '+66'),
    ('🇮🇩 Indonesia', '+62'),
    ('🇵🇭 Philippines', '+63'),
    ('🇵🇰 Pakistan', '+92'),
    ('🇧🇩 Bangladesh', '+880'),
    ('🇱🇰 Sri Lanka', '+94'),
    ('🇳🇵 Nepal', '+977'),
    ('🇲🇲 Myanmar', '+95'),
    ('🇻🇳 Vietnam', '+84'),
    ('🇰🇭 Cambodia', '+855'),
    ('🇱🇦 Laos', '+856'),
    # East Asia
    ('🇨🇳 China', '+86'),
    ('🇯🇵 Japan', '+81'),
    ('🇰🇷 South Korea', '+82'),
    ('🇭🇰 Hong Kong', '+852'),
    ('🇹🇼 Taiwan', '+886'),
    # Europe
    ('🇩🇪 Germany', '+49'),
    ('🇫🇷 France', '+33'),
    ('🇮🇹 Italy', '+39'),
    ('🇪🇸 Spain', '+34'),
    ('🇷🇺 Russia', '+7'),
    ('🇳🇱 Netherlands', '+31'),
    ('🇵🇱 Poland', '+48'),
    ('🇸🇪 Sweden', '+46'),
    ('🇳🇴 Norway', '+47'),
    ('🇩🇰 Denmark', '+45'),
    ('🇫🇮 Finland', '+358'),
    ('🇨🇭 Switzerland', '+41'),
    ('🇦🇹 Austria', '+43'),
    ('🇧🇪 Belgium', '+32'),
    ('🇮🇪 Ireland', '+353'),
    ('🇵🇹 Portugal', '+351'),
    ('🇬🇷 Greece', '+30'),
    # Americas
    ('🇧🇷 Brazil', '+55'),
    ('🇲🇽 Mexico', '+52'),
    ('🇦🇷 Argentina', '+54'),
    ('🇨🇴 Colombia', '+57'),
    ('🇨🇱 Chile', '+56'),
    ('🇵🇪 Peru', '+51'),
    ('🇻🇪 Venezuela', '+58'),
    # Africa
    ('🇿🇦 South Africa', '+27'),
    ('🇪🇬 Egypt', '+20'),
    ('🇳🇬 Nigeria', '+234'),
    ('🇰🇪 Kenya', '+254'),
    ('🇬🇭 Ghana', '+233'),
    ('🇺🇬 Uganda', '+256'),
    ('🇹🇿 Tanzania', '+255'),
    ('🇪🇹 Ethiopia', '+251'),
    ('🇲🇦 Morocco', '+212'),
    ('🇩🇿 Algeria', '+213'),
    ('🇹🇳 Tunisia', '+216'),
    ('🇿🇼 Zimbabwe', '+263'),
    ('🇿🇲 Zambia', '+260'),
    ('🇧🇼 Botswana', '+267'),
    ('🇳🇦 Namibia', '+264'),
    ('🇲🇺 Mauritius', '+230'),
]

# Page config
st.set_page_config(
    page_title="Astro Compass",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize engine
@st.cache_resource
def init_engine():
    api_key = get_api_key()
    return AstroEngine(api_key)

engine = init_engine()

# Session state initialization
if 'phone' not in st.session_state:
    st.session_state.phone = None
if 'session_token' not in st.session_state:
    st.session_state.session_token = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'otp_phone' not in st.session_state:
    st.session_state.otp_phone = None
if 'registration_step' not in st.session_state:
    st.session_state.registration_step = 1
if 'show_registration' not in st.session_state:
    st.session_state.show_registration = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

# Check for existing session on startup
if st.session_state.phone is None and st.session_state.session_token is None:
    # Try to restore session from browser storage
    if 'session_token_check' not in st.session_state:
        st.session_state.session_token_check = True

# Helper functions
def send_otp(phone):
    """Send OTP to phone number"""
    result = otp_service.send_otp(phone)
    if result['success']:
        st.session_state.otp_sent = True
        st.session_state.otp_phone = phone
        st.success(f"✅ OTP sent to {phone}")
        if result.get('dev_otp'):
            st.info(f"🔧 DEV MODE: Your OTP is **{result['dev_otp']}**")
        return True
    else:
        st.error(f"❌ {result['message']}")
        return False

def verify_otp(phone, otp_code):
    """Verify OTP code"""
    result = otp_service.verify_otp(phone, otp_code)
    if result['success']:
        return True
    else:
        st.error(f"❌ {result['message']}")
        return False

def create_session(phone, stay_signed_in=True):
    """Create new session for user"""
    user = engine.db.get_user(phone)
    if not user:
        return None
    
    result = session_manager.create_session(
        user_phone=phone,
        user_tier=user.get('tier', 'FREE'),
        stay_signed_in=stay_signed_in
    )
    
    if result['success']:
        st.session_state.session_token = result['session_token']
        st.session_state.phone = phone
        return result['session_token']
    else:
        st.error(f"❌ {result['message']}")
        return None

def logout():
    """Logout current session"""
    if st.session_state.session_token:
        session_manager.logout_session(st.session_state.session_token)
    
    st.session_state.phone = None
    st.session_state.session_token = None
    st.session_state.chat_history = []
    st.session_state.otp_sent = False
    st.session_state.otp_phone = None
    st.session_state.registration_step = 1
    st.session_state.show_registration = False
    st.rerun()

# Header
st.title("🧭 Astro Compass")
st.caption("Your Cosmic Guide • 5-System Consensus + AI Insights")

# Sidebar - Login/Register/User Info
with st.sidebar:
    if st.session_state.phone:
        # User logged in - show info
        user = engine.db.get_user(st.session_state.phone)
        if user:
            st.success(f"👤 {user['name']}")
            
            # Show tier and quota
            tier = user.get('tier', 'FREE')
            questions_asked = user.get('questions_asked', 0)
            questions_limit = user.get('questions_limit', 7)
            
            st.info(f"**Tier:** {tier}\n**Questions:** {questions_asked}/{questions_limit}")
            
            # Show active sessions
            user_sessions = session_manager.get_user_sessions(st.session_state.phone)
            active_count = len(user_sessions)
            
            if tier == 'FREE':
                max_devices = 1
            elif tier == 'PAID':
                max_devices = 2
            elif tier == 'PREMIUM':
                max_devices = 3
            else:  # VIP
                max_devices = float('inf')
            
            device_text = f"∞" if max_devices == float('inf') else str(max_devices)
            st.caption(f"📱 Active Devices: {active_count}/{device_text}")
            
            # Navigation
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 Home", use_container_width=True):
                    st.session_state.current_page = 'main'
                    st.rerun()
            with col2:
                if st.button("⚙️ Sessions", use_container_width=True):
                    st.session_state.current_page = 'sessions'
                    st.rerun()
            
            # Logout button
            st.divider()
            if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                logout()
    
    else:
        # Not logged in - show login/register
        st.header("Welcome!")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        # LOGIN TAB
        with tab1:
            if not st.session_state.otp_sent:
                # Step 1: Phone number entry
                login_country = st.selectbox(
                    "Country",
                    options=[c[0] for c in ALL_COUNTRIES],
                    key="login_country"
                )
                login_code = next(c[1] for c in ALL_COUNTRIES if c[0] == login_country)
                
                st.info(f"**Code:** {login_code}")
                
                phone_only = st.text_input(
                    f"Phone Number",
                    placeholder="9876543210",
                    key="login_phone_input"
                )
                
                phone_input = f"{login_code}{phone_only}" if phone_only else ""
                
                if st.button("Send OTP", use_container_width=True):
                    if phone_input:
                        user = engine.db.get_user(phone_input)
                        if user:
                            send_otp(phone_input)
                        else:
                            st.error("❌ User not found. Please register.")
                    else:
                        st.warning("⚠️ Enter phone number")
            
            else:
                # Step 2: OTP verification
                st.success(f"OTP sent to {st.session_state.otp_phone}")
                
                otp_code = st.text_input("Enter 6-digit OTP", max_chars=6, key="login_otp")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Verify", use_container_width=True):
                        if verify_otp(st.session_state.otp_phone, otp_code):
                            create_session(st.session_state.otp_phone)
                            st.session_state.otp_sent = False
                            st.rerun()
                
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.otp_sent = False
                        st.session_state.otp_phone = None
                        st.rerun()
        
        # REGISTER TAB
        with tab2:
            if st.session_state.registration_step == 1:
                # Step 1: Basic info + OTP
                st.markdown("### Step 1: Verify Phone")
                
                reg_country = st.selectbox(
                    "Country",
                    options=[c[0] for c in ALL_COUNTRIES],
                    key="reg_country"
                )
                reg_code = next(c[1] for c in ALL_COUNTRIES if c[0] == reg_country)
                
                st.info(f"**Code:** {reg_code}")
                
                reg_name = st.text_input("Full Name*", key="reg_name")
                reg_phone_only = st.text_input("Phone Number*", placeholder="9876543210", key="reg_phone")
                reg_email = st.text_input("Email (optional)", placeholder="name@example.com", key="reg_email")
                
                reg_phone = f"{reg_code}{reg_phone_only}" if reg_phone_only else ""
                
                if not st.session_state.otp_sent:
                    if st.button("Send OTP", use_container_width=True):
                        if reg_name and reg_phone:
                            # Check if user exists
                            existing = engine.db.get_user(reg_phone)
                            if existing:
                                st.error("❌ Phone already registered. Please login.")
                            else:
                                # Save temp data
                                st.session_state.temp_name = reg_name
                                st.session_state.temp_phone = reg_phone
                                st.session_state.temp_email = reg_email
                                st.session_state.temp_country = reg_country.split(' ', 1)[1]
                                send_otp(reg_phone)
                        else:
                            st.warning("⚠️ Fill all required fields")
                else:
                    # OTP verification
                    st.success(f"OTP sent to {st.session_state.otp_phone}")
                    otp_code = st.text_input("Enter 6-digit OTP", max_chars=6, key="reg_otp")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Verify & Continue", use_container_width=True):
                            if verify_otp(st.session_state.otp_phone, otp_code):
                                st.session_state.registration_step = 2
                                st.session_state.otp_sent = False
                                st.rerun()
                    
                    with col2:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state.otp_sent = False
                            st.session_state.registration_step = 1
                            st.rerun()
            
            elif st.session_state.registration_step == 2:
                # Step 2: Birth data
                st.markdown("### Step 2: Birth Details")
                
                # Birth data quality selector
                birth_quality = st.radio(
                    "How accurate is your birth data?",
                    options=["Exact", "Approximate", "None (Use Prashna)"],
                    key="birth_quality"
                )
                
                if birth_quality == "Exact":
                    # Full birth details
                    col1, col2 = st.columns(2)
                    with col1:
                        dob = st.date_input(
                            "Date of Birth*",
                            min_value=datetime(1900, 1, 1),
                            max_value=datetime.now(),
                            key="reg_dob"
                        )
                    with col2:
                        time_col1, time_col2 = st.columns(2)
                        with time_col1:
                            hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12, key="reg_hour")
                        with time_col2:
                            minute = st.number_input("Min (0-59)", min_value=0, max_value=59, value=0, key="reg_min")
                    
                    tob = f"{hour:02d}:{minute:02d}"
                    
                    # Location
                    pob_city = st.text_input("Birth City*", key="reg_city")
                    pob_state = st.text_input("Birth State/Region", key="reg_state")
                    pob_country = st.text_input("Birth Country*", value=st.session_state.temp_country, key="reg_birth_country")
                    
                    if st.button("Complete Registration", use_container_width=True):
                        if pob_city and pob_country:
                            # Get coordinates and timezone
                            coords = get_coordinates(pob_city, pob_country)
                            if coords:
                                # Create user
                                user_data = {
                                    'name': st.session_state.temp_name,
                                    'phone': st.session_state.temp_phone,
                                    'email': st.session_state.temp_email,
                                    'dob': dob.strftime('%Y-%m-%d'),
                                    'tob': tob,
                                    'pob': f"{pob_city}, {pob_country}",
                                    'birth_city': pob_city,
                                    'birth_state': pob_state,
                                    'birth_country': pob_country,
                                    'birth_timezone': coords['timezone'],
                                    'birth_data_quality': 'exact',
                                    'tier': 'FREE',
                                    'questions_limit': 7,
                                    'otp_verified': True
                                }
                                
                                engine.db.register_user(**user_data)
                                create_session(st.session_state.temp_phone)
                                
                                # Clear temp data
                                st.session_state.registration_step = 1
                                st.session_state.show_registration = False
                                st.success("✅ Registration complete!")
                                st.rerun()
                            else:
                                st.error("❌ Could not find location. Please check city/country.")
                        else:
                            st.warning("⚠️ Fill all required fields")
                
                elif birth_quality == "Approximate":
                    st.info("📅 Approximate birth data mode - AI will work with ranges")
                    
                    year_range_start = st.number_input("Birth Year (approx start)", min_value=1900, max_value=datetime.now().year, value=1990, key="year_start")
                    year_range_end = st.number_input("Birth Year (approx end)", min_value=1900, max_value=datetime.now().year, value=1995, key="year_end")
                    
                    time_of_day = st.selectbox("Time of Day", ["Morning (6-12)", "Afternoon (12-18)", "Evening (18-24)", "Night (0-6)"], key="time_of_day")
                    
                    pob_city = st.text_input("Birth City (if known)", key="approx_city")
                    pob_country = st.text_input("Birth Country*", value=st.session_state.temp_country, key="approx_country")
                    
                    if st.button("Complete Registration", use_container_width=True):
                        if pob_country:
                            user_data = {
                                'name': st.session_state.temp_name,
                                'phone': st.session_state.temp_phone,
                                'email': st.session_state.temp_email,
                                'dob': f"{year_range_start}-{year_range_end}",
                                'tob': time_of_day,
                                'pob': f"{pob_city if pob_city else 'Unknown'}, {pob_country}",
                                'birth_city': pob_city,
                                'birth_country': pob_country,
                                'birth_data_quality': 'approximate',
                                'tier': 'FREE',
                                'questions_limit': 7,
                                'otp_verified': True
                            }
                            
                            engine.db.register_user(**user_data)
                            create_session(st.session_state.temp_phone)
                            
                            st.session_state.registration_step = 1
                            st.session_state.show_registration = False
                            st.success("✅ Registration complete!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Enter birth country")
                
                else:  # None
                    st.info("🔮 Prashna mode - AI will answer based on time of question")
                    
                    if st.button("Complete Registration", use_container_width=True):
                        user_data = {
                            'name': st.session_state.temp_name,
                            'phone': st.session_state.temp_phone,
                            'email': st.session_state.temp_email,
                            'birth_data_quality': 'none',
                            'tier': 'FREE',
                            'questions_limit': 7,
                            'otp_verified': True
                        }
                        
                        engine.db.register_user(**user_data)
                        create_session(st.session_state.temp_phone)
                        
                        st.session_state.registration_step = 1
                        st.session_state.show_registration = False
                        st.success("✅ Registration complete!")
                        st.rerun()

# Main content based on current page
if st.session_state.current_page == 'sessions':
    # Session Management Page
    st.header("⚙️ Manage Your Sessions")
    
    if st.session_state.phone:
        user = engine.db.get_user(st.session_state.phone)
        user_sessions = session_manager.get_user_sessions(st.session_state.phone)
        
        tier = user.get('tier', 'FREE')
        if tier == 'FREE':
            max_devices = 1
        elif tier == 'PAID':
            max_devices = 2
        elif tier == 'PREMIUM':
            max_devices = 3
        else:
            max_devices = float('inf')
        
        device_text = "Unlimited" if max_devices == float('inf') else str(max_devices)
        st.info(f"**Your Plan:** {tier} - Up to {device_text} devices")
        
        st.divider()
        
        if user_sessions:
            st.subheader(f"Active Sessions ({len(user_sessions)})")
            
            for idx, session in enumerate(user_sessions, 1):
                with st.expander(f"📱 Device {idx} - {session['device_info']['browser']} on {session['device_info']['os']}"):
                    st.write(f"**Last Active:** {session['last_activity']}")
                    st.write(f"**Created:** {session['created_at']}")
                    
                    is_current = session['session_token'] == st.session_state.session_token
                    if is_current:
                        st.success("✅ Current Device")
                    else:
                        if st.button(f"Logout Device {idx}", key=f"logout_{idx}"):
                            session_manager.logout_session(session['session_token'])
                            st.success(f"✅ Device {idx} logged out")
                            st.rerun()
        else:
            st.info("No active sessions found")
        
        if tier != 'VIP' and len(user_sessions) >= max_devices:
            st.warning(f"⚠️ You've reached your device limit ({max_devices})")
            st.info("💎 Upgrade to VIP for unlimited devices!")

elif st.session_state.current_page == 'main':
    # Main Chat Interface
    if not st.session_state.phone:
        # Welcome screen
        st.markdown("""
        ### 🌟 Welcome to Astro Compass
        
        **Your Personal Cosmic Guide powered by AI + Ancient Wisdom**
        
        #### ✨ What Makes Us Different?
        
        - **5-System Consensus**: We combine Vedic, KP, Western, Chinese & Mayan astrology
        - **70-90% Accuracy**: Multi-system validation ensures reliable insights
        - **No Birth Data? No Problem!**: Prashna astrology works without birth details
        - **Forever Login**: Stay signed in across all your devices
        - **7 Free Questions**: Start exploring immediately!
        
        #### 🎁 Free Tier (7 Questions)
        Perfect for trying out the service
        
        #### 💎 Premium Tiers
        """)
        
        with st.expander("📊 View All Plans"):
            st.markdown("""
            | Feature | FREE | PAID ($1) | PREMIUM ($5) | VIP ($50) |
            |---------|------|-----------|--------------|-----------|
            | Questions | 7 | 100 | 500 | Unlimited |
            | Devices | 1 | 2 | 3 | Unlimited |
            | AI Systems | 5 core | 5 core + 6 | All 16 | All 16 + Priority |
            | Birth Rectification | ❌ | ✅ | ✅ | ✅ Advanced |
            | Prashna/Palmistry | ❌ | ✅ | ✅ | ✅ Enhanced |
            | Response Depth | Basic | Detailed | Comprehensive | Ultra-Detailed |
            | Weekly Forecasts | ❌ | ❌ | ✅ | ✅ Daily |
            | Priority Support | ❌ | ❌ | ❌ | ✅ 24/7 |
            """)
        
        st.markdown("""
        ### 🚀 Get Started
        
        👈 **Login or Register** in the sidebar to begin your cosmic journey!
        """)
    
    else:
        # Logged in - show chat interface
        user = engine.db.get_user(st.session_state.phone)
        
        # Check quota
        if not engine.db.can_ask_question(st.session_state.phone):
            st.error("❌ You've reached your question limit!")
            st.info("💎 Upgrade your plan to ask more questions")
            
            if st.button("Upgrade Now"):
                st.info("💳 Payment integration coming soon!")
        else:
            # Suggested questions
            if not st.session_state.chat_history:
                st.markdown("### 💫 Suggested Questions")
                
                suggestions = [
                    "What does my birth chart say about my career?",
                    "When is a good time for important decisions?",
                    "What are my karmic lessons in this lifetime?",
                    "How can I improve my relationships?",
                    "What is my life purpose according to my chart?"
                ]
                
                cols = st.columns(2)
                for idx, suggestion in enumerate(suggestions):
                    with cols[idx % 2]:
                        if st.button(suggestion, key=f"sug_{idx}", use_container_width=True):
                            st.session_state.chat_history.append({"role": "user", "content": suggestion})
                            st.rerun()
            
            # Chat history
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask your question..."):
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Get AI response
                with st.chat_message("assistant"):
                    with st.spinner("Consulting the cosmos..."):
                        response = engine.get_prediction(
                            user_data=user,
                            question=prompt
                        )
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Increment question count
                engine.db.increment_question_count(st.session_state.phone)
                st.rerun()

# Footer
st.divider()
st.caption("🧭 Astro Compass • Powered by AI + Ancient Wisdom • Made with ❤️ in India")
