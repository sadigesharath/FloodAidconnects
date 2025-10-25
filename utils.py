import streamlit as st
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

def format_datetime(dt):
    """Format datetime for display"""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_status_color(status):
    """Get color for status indicators"""
    colors = {
        'safe': '#28a745',      # Green
        'help': '#ffc107',      # Yellow/Orange
        'trapped': '#dc3545',   # Red
        'open': '#28a745',      # Green
        'limited': '#ffc107',   # Yellow
        'blocked': '#dc3545',   # Red
        'available': '#28a745', # Green
        'active': '#dc3545'     # Red
    }
    return colors.get(status.lower(), '#6c757d')

def get_status_emoji(status):
    """Get emoji for status"""
    emojis = {
        'safe': '✅',
        'help': '⚠️',
        'trapped': '🆘',
        'open': '✅',
        'limited': '⚠️',
        'blocked': '🚫',
        'available': '✅',
        'limited': '⚠️',
        'full': '❌'
    }
    return emojis.get(status.lower(), '❓')

def process_uploaded_image(uploaded_file):
    """Process uploaded image and return base64 encoded string"""
    if uploaded_file is not None:
        try:
            # Open and resize image
            image = Image.open(uploaded_file)
            
            # Resize image to maximum 800x600 to save space
            image.thumbnail((800, 600), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save to bytes
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            
            # Encode to base64
            img_str = base64.b64encode(buffer.read()).decode()
            return f"data:image/jpeg;base64,{img_str}"
            
        except Exception as e:
            st.error(f"Error processing image: {e}")
            return None
    
    return None

def display_image_from_base64(base64_string, caption="", width=None):
    """Display image from base64 string"""
    if base64_string:
        st.image(base64_string, caption=caption, width=width)

def create_alert_box(message, alert_type="info"):
    """Create styled alert box"""
    colors = {
        'success': '#d4edda',
        'info': '#d1ecf1',
        'warning': '#fff3cd',
        'danger': '#f8d7da'
    }
    
    border_colors = {
        'success': '#28a745',
        'info': '#17a2b8',
        'warning': '#ffc107',
        'danger': '#dc3545'
    }
    
    st.markdown(f"""
    <div style="
        background-color: {colors.get(alert_type, colors['info'])};
        border-left: 5px solid {border_colors.get(alert_type, border_colors['info'])};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    ">
        {message}
    </div>
    """, unsafe_allow_html=True)

def get_hyderabad_coordinates():
    """Get default coordinates for Hyderabad"""
    return 17.3850, 78.4867

def validate_coordinates(lat, lon):
    """Validate if coordinates are within reasonable bounds for Hyderabad"""
    # Rough bounds for Hyderabad and surrounding areas
    if lat is None or lon is None:
        return False
    
    lat_min, lat_max = 17.0, 18.0
    lon_min, lon_max = 78.0, 79.0
    
    return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max

def format_phone_number(phone):
    """Format phone number for display"""
    if phone and len(phone) >= 10:
        if phone.startswith('+91'):
            return phone
        elif phone.startswith('91'):
            return '+' + phone
        else:
            return '+91-' + phone
    return phone

def get_rescue_team_responses():
    """Get predefined rescue team responses"""
    return [
        "🚁 We are coming to your location, please wait and don't panic",
        "📍 Help is on the way, stay where you are and remain calm",
        "⚡ Emergency response team dispatched to your location",
        "🏥 Medical assistance is being arranged, hold tight",
        "🛟 Rescue boat deployed to your area, please wait safely",
        "📞 Please call emergency number immediately for urgent assistance",
        "⚠️ Move to higher ground if possible, help is coming",
        "🆘 Stay visible and keep your phone charged, we're tracking you",
        "🚨 Multiple rescue teams en route to flood-affected areas",
        "💧 Avoid walking through flood water, rescue team approaching"
    ]
