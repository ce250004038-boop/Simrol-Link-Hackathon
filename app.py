import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from PIL import Image
import json
import uuid
import random
import hashlib
import smtplib
from email.message import EmailMessage
from datetime import datetime


st.set_page_config(page_title="Simrol-Link", page_icon="🚕", layout="wide")


model = None
api_status = "ok" # ok, no_secrets, no_key

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        api_status = "no_key"
except FileNotFoundError:
    api_status = "no_secrets"
except Exception:
    api_status = "no_secrets"







st.markdown("""
    <style>
    /* 1. Main Background - Deep Purple Gradient */
    .stApp {
        background: linear-gradient(to right, #2c003e 0%, #1a0b2e 100%);
        background-attachment: fixed;
    }

    /* 2. Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: rgba(17, 5, 31, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3. General Text Colors - WHITE */
    h1, h2, h3, h4, h5, p, label, .stMarkdown, .stRadio > label, .stCheckbox > label, span, div {
        color: white !important;
        font-family: 'Courier New', sans-serif;
    }
    
    /* 4. Main Title Glow */
    h1 {
        font-size: 3.5rem !important;
        text-shadow: 0 0 10px #ff00cc, 0 0 20px #ff00cc, 0 0 40px #ff00cc;
    }

    /* 5. INPUT BOXES (Inputs, TextAreas, Selects) - Black with White Text */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: #000000 !important;
        color: #ffffff !important;
        caret-color: #ffffff !important; /* White Cursor */
        border: 2px solid #ff00cc;
        font-weight: bold;
    }
    
    /* Fix for placeholder text color if needed */
    ::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
        opacity: 1; 
    }
    
    .stSelectbox svg { fill: white !important; }

    /* 6. *** DARK DROPDOWN MENU *** */
    /* Target the top-level popover container used by Streamlit for dropdowns */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #000000 !important;
        border: none !important;
    }
    
    /* Force all text inside the popover to be white */
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] * {
        color: #ffffff !important;
        background-color: #000000 !important;
    }

    /* The options inside the list */
    li[data-baseweb="option"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* Hover effects need strictly higher specificity or order to override the universal * selector above */
    li[data-baseweb="option"]:hover, 
    li[aria-selected="true"],
    li[data-baseweb="option"]:hover > div,
    li[aria-selected="true"] > div {
        background-color: #ff00cc !important; 
        color: #ffffff !important;
    }
    
    /* Ensure no white backgrounds on sub-elements */
    div[data-baseweb="select"] > div {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* 7. Profile Image Uploader - Black Box */
    [data-testid='stFileUploader'] section {
        background-color: #000000 !important;
        border: 2px dashed #ff00cc !important;
    }
    [data-testid='stFileUploader'] section > div, 
    [data-testid='stFileUploader'] section span, 
    [data-testid='stFileUploader'] section small {
        color: #ffffff !important;
    }
    [data-testid='stFileUploader'] button {
        background-color: #ff00cc !important;
        color: white !important;
        border: none !important;
    }

    /* 8. Buttons */
    .stButton>button {
        background-color: #ff00cc;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0px 0px 15px rgba(255, 0, 204, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 30px rgba(255, 0, 204, 1);
    }

    /* Hide Header and Footer */
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    iframe { margin-bottom: -20px; }
    
    /* Expander Styling - Force Black Background */
    div[data-testid="stExpander"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    div[data-testid="stExpander"] > details > summary {
        background-color: #000000 !important;
        background: #000000 !important;
        border: 1px solid #ff00cc !important;
        color: white !important;
        border-radius: 10px;
    }
    
    div[data-testid="stExpander"] > details[open] > summary {
         border-bottom-left-radius: 0 !important;
         border-bottom-right-radius: 0 !important;
    }
    
    div[data-testid="stExpander"] > details > div {
        background-color: rgba(0,0,0,0.8) !important;
        border: 1px solid #ff00cc;
        border-top: none;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }
    
    /* --- FIXES BY ANTIGRAVITY --- */
    /* Force Date Input to Black */
    div[data-testid="stDateInput"] input {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #ff00cc !important;
    }
    
    /* Force Form Submit Button (Publish Ride) to Black */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 2px solid #ff00cc !important;
    }
    div[data-testid="stFormSubmitButton"] > button:p {
        color: #ffffff !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #222222 !important;
        color: #ffffff !important;
        border-color: #ff00cc !important;
    }

    </style>
    """, unsafe_allow_html=True)


# --- HELPER FUNCTIONS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RIDES_FILE = os.path.join(BASE_DIR, "rides.json")

