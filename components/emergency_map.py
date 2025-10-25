import streamlit as st
import folium
from streamlit_folium import st_folium
from database import get_shelters, get_roads, get_status_reports, get_active_sos_alerts
from utils import get_hyderabad_coordinates, get_status_color

def emergency_map_page():
    """Emergency map page showing flood conditions, shelters, and incidents"""
    st.header("🗺️ Emergency Flood Map")
    st.write("Real-time view of flood conditions, shelters, and emergency incidents across Hyderabad")
    
    # Map controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_shelters = st.checkbox("🏠 Show Shelters", value=True)
    with col2:
        show_roads = st.checkbox("🛣️ Show Road Status", value=True)
    with col3:
        show_incidents = st.checkbox("🚨 Show Incidents", value=True)
    
    # Get data
    shelters = get_shelters() if show_shelters else []
    roads = get_roads() if show_roads else []
    sos_alerts = get_active_sos_alerts() if show_incidents else []
    status_reports = get_status_reports() if show_incidents else []
    
    # Create map
    center_lat, center_lon = get_hyderabad_coordinates()
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add custom CSS for watermark
    watermark_html = """
    <div style="position: fixed; 
                top: 10px; 
                left: 50%; 
                transform: translateX(-50%);
                background-color: rgba(255, 107, 107, 0.9);
                color: white;
                padding: 5px 15px;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
                z-index: 1000;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
        🚨 FloodRescueNet - Live Emergency Map
    </div>
    """
    # Add watermark using folium HTML
    watermark = folium.Element(watermark_html)
    m.get_root().add_child(watermark)
    
    # Add shelters
    if shelters:
        for shelter in shelters:
            shelter_id, name, address, lat, lon, capacity, occupancy, status, contact, facilities, updated_at = shelter
            
            if lat and lon:
                # Color based on availability
                if status == 'available':
                    color = 'green'
                    icon = 'home'
                elif status == 'limited':
                    color = 'orange'
                    icon = 'home'
                else:
                    color = 'red'
                    icon = 'home'
                
                occupancy_rate = (occupancy / capacity * 100) if capacity > 0 else 0
                
                popup_text = f"""
                <b>🏠 {name}</b><br>
                📍 {address}<br>
                📞 {contact}<br>
                👥 Capacity: {occupancy}/{capacity} ({occupancy_rate:.1f}%)<br>
                🔄 Status: {status.title()}<br>
                🛠️ Facilities: {facilities}<br>
                ⏰ Updated: {updated_at.strftime('%H:%M') if updated_at else 'N/A'}
                """
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"Shelter: {name}",
                    icon=folium.Icon(color=color, icon=icon, prefix='fa')
                ).add_to(m)
    
    # Add road status
    if roads:
        for road in roads:
            road_id, name, status, description, lat, lon, updated_at = road
            
            if lat and lon:
                # Color based on road status
                if status == 'open':
                    color = 'green'
                    icon = 'road'
                elif status == 'limited':
                    color = 'orange'
                    icon = 'exclamation-triangle'
                else:
                    color = 'red'
                    icon = 'ban'
                
                popup_text = f"""
                <b>🛣️ {name}</b><br>
                🚦 Status: {status.title()}<br>
                📝 {description}<br>
                ⏰ Updated: {updated_at.strftime('%H:%M') if updated_at else 'N/A'}
                """
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_text, max_width=250),
                    tooltip=f"Road: {name} - {status.title()}",
                    icon=folium.Icon(color=color, icon=icon, prefix='fa')
                ).add_to(m)
    
    # Add SOS alerts
    if sos_alerts:
        for alert in sos_alerts:
            alert_id, username, location, lat, lon, message, created_at = alert
            
            if lat and lon:
                popup_text = f"""
                <b>🆘 SOS ALERT</b><br>
                👤 Reporter: {username}<br>
                📍 Location: {location}<br>
                💬 Message: {message}<br>
                ⏰ Time: {created_at.strftime('%H:%M') if created_at else 'N/A'}
                """
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip="🆘 Active SOS Alert",
                    icon=folium.Icon(color='red', icon='exclamation-circle', prefix='fa')
                ).add_to(m)
    
    # Add status reports (recent trapped/help requests)
    if status_reports:
        recent_reports = [r for r in status_reports if r[2] in ['help', 'trapped']][:20]  # Last 20 help requests
        
        for report in recent_reports:
            report_id, user_id, status, location, lat, lon, description, photo_path, created_at, username = report
            
            if lat and lon:
                if status == 'trapped':
                    color = 'red'
                    icon = 'exclamation-triangle'
                else:  # help
                    color = 'orange'
                    icon = 'question-circle'
                
                popup_text = f"""
                <b>📊 Status Report - {status.title()}</b><br>
                👤 Reporter: {username}<br>
                📍 Location: {location}<br>
                📝 Details: {description or 'No additional details'}<br>
                ⏰ Time: {created_at.strftime('%H:%M') if created_at else 'N/A'}
                """
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"Status: {status.title()}",
                    icon=folium.Icon(color=color, icon=icon, prefix='fa')
                ).add_to(m)
    
    # Display map
    map_data = st_folium(m, width=700, height=500)
    
    # Legend
    st.subheader("🔍 Map Legend")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Shelters:**
        - 🟢 Available (< 80% capacity)
        - 🟡 Limited (80-95% capacity)
        - 🔴 Full/Unavailable (> 95% capacity)
        
        **Roads:**
        - 🟢 Open (Normal traffic)
        - 🟡 Limited (Slow traffic/water)
        - 🔴 Blocked (Closed/flooded)
        """)
    
    with col2:
        st.markdown("""
        **Emergency Incidents:**
        - 🆘 Active SOS alerts
        - 🔴 People trapped
        - 🟡 People needing help
        
        **Map Features:**
        - Click markers for detailed information
        - Zoom in/out for better visibility
        - Real-time updates every 5 minutes
        """)
    
    # Quick stats
    st.divider()
    st.subheader("📊 Current Situation Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_shelters = len(shelters) if shelters else 0
        available_shelters = len([s for s in shelters if s[7] == 'available']) if shelters else 0
        st.metric("Available Shelters", f"{available_shelters}/{total_shelters}")
    
    with col2:
        total_roads = len(roads) if roads else 0
        open_roads = len([r for r in roads if r[2] == 'open']) if roads else 0
        st.metric("Open Roads", f"{open_roads}/{total_roads}")
    
    with col3:
        active_sos = len(sos_alerts) if sos_alerts else 0
        st.metric("Active SOS Alerts", active_sos)
    
    with col4:
        if status_reports:
            help_requests = len([r for r in status_reports if r[2] in ['help', 'trapped']])
        else:
            help_requests = 0
        st.metric("Active Help Requests", help_requests)
    
    # Auto-refresh notice
    st.info("🔄 Map data refreshes automatically. Click 'Refresh' in your browser to get the latest updates.")
