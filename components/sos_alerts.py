import streamlit as st
from datetime import datetime
from database import create_sos_alert, get_active_sos_alerts, send_message
from utils import get_hyderabad_coordinates, create_alert_box, format_datetime, get_rescue_team_responses

def sos_alerts_page():
    """SOS alerts page for emergency distress signals"""
    st.header("🆘 SOS Emergency Alerts")
    
    if st.session_state.user_role == "citizen":
        citizen_sos_interface()
    elif st.session_state.user_role == "rescue_team":
        rescue_team_sos_interface()
    else:  # government
        government_sos_interface()

def citizen_sos_interface():
    """SOS interface for citizens"""
    st.write("Send emergency SOS alerts to rescue teams with your location and situation details")
    
    # Emergency alert banner
    st.markdown("""
    <div style="background-color: #ffebee; border: 2px solid #f44336; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <h3 style="color: #d32f2f; margin: 0;">⚠️ EMERGENCY SOS SYSTEM</h3>
        <p style="margin: 0.5rem 0 0 0;">Use this only for life-threatening emergencies. Rescue teams will be immediately notified.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SOS Alert Form
    with st.form("sos_alert_form"):
        st.subheader("🚨 Send SOS Alert")
        
        # Location information
        st.write("📍 **Location Information**")
        location = st.text_input(
            "Describe your location",
            placeholder="e.g., 3rd floor, Blue Building, Gachibowli Main Road",
            help="Be as specific as possible - building name, floor, nearby landmarks"
        )
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            latitude = st.number_input(
                "Latitude",
                value=17.3850,
                format="%.6f",
                help="Your current latitude - use GPS if possible"
            )
        with col_lon:
            longitude = st.number_input(
                "Longitude",
                value=78.4867,
                format="%.6f",
                help="Your current longitude - use GPS if possible"
            )
        
        # Emergency details
        st.write("💬 **Emergency Details**")
        emergency_type = st.selectbox(
            "Type of Emergency",
            ["trapped_flood", "medical_emergency", "building_collapse", "fire", "other"],
            format_func=lambda x: {
                "trapped_flood": "🌊 Trapped by flood water",
                "medical_emergency": "🏥 Medical emergency",
                "building_collapse": "🏢 Building/structure collapse",
                "fire": "🔥 Fire emergency",
                "other": "❓ Other emergency"
            }[x]
        )
        
        message = st.text_area(
            "Emergency Message",
            placeholder="Describe your emergency: number of people, injuries, immediate dangers, etc.",
            help="Provide crucial information that will help rescue teams prepare and respond effectively",
            height=100
        )
        
        # People count
        people_count = st.number_input(
            "Number of people at location",
            min_value=1,
            max_value=50,
            value=1,
            help="How many people need rescue?"
        )
        
        # Immediate dangers
        dangers = st.multiselect(
            "Immediate dangers present",
            ["rising_water", "structural_damage", "electrical_hazard", "fire", "injury", "medical_condition"],
            format_func=lambda x: {
                "rising_water": "🌊 Rising water levels",
                "structural_damage": "🏗️ Building/structural damage",
                "electrical_hazard": "⚡ Electrical hazards",
                "fire": "🔥 Fire",
                "injury": "🩹 Physical injuries",
                "medical_condition": "🏥 Medical emergency"
            }[x]
        )
        
        # Submit SOS
        submitted = st.form_submit_button(
            "🚨 SEND SOS ALERT",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not location or not message:
                st.error("Please provide location and emergency details!")
                return
            
            # Create comprehensive emergency message
            full_message = f"""
EMERGENCY TYPE: {emergency_type.replace('_', ' ').title()}
PEOPLE COUNT: {people_count}
IMMEDIATE DANGERS: {', '.join(dangers) if dangers else 'None specified'}

DETAILS: {message}
"""
            
            # Submit SOS alert
            result = create_sos_alert(
                st.session_state.user_id,
                location,
                latitude,
                longitude,
                full_message
            )
            
            if result:
                st.success("🚨 SOS ALERT SENT SUCCESSFULLY!")
                st.balloons()
                
                create_alert_box("""
                **Your SOS alert has been sent to all rescue teams!**
                
                - Rescue teams have been notified immediately
                - Your location is now prioritized on the emergency map
                - Keep your phone charged and stay at your location if safe
                - Rescue teams will respond as quickly as possible
                
                **What to do while waiting:**
                - Stay calm and conserve energy
                - Make noise periodically to help rescuers locate you
                - Avoid unnecessary movement that could worsen your situation
                - Keep monitoring the Messages section for rescue team updates
                """, "success")
                
            else:
                st.error("Failed to send SOS alert. Please try again or call emergency services directly.")

def rescue_team_sos_interface():
    """SOS interface for rescue teams"""
    st.write("Monitor and respond to active SOS alerts from flood victims")
    
    # Get active SOS alerts
    sos_alerts = get_active_sos_alerts()
    
    if not sos_alerts:
        st.info("✅ No active SOS alerts at this time.")
        return
    
    st.subheader(f"🚨 Active SOS Alerts ({len(sos_alerts)})")
    
    for alert in sos_alerts:
        alert_id, username, location, lat, lon, message, created_at = alert
        
        with st.expander(f"🆘 SOS Alert from {username} - {location}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **👤 Reporter:** {username}
                **📍 Location:** {location}
                **📌 Coordinates:** {lat:.6f}, {lon:.6f}
                **⏰ Time:** {format_datetime(created_at)}
                
                **💬 Emergency Details:**
                {message}
                """)
                
                # Map link
                if lat and lon:
                    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
                    st.markdown(f"[📍 Open location in Google Maps]({maps_url})")
            
            with col2:
                st.subheader("📞 Quick Response")
                
                # Predefined responses
                response_type = st.selectbox(
                    "Response Type",
                    ["dispatch", "info_request", "safety_advice", "custom"],
                    format_func=lambda x: {
                        "dispatch": "🚁 Dispatch rescue team",
                        "info_request": "❓ Request more information",
                        "safety_advice": "🛡️ Provide safety advice",
                        "custom": "✏️ Custom message"
                    }[x],
                    key=f"response_type_{alert_id}"
                )
                
                if response_type != "custom":
                    if response_type == "dispatch":
                        predefined_messages = [
                            "🚁 Rescue team dispatched to your location, ETA 15-20 minutes",
                            "🛟 Boat rescue team en route, please stay visible",
                            "⚡ Emergency response team activated, help is coming",
                            "🏥 Medical rescue team dispatched with necessary equipment"
                        ]
                    elif response_type == "info_request":
                        predefined_messages = [
                            "📍 Can you provide more specific location details?",
                            "👥 How many people need rescue?",
                            "🏥 Are there any medical emergencies?",
                            "🌊 What is the current water level at your location?"
                        ]
                    else:  # safety_advice
                        predefined_messages = [
                            "🛡️ Stay where you are, avoid moving through flood water",
                            "🔋 Conserve phone battery, help is on the way",
                            "📢 Make noise periodically to help us locate you",
                            "⬆️ Move to higher ground if it's safe to do so"
                        ]
                    
                    selected_message = st.selectbox(
                        "Select message",
                        predefined_messages,
                        key=f"predefined_msg_{alert_id}"
                    )
                    response_message = selected_message
                else:
                    response_message = st.text_area(
                        "Custom response",
                        placeholder="Type your custom response...",
                        key=f"custom_msg_{alert_id}"
                    )
                
                if st.button(f"Send Response", key=f"send_response_{alert_id}"):
                    if response_message:
                        # Send message to the user who created the SOS alert
                        # Note: We'd need to get the user_id from the username
                        # For now, we'll broadcast the message
                        result = send_message(
                            st.session_state.user_id,
                            None,  # Broadcast to all or specific user
                            f"RESCUE TEAM RESPONSE to your SOS alert:\n\n{response_message}",
                            "sos_response",
                            alert_id
                        )
                        
                        if result:
                            st.success("✅ Response sent!")
                        else:
                            st.error("Failed to send response")
                    else:
                        st.error("Please enter a response message")