def load_data():
    if not os.path.exists(RIDES_FILE):
        return []
    with open(RIDES_FILE, "r", encoding="utf-8") as f:
        try:
            rides = json.load(f)
        except: return []
    
    # Auto-delete expired rides
    valid_rides = []
    current_time = datetime.now()
    has_changes = False
    
    for ride in rides:
        try:
          
            ride_dt = datetime.strptime(f"{ride['Date']} {ride['Time']}", "%Y-%m-%d %H:%M:%S")
            if ride_dt > current_time:
                valid_rides.append(ride)
            else:
                has_changes = True
        except:
            valid_rides.append(ride) # Keep if format error to be safe
    
    if has_changes:
        save_rides_list(valid_rides)
        return valid_rides
    return rides

def save_rides_list(rides):
    with open(RIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(rides, f)

PROFILES_FILE = os.path.join(BASE_DIR, "profiles.json")
def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except: return {}

def save_profile_to_disk(email, data):
    profiles = load_profiles()
    profiles[email] = data
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f)

def get_profile(email):
    profiles = load_profiles()
    return profiles.get(email, {})

def save_data(new_entry):
    rides = load_data()
    rides.append(new_entry)
    save_rides_list(rides)

def update_ride_request(ride_id, requester_email, action, requester_details=None):
    rides = load_data()
    for ride in rides:
        if ride["id"] == ride_id:
            if "requests" not in ride: ride["requests"] = []
            
            if action == "send":
                # Check if already requested
                for req in ride["requests"]:
                    if req["email"] == requester_email: return False
                
                ride["requests"].append({
                    "email": requester_email,
                    "details": requester_details,
                    "status": "Pending"
                })
                # Structured notification for actionable review
                notif_payload = {
                    "text": f"📩 New Ride Request: {requester_details['name']} wants to join your ride to {ride['Destination']}.",
                    "type": "review_request",
                    "ride_id": ride["id"],
                    "requester_email": requester_email
                }
                add_notification(ride['host_email'], notif_payload)
                
            elif action == "accept":
                for req in ride["requests"]:
                    if req["email"] == requester_email:
                        req["status"] = "Accepted"
                        # Decrease seats
                        if int(ride["Seats"]) > 0:
                            ride["Seats"] = int(ride["Seats"]) - 1
                        add_notification(requester_email, f"✅ Request Accepted: Your request to join {ride['HostName']}'s ride to {ride['Destination']} was accepted!")
            
            elif action == "decline":
                for req in ride["requests"]:
                    if req["email"] == requester_email:
                        req["status"] = "Declined"
                        add_notification(requester_email, f"🚫 Request Declined: Your request to join {ride['HostName']}'s ride to {ride['Destination']} was declined.")
            
            save_rides_list(rides)
            save_rides_list(rides)
            return True
    return False

# --- NOTIFICATION & DELETION HELPERS ---
NOTIFICATIONS_FILE = os.path.join(BASE_DIR, "notifications.json")

def load_notifications():
    if not os.path.exists(NOTIFICATIONS_FILE): return {}
    with open(NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_notifications(data):
    with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f: json.dump(data, f)

def add_notification(email, message):
    notifs = load_notifications()
    if email not in notifs: notifs[email] = []
    notifs[email].append(message)
    save_notifications(notifs)

def get_notifications(email):
    notifs = load_notifications()
    return notifs.get(email, [])

def clear_notifications(email):
    notifs = load_notifications()
    if email in notifs:
        notifs[email] = []
        save_notifications(notifs)

def delete_profile_data(email):
    profiles = load_profiles()
    if email in profiles:
        del profiles[email]
        with open(PROFILES_FILE, "w", encoding="utf-8") as f: json.dump(profiles, f)

# --- AUTH HELPERS ---
USERS_FILE = os.path.join(BASE_DIR, "users.json")

def load_users():
    if not os.path.exists(USERS_FILE): return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except: return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f)

# --- SESSION HELPERS (PERSISTENCE) ---
SESSION_FILE = os.path.join(BASE_DIR, "session_token.json")

def load_session_from_disk():
    if not os.path.exists(SESSION_FILE): return None
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Basic validation (could add expiry)
            if "email" in data: return data
    except: pass
    return None

def save_session_to_disk(email, name):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"email": email, "name": name}, f)

def clear_session_from_disk():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(email, password):
    users = load_users()
    if email in users and users[email].get("password") == hash_password(password):
        return True
    return False

def register_user(email, password):
    users = load_users()
    users[email] = {"password": hash_password(password)}
    save_users(users)

def delete_user_auth(email):
    users = load_users()
    if email in users:
        del users[email]
        save_users(users)
    delete_profile_data(email) # Also delete profile data


