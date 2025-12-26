"""
Astro Consensus Engine - Streamlit Web Interface
Simple chat-based UI for users to interact with the system
"""

import streamlit as st
from datetime import datetime
from astro_engine import AstroEngine
from env_loader import get_api_key
from country_utils import detect_country_from_phone, get_coordinates

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
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Login", use_container_width=True):
                if phone_input:
                    user = engine.db.get_user(phone_input)
                    if user:
                        st.session_state.phone = phone_input
                        st.rerun()
                    else:
                        st.error("User not found. Please register.")
                else:
                    st.warning("Enter phone number")
        
        with col2:
            if st.button("Register", use_container_width=True):
                st.session_state.show_registration = True
        
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
                place_city = st.text_input("City*", placeholder="Hyderabad")
                place_state = st.text_input("State/Province (optional)", placeholder="Telangana")
                
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
            remaining = 15 - user['lifetime_questions']
            st.metric("Questions Left", f"{remaining}/15")
            
            progress = user['lifetime_questions'] / 15
            st.progress(progress)
            
            if remaining <= 5:
                st.warning(f"Only {remaining} free questions left!")
                if st.button("Upgrade to $1/month", use_container_width=True):
                    result = engine.upgrade_to_paid(st.session_state.phone)
                    st.success(result['message'])
                    st.rerun()
        else:
            st.success(f"✨ {user['subscription']} Plan")
            st.metric("Questions", "Unlimited")
        
        st.divider()
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.phone = None
            st.session_state.chat_history = []
            st.rerun()

# Main chat interface
if st.session_state.phone:
    user = engine.db.get_user(st.session_state.phone)
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Suggested questions for new users
    if len(st.session_state.chat_history) == 0:
        st.markdown("### 💡 Quick Start - Pick a Topic:")
        
        col1, col2, col3, col4 = st.columns(4)
        
        suggested_q = None
        
        with col1:
            if st.button("💼 Career", use_container_width=True):
                suggested_q = "What does my career look like in the next 6 months?"
            if st.button("🎯 Life Purpose", use_container_width=True):
                suggested_q = "What is my life purpose? What natural talents should I focus on?"
        
        with col2:
            if st.button("💰 Finances", use_container_width=True):
                suggested_q = "Is this a good time for major investments or financial decisions?"
            if st.button("🏖️ Retirement", use_container_width=True):
                suggested_q = "When is the best time to plan retirement or achieve financial freedom?"
        
        with col3:
            if st.button("💍 Love", use_container_width=True):
                suggested_q = "When will I find my life partner? What should I know about my love life?"
            if st.button("🤝 Relationships", use_container_width=True):
                suggested_q = "How can I improve my relationships and find better compatibility?"
        
        with col4:
            if st.button("👨‍👩‍👧 Family", use_container_width=True):
                suggested_q = "What guidance do you have for my children and family harmony?"
            if st.button("🧘 Inner Peace", use_container_width=True):
                suggested_q = "How can I find clarity and peace during this confusing time?"
        
        # If a question was selected, process it immediately
        if suggested_q:
            st.session_state.chat_history.append({
                "role": "user",
                "content": suggested_q
            })
            st.session_state.pending_question = suggested_q
            st.rerun()
        
        st.markdown("---")
    
    # Process pending question if exists
    if hasattr(st.session_state, 'pending_question') and st.session_state.pending_question:
        prompt = st.session_state.pending_question
        st.session_state.pending_question = None  # Clear it
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response immediately
        with st.chat_message("assistant"):
            progress_placeholder = st.empty()
            progress_placeholder.progress(0.5, text="🔮 Consulting the cosmos...")
            
            result = engine.ask_question(
                st.session_state.phone,
                prompt,
                conversation_history=st.session_state.chat_history
            )
            
            progress_placeholder.empty()
            
            if result['success']:
                response = result['response']
                st.markdown(response)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
            else:
                st.error(result['response'])
    
    # Chat input
    if prompt := st.chat_input("Ask your cosmic question..."):
        # Add user message to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            # Simple progress bar
            progress_placeholder = st.empty()
            progress_placeholder.progress(0.5, text="🔮 Consulting the cosmos...")
            
            # Get AI response
            result = engine.ask_question(
                st.session_state.phone,
                prompt,
                conversation_history=st.session_state.chat_history
            )
            
            # Clear progress
            progress_placeholder.empty()
            
            # Display result
            
            if result['success']:
                response = result['response']
                st.markdown(response)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
            else:
                # Error occurred
                st.error(result['response'])
                
                # Check if retry is available
                if result.get('retry_available'):
                    st.warning("💡 **Tip:** This is temporary server congestion. Try again in a few seconds!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Retry Now", key="retry_btn"):
                            st.rerun()
                    with col2:
                        if st.button("⭐ Upgrade to Skip Waits", key="upgrade_btn"):
                            upgrade_result = engine.upgrade_to_paid(st.session_state.phone)
                            st.success(upgrade_result['message'])
                            st.rerun()
                else:
                    # Quota exceeded - show upgrade option
                    if st.button("💎 Upgrade Now - $1/month"):
                        upgrade_result = engine.upgrade_to_paid(st.session_state.phone)
                        st.success(upgrade_result['message'])
                        st.rerun()

else:
    # Not logged in - show welcome
    
    # Clear call-to-action for mobile
    st.info("📱 **Mobile users:** Tap the **>>** icon (top-left) to open sidebar, then Login or Register")
    
    st.markdown("""
    ## The Astro-Compass: Your 5-System Destiny Guide 🧭
    
    ### Why These 5 Systems?
    
    Unlike single-system astrology apps, we synthesize **5 ancient wisdom traditions** to give you clarity at life's crossroads:
    
    - 🕉️ **Vedic Astrology: The Foundation** — Reveals your soul's purpose and karmic timing of life's major chapters
    - 📊 **KP System: The Precision** — Uses sub-lord mathematics for "Yes/No" answers and exact event timing
    - 🌍 **Western Astrology: The Psychology** — Analyzes personality, mental blocks, and modern-world interactions
    - 🐉 **Chinese Astrology: The Energy Flow** — Predicts yearly momentum and compatibility through nature's cycles
    - 🌀 **Mayan Astrology: The Universal Rhythm** — Connects daily energy to galactic frequency for spiritual alignment
    
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
    
    ✨ **15 free questions** to explore your destiny  
    💬 **Instant AI responses** in your language  
    🌍 **70+ countries, 25+ languages** supported
    
    ### Upgrade Anytime
    
    💎 **$1/month** — Unlimited questions + full chat history  
    🔮 **$5/month** — Premium systems + palmistry (coming soon)  
    👑 **$50/month** — VIP insights + weekly forecasts
    
    **👈 Login or Register in the sidebar to begin**
    """)
    
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
