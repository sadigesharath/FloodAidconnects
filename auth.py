import hashlib
import streamlit as st
from database import get_user_by_username, create_user

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user and return user ID if successful"""
    
    # DEMO CREDENTIALS - Check these first before database
    demo_users = {
        "citizen2": {"password": "password123", "role": "citizen", "user_id": 1},
        "gov_official": {"password": "admin123", "role": "government", "user_id": 2},
        "rescue1": {"password": "rescue123", "role": "rescue", "user_id": 3}
    }
    
    # Check demo credentials first
    if username in demo_users and demo_users[username]["password"] == password:
        return demo_users[username]["user_id"]
    
    # If not demo user, check database
    users = get_user_by_username(username)
    
    if users and len(users) > 0:
        user = users[0]
        user_id, stored_username, stored_hash, role = user
        
        if hash_password(password) == stored_hash:
            return user_id
    
    return None

def register_user(username, password, role="citizen"):
    """Register a new user"""
    # Check if user already exists
    existing_users = get_user_by_username(username)
    if existing_users:
        return False
    
    password_hash = hash_password(password)
    result = create_user(username, password_hash, role)
    
    return result is not None and result > 0

def get_user_role(user_id):
    """Get user role by user ID"""
    
    # DEMO USER ROLES
    demo_roles = {
        1: "citizen",
        2: "government",
        3: "rescue"
    }
    
    # Check demo users first
    if user_id in demo_roles:
        return demo_roles[user_id]
    
    # Otherwise check database
    from database import execute_query
    
    result = execute_query(
        "SELECT role FROM users WHERE id = %s",
        (user_id,),
        fetch=True
    )
    
    if result and len(result) > 0:
        return result[0][0]
    
    return "citizen"

def logout_user():
    """Logout user by clearing session state"""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_role = None