def delete_ride_data(ride_id):
    rides = load_data()
    ride = next((r for r in rides if r['id'] == ride_id), None)
    if ride:
        host_name = ride.get('HostName', 'Host')
        for req in ride.get('requests', []):
            if req['status'] == 'Accepted':
                 add_notification(req['email'], f"⚠️ Ride Cancelled: {host_name} cancelled the ride from {ride['Source']} to {ride['Destination']}.")
        
        rides = [r for r in rides if r['id'] != ride_id]
        save_rides_list(rides)

def leave_ride_action(ride_id, user_email, user_name):
    rides = load_data()
    for ride in rides:
        if ride['id'] == ride_id:
             for req in ride.get('requests', []):
                 if req['email'] == user_email and req['status'] == 'Accepted':
                     req['status'] = 'Left'
                     ride['Seats'] = int(ride['Seats']) + 1 
                     add_notification(ride['host_email'], f"📢 {user_name} left your ride ({ride['Source']} -> {ride['Destination']}). Seat restored.")
             save_rides_list(rides)
             return



# --- DATA: IIT INDORE ACADEMIC STRUCTURE ---
academic_structure = {
    "B.Tech": ["Computer Science and Engineering", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Metallurgical Engineering and Materials Science", "Chemical Engineering", "Mathematics and Computing", "Engineering Physics", "Space Science and Engineering (SSE)"],
    "B.Des": ["Bachelor of Design (B.Des)"],
    "M.Tech": ["Electrical Engineering - Communication and Signal Processing", "Electrical Engineering - VLSI Design and Nanoelectronics", "Mechanical Engineering - Advanced Manufacturing (AM)", "Mechanical Engineering - Thermal Energy Systems (TES)", "Mechanical Engineering - Mechanical Systems Design", "Metallurgical Eng. & Mat. Sci. - Materials Science and Engineering", "Metallurgical Eng. & Mat. Sci. - Metallurgical Engineering", "Electric Vehicle Technology (CEVITS)", "Space Engineering (DAASE)", "Computer Science and Engineering", "Civil Engineering - Water, Climate and Sustainability", "Biosciences and Biomedical Engineering", "Mechanical Engineering - Applied Optics and Laser Technology", "Civil Engineering - Structural Engineering", "Defence Technology (CFDST)", "Electrical Engineering - Power Systems and Power Electronics", "Biosciences and Biomedical Engineering - Biomedical Devices"],
    "M.Sc": ["Chemistry", "Physics", "Mathematics", "Biotechnology", "Astronomy"],
    "B.Tech + M.Tech (Dual Degree)": ["BTech EE + MTech Communication & Signal Processing", "BTech EE + MTech VLSI Design & Nanoelectronics", "BTech ME + MTech Production & Industrial Engineering", "BTech ME + MTech Mechanical Systems Design"],
    "MS (Research)": ["Computer Science and Engineering", "Electrical Engineering", "Mechanical Engineering", "Space Science and Engineering (DAASE)", "Humanities and Social Sciences (HSS)", "Data Science and Management (MS-DSM)"],
    "PhD": ["Computer Science and Engineering", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Metallurgical Engineering and Materials Science", "Bio-sciences and Bio-medical Engineering", "Chemistry", "Physics", "Mathematics", "English", "Philosophy", "Economics", "Psychology", "Sociology", "Astronomy, Astrophysics and Space Engineering", "Centre of Advanced Electronics", "Centre for Rural Development and Technology (CRDT)", "Center for Electric Vehicle and Intelligent Transport Systems (CEVITS)", "Center of Futuristic Defense and Space Technology (CFDST)", "JP Narayan National Center of Excellence in the Humanities", "Chemical Engineering"],
    "M.A.": ["English (Literature and Linguistics)"]
}

# --- LOCATIONS LIST ---
INDORE_LOCATIONS = sorted([
    "Rajwada Palace", "Lalbagh Palace", "Gandhi Hall (Town Hall)", "Chhatri Bagh",
    "Kanch Mandir (Glass Temple)", "Khajrana Ganesh Mandir", "Annapurna Temple", "Bada Ganpati",
    "ISKCON Indore", "Patalpani Waterfall", "Ralamandal Wildlife Sanctuary", "Pipliyapala Regional Park",
    "Janapav Hill", "Choral Dam & Tincha Falls", "Sarafa Bazaar", "Chhappan Dukan",
    "Central Museum Indore", "Kamla Nehru Prani Sangrahalay", "Mandu (Mandavgad Forts)",
    "Maheshwar & Omkareshwar", "Phoenix Citadel", "Treasure Island Mall", "C21 Mall", "Malhar Mega Mall",
    "Devi Ahilya Bai Holkar Airport", "Indore Railway Station"
])

# --- SESSION STATE ---
# --- SESSION STATE & AUTO-LOGIN ---
if "logged_in" not in st.session_state:
    # Try to load from disk first
    disk_session = load_session_from_disk()
    if disk_session:
        st.session_state.logged_in = True
        st.session_state.user_email = disk_session["email"]
        st.session_state.user_name = disk_session.get("name", "")
        # Load other profile stats
        profile_data = get_profile(st.session_state.user_email)
        if profile_data:
            st.session_state.user_gender = profile_data.get("gender", "Male")
            st.session_state.user_degree = profile_data.get("degree", list(academic_structure.keys())[0])
            st.session_state.user_branch = profile_data.get("branch", academic_structure[st.session_state.user_degree][0])
            st.session_state.user_year = profile_data.get("year", "1st")
    else:
        st.session_state.logged_in = False

if "current_view" not in st.session_state: st.session_state.current_view = "Home" # Home, Profile
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "user_gender" not in st.session_state: st.session_state.user_gender = "Male"
if "user_degree" not in st.session_state: st.session_state.user_degree = list(academic_structure.keys())[0]
if "user_branch" not in st.session_state: st.session_state.user_branch = academic_structure[st.session_state.user_degree][0]
if "user_year" not in st.session_state: st.session_state.user_year = "1st"
if "ride_published" not in st.session_state: st.session_state.ride_published = False
if "editing_ride_id" not in st.session_state: st.session_state.editing_ride_id = None

# ==========================================
# 🔒 PAGE 1: AUTHENTICATION (Login / Signup)
# ==========================================
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True) 
        st.title("Simrol-Link 🔐")

        
        with st.container(border=True):
            auth_tab1, auth_tab2, auth_tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
            
            # --- LOGIN TAB ---
            with auth_tab1:
                st.subheader("Welcome Back!")
                l_email = st.text_input("Email", key="l_email")
                l_pass = st.text_input("Password", type="password", key="l_pass")
                l_name = st.text_input("Your Name", key="l_name_input") # Ask for name

                if st.button("Login", use_container_width=True, key="btn_login"):
                    if verify_credentials(l_email, l_pass):
                        if not l_name:
                            st.error("Please enter your name.")
                        else:
                            st.session_state.logged_in = True
                            st.session_state.user_email = l_email
                            st.session_state.user_name = l_name
                            
                            save_session_to_disk(l_email, l_name) # Persist Login
                        # Load Profile
                        profile_data = get_profile(l_email)
                        if profile_data:
                            st.session_state.user_name = profile_data.get("name", "")
                            st.session_state.user_gender = profile_data.get("gender", "Male")
                            st.session_state.user_degree = profile_data.get("degree", list(academic_structure.keys())[0])
                            st.session_state.user_branch = profile_data.get("branch", academic_structure[st.session_state.user_degree][0])
                            st.session_state.user_year = profile_data.get("year", "1st")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid Email or Password")

            # --- SIGN UP TAB ---
            with auth_tab2:
                st.subheader("New User?")
                s_email = st.text_input("Enter Email (@iiti.ac.in)", key="s_email")
                s_pass = st.text_input("Set Password", type="password", key="s_pass")
                s_conf = st.text_input("Confirm Password", type="password", key="s_conf")
                
                if st.button("Sign Up", key="btn_signup"):
                    if not s_email.endswith("@iiti.ac.in"):
                        st.error("⚠️ Only @iiti.ac.in emails allowed.")
                    elif s_pass != s_conf:
                        st.error("⚠️ Passwords do not match.")
                    elif not s_pass:
                        st.error("⚠️ Password cannot be empty.")
                    else:
                        users = load_users()
                        if s_email in users:
                            st.error("🚫 User already exists! Please Login.")
                        else:
                            register_user(s_email, s_pass)
                           
                            st.session_state.logged_in = True
                            st.session_state.user_email = s_email
                            st.session_state.user_name = s_email.split("@")[0] # Default name
                            save_session_to_disk(s_email, st.session_state.user_name)
                            st.balloons()
                            st.success("Account Created Successfully!")
                            st.rerun()

            # --- FORGOT PASSWORD (RESET) TAB ---
            with auth_tab3:
                st.subheader("Reset Account")
                st.warning("⚠️ Forgot your password? This will **DELETE** your account and profile data so you can sign up again.")
                
                f_email = st.text_input("Enter Registered Email to Reset", key="f_email")
                
                if st.button("🗑️ Delete Account & Reset", key="btn_reset"):
                    users = load_users()
                    if f_email in users:
                        delete_user_auth(f_email)
                        st.success(f"♻️ Account for {f_email} has been deleted. You can now Sign Up again.")
                    else:
                        st.error("🚫 Email not found in our records.")

# ==========================================
# 🚕 PAGE 2: MAIN APP
# ==========================================
else:
    # --- SIDEBAR: NAVIGATION ---
    with st.sidebar:
        first_name = st.session_state.user_name.split()[0] if st.session_state.user_name else "Student"
        st.header(f"Hi, {first_name}! 👋")

        # --- PROFILE (EXPANDER) ---
        p_data = get_profile(st.session_state.user_email)
        is_complete = all([
            p_data.get("name"), 
            p_data.get("gender"), 
            p_data.get("degree"), 
            p_data.get("branch"), 
            p_data.get("year")
        ])
        
        if "force_edit" not in st.session_state: st.session_state.force_edit = False

        show_editor = (not is_complete) or st.session_state.force_edit
        
        if show_editor:
            expander_title = "✏️ Edit Details" if is_complete else "✏️ Complete Your Profile"
            with st.expander(expander_title, expanded=True):
                uploaded_file = st.file_uploader("Upload Profile Pic", type=['jpg', 'png'])
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="That's you!", width=150)
                
                my_name = st.text_input("Name", st.session_state.user_name)
                
                g_idx = ["Male", "Female", "Other"].index(st.session_state.user_gender) if st.session_state.user_gender in ["Male", "Female", "Other"] else 0
                my_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=g_idx)
                
                degree_keys = list(academic_structure.keys())
                d_idx = degree_keys.index(st.session_state.user_degree) if st.session_state.user_degree in degree_keys else 0
                my_degree = st.selectbox("Degree Program", degree_keys, index=d_idx)
                
                available_branches = academic_structure[my_degree]
                current_b_idx = 0
                if my_degree == st.session_state.user_degree and st.session_state.user_branch in available_branches:
                    current_b_idx = available_branches.index(st.session_state.user_branch)
                    
                my_branch = st.selectbox("Specialization / Branch", available_branches, index=current_b_idx)
                
                y_options = ["1st", "2nd", "3rd", "4th", "5th+"]
                y_idx = y_options.index(st.session_state.user_year) if st.session_state.user_year in y_options else 0
                my_year = st.selectbox("Year", y_options, index=y_idx)
                
                if st.button("Save Profile", use_container_width=True):
                    st.session_state.user_name = my_name
                    st.session_state.user_gender = my_gender
                    st.session_state.user_degree = my_degree
                    st.session_state.user_branch = my_branch
                    st.session_state.user_year = my_year
                    
                    # Update Session on Disk too if name changed
                    save_session_to_disk(st.session_state.user_email, my_name)

                    save_profile_to_disk(st.session_state.user_email, {
                        "name": my_name,
                        "gender": my_gender,
                        "degree": my_degree,
                        "branch": my_branch,
                        "year": my_year
                    })
                    st.session_state.force_edit = False # Hide after saving
                    st.success("Profile Updated! ✅")
                    st.rerun()
        else:
           
             if st.button("⚙️ Edit Profile", key="open_edit"):
                 st.session_state.force_edit = True
                 st.rerun()

        st.divider()

        # --- GEMINI SAFETY TOOL (MOVED) ---
        with st.expander("✨ Ask Gemini: Travel Safety Tip"):
            if st.button("Get a Safety Tip"):
                if model:
                    try:
                        response = model.generate_content("Give me a short, practical travel safety tip for students in India.")
                        st.success(f"🤖 AI Safety Tip: {response.text}")
                    except Exception as e:
                        st.error(f"Error fetching tip: {e}")
                elif api_status == "no_key":
                     st.warning("⚠️ Gemini API Key is missing. Set it in code or environment variables.")
                elif api_status == "no_secrets":
                     st.warning("⚠️ secrets.toml file missing. Create one with your API key.")
                else:
                     st.error("⚠️ Gemini Model not initialized.")
                
                if not model:
                    st.info("🤖 AI Safety Tip (Offline): Always share your live location with a trusted friend or family member while travelling.")

        st.divider()
        
        if st.button("🔓 Logout", use_container_width=True):
            clear_session_from_disk()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        if st.button("🗑️ Delete Profile", key="del_prof"):
            delete_profile_data(st.session_state.user_email)
            st.warning("Profile details cleared!")
            st.rerun()

    # --- MAIN CONTENT ---
  
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Simrol-Link 🚕✨")
        first_name = st.session_state.user_name.split()[0] if st.session_state.user_name else "Student"
        st.write(f"Welcome, **{first_name}**!") # Welcome [Name]

    


    # Fetch Notifications
    my_notifs = get_notifications(st.session_state.user_email)
    notif_count = len(my_notifs)
    notif_label = f"🔔 Notifications ({notif_count})" if notif_count > 0 else "🔔 Notifications"

    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Find a Ride", "➕ Post a Ride", "My Rides 🚗", notif_label])

    # --- TAB 1: FIND ---
    with tab1:
        st.header("Find your Squad 👯‍♂️")
        with st.container(border=True):
            filter_dir = st.radio("Direction", ["Campus ⮕ City", "City ⮕ Campus"], horizontal=True)
            
            selected_location = st.selectbox("Select Location", ["All"] + INDORE_LOCATIONS)
            
            with st.expander("➕ Add Filters"):
                c1, c2 = st.columns(2)
                f_gender = c1.selectbox("Gender", ["All", "Male", "Female", "Other"])
                f_year = c2.selectbox("Year", ["All", "1st", "2nd", "3rd", "4th", "5th+"])
                
                f_degree = c1.selectbox("Degree", ["All"] + list(academic_structure.keys()))
                
                avail_branches = ["All"]
                if f_degree != "All":
                    avail_branches += academic_structure[f_degree]
                f_branch = c2.selectbox("Branch", avail_branches)
        
        rides = load_data()
        if rides:
          
            visible_rides = [r for r in rides if r["Direction"] == filter_dir]
            
            # Filter by Location
            if selected_location != "All":
                if filter_dir == "Campus ⮕ City":
                    visible_rides = [r for r in visible_rides if r["Destination"] == selected_location]
                else:
                    visible_rides = [r for r in visible_rides if r["Source"] == selected_location]

            # Additional Filters
            if f_gender != "All": visible_rides = [r for r in visible_rides if r["Gender"] == f_gender]
            if f_year != "All": visible_rides = [r for r in visible_rides if r["Year"] == f_year]
            if f_degree != "All": visible_rides = [r for r in visible_rides if r["Degree"] == f_degree]
            if f_branch != "All": visible_rides = [r for r in visible_rides if r["Branch"] == f_branch]
            
            final_rides = []
            for r in visible_rides:
                is_host = r.get("host_email") == st.session_state.user_email
                has_req = any(req['email'] == st.session_state.user_email for req in r.get('requests', []))
                seats = int(r.get("Seats", 0))
                
                if seats > 0 or has_req:
                    # Exclude own rides from "Find a Ride" (they are in "My Rides")
                    if not is_host:
                        final_rides.append(r)
            visible_rides = final_rides
            
            if visible_rides:
                for ride in visible_rides:
                    is_my_ride = ride.get("host_email") == st.session_state.user_email
                    
                    title_prefix = "🌟 MY RIDE | " if is_my_ride else ""
                    with st.expander(f"{title_prefix}{ride['Time']} | {ride['Source']} ⮕ {ride['Destination']} ({ride['Seats']} Seats Left)"):
                        sc1, sc2 = st.columns(2)
                        sc1.write(f"**📅 Date:** {ride['Date']}")
                        sc1.write(f"**💺 Seats Left:** {ride['Seats']}")
                        deg = ride.get('Degree', 'N/A')
                        br = ride.get('Branch', 'N/A')
                        yr = ride.get('Year', 'N/A')
                        sc1.write(f"**🎓 Batch:** {deg} ({yr})")
                        sc1.caption(f"{br}")
                        sc2.write(f"**⚧ Gender:** {ride['Gender']}")
                        
                        if ride['Contact']:
                            sc2.markdown(f"#### 📞 [WhatsApp Link]({ride['Contact']})")
                        else:
                            sc2.info("No Contact Link")
                        
                        # --- SHOW MEMBERS ---
                        # Prepare data
                        squad_names = [ride['HostName']]
                        squad_details = [{
                            "Name": ride['HostName'], 
                            "Role": "Host", 
                            "Gender": ride['Gender'], 
                            "Year": ride['Year'],
                            "Branch": ride['Branch']
                        }]
                        
                        for req in ride.get('requests', []):
                            if req['status'] == 'Accepted':
                                r_det = req['details']
                                squad_names.append(r_det.get('name', 'User'))
                                squad_details.append({
                                    "Name": r_det.get('name', 'User'),
                                    "Role": "Passenger",
                                    "Gender": r_det.get('gender', 'N/A'),
                                    "Year": r_det.get('year', 'N/A'),
                                    "Branch": r_det.get('branch', 'N/A')
                                })
                        
                        st.write(f"**👥 Squad ({len(squad_names)}):** {', '.join(squad_names)}")
                        
                        with st.expander("Show Details"):
                            for mem in squad_details:
                                st.markdown(f"**{mem['Name']}** ({mem['Role']})")
                                st.caption(f"{mem['Gender']} | {mem['Year']} | {mem['Branch']}")
                                st.write("---")
                        
                        st.divider()
                        
                        # --- REQUEST LOGIC ---
                        if is_my_ride:
                            if st.button("❌ Delete Ride", key=f"del_ride_{ride['id']}"):
                                delete_ride_data(ride['id'])
                                st.rerun()
                                
                            st.write("### Incoming Requests 📩")
                            requests = ride.get("requests", [])
                            if not requests:
                                st.info("No requests yet.")
                            else:
                                for req in requests:
                                    rc1, rc2, rc3 = st.columns([2,1,1])
                                    r_det = req['details']
                                    rc1.write(f"**{r_det['name']}** ({r_det['degree']}, {r_det['year']})")
                                    rc1.caption(f"Status: {req['status']}")
                                    
                                    if req['status'] == "Pending":
                                        if rc2.button("✅ Accept", key=f"acc_{ride['id']}_{req['email']}"):
                                            update_ride_request(ride["id"], req["email"], "accept")
                                            st.rerun()
                                        if rc3.button("❌ Decline", key=f"dec_{ride['id']}_{req['email']}"):
                                            update_ride_request(ride["id"], req["email"], "decline")
                                            st.rerun()
                        else:
                            # Check my request status
                            my_req_status = None
                            for req in ride.get("requests", []):
                                if req["email"] == st.session_state.user_email:
                                    my_req_status = req["status"]
                                    break
                            
                            if my_req_status:
                                if my_req_status == "Pending":
                                    st.warning(f"Request Sent (Status: {my_req_status}) ⏳")
                                elif my_req_status == "Accepted":
                                    st.success("Request Accepted! 🎉 You can join the ride.")
                                    if st.button("🏃‍♂️ Leave Ride", key=f"leave_{ride['id']}"):
                                        leave_ride_action(ride['id'], st.session_state.user_email, st.session_state.user_name)
                                        st.rerun()
                                else:
                                    st.error("Request Declined 🛑")
                            else:
                                if int(ride["Seats"]) > 0:
                                    if st.button("🙋‍♂️ Request to Join", key=f"req_{ride['id']}"):
                                        my_details = {
                                            "name": st.session_state.user_name,
                                            "degree": st.session_state.user_degree,
                                            "year": st.session_state.user_year,
                                            "gender": st.session_state.user_gender,
                                            "branch": st.session_state.user_branch
                                        }
                                        update_ride_request(ride["id"], st.session_state.user_email, "send", my_details)
                                        st.success("Request Sent!")
                                        st.rerun()
                                else:
                                    st.error("Ride Full 🚫")
                                    

            else: st.warning("No rides match your filters.")
        else: st.info("No rides posted yet.")

    # --- TAB 2: POST ---
    with tab2:
        st.header("Host a Ride 🚘")
        
        if st.session_state.ride_published:
            st.success("Ride Published")
            if st.button("Publish Another"):
                st.session_state.ride_published = False
                st.rerun()
        else:
            with st.container(border=True):
                with st.form("post_ride"):
                    direction = st.selectbox("Route", ["Campus ⮕ City", "City ⮕ Campus"])
                    if direction == "Campus ⮕ City":
                        source = "IIT Indore"
                        destination = st.selectbox("Destination", INDORE_LOCATIONS, key="post_dest")
                    else:
                        source = st.selectbox("Pickup Point", INDORE_LOCATIONS, key="post_src")
                        destination = "IIT Indore"
                    c1, c2 = st.columns(2)
                    date = c1.date_input("Date")
                    time = c2.time_input("Time")
                    seats = st.slider("Seats Empty", 1, 6, 3)
                    contact = st.text_input("WhatsApp Group Link (Optional)")
                    host_name = st.session_state.user_name if st.session_state.user_name else "Anonymous"
                    
                    submitted = st.form_submit_button("🚀 Publish Ride", use_container_width=True)
                    if submitted:
                        new_ride = {
                            "id": str(uuid.uuid4()),
                            "host_email": st.session_state.user_email,
                            "Direction": direction, "Source": source, "Destination": destination, 
                            "Date": str(date), "Time": str(time), "Seats": seats, 
                            "Contact": contact, "HostName": host_name, 
                            "Gender": st.session_state.user_gender, "Degree": st.session_state.user_degree, 
                            "Branch": st.session_state.user_branch, "Year": st.session_state.user_year,
                            "requests": []
                        }
                        save_data(new_ride)
                        st.balloons()
                        st.session_state.ride_published = True
                        st.rerun()

    # --- TAB 3: MY RIDES ---
    with tab3:
        st.header("My Rides 🚗")
        rides = load_data()
        my_rides = [r for r in rides if r.get("host_email") == st.session_state.user_email]
        
        if my_rides:
            for ride in my_rides:
                with st.expander(f"{ride['Date']} | {ride['Source']} ⮕ {ride['Destination']}"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**Time:** {ride['Time']}")
                    c1.write(f"**Seats:** {ride['Seats']}")
                    c2.write(f"**Status:** Active")
                    
                    rid = ride['id']
                    
                    # Toggle Edit Mode
                    is_editing = (st.session_state.editing_ride_id == rid)
                    
                    if not is_editing:
                        if st.button("✏️ Edit Ride", key=f"btn_edit_{rid}"):
                            st.session_state.editing_ride_id = rid
                            st.rerun()
                    
                    if is_editing:
                        st.subheader("Edit Details")
                        with st.form(key=f"edit_{rid}"):
                             # Parse existing date/time safe-guarded
                             try:
                                 curr_date = datetime.strptime(ride['Date'], '%Y-%m-%d').date()
                             except:
                                 curr_date = datetime.now().date()
                                 
                             try:
                                 curr_time_obj = datetime.strptime(ride['Time'], '%H:%M:%S').time()
                             except:
                                 curr_time_obj = datetime.now().time()

                             new_date = st.date_input("Date", curr_date)
                             new_time = st.time_input("Time", curr_time_obj)
                             # Handle seats as int
                             try:
                                 curr_seats = int(ride['Seats'])
                             except:
                                 curr_seats = 3
                                 
                             new_seats = st.slider("Seats Empty", 1, 6, curr_seats)
                             new_contact = st.text_input("Contact Link", value=ride.get('Contact', ''))
                             
                             c_save, c_cancel = st.columns(2)
                             if c_save.form_submit_button("Save Changes"):
                                 ride['Date'] = str(new_date)
                                 ride['Time'] = str(new_time)
                                 ride['Seats'] = new_seats
                                 ride['Contact'] = new_contact
                                 save_rides_list(rides)
                                 
                                 # Notify Accepted Members
                                 for req in ride.get('requests', []):
                                     if req['status'] == 'Accepted':
                                          add_notification(req['email'], f"📢 Ride Update: The ride from {ride['Source']} to {ride['Destination']} details have been modified by host.")
                                 
                                 st.session_state.editing_ride_id = None # Close edit mode
                                 st.success("Ride Updated Successfully!")
                                 st.rerun()
                                 
                             if c_cancel.form_submit_button("Cancel"):
                                 st.session_state.editing_ride_id = None
                                 st.rerun()
                    
                    if st.button("🗑️ Delete Ride", key=f"del_my_ride_{rid}"):
                        delete_ride_data(rid)
                        st.success("Ride Deleted")
                        st.rerun()
        else:
            st.info("You haven't posted any rides yet.")

    # --- TAB 4: NOTIFICATIONS (Renamed from TAB 3) ---
    with tab4:
        st.header("Notifications 📢")
        if my_notifs:
            if st.button("Clear All Notifications", key="clear_notifs"):
                clear_notifications(st.session_state.user_email)
                st.rerun()
            
            for i, msg in enumerate(reversed(my_notifs)):
                # Handle dictionary notifications (Actionable)
                if isinstance(msg, dict) and msg.get("type") == "review_request":
                    st.info(msg["text"])
                    with st.expander(f"👀 Review Request (Item #{i+1})"):
                        # Fetch current ride status
                        rides = load_data()
                        target_ride = next((r for r in rides if r["id"] == msg["ride_id"]), None)
                        
                        if target_ride:
                            # Find the specific request
                            target_req = next((req for req in target_ride.get("requests", []) if req["email"] == msg["requester_email"]), None)
                            
                            if target_req:
                                st.write(f"**Status:** {target_req['status']}")
                                if target_req['status'] == "Pending":
                                    c1, c2 = st.columns(2)
                                    if c1.button("✅ Accept", key=f"notif_acc_{i}"):
                                        update_ride_request(msg["ride_id"], msg["requester_email"], "accept")
                                        st.rerun()
                                    if c2.button("❌ Decline", key=f"notif_dec_{i}"):
                                        update_ride_request(msg["ride_id"], msg["requester_email"], "decline")
                                        st.rerun()
                                else:
                                    st.write("This request has already been handled.")
                            else:
                                st.warning("Request data not found. It might have been cancelled.")
                        else:
                            st.error("Ride not found. It might have been deleted.")

                # Handle legacy string notifications or other types
                elif isinstance(msg, dict):
                    st.info(msg.get("text", str(msg)))
                else:
                    st.info(msg)
        else:
            st.write("You have no new notifications.")

