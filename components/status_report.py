import streamlit as st
from database import create_status_report
from utils import process_uploaded_image, create_alert_box, get_hyderabad_coordinates

def status_report_page():
    """Status report page for citizens to report their safety status"""
    st.header("📊 Safety Status Report")
    st.write("Report your current safety status to help rescue teams coordinate efforts.")
    
    # Current status display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🟢 Safe Reports", "145", "+12")
    with col2:
        st.metric("🟡 Need Help", "23", "+5")
    with col3:
        st.metric("🔴 Trapped", "8", "+2")
    
    st.divider()
    
    # Status reporting form
    st.subheader("📝 Report Your Status")
    
    with st.form("status_report_form"):
        # Status selection
        status = st.selectbox(
            "Your Current Status",
            ["safe", "help", "trapped"],
            format_func=lambda x: {
                "safe": "✅ I'm Safe",
                "help": "⚠️ I Need Help",
                "trapped": "🆘 I'm Trapped"
            }[x],
            help="Select your current safety status"
        )
        
        # Location information
        st.subheader("📍 Location Information")
        location = st.text_input(
            "Location Description",
            placeholder="e.g., Gachibowli, Building name, Floor number",
            help="Provide as much detail as possible about your location"
        )
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            latitude = st.number_input(
                "Latitude",
                value=17.3850,
                format="%.6f",
                help="Your current latitude coordinate"
            )
        with col_lon:
            longitude = st.number_input(
                "Longitude", 
                value=78.4867,
                format="%.6f",
                help="Your current longitude coordinate"
            )
        
        # Description
        description = st.text_area(
            "Additional Details",
            placeholder="Describe your situation, number of people with you, immediate needs, etc.",
            help="Any additional information that might help rescue teams"
        )
        
        # Photo upload
        st.subheader("📸 Photo Evidence")
        uploaded_file = st.file_uploader(
            "Upload a photo of your current situation",
            type=['png', 'jpg', 'jpeg'],
            help="Photos help rescue teams assess the situation better"
        )
        
        # Display uploaded image preview
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Photo preview", width=300)
        
        # Submit button
        submitted = st.form_submit_button(
            "🚨 Submit Status Report",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not location:
                st.error("Please provide location information!")
                return
            
            # Process uploaded image
            photo_data = None
            if uploaded_file is not None:
                photo_data = process_uploaded_image(uploaded_file)
            
            # Submit to database
            result = create_status_report(
                st.session_state.user_id,
                status,
                location,
                latitude,
                longitude,
                description,
                photo_data
            )
            
            if result:
                status_text = {
                    "safe": "✅ Safe status reported successfully!",
                    "help": "⚠️ Help request submitted! Rescue teams have been notified.",
                    "trapped": "🆘 Emergency alert sent! Rescue teams are being dispatched."
                }
                
                create_alert_box(status_text[status], "success")
                
                if status in ["help", "trapped"]:
                    st.balloons()
                    st.markdown("""
                    **What happens next:**
                    - Rescue teams have been automatically notified
                    - Your location has been added to the emergency map
                    - You will receive updates in the Messages section
                    - Keep your phone charged and stay where you are if safe
                    """)
            else:
                st.error("Failed to submit status report. Please try again.")
    
    st.divider()
    
    # Safety tips
    st.subheader("🛡️ Safety Tips During Floods")
    
    with st.expander("Emergency Safety Guidelines"):
        st.markdown("""
        **If you're safe:**
        - Stay indoors and avoid unnecessary travel
        - Keep monitoring weather updates
        - Charge your devices and keep emergency supplies ready
        
        **If you need help:**
        - Stay calm and report your exact location
        - Conserve phone battery for emergency communications
        - Signal for help using bright clothing or flashlight
        
        **If you're trapped:**
        - Don't panic - help is on the way
        - Stay put unless moving to higher ground is absolutely safe
        - Make noise to help rescuers locate you
        - Avoid electrical equipment and standing water
        """)
    
    # Recent status updates
    st.subheader("📈 Recent Status Updates")
    
    # Mock recent updates display
    with st.container():
        st.write("**Latest reports from your area:**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write("🕐 **Time**")
        with col2:
            st.write("📍 **Location**")
        with col3:
            st.write("📊 **Status**")
        
        # Sample recent reports
        recent_reports = [
            ("2 min ago", "Gachibowli Main Road", "safe"),
            ("5 min ago", "Hitech City", "help"),
            ("8 min ago", "Jubilee Hills", "safe"),
            ("12 min ago", "Kondapur", "trapped")
        ]
        
        for time, loc, stat in recent_reports:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(time)
            with col2:
                st.write(loc)
            with col3:
                if stat == "safe":
                    st.write("✅ Safe")
                elif stat == "help":
                    st.write("⚠️ Need Help")
                else:
                    st.write("🆘 Trapped")
