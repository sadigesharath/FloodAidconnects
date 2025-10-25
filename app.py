import streamlit as st
import os
from auth import authenticate_user, get_user_role, logout_user
from database import init_database
from components.status_report import status_report_page
from components.emergency_map import emergency_map_page
from components.shelters import shelters_page
from components.sos_alerts import sos_alerts_page
from components.emergency_contacts import emergency_contacts_page
from components.messaging import messaging_page
from components.government_dashboard import government_dashboard_page

# Initialize database
init_database()

# Set page config
st.set_page_config(
    page_title="FloodRescueNet - Emergency Response System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for emergency theme
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}
.emergency-alert {
    background-color: #FFE5E5;
    border-left: 5px solid #FF6B6B;
    padding: 1rem;
    margin: 1rem 0;
}
.status-safe { color: #28a745; font-weight: bold; }
.status-help { color: #ffc107; font-weight: bold; }
.status-trapped { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚨 FloodRescueNet - Emergency Response System</h1>
        <p>Coordinating rescue efforts and safety reporting for Hyderabad</p>
    </div>
    """, unsafe_allow_html=True)

    # Authentication check
    if not st.session_state.authenticated:
        st.subheader("🔐 Login Required")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_register = st.columns(2)
            with col_login:
                if st.button("Login", use_container_width=True):
                    user_id = authenticate_user(username, password)
                    if user_id:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.user_role = get_user_role(user_id)
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials!")
            
            with col_register:
                if st.button("Register as Citizen", use_container_width=True):
                    from auth import register_user
                    if username and password:
                        if register_user(username, password, "citizen"):
                            st.success("Registration successful! Please login.")
                        else:
                            st.error("Registration failed! Username might already exist.")
                    else:
                        st.error("Please fill in all fields.")

        # Demo credentials info
        st.info("""
        **Demo Credentials:**
        - Citizen: username: `citizen1`, password: `password123`
        - Government Official: username: `gov_official`, password: `admin123`
        - Rescue Team: username: `rescue1`, password: `rescue123`
        """)
        
        return

    # Sidebar for authenticated users
    with st.sidebar:
        user_role_display = st.session_state.user_role.title() if st.session_state.user_role else "User"
        st.header(f"Welcome, {user_role_display}!")
        
        # Emergency status indicator
        st.markdown("""
        <div class="emergency-alert">
            <strong>🚨 FLOOD ALERT ACTIVE</strong><br>
            Heavy rainfall warning for Hyderabad<br>
            Stay safe and report your status
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation based on role
        if st.session_state.user_role == "government":
            pages = ["Government Dashboard", "Emergency Map", "Messages", "Emergency Contacts"]
        elif st.session_state.user_role == "rescue_team":
            pages = ["Emergency Map", "SOS Alerts", "Messages", "Shelters", "Emergency Contacts"]
        else:  # citizen
            pages = ["Status Report", "Emergency Map", "Shelters", "SOS Alerts", "Messages", "Emergency Contacts"]
        
        selected_page = st.selectbox("Navigate to:", pages)
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()

    # Main content area
    if selected_page == "Status Report":
        status_report_page()
    elif selected_page == "Emergency Map":
        emergency_map_page()
    elif selected_page == "Shelters":
        shelters_page()
    elif selected_page == "SOS Alerts":
        sos_alerts_page()
    elif selected_page == "Messages":
        messaging_page()
    elif selected_page == "Emergency Contacts":
        emergency_contacts_page()
    elif selected_page == "Government Dashboard":
        government_dashboard_page()

if __name__ == "__main__":
    main()