def government_sos_interface():
    """SOS interface for government officials"""
    st.write("Monitor SOS alert statistics and overall emergency response coordination")
    
    # Get active SOS alerts
    sos_alerts = get_active_sos_alerts()
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active SOS Alerts", len(sos_alerts))
    with col2:
        high_priority = len([a for a in sos_alerts if any(danger in a[5].lower() for danger in ['medical', 'fire', 'collapse'])])
        st.metric("High Priority", high_priority)
    with col3:
        recent_alerts = len([a for a in sos_alerts if a[6] and (datetime.now() - a[6]).seconds < 1800])  # Last 30 min
        st.metric("Last 30 min", recent_alerts)
    with col4:
        st.metric("Response Teams", "12")  # This would come from a rescue teams table
    
    if sos_alerts:
        st.subheader("📊 SOS Alerts Overview")
        
        # Create a simple table view for government monitoring
        alert_data = []
        for alert in sos_alerts:
            alert_id, username, location, lat, lon, message, created_at = alert
            alert_data.append({
                "Time": format_datetime(created_at),
                "Location": location,
                "Reporter": username,
                "Type": message.split('\n')[0].replace('EMERGENCY TYPE: ', '') if 'EMERGENCY TYPE:' in message else 'General',
                "Status": "Active"
            })
        
        import pandas as pd
        df = pd.DataFrame(alert_data)
        st.dataframe(df, use_container_width=True)
        
        # Geographic distribution
        st.subheader("📍 Geographic Distribution")
        if sos_alerts:
            locations = [alert[2] for alert in sos_alerts]
            location_counts = {}
            for loc in locations:
                area = loc.split(',')[0] if ',' in loc else loc
                location_counts[area] = location_counts.get(area, 0) + 1
            
            for area, count in location_counts.items():
                st.write(f"**{area}:** {count} alert(s)")
    else:
        st.success("✅ No active SOS alerts - situation under control")
