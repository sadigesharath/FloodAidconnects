import streamlit as st
from datetime import datetime
from database import get_messages_for_user, send_message, execute_query
from utils import format_datetime, create_alert_box, get_rescue_team_responses

def messaging_page():
    """Messaging page for communication between users and rescue teams"""
    st.header("💬 Emergency Messages")
    
    if st.session_state.user_role == "citizen":
        citizen_messaging_interface()
    elif st.session_state.user_role == "rescue_team":
        rescue_team_messaging_interface()
    else:  # government
        government_messaging_interface()

def citizen_messaging_interface():
    """Messaging interface for citizens"""
    st.write("Receive updates from rescue teams and emergency services")
    
    # Get messages for the user
    messages = get_messages_for_user(st.session_state.user_id)
    
    # Message statistics
    col1, col2, col3 = st.columns(3)
    
    if messages:
        sos_responses = [m for m in messages if m[4] == 'sos_response']
        general_messages = [m for m in messages if m[4] == 'general']
        alerts = [m for m in messages if m[4] == 'alert']
    else:
        sos_responses = general_messages = alerts = []
    
    with col1:
        st.metric("SOS Responses", len(sos_responses))
    with col2:
        st.metric("General Messages", len(general_messages))
    with col3:
        st.metric("Emergency Alerts", len(alerts))
    
    st.divider()
    
    # Display messages
    if not messages:
        st.info("📭 No messages yet. Messages from rescue teams and emergency services will appear here.")
        
        # Show sample message format
        st.subheader("📝 What to expect:")
        st.markdown("""
        **You will receive messages for:**
        - Responses to your SOS alerts
        - Updates on your status reports
        - General emergency information
        - Evacuation instructions
        - Rescue team coordination
        """)
        
    else:
        st.subheader(f"📬 Your Messages ({len(messages)})")
        
        # Message filter
        message_filter = st.selectbox(
            "Filter messages",
            ["all", "sos_response", "general", "alert"],
            format_func=lambda x: {
                "all": "All Messages",
                "sos_response": "SOS Responses",
                "general": "General Messages", 
                "alert": "Emergency Alerts"
            }[x]
        )
        
        # Filter messages
        if message_filter != "all":
            filtered_messages = [m for m in messages if m[4] == message_filter]
        else:
            filtered_messages = messages
        
        # Display filtered messages
        for message in filtered_messages:
            message_id, sender_id, recipient_id, alert_id, message_text, message_type, created_at, sender_name = message
            
            # Message styling based on type
            if message_type == "sos_response":
                st.markdown(f"""
                <div style="background-color: #e8f5e8; border-left: 5px solid #28a745; padding: 1rem; margin: 1rem 0; border-radius: 0 10px 10px 0;">
                    <h4 style="color: #155724; margin: 0 0 0.5rem 0;">🆘 SOS Response from {sender_name}</h4>
                    <p style="margin: 0; color: #155724;">{message_text}</p>
                    <small style="color: #6c757d;">📅 {format_datetime(created_at)}</small>
                </div>
                """, unsafe_allow_html=True)
            
            elif message_type == "alert":
                st.markdown(f"""
                <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 1rem; margin: 1rem 0; border-radius: 0 10px 10px 0;">
                    <h4 style="color: #856404; margin: 0 0 0.5rem 0;">⚠️ Emergency Alert</h4>
                    <p style="margin: 0; color: #856404;">{message_text}</p>
                    <small style="color: #6c757d;">📅 {format_datetime(created_at)}</small>
                </div>
                """, unsafe_allow_html=True)
            
            else:  # general
                st.markdown(f"""
                <div style="background-color: #d1ecf1; border-left: 5px solid #17a2b8; padding: 1rem; margin: 1rem 0; border-radius: 0 10px 10px 0;">
                    <h4 style="color: #0c5460; margin: 0 0 0.5rem 0;">💬 Message from {sender_name}</h4>
                    <p style="margin: 0; color: #0c5460;">{message_text}</p>
                    <small style="color: #6c757d;">📅 {format_datetime(created_at)}</small>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Emergency communication tips
    st.subheader("📱 Emergency Communication Tips")
    
    with st.expander("Communication Guidelines"):
        st.markdown("""
        **To ensure effective communication:**
        
        - **Keep your phone charged** - Use power-saving mode during emergencies
        - **Check messages regularly** - Rescue teams may send time-sensitive updates
        - **Save important numbers** - Have backup communication methods ready
        - **Be specific in reports** - Provide clear location and situation details
        - **Follow instructions** - Rescue teams provide expert guidance
        
        **If you don't receive responses:**
        - Network congestion is common during disasters
        - Emergency services prioritize life-threatening situations
        - Keep reporting your status if conditions change
        - Use alternative communication methods if available
        """)

def rescue_team_messaging_interface():
    """Messaging interface for rescue teams"""
    st.write("Send messages and responses to citizens and coordinate with other teams")
    
    # Message composition section
    st.subheader("📝 Send Message")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Message type
        message_type = st.selectbox(
            "Message Type",
            ["broadcast", "sos_response", "individual"],
            format_func=lambda x: {
                "broadcast": "📢 Broadcast to All Citizens",
                "sos_response": "🆘 Response to SOS Alert",
                "individual": "👤 Individual Message"
            }[x]
        )
        
        if message_type == "broadcast":
            st.write("**Send message to all citizens in affected areas**")
            message_content = st.text_area(
                "Broadcast Message",
                placeholder="Enter emergency information, evacuation instructions, or safety updates...",
                height=100
            )
            
        elif message_type == "sos_response":
            # Get active SOS alerts for response
            sos_alerts = execute_query(
                "SELECT id, location, message FROM sos_alerts WHERE status = 'active' ORDER BY created_at DESC",
                fetch=True
            )
            
            if sos_alerts:
                selected_alert = st.selectbox(
                    "Select SOS Alert to Respond to",
                    sos_alerts,
                    format_func=lambda x: f"Alert #{x[0]} - {x[1]} - {x[2][:50]}..."
                )
                
                # Predefined responses
                predefined_response = st.selectbox(
                    "Quick Response Template",
                    ["custom"] + get_rescue_team_responses()
                )
                
                if predefined_response == "custom":
                    message_content = st.text_area(
                        "Custom Response",
                        placeholder="Enter your response to the SOS alert...",
                        height=100
                    )
                else:
                    message_content = predefined_response
                    st.text_area("Response Preview", value=message_content, height=100, disabled=True)
            else:
                st.info("No active SOS alerts to respond to.")
                message_content = ""
        
        else:  # individual
            # Get list of users who have submitted reports or SOS alerts
            recent_users = execute_query("""
                SELECT DISTINCT u.id, u.username 
                FROM users u 
                WHERE u.id IN (
                    SELECT user_id FROM status_reports WHERE created_at > NOW() - INTERVAL '24 hours'
                    UNION 
                    SELECT user_id FROM sos_alerts WHERE created_at > NOW() - INTERVAL '24 hours'
                ) AND u.role = 'citizen'
            """, fetch=True)
            
            if recent_users:
                selected_user = st.selectbox(
                    "Select Recipient",
                    recent_users,
                    format_func=lambda x: x[1]
                )
                
                message_content = st.text_area(
                    "Individual Message",
                    placeholder="Enter message for the selected user...",
                    height=100
                )
            else:
                st.info("No recent citizen reports to respond to.")
                message_content = ""
    
    with col2:
        st.subheader("📋 Quick Actions")
        
        if st.button("🚁 Dispatch Team", use_container_width=True):
            st.session_state.quick_message = "🚁 Rescue team has been dispatched to your location. Please stay where you are and remain calm. Help is on the way."
        
        if st.button("📍 Request Location", use_container_width=True):
            st.session_state.quick_message = "📍 Please provide more specific location details to help us reach you faster. Include building name, floor number, and nearby landmarks."
        
        if st.button("🛡️ Safety Instructions", use_container_width=True):
            st.session_state.quick_message = "🛡️ For your safety: Stay where you are, avoid moving through flood water, conserve phone battery, and make noise periodically to help us locate you."
        
        if st.button("🏥 Medical Help", use_container_width=True):
            st.session_state.quick_message = "🏥 Medical assistance team is being arranged. If you have immediate medical needs, please specify the nature of the emergency."
        
        # Apply quick message if selected
        if hasattr(st.session_state, 'quick_message'):
            message_content = st.session_state.quick_message
            del st.session_state.quick_message
    
    # Send message button
    if st.button("📤 Send Message", type="primary", use_container_width=True):
        if message_content:
            if message_type == "broadcast":
                # Send to all citizens (recipient_id = None for broadcast)
                result = send_message(
                    st.session_state.user_id,
                    None,
                    f"EMERGENCY BROADCAST:\n\n{message_content}",
                    "alert"
                )
                
            elif message_type == "sos_response" and sos_alerts:
                # Send response to SOS alert
                alert_id = selected_alert[0]
                result = send_message(
                    st.session_state.user_id,
                    None,  # Would need to get user_id from alert
                    f"RESCUE TEAM RESPONSE:\n\n{message_content}",
                    "sos_response",
                    alert_id
                )
                
            elif message_type == "individual" and recent_users:
                # Send to specific user
                user_id = selected_user[0]
                result = send_message(
                    st.session_state.user_id,
                    user_id,
                    message_content,
                    "general"
                )
            else:
                result = False
            
            if result:
                st.success("✅ Message sent successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to send message. Please try again.")
        else:
            st.error("Please enter a message to send.")
    
    st.divider()
    
    # Recent messages sent
    st.subheader("📤 Recent Messages Sent")
    
    recent_sent = execute_query(
        "SELECT message, message_type, created_at FROM messages WHERE sender_id = %s ORDER BY created_at DESC LIMIT 10",
        (st.session_state.user_id,),
        fetch=True
    )
    
    if recent_sent:
        for message_text, msg_type, created_at in recent_sent:
            st.markdown(f"""
            **{msg_type.replace('_', ' ').title()}** - {format_datetime(created_at)}
            > {message_text[:100]}{'...' if len(message_text) > 100 else ''}
            """)
    else:
        st.info("No recent messages sent.")

def government_messaging_interface():
    """Messaging interface for government officials"""
    st.write("Monitor communication patterns and send official emergency broadcasts")
    
    # Communication statistics
    st.subheader("📊 Communication Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get statistics
    total_messages = execute_query("SELECT COUNT(*) FROM messages", fetch=True)[0][0] if execute_query("SELECT COUNT(*) FROM messages", fetch=True) else 0
    sos_responses = execute_query("SELECT COUNT(*) FROM messages WHERE message_type = 'sos_response'", fetch=True)[0][0] if execute_query("SELECT COUNT(*) FROM messages WHERE message_type = 'sos_response'", fetch=True) else 0
    broadcasts = execute_query("SELECT COUNT(*) FROM messages WHERE message_type = 'alert'", fetch=True)[0][0] if execute_query("SELECT COUNT(*) FROM messages WHERE message_type = 'alert'", fetch=True) else 0
    
    with col1:
        st.metric("Total Messages", total_messages)
    with col2:
        st.metric("SOS Responses", sos_responses)
    with col3:
        st.metric("Broadcasts Sent", broadcasts)
    with col4:
        active_rescue_teams = execute_query("SELECT COUNT(*) FROM users WHERE role = 'rescue_team'", fetch=True)[0][0] if execute_query("SELECT COUNT(*) FROM users WHERE role = 'rescue_team'", fetch=True) else 0
        st.metric("Active Rescue Teams", active_rescue_teams)
    
    st.divider()
    
    # Official broadcast section
    st.subheader("📢 Send Official Emergency Broadcast")
    
    with st.form("government_broadcast"):
        broadcast_type = st.selectbox(
            "Broadcast Type",
            ["general_alert", "evacuation_order", "shelter_info", "weather_update", "all_clear"],
            format_func=lambda x: {
                "general_alert": "⚠️ General Emergency Alert",
                "evacuation_order": "🚨 Evacuation Order",
                "shelter_info": "🏠 Shelter Information Update",
                "weather_update": "🌧️ Weather Update",
                "all_clear": "✅ All Clear Notice"
            }[x]
        )
        
        priority = st.selectbox(
            "Priority Level",
            ["high", "medium", "low"],
            format_func=lambda x: x.upper()
        )
        
        area_affected = st.multiselect(
            "Areas Affected",
            ["Gachibowli", "Hitech City", "Jubilee Hills", "Banjara Hills", "Kondapur", "Madhapur", "Secunderabad", "Old City", "All Hyderabad"],
            default=["All Hyderabad"]
        )
        
        broadcast_message = st.text_area(
            "Official Broadcast Message",
            placeholder="Enter official emergency broadcast message...",
            height=150,
            help="This message will be sent to all citizens and rescue teams"
        )
        
        # Message preview
        if broadcast_message:
            preview_text = f"""
**OFFICIAL EMERGENCY BROADCAST - {priority.upper()} PRIORITY**

**Type:** {broadcast_type.replace('_', ' ').title()}
**Areas:** {', '.join(area_affected)}
**Issued by:** Telangana Emergency Management

{broadcast_message}

**Time:** {format_datetime(datetime.now())}
**Contact:** Emergency Operations Center: +91-40-2345-1111
"""
            
            st.subheader("📄 Message Preview")
            st.markdown(preview_text)
        
        submitted = st.form_submit_button("📡 Send Official Broadcast", type="primary")
        
        if submitted:
            if broadcast_message:
                # Create official broadcast message
                official_message = f"""
OFFICIAL EMERGENCY BROADCAST - {priority.upper()} PRIORITY

Type: {broadcast_type.replace('_', ' ').title()}
Areas: {', '.join(area_affected)}
Issued by: Telangana Emergency Management

{broadcast_message}

Contact Emergency Operations Center: +91-40-2345-1111
"""
                
                result = send_message(
                    st.session_state.user_id,
                    None,  # Broadcast to all
                    official_message,
                    "alert"
                )
                
                if result:
                    st.success("✅ Official broadcast sent successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to send broadcast. Please try again.")
            else:
                st.error("Please enter a broadcast message.")
    
    st.divider()
    
    # Recent activity monitoring
    st.subheader("📊 Recent Communication Activity")
    
    # Get recent messages for monitoring
    recent_activity = execute_query("""
        SELECT m.message, m.message_type, m.created_at, u.username, u.role 
        FROM messages m 
        JOIN users u ON m.sender_id = u.id 
        ORDER BY m.created_at DESC 
        LIMIT 20
    """, fetch=True)
    
    if recent_activity:
        import pandas as pd
        
        activity_data = []
        for message, msg_type, created_at, username, role in recent_activity:
            activity_data.append({
                "Time": format_datetime(created_at),
                "Type": msg_type.replace('_', ' ').title(),
                "Sender": f"{username} ({role})",
                "Message": message[:50] + "..." if len(message) > 50 else message
            })
        
        df = pd.DataFrame(activity_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No recent communication activity.")
    
    # Communication guidelines
    st.subheader("📋 Government Communication Guidelines")
    
    with st.expander("Official Broadcasting Guidelines"):
        st.markdown("""
        **When to send official broadcasts:**
        - Immediate threats to public safety
        - Evacuation orders or shelter-in-place instructions  
        - Critical infrastructure failures
        - Weather warnings and updates
        - All-clear notifications after emergency ends
        
        **Message formatting requirements:**
        - Clear, concise, and actionable language
        - Specific geographic areas affected
        - Official contact information included
        - Time-sensitive information clearly marked
        - Multiple language versions for diverse populations
        
        **Priority levels:**
        - **HIGH:** Immediate life-threatening situations
        - **MEDIUM:** Significant safety concerns
        - **LOW:** General information and updates
        """)
