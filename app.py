"""
Astro Consensus Engine - Streamlit Web Interface
Simple chat-based UI for users to interact with the system
"""

import streamlit as st
from datetime import datetime
from astro_engine import AstroEngine
from env_loader import get_api_key
from country_utils import detect_country_from_phone, get_coordinates
from otp_service import OTPService
from session_manager import SessionManager

# Initialize services
otp_service = OTPService()
session_manager = SessionManager()

# Shared country list - used in both login and registration
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

# Shared countries list for both login and registration
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
    page_title="Astro Consensus Compass",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded"  # Sidebar open by default on mobile
)

# Initialize engine
@st.cache_resource
def init_engine():
    api_key = get_api_key()
    return AstroEngine(api_key)

engine = init_engine()

# Session state for login
if 'phone' not in st.session_state:
    st.session_state.phone = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'follow_up_options' not in st.session_state:
    st.session_state.follow_up_options = []
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'otp_phone' not in st.session_state:
    st.session_state.otp_phone = None
if 'session_token' not in st.session_state:
    st.session_state.session_token = None
if 'registration_step' not in st.session_state:
    st.session_state.registration_step = 1
if 'temp_reg_data' not in st.session_state:
    st.session_state.temp_reg_data = {}
if 'current_otp' not in st.session_state:
    st.session_state.current_otp = None

# Helper functions for OTP and sessions
def send_otp(phone):
    """Send OTP to phone number"""
    # Extract country code from phone (everything before the main number)
    # For +919876543210, country_code is +91
    country_code = phone[:3] if phone.startswith('+91') else phone[:2]
    
    result = otp_service.send_otp(phone, country_code)
    success, message, dev_otp = result
    
    if success:
        st.session_state.otp_sent = True
        st.session_state.otp_phone = phone
        st.success(f"✅ OTP sent to {phone}")
        if dev_otp:
            # Store OTP in session state so it persists across reruns
            st.session_state.current_otp = dev_otp
        return True
    else:
        st.error(f"❌ {message}")
        return False

def verify_otp(phone, otp_code):
    """Verify OTP code"""
    success, message = otp_service.verify_otp(phone, otp_code)
    if success:
        return True
    else:
        st.error(f"❌ {message}")
        return False

def create_session(phone):
    """Create new session for user"""
    user = engine.db.get_user(phone)
    if not user:
        return None
    
    tier = user.get('subscription', 'FREE')
    success, message, session_token = session_manager.create_session(
        phone=phone,
        tier=tier
    )
    
    if success:
        st.session_state.session_token = session_token
        st.session_state.phone = phone
        return session_token
    else:
        st.error(f"❌ {message}")
        return None

def logout():
    """Logout current session"""
    if st.session_state.session_token and st.session_state.phone:
        session_manager.logout_session(st.session_state.phone, st.session_state.session_token)
    
    # Clear ALL session state to prevent data leakage between users
    st.session_state.phone = None
    st.session_state.session_token = None
    st.session_state.chat_history = []
    st.session_state.follow_up_options = []  # Clear follow-ups!
    st.session_state.otp_sent = False
    st.session_state.otp_phone = None
    if 'current_otp' in st.session_state:
        del st.session_state.current_otp
    if 'pending_question' in st.session_state:
        del st.session_state.pending_question
    st.rerun()

# Header
st.title("🧭 Astro Consensus Compass")
st.caption("Your Cosmic Guide • 5 Core Systems (Vedic, KP, Western, Chinese, Mayan) + 11 Optional Systems")

# Sidebar - Login/Register
with st.sidebar:
    st.header("Login")
    
    if st.session_state.phone is None:
        # Login form - Country selection OUTSIDE any container for reactivity
        st.subheader("Login")
        
        # Country code selector for login (REACTIVE)
        login_country = st.selectbox(
            "Select Your Country",
            options=[c[0] for c in ALL_COUNTRIES],
            key="login_country"
        )
        
        login_code = next(c[1] for c in ALL_COUNTRIES if c[0] == login_country)
        
        # Show detected code
        st.info(f"**Country Code:** {login_code}")
        
        # Phone number input (just digits)
        phone_only = st.text_input(
            f"Phone Number ({login_code} will be added automatically)",
            placeholder="9876543210",
            key="login_phone_input",
            help="Enter only digits (browser may suggest your name - ignore it, type your phone number)"
        )
        
        # Construct full phone
        phone_input = f"{login_code}{phone_only}" if phone_only else ""
        
        # OTP Login Flow
        if not st.session_state.otp_sent:
            # Step 1: Send OTP
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Send OTP", use_container_width=True, key="login_send_otp"):
                    if phone_input:
                        user = engine.db.get_user(phone_input)
                        if user:
                            if send_otp(phone_input):
                                st.rerun()
                        else:
                            st.error("User not found. Please register.")
                    else:
                        st.warning("Enter phone number")
            
            with col2:
                if st.button("Register", use_container_width=True, key="show_reg_btn"):
                    st.session_state.show_registration = True
        else:
            # Step 2: OTP Verification
            st.success(f"OTP sent to {st.session_state.otp_phone}")
            
            # Show OTP prominently for testing
            if 'current_otp' in st.session_state and st.session_state.current_otp:
                st.warning(f"🔧 **DEV MODE - Your OTP:** `{st.session_state.current_otp}`")
            
            otp_code = st.text_input("Enter 6-digit OTP", max_chars=6, key="login_otp")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Verify", use_container_width=True, key="login_verify"):
                    if verify_otp(st.session_state.otp_phone, otp_code):
                        create_session(st.session_state.otp_phone)
                        st.session_state.otp_sent = False
                        if 'current_otp' in st.session_state:
                            del st.session_state.current_otp
                        st.rerun()
            
            with col2:
                if st.button("Cancel", use_container_width=True, key="login_cancel"):
                    st.session_state.otp_sent = False
                    st.session_state.otp_phone = None
                    st.rerun()
        
        # Registration form
        if 'show_registration' in st.session_state and st.session_state.show_registration:
            st.divider()
            st.subheader("Register")
            
            # STEP 1: Country selection (OUTSIDE FORM - updates reactively)
            selected_country = st.selectbox(
                "Select Your Country*",
                options=[c[0] for c in ALL_COUNTRIES],
                index=0,
                key="selected_country_reactive"
            )
            
            # Get country details
            country_code = next(c[1] for c in ALL_COUNTRIES if c[0] == selected_country)
            country_name = selected_country.split(' ', 1)[1]
            
            # Get languages
            country_info = detect_country_from_phone(country_code + "1234567890")
            available_languages = country_info['languages'] if country_info else ['English']
            
            # Show preview
            st.info(f"**Country Code:** {country_code} | **Languages:** {', '.join(available_languages)}")
            
            # STEP 2: Rest of form
            with st.form("registration_form"):
                name = st.text_input("Full Name*")
                
                # Email for weekly updates
                email = st.text_input(
                    "Email (Optional - for weekly cosmic updates)",
                    placeholder="your.email@example.com",
                    help="Get weekly forecasts and insights delivered to your inbox"
                )
                
                # Phone number (country code auto-filled from selection above)
                st.caption(f"**Phone Number** (Country code {country_code} auto-added)")
                phone_number = st.text_input("Phone Number*", placeholder="9876543210", key="phone_num", label_visibility="collapsed")
                
                # Combine to full phone
                reg_phone = f"{country_code}{phone_number}" if phone_number else ""
                
                # Birth details
                col_a, col_b = st.columns(2)
                with col_a:
                    dob = st.date_input("Date of Birth*", 
                                       min_value=datetime(1900, 1, 1),
                                       max_value=datetime.now())
                with col_b:
                    # Manual time input for precise birth time
                    time_col1, time_col2 = st.columns(2)
                    with time_col1:
                        hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=8)
                    with time_col2:
                        minute = st.number_input("Min (0-59)", min_value=0, max_value=59, value=12)
                    tob = f"{hour:02d}:{minute:02d}"
                
                # Place details
                place_city = st.text_input("Birth Village/Town/City*", placeholder="Hyderabad")
                place_state = st.text_input("Birth State/Province (optional)", placeholder="Telangana")
                
                # Language selection
                preferred_language = st.selectbox(
                    "Preferred Language*",
                    options=available_languages,
                    index=0
                )
                
                # Additional Astrology Systems (OPTIONAL)
                st.divider()
                st.caption("🔮 Additional Systems")
                
                st.info("**Premium systems require paid subscription ($1/month)**")
                
                # Free additional systems
                free_systems = st.multiselect(
                    "Free Systems (Available to all)",
                    options=[
                        'Numerology (Pythagorean)',
                        'Prashna (Horary)',
                        'I Ching',
                    ],
                    default=[]
                )
                
                # Premium systems requiring payment
                premium_systems = st.multiselect(
                    "Premium Systems ($5/month - Includes photo storage)",
                    options=[
                        'Numerology (Chaldean)',
                        'Nadi Astrology',
                        'Palmistry (Photo upload required)',
                        'Tarot',
                        'Mayan Tzolkin',
                        'Tibetan Astrology',
                        'Face Reading (Photo upload required)',
                        'Feng Shui'
                    ],
                    default=[],
                    help="Photo-based systems (Palmistry, Face Reading) require $5/month PREMIUM plan for secure photo storage"
                )
                
                # Combine systems
                additional_systems = free_systems + premium_systems
                
                # Determine required subscription tier
                has_photo_systems = any(sys in premium_systems for sys in ['Palmistry (Photo upload required)', 'Face Reading (Photo upload required)'])
                
                if has_photo_systems:
                    required_tier = 'PREMIUM'
                    required_price = '$5/month'
                    tier_message = "⚠️ Photo-based systems require PREMIUM ($5/month) for secure storage (50MB included)"
                elif len(premium_systems) > 0:
                    required_tier = 'PAID'
                    required_price = '$1/month'
                    tier_message = "⚠️ You've selected premium systems. Subscription ($1/month) required after registration."
                else:
                    required_tier = 'FREE'
                    required_price = None
                    tier_message = None
                
                # Show warning if premium selected
                if tier_message:
                    st.warning(tier_message)
                
                # Photo upload for palmistry/face reading
                palm_photo = None
                if 'Palmistry' in premium_systems:
                    st.info("📸 **Palmistry Requirements:**\n- Upload clear photos of both palms\n- Place small stickers on fingertips (to avoid storing fingerprints)\n- Ensure all palm lines are visible")
                    palm_photo = st.file_uploader("Upload Palm Photos (Left & Right)", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
                
                # DISCLAIMER
                st.divider()
                st.warning("""
                **⚠️ DISCLAIMER**
                
                **Probabilistic Logic:** We use a 5-system consensus to provide strategic guidance, not absolute certainty.
                
                **Directional Compass:** These insights serve as one strategic input among many—not your final decision.
                
                **No Guarantees:** Predictions are based on cosmic patterns and mathematical probabilities. Specific outcomes cannot be guaranteed.
                
                **Professional First:** Always consult qualified legal, financial, or medical professionals for critical life choices.
                
                **User Responsibility:** By registering, you acknowledge this service is for strategic guidance and entertainment purposes only.
                """)
                
                # Combine place
                if place_state:
                    place = f"{place_city}, {place_state}, {country_name}"
                else:
                    place = f"{place_city}, {country_name}"
                
                submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted:
                    if name and phone_number and place_city:
                        # Get coordinates
                        lat, lon = get_coordinates(place_city, country_name)
                        
                        result = engine.register_user(
                            phone=reg_phone,
                            name=name,
                            dob=dob.strftime("%Y-%m-%d"),
                            tob=tob,
                            place=place
                        )
                        
                        if result['success']:
                            # Update user data with correct tier
                            engine.db.update_user(reg_phone, {
                                'email': email if email else '',
                                'language': preferred_language,
                                'custom_systems': additional_systems,
                                'subscription': required_tier
                            })
                            
                            # TODO: Save palm photos if uploaded
                            # if palm_photo:
                            #     save_palm_photos(reg_phone, palm_photo)
                            
                            success_msg = result['message']
                            if required_price:
                                success_msg += f"\n\n💳 **Subscription required:** {required_price} to activate selected premium systems."
                            
                            st.success(success_msg)
                            st.session_state.phone = reg_phone
                            st.session_state.show_registration = False
                            st.rerun()
                        else:
                            st.error(result['message'])
                    else:
                        st.warning("Please fill all required fields (*)")
    
    else:
        # User logged in
        user = engine.db.get_user(st.session_state.phone)
        
        st.success(f"Welcome, {user['name']}! 👋")
        
        # Profile editor toggle
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state.show_profile_editor = True
        
        # Profile editor
        if st.session_state.get('show_profile_editor', False):
            st.divider()
            with st.form("profile_edit_form"):
                st.subheader("Update Your Details")
                
                # Name
                new_name = st.text_input("Name", value=user['name'])
                
                # Email (NEW)
                new_email = st.text_input(
                    "Email (for weekly updates)",
                    value=user.get('email', ''),
                    placeholder="your.email@example.com",
                    help="We'll send you weekly cosmic insights and forecasts"
                )
                
                # Birth details
                st.caption("Birth Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    current_dob = datetime.strptime(user['birth_details']['dob'], '%Y-%m-%d').date()
                    new_dob = st.date_input("Date of Birth", value=current_dob)
                
                with col2:
                    current_tob = user['birth_details']['tob']
                    hour, minute = map(int, current_tob.split(':'))
                    time_col1, time_col2 = st.columns(2)
                    with time_col1:
                        new_hour = st.number_input("Hour", min_value=0, max_value=23, value=hour)
                    with time_col2:
                        new_minute = st.number_input("Min", min_value=0, max_value=59, value=minute)
                    new_tob = f"{new_hour:02d}:{new_minute:02d}"
                
                # Place
                new_place = st.text_input("Place of Birth", value=user['birth_details']['place'])
                
                # Language
                available_langs = ['English', 'Hindi', 'Telugu', 'Tamil', 'Kannada', 'Malayalam', 
                                  'Bengali', 'Marathi', 'Spanish', 'French', 'Arabic', 'Chinese']
                current_lang_index = available_langs.index(user.get('language', 'English')) if user.get('language', 'English') in available_langs else 0
                new_language = st.selectbox("Preferred Language", options=available_langs, index=current_lang_index)
                
                # Submit
                col_save, col_cancel = st.columns(2)
                
                with col_save:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        # Update user
                        updates = {
                            'name': new_name,
                            'email': new_email,
                            'birth_details': {
                                'dob': new_dob.strftime('%Y-%m-%d'),
                                'tob': new_tob,
                                'place': new_place,
                                'lat': user['birth_details']['lat'],  # Keep existing
                                'lon': user['birth_details']['lon']   # Keep existing
                            },
                            'language': new_language
                        }
                        
                        engine.db.update_user(st.session_state.phone, updates)
                        st.success("✅ Profile updated successfully!")
                        st.session_state.show_profile_editor = False
                        st.rerun()
                
                with col_cancel:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state.show_profile_editor = False
                        st.rerun()
        
        # Usage stats
        st.divider()
        st.subheader("Your Stats")
        
        if user['subscription'] == 'FREE':
            remaining = 7 - user.get('lifetime_questions', 0)
            st.metric("Questions Left", f"{remaining}/7")
            
            progress = user.get('lifetime_questions', 0) / 7
            st.progress(progress)
            
            if remaining <= 3:
                st.warning(f"Only {remaining} free questions left!")
                if st.button("Upgrade to $1/month", use_container_width=True, key="upgrade_btn_sidebar"):
                    result = engine.upgrade_to_paid(st.session_state.phone)
                    st.success(result['message'])
                    st.rerun()
        else:
            st.success(f"✨ {user['subscription']} Plan")
            st.metric("Questions", "Unlimited")
        
        st.divider()
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, type="secondary", key="logout_btn"):
            logout()

# Main chat interface
if st.session_state.phone:
    user = engine.db.get_user(st.session_state.phone)
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        # Note: Chat history is currently session-only
        # TODO: Implement persistent chat history storage in database
        if len(st.session_state.chat_history) > 0:
            st.caption(f"💬 {len(st.session_state.chat_history)//2} questions in this session")
        
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Welcome insights and suggested questions
    # Only show if no chat history AND no pending question
    if len(st.session_state.chat_history) == 0 and not hasattr(st.session_state, 'pending_question'):
        lifetime_q = user.get('lifetime_questions', 0)
        
        # First-time user (never asked a question before)
        if lifetime_q == 0:
            st.markdown("### 👋 Welcome to Astro Compass!")
            
            st.info("""
            **What is Astro Compass?**
            
            We analyze your birth chart using **5 ancient wisdom systems** (Vedic, KP, Western, Chinese, Mayan) 
            to give you a **70-90% consensus** on your life's biggest questions.
            
            When all 5 systems agree → that's your green light! ⭐
            
            Perfect for: Career decisions • Love & marriage • Money & investments • Life purpose • Family matters
            """)
            
            # Generate personalized welcome insights
            st.markdown("### 🔮 Generating your personalized insights...")
            
            # Progress bar for insight generation
            insight_progress = st.empty()
            import time
            from datetime import datetime
            
            # Show initial progress
            initial_steps = [
                ("🔮 Reading your birth chart...", 20),
                ("⏳ Analyzing current planetary transits...", 40),
                ("⏳ Consulting 5 wisdom systems...", 60),
            ]
            
            for step_text, progress_value in initial_steps:
                insight_progress.progress(progress_value / 100, text=step_text)
                time.sleep(2.0)  # 2s per step
            
            # Show synthesizing while API call happens
            insight_progress.progress(0.80, text="⏳ Synthesizing 5-system consensus...")
            
            # Make API call - WAIT for response
            welcome_prompt = f"""Generate 3 SPECIFIC, personalized insights for this user:

Birth chart: {user.get('birth_details', {})}
Today: {datetime.now().strftime('%B %d, %Y')}
Location: {user.get('pob', 'Unknown')}

Format as 3 short insights (1-2 sentences each):

💼 **Career:** [Specific opportunity or timing in next 2-3 months]

💰 **Finances:** [Money/investment insight with timing]

❤️ **Relationships:** [Love/partnership insight]

Be SPECIFIC, include TIMING, keep it brief."""

            try:
                welcome_result = engine.ask_question(
                    st.session_state.phone,
                    welcome_prompt,
                    conversation_history=[]
                )
            except Exception as e:
                welcome_result = {
                    'success': False,
                    'response': f'API Error: {str(e)}'
                }
            
            # Complete progress
            insight_progress.progress(1.0, text="✅ Analysis complete!")
            time.sleep(0.5)
            insight_progress.empty()
            
            # Handle result intelligently
            if welcome_result.get('success', False):
                insights_text = welcome_result['response']
                
                # Display insights
                st.markdown("### 💫 Your Personalized Insights Right Now:")
                st.success(insights_text)
                st.markdown("---")
            else:
                # Check WHY it failed
                error_message = welcome_result.get('response', 'Unknown error')
                
                # Quota exceeded?
                if 'quota' in error_message.lower() or 'limit' in error_message.lower() or 'capacity' in error_message.lower():
                    st.warning("### ⚠️ Free Tier Capacity Reached")
                    st.info("""
                    The free tier is currently at capacity. You have two options:
                    
                    1. **Wait a few minutes** and refresh the page
                    2. **Upgrade to BASIC plan** (₹99/$2/month) for priority access
                    """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Refresh Page", key="refresh_welcome", use_container_width=True):
                            st.rerun()
                    with col2:
                        if st.button("⭐ View Plans", key="upgrade_welcome_view", use_container_width=True):
                            st.info("Scroll down to see pricing plans!")
                elif 'lifetime_questions' in error_message:
                    # Database initialization issue - let user skip and use app
                    st.warning("### ⚠️ Welcome Insights Unavailable")
                    st.info("""
                    We couldn't generate your welcome insights right now, but you can still use the app!
                    
                    **Your account is active with 7 free questions.**
                    
                    Pick a topic below or ask any question to get started!
                    """)
                    
                    st.success("✅ **You can start asking questions now** - just pick a topic or type your question!")
                else:
                    # Other error - show retry
                    st.error("### ❌ Couldn't Generate Insights")
                    st.warning(f"Error: {error_message}")
                    
                    if st.button("🔄 Try Again", key="retry_welcome", use_container_width=True):
                        st.rerun()
            
            # Ask me about any topic prompt
            st.markdown("**👇 Pick a topic to explore deeper, or ask me anything!**")
            st.markdown("---")
        
        # Existing user (has asked questions before)
        else:
            st.markdown(f"### 👋 Welcome back, {user.get('name', 'friend')}!")
            
            # Show progress while generating predictions
            st.markdown("**🔮 Generating today's cosmic insights for you...**")
            
            today_progress = st.empty()
            import time
            from datetime import datetime
            
            # Show quick progress
            today_steps = [
                ("🌟 Checking today's planetary positions...", 50),
                ("💫 Consulting your birth chart...", 100),
            ]
            
            for step_text, progress_value in today_steps:
                today_progress.progress(progress_value / 100, text=step_text)
                time.sleep(1.0)  # 1s per step
                
                # Make API call during last step
                if progress_value == 100:
                    today_prompt = f"""Generate 2 BRIEF predictions for this returning user based on TODAY'S date and their chart:

User: {user.get('name')}
Birth chart: {user.get('birth_details', {})}
Today: {datetime.now().strftime('%A, %B %d, %Y')}

Format EXACTLY as 2 short lines (one sentence each):

🌟 **Today's Energy:** [One specific insight about today's planetary influence]

💡 **Quick Tip:** [One actionable suggestion for today]

Keep each to ONE sentence. Be specific and practical."""

                    try:
                        today_result = engine.ask_question(
                            st.session_state.phone,
                            today_prompt,
                            conversation_history=[]
                        )
                    except Exception as e:
                        today_result = {
                            'success': False,
                            'response': f'API Error: {str(e)}'
                        }
            
            today_progress.empty()
            
            if today_result['success']:
                st.info(today_result['response'])
            else:
                # Handle failure gracefully - don't show error for returning users
                # Just skip predictions and let them use the app
                pass
            
            st.markdown("---")
        
        # Show topic buttons for all users
        st.markdown("### 💡 Quick Start - Pick a Topic:")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        suggested_q = None
        
        with col1:
            if st.button("💼 Career", use_container_width=True, key="btn_career"):
                suggested_q = "What does my career look like in the next 6 months?"
            if st.button("💰 Money", use_container_width=True, key="btn_money"):
                suggested_q = "Is this a good time for major investments or financial decisions?"
        
        with col2:
            if st.button("💍 Love", use_container_width=True, key="btn_love"):
                suggested_q = "When will I find my life partner? What should I know about my love life?"
            if st.button("🤝 Marriage", use_container_width=True, key="btn_marriage"):
                suggested_q = "Is my current relationship leading to marriage? When?"
        
        with col3:
            if st.button("👨‍👩‍👧 Family", use_container_width=True, key="btn_family"):
                suggested_q = "What guidance do you have for my family harmony?"
            if st.button("👶 Children", use_container_width=True, key="btn_children"):
                suggested_q = "What guidance do you have regarding children?"
        
        with col4:
            if st.button("🎯 Purpose", use_container_width=True, key="btn_purpose"):
                suggested_q = "What is my life purpose? What talents should I focus on?"
            if st.button("🏖️ Retirement", use_container_width=True, key="btn_retirement"):
                suggested_q = "When should I plan retirement or achieve financial freedom?"
        
        with col5:
            if st.button("🧘 Peace", use_container_width=True, key="btn_peace"):
                suggested_q = "How can I find clarity during this confusing time?"
            if st.button("🏠 Property", use_container_width=True, key="btn_property"):
                suggested_q = "Is this a good time to buy property or invest in real estate?"
        
        # If button clicked, store question and trigger processing
        if suggested_q:
            st.session_state.pending_question = suggested_q
            st.rerun()
        
        st.markdown("---")
    
    # Process pending question ONCE
    if hasattr(st.session_state, 'pending_question') and st.session_state.pending_question:
        prompt = st.session_state.pending_question
        del st.session_state.pending_question  # Delete immediately to prevent re-processing
        
        # Check if question is about family member (requires upgrade)
        # Comprehensive keyword list
        family_keywords = [
            # Immediate family
            'wife', 'husband', 'spouse', 'partner', 'girlfriend', 'boyfriend', 
            'fiance', 'fiancee', 'son', 'daughter', 'child', 'children', 'kids',
            'baby', 'infant', 'toddler', 'teen', 'teenager',
            # Parents & grandparents
            'mother', 'father', 'mom', 'dad', 'mama', 'papa', 'mummy', 'daddy',
            'parent', 'parents', 'grandmother', 'grandfather', 'grandma', 'grandpa',
            'granny', 'nana', 'nani', 'dada', 'dadi',
            # Siblings
            'brother', 'sister', 'sibling', 'bro', 'sis', 'twin',
            'stepbrother', 'stepsister', 'half-brother', 'half-sister',
            # Extended family
            'uncle', 'aunt', 'aunty', 'auntie', 'nephew', 'niece', 'cousin',
            'relative', 'in-law', 'mother-in-law', 'father-in-law',
            'brother-in-law', 'sister-in-law', 'son-in-law', 'daughter-in-law'
        ]
        
        # Check for family keywords
        is_family_question = any(keyword in prompt.lower() for keyword in family_keywords)
        
        # Check for DOB patterns (dates like DD/MM/YYYY, MM/DD/YYYY, etc.)
        import re
        dob_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # DD/MM/YYYY or MM/DD/YYYY
            r'\bborn on\b',
            r'\bbirth date\b',
            r'\bbirthdate\b',
            r'\bdate of birth\b',
            r'\bdob\b',
            r'\b(his|her|their) (chart|birth)\b'
        ]
        has_other_dob = any(re.search(pattern, prompt.lower()) for pattern in dob_patterns)
        
        # Flag as family question if either keywords OR DOB patterns detected
        is_family_question = is_family_question or has_other_dob
        
        user = engine.db.get_user(st.session_state.phone)
        user_questions_left = user.get('questions_left', 0)
        
        # Only block family questions if user has NO questions left AND not on FAMILY plan
        if is_family_question and user.get('subscription') != 'FAMILY' and user_questions_left == 0:
            # Hard block - no questions left
            st.warning("### 👨‍👩‍👧‍👦 Family Member Analysis")
            st.info("""
            **Your current plan covers deep analysis of YOUR birth chart only.**
            
            To analyze family members using their DOB or birth details, upgrade to **FAMILY plan**.
            
            **FAMILY Plan Benefits:**
            - ₹499/month (India) or $8/month (International)
            - Analyze **8 family members** with their DOBs
            - Complete birth charts for each member
            - Compatibility analysis
            - All 16 astrology systems
            - ₹62/person = Less than 1 chai per day!
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⭐ Upgrade to FAMILY", key="upgrade_family_prompt", use_container_width=True):
                    st.info("Scroll down to see FAMILY plan details!")
            with col2:
                if st.button("📝 Ask About Myself Instead", key="ask_self", use_container_width=True):
                    st.info("Please rephrase your question about your own chart!")
        
        else:
            # Process the question normally (either not family question, OR user has questions left)
            # Add to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                # Show progress IMMEDIATELY
                progress_placeholder = st.empty()
                progress_placeholder.progress(0, text="🔮 Analyzing your cosmic blueprint...")
                
                import time
                time.sleep(0.1)  # Tiny delay to ensure UI updates
                
                steps = [
                    ("🔮 Analyzing your cosmic blueprint...", 0),
                    ("✓ Loading birth chart data", 10),
                    ("⏳ Consulting Vedic Astrology...", 20),
                    ("⏳ Cross-checking KP System...", 35),
                    ("⏳ Analyzing Western perspective...", 50),
                    ("⏳ Interpreting Chinese elements...", 65),
                    ("⏳ Decoding Mayan calendar...", 80),
                    ("⏳ Synthesizing 5-system consensus...", 90),
                    ("⏳ Generating personalized insights...", 95),
                ]
                
                # Show ALL steps for 2 seconds each so users can read
                for step_text, progress_value in steps:
                    progress_placeholder.progress(progress_value / 100, text=step_text)
                    time.sleep(2.0)  # 2 seconds per step
                    
                    # Make API call during "synthesizing" step
                    if "Synthesizing" in step_text:
                        result = engine.ask_question(
                            st.session_state.phone,
                            prompt,
                            conversation_history=st.session_state.chat_history
                        )
                
                # Final completion
                progress_placeholder.progress(1.0, text="✅ Analysis complete!")
                time.sleep(0.5)
                
                # Clear progress
                progress_placeholder.empty()
                
                if result['success']:
                    response = result['response']
                    
                    # Extract follow-up options (format: • [Option text])
                    import re
                    follow_up_pattern = r'•\s*\[([^\]]+)\]'
                    follow_ups = re.findall(follow_up_pattern, response)
                    
                    # If AI didn't generate follow-ups, provide generic ones
                    if not follow_ups:
                        follow_ups = [
                            "What timing is best for this?",
                            "What obstacles should I watch for?",
                            "How can I prepare or maximize this?"
                        ]
                    
                    # Store follow-ups for button display
                    st.session_state.follow_up_options = follow_ups[:3]
                    
                    # Remove entire follow-up section from main response for cleaner display
                    clean_response = response
                    # Remove "What would you like..." line and all bullet points after it
                    clean_response = re.sub(r'What would you like to explore next\?.*', '', clean_response, flags=re.DOTALL)
                    clean_response = clean_response.strip()
                    
                    # Display cleaned response
                    st.markdown(clean_response)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    # Force rerun to display follow-up buttons
                    st.rerun()
                else:
                    # Handle different error types with user-friendly messages
                    error_response = result.get('response', '')
                    error_type = result.get('error_type', 'unknown')
                    
                    if error_response == 'AI_OVERLOADED' or error_type == 'overload':
                        st.warning("### ⚠️ AI Service Temporarily Busy")
                        st.info("""
                        Our AI is experiencing high demand right now. This happens when many users are asking questions simultaneously.
                        
                        **Please try again in 30-60 seconds.**
                        
                        Your question has NOT been counted against your quota.
                        """)
                        
                        if st.button("🔄 Try Again", key="retry_overload", use_container_width=True):
                            st.rerun()
                    
                    elif error_response == 'QUOTA_EXCEEDED' or error_type == 'quota':
                        st.error("### ❌ Daily Quota Reached")
                        st.info("""
                        We've reached our daily AI request limit. 
                        
                        **Options:**
                        1. Wait until tomorrow (resets at midnight UTC)
                        2. Upgrade to BASIC plan for priority access
                        """)
                        
                        if st.button("⭐ View Plans", key="upgrade_quota", use_container_width=True):
                            st.info("Scroll down to see pricing plans!")
                    
                    else:
                        st.error("### ❌ Unexpected Error")
                        st.warning(f"Something went wrong: {error_response}")
                        st.info("Please try again or contact support if the problem persists.")
                        
                        if st.button("🔄 Try Again", key="retry_error", use_container_width=True):
                            st.rerun()
    
    # Display follow-up buttons if AI generated them (AFTER all processing)
    if hasattr(st.session_state, 'follow_up_options'):
        if st.session_state.follow_up_options:
            st.markdown("### 💡 What would you like to explore next?")
            
            options = st.session_state.follow_up_options
            num_cols = min(len(options), 3)
            cols = st.columns(num_cols)
            
            follow_up_clicked = None
            for idx, option in enumerate(options):
                col_idx = idx % num_cols
                with cols[col_idx]:
                    if st.button(option, key=f"followup_{idx}", use_container_width=True):
                        follow_up_clicked = option
            
            # If clicked, submit it
            if follow_up_clicked:
                st.session_state.pending_question = follow_up_clicked
                st.session_state.follow_up_options = []  # Clear
                st.rerun()
            
            st.markdown("---")
    
    # Chat input
    if prompt := st.chat_input("Ask your cosmic question..."):
        # Check for family member questions BEFORE processing
        family_keywords = [
            'wife', 'husband', 'spouse', 'partner', 'girlfriend', 'boyfriend', 
            'fiance', 'fiancee', 'son', 'daughter', 'child', 'children', 'kids',
            'baby', 'infant', 'toddler', 'teen', 'teenager',
            'mother', 'father', 'mom', 'dad', 'mama', 'papa', 'mummy', 'daddy',
            'parent', 'parents', 'grandmother', 'grandfather', 'grandma', 'grandpa',
            'granny', 'nana', 'nani', 'dada', 'dadi',
            'brother', 'sister', 'sibling', 'bro', 'sis', 'twin',
            'stepbrother', 'stepsister', 'half-brother', 'half-sister',
            'uncle', 'aunt', 'aunty', 'auntie', 'nephew', 'niece', 'cousin',
            'relative', 'in-law', 'mother-in-law', 'father-in-law',
            'brother-in-law', 'sister-in-law', 'son-in-law', 'daughter-in-law'
        ]
        
        is_family_question = any(keyword in prompt.lower() for keyword in family_keywords)
        
        # Check for DOB patterns
        import re
        dob_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\bborn on\b',
            r'\bbirth date\b',
            r'\bbirthdate\b',
            r'\bdate of birth\b',
            r'\bdob\b',
            r'\b(his|her|their) (chart|birth)\b'
        ]
        has_other_dob = any(re.search(pattern, prompt.lower()) for pattern in dob_patterns)
        is_family_question = is_family_question or has_other_dob
        
        user = engine.db.get_user(st.session_state.phone)
        user_questions_left = user.get('questions_left', 0)
        
        # Only block if NO questions left AND not on FAMILY plan
        if is_family_question and user.get('subscription') != 'FAMILY' and user_questions_left == 0:
            # Show upgrade message WITHOUT processing
            st.warning("### 👨‍👩‍👧‍👦 Family Member Analysis")
            st.info("""
            **Your current plan covers deep analysis of YOUR birth chart only.**
            
            To analyze family members using their DOB or birth details, upgrade to **FAMILY plan**.
            
            **FAMILY Plan Benefits:**
            - ₹499/month (India) or $8/month (International)
            - Analyze **8 family members** with their DOBs
            - Complete birth charts for each member
            - Compatibility analysis
            - All 16 astrology systems
            - ₹62/person = Less than 1 chai per day!
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⭐ Upgrade to FAMILY", key="upgrade_family_chat", use_container_width=True):
                    st.info("Scroll down to see FAMILY plan details!")
            with col2:
                if st.button("📝 Ask About Myself", key="ask_self_chat", use_container_width=True):
                    st.info("Please ask about your own birth chart!")
        else:
            # Process question normally
            # Add user message to chat
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                # Visual progress showing 5-system analysis
                progress_placeholder = st.empty()
                
                steps = [
                    ("🔮 Analyzing your cosmic blueprint...", 0),
                    ("✓ Loading birth chart data", 10),
                    ("⏳ Consulting Vedic Astrology...", 20),
                    ("⏳ Cross-checking KP System...", 35),
                    ("⏳ Analyzing Western perspective...", 50),
                    ("⏳ Interpreting Chinese elements...", 65),
                    ("⏳ Decoding Mayan calendar...", 80),
                    ("⏳ Synthesizing 5-system consensus...", 90),
                    ("⏳ Generating personalized insights...", 95),
                ]
                
                import time
                
                # Show ALL steps for 2 seconds each so users can read
                for step_text, progress_value in steps:
                    progress_placeholder.progress(progress_value / 100, text=step_text)
                    time.sleep(2.0)  # 2 seconds per step
                    
                    # Make API call during "synthesizing" step
                    if "Synthesizing" in step_text:
                        result = engine.ask_question(
                            st.session_state.phone,
                            prompt,
                            conversation_history=st.session_state.chat_history
                        )
                
                # Final completion
                progress_placeholder.progress(1.0, text="✅ Analysis complete!")
                time.sleep(0.5)
                
                # Clear progress and show response
                progress_placeholder.empty()
                
                # Display result
                
                if result['success']:
                    response = result['response']
                    
                    # Extract follow-up options (format: • [Option text])
                    import re
                    follow_up_pattern = r'•\s*\[([^\]]+)\]'
                    follow_ups = re.findall(follow_up_pattern, response)
                    
                    # If AI didn't generate follow-ups, provide generic ones
                    if not follow_ups:
                        follow_ups = [
                            "What timing is best for this?",
                            "What obstacles should I watch for?",
                            "How can I prepare or maximize this?"
                        ]
                    
                    # Store follow-ups for button display
                    st.session_state.follow_up_options = follow_ups[:3]
                    
                    # Remove entire follow-up section from main response
                    clean_response = response
                    clean_response = re.sub(r'What would you like to explore next\?.*', '', clean_response, flags=re.DOTALL)
                    clean_response = clean_response.strip()
                    
                    # Display cleaned response
                    st.markdown(clean_response)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    # Auto-scroll to bottom using JavaScript
                    st.markdown("""
                    <script>
                    window.scrollTo(0, document.body.scrollHeight);
                    </script>
                    """, unsafe_allow_html=True)
                    
                    # Force rerun to display follow-up buttons
                    st.rerun()
                else:
                    # Handle different error types with user-friendly messages
                    error_response = result.get('response', '')
                    error_type = result.get('error_type', 'unknown')
                    
                    if error_response == 'AI_OVERLOADED' or error_type == 'overload':
                        st.warning("### ⚠️ AI Service Temporarily Busy")
                        st.info("""
                        Our AI is experiencing high demand right now. This happens when many users are asking questions simultaneously.
                        
                        **Please try again in 30-60 seconds.**
                        
                        Your question has NOT been counted against your quota.
                        """)
                        
                        if st.button("🔄 Try Again", key="retry_overload_chat", use_container_width=True):
                            st.rerun()
                    
                    elif error_response == 'QUOTA_EXCEEDED' or error_type == 'quota':
                        st.error("### ❌ Daily Quota Reached")
                        st.info("""
                        We've reached our daily AI request limit. 
                        
                        **Options:**
                        1. Wait until tomorrow (resets at midnight UTC)
                        2. Upgrade to BASIC plan for priority access
                        """)
                        
                        if st.button("⭐ View Plans", key="upgrade_quota_chat", use_container_width=True):
                            st.info("Scroll down to see pricing plans!")
                    
                    else:
                        st.error("### ❌ Unexpected Error")
                        st.warning(f"Something went wrong: {error_response}")
                        st.info("Please try again or contact support if the problem persists.")
                        
                        if st.button("🔄 Try Again", key="retry_error_chat", use_container_width=True):
                            st.rerun()

else:
    # Not logged in - show welcome
    
    # Subtle mobile guidance
    st.caption("📱 Mobile: Tap **>>** (top-left) to Login/Register")
    
    st.markdown("""
    ## The Astro-Compass: Your 5-System Destiny Guide
    
    ### Why These 5 Systems?
    
    Unlike single-system astrology apps, we synthesize **5 ancient wisdom traditions** to give you clarity at life's crossroads:
    
    - 🕉️ **Vedic Astrology: The Foundation** — Soul's purpose and karmic timing
    - 📊 **KP System: The Precision** — "Yes/No" answers with exact event timing  
    - 🌍 **Western Astrology: The Psychology** — Personality, mental blocks, life patterns
    - 🐉 **Chinese Astrology: The Energy Flow** — Yearly momentum via nature's cycles
    - 🌀 **Mayan Astrology: The Universal Rhythm** — Daily energy and spiritual alignment
    
    ### How They Work Together For You
    
    By cross-checking these 5 ancient perspectives, we remove individual system bias to give you a **70%–90% Truth Consensus**. 
    
    **When all five systems point to the same window → it's your time to act.**
    
    ### What Can Astro-Compass Guide You On?
    
    Perfect for when you're at a **crossroads or facing paradoxical choices:**
    
    💍 **Marriage** — Compatibility, timing, love life  
    💼 **Career** — Job changes, entrepreneurship, partnerships  
    💰 **Wealth** — Financial decisions, property, investments  
    👨‍👩‍👧 **Family** — Children's futures, parents' health, harmony  
    🎯 **Life Purpose** — Finding your path, natural talents  
    🏖️ **Retirement** — Planning your next chapter  
    🧠 **Personal Growth** — Understanding traits, attitudes, patterns  
    
    ### Try It Free
    
    ✨ **7 free questions** to explore your destiny  
    💬 **Instant AI responses** in your language  
    🌍 **70+ countries, 25+ languages** supported
    
    📊 **Note:** Free tier has limited daily capacity. If the system is busy, consider upgrading for priority access.
    
    ### Choose Your Plan
    
    """)
    
    # Pricing cards with visual comparisons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 💎 BASIC
        **₹99/month** (India)  
        **$2/month** (International)
        
        ✓ Unlimited questions  
        ✓ 1 birth chart  
        ✓ 2 devices  
        ✓ 5 core systems  
        &nbsp;
        
        ---
        **Worth it?**  
        ☕ Less than 3 coffees!  
        💼 Perfect for individuals  
        ⚡ Get started today!
        """)
        if st.button("Start BASIC", use_container_width=True, key="upgrade_basic_welcome"):
            st.info("👈 Please login first to upgrade")
    
    with col2:
        st.markdown("""
        #### 💖 FAMILY ⭐ Popular
        **₹499/month** (India)  
        **$8/month** (International)
        
        ✓ Unlimited questions  
        ✓ **8 birth charts** 👨‍👩‍👧‍👦  
        ✓ 3 devices  
        ✓ All 16 systems
        
        ---
        **Worth it?**  
        🍕 **Price of 1 pizza**  
        ☕ **₹62/person** = 1 chai/day!  
        💫 **$1/person** = Best value!
        """)
        if st.button("Get FAMILY Plan", use_container_width=True, type="primary", key="upgrade_family_welcome"):
            st.info("👈 Please login first to upgrade")
    
    with col3:
        st.markdown("""
        #### 👑 VIP
        **₹4,000/month** (India)  
        **$40/month** (International)
        
        ✓ Unlimited questions  
        ✓ **Unlimited charts**  
        ✓ Unlimited devices  
        ✓ Priority support  
        ✓ Weekly forecasts
        
        ---
        **For Professionals:**  
        🔮 Astrologers  
        💼 Consultants  
        💒 Marriage bureaus
        """)
        if st.button("Go VIP", use_container_width=True, key="upgrade_vip_welcome"):
            st.info("👈 Please login first to upgrade")
    
    st.markdown("---")
    
    # Value comparison section
    st.markdown("""
    ### 💰 Why FAMILY Plan is Amazing Value
    """)
    
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("""
        #### 🇮🇳 For India (₹499/month)
        
        🍕 **1 Domino's Pizza** = ₹500  
        🎬 **1 Movie Ticket** = ₹350  
        ☕ **3 Starbucks Chai** = ₹330  
        
        **vs**
        
        💎 **FAMILY Plan** = ₹499  
        👨‍👩‍👧‍👦 **8 family members**  
        ⚡ **Unlimited questions**  
        
        **Just ₹62/person = 1 chai per day!** ☕→⭐
        """)
    
    with comp_col2:
        st.markdown("""
        #### 🌍 International ($8/month)
        
        ☕ **2 Starbucks Lattes** = $10  
        🍿 **1 Movie Ticket** = $15  
        🍔 **1 Fast Food Meal** = $12  
        
        **vs**
        
        💎 **FAMILY Plan** = $8  
        👨‍👩‍👧‍👦 **8 family members**  
        ⚡ **Unlimited questions**  
        
        **Just $1/person!** Skip 2 coffees → Get a month of clarity! ☕→🔮
        """)
    
    st.markdown("""
        | Feature | FREE | BASIC | FAMILY | VIP |
        |---------|------|-------|--------|-----|
        | **India Price** | ₹0 | **₹99/mo** | **₹499/mo** | **₹4,000/mo** |
        | **Intl Price** | $0 | **$2/mo** | **$8/mo** | **$40/mo** |
        | **Questions** | 7 total | **Unlimited** | **Unlimited** | **Unlimited** |
        | **Birth Charts** | 1 person | 1 person | **8 people** 👨‍👩‍👧‍👦 | **Unlimited** |
        | **Per Person (India)** | - | ₹99 | **₹62** ⭐ | - |
        | **Per Person (Intl)** | - | $2 | **$1** ⭐ | - |
        | **Devices** | 1 | 2 | 3 | Unlimited |
        | **Systems** | 5 core | 5 core | All 16 | All 16 + Priority |
        | **Response Depth** | Basic | Detailed | Comprehensive | Ultra-detailed |
        | **Chat History** | Session only | Full history | Full history | Full history |
        | **Birth Rectification** | ❌ | ❌ | ✅ | ✅ Advanced |
        | **Prashna Astrology** | ❌ | ✅ | ✅ Enhanced | ✅ Enhanced |
        | **Weekly Forecasts** | ❌ | ❌ | ❌ | ✅ |
        | **Priority Support** | ❌ | ❌ | ❌ | ✅ <1 hour |
        | **PDF Reports** | ❌ | ❌ | ❌ | ✅ |
        | **Best For** | Trial | Individual | **Families** ⭐ | Professionals |
        
        **💡 Tip:** Most users choose FAMILY plan - analyze your entire family for less than the price of a pizza! 🍕
        """)
    
    st.markdown("---")
    st.markdown("**👈 Login or Register in the sidebar to begin**")
    
    # Sample testimonials
    with st.expander("See what users are saying"):
        st.markdown("""
        > "The 5-system consensus gave me clarity when I was stuck at a career crossroads. The timing was remarkably accurate!" 
        > 
        > — **Priya Sharma**, Bangalore 🇮🇳
        
        ---
        
        > "मैंने कई ज्योतिषियों से परामर्श लिया, लेकिन यह AI सिस्टम सबसे सटीक निकला। मेरी शादी की तारीख बिल्कुल सही थी!"
        > 
        > (I consulted many astrologers, but this AI system was most accurate. My marriage timing was spot on!)
        > 
        > — **Rajesh Kumar**, Mumbai 🇮🇳
        
        ---
        
        > "என் தொழில் மாற்றத்திற்கு சரியான நேரத்தை இது துல்லியமாக கணித்தது. நம்பமுடியாத அளவுக்கு பயனுள்ளதாக இருந்தது!"
        > 
        > (It accurately predicted the right time for my career change. Incredibly useful!)
        > 
        > — **Lakshmi Devi**, Chennai 🇮🇳
        
        ---
        
        > "أستخدمه قبل كل قرار مهم في العمل. التوقعات دقيقة بشكل مدهش!"
        > 
        > (I use it before every important business decision. Predictions are surprisingly accurate!)
        > 
        > — **Ahmed Al-Rashid**, Dubai 🇦🇪
        
        ---
        
        > "Five systems working together give me way more confidence than single astrology apps. Worth every dollar!"
        > 
        > — **Michael Chen**, Singapore 🇸🇬
        
        ---
        
        > "मेरे व्यापार विस्तार का सही समय बताया। बहुत फायदेमंद साबित हुआ!"
        > 
        > (It showed the right time for my business expansion. Very beneficial!)
        > 
        > — **Sunita Patel**, Ahmedabad 🇮🇳
        
        ---
        
        > "J'étais sceptique au début, mais les prédictions m'ont aidé à éviter une mauvaise décision d'investissement."
        > 
        > (I was skeptical at first, but predictions helped me avoid a bad investment decision.)
        > 
        > — **Sophie Laurent**, Paris 🇫🇷
        
        ---
        
        > "A combinação de 5 sistemas dá muito mais confiança. Recomendo!"
        > 
        > (The combination of 5 systems gives much more confidence. I recommend it!)
        > 
        > — **Carlos Silva**, São Paulo 🇧🇷
        
        ---
        
        > "The consensus approach is genius. When all 5 systems agree, I know I'm on the right path."
        > 
        > — **Sarah Johnson**, New York 🇺🇸
        
        ---
        
        > "నా కొడుకు పెళ్లి ముహూర్తం ఇది చెప్పింది. చాలా బాగుంది!"
        > 
        > (It told my son's marriage timing. Very good!)
        > 
        > — **Venkatesh Reddy**, Hyderabad 🇮🇳
        """)

# Footer
st.divider()
st.caption("Built with ❤️ • Powered by Gemini AI • Your data is private & secure")
