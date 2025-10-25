import streamlit as st
from database import get_shelters
from utils import get_status_emoji, get_status_color, format_phone_number

def shelters_page():
    """Shelters page showing available emergency shelters"""
    st.header("🏠 Emergency Shelters")
    st.write("Find nearby emergency shelters and check their current availability")
    
    # Get shelter data
    shelters = get_shelters()
    
    if not shelters:
        st.error("Unable to load shelter information. Please try again later.")
        return
    
    # Filter and sort options
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Availability",
            ["all", "available", "limited", "full"],
            format_func=lambda x: {
                "all": "All Shelters",
                "available": "Available",
                "limited": "Limited Space",
                "full": "Full"
            }[x]
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["name", "capacity", "occupancy_rate"],
            format_func=lambda x: {
                "name": "Name",
                "capacity": "Capacity",
                "occupancy_rate": "Occupancy Rate"
            }[x]
        )
    
    # Filter shelters
    filtered_shelters = shelters
    if status_filter != "all":
        filtered_shelters = [s for s in shelters if s[7] == status_filter]
    
    # Sort shelters
    if sort_by == "name":
        filtered_shelters = sorted(filtered_shelters, key=lambda x: x[1])
    elif sort_by == "capacity":
        filtered_shelters = sorted(filtered_shelters, key=lambda x: x[5], reverse=True)
    elif sort_by == "occupancy_rate":
        filtered_shelters = sorted(filtered_shelters, key=lambda x: (x[6]/x[5] if x[5] > 0 else 0))
    
    # Summary statistics
    st.subheader("📊 Shelter Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_capacity = sum(s[5] for s in shelters)
    total_occupancy = sum(s[6] for s in shelters)
    available_shelters = len([s for s in shelters if s[7] == 'available'])
    
    with col1:
        st.metric("Total Shelters", len(shelters))
    with col2:
        st.metric("Available", available_shelters)
    with col3:
        st.metric("Total Capacity", total_capacity)
    with col4:
        occupancy_rate = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
        st.metric("Overall Occupancy", f"{occupancy_rate:.1f}%")
    
    st.divider()
    
    # Display shelters
    st.subheader(f"📋 Shelter List ({len(filtered_shelters)} shelters)")
    
    if not filtered_shelters:
        st.warning("No shelters match your current filter criteria.")
        return
    
    for shelter in filtered_shelters:
        shelter_id, name, address, lat, lon, capacity, occupancy, status, contact, facilities, updated_at = shelter
        
        # Calculate occupancy rate
        occupancy_rate = (occupancy / capacity * 100) if capacity > 0 else 0
        
        # Status color and emoji
        status_emoji = get_status_emoji(status)
        status_color = get_status_color(status)
        
        # Create expandable container for each shelter
        with st.expander(f"{status_emoji} {name} - {status.title()}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **📍 Address:** {address}
                
                **📞 Contact:** {format_phone_number(contact)}
                
                **👥 Capacity:** {occupancy}/{capacity} people ({occupancy_rate:.1f}% full)
                
                **🛠️ Facilities:** {facilities}
                
                **⏰ Last Updated:** {updated_at.strftime('%Y-%m-%d %H:%M') if updated_at else 'N/A'}
                """)
                
                # Status-specific information
                if status == 'available':
                    st.success(f"✅ {capacity - occupancy} spaces available")
                elif status == 'limited':
                    st.warning(f"⚠️ Limited space: {capacity - occupancy} spaces left")
                else:
                    st.error("❌ No spaces currently available")
            
            with col2:
                # Progress bar for occupancy
                st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
                st.progress(occupancy_rate / 100)
                
                # Quick action buttons
                if st.session_state.user_role == "rescue_team":
                    if st.button(f"Update {name}", key=f"update_{shelter_id}"):
                        st.info("Shelter update feature would be implemented here")
                
                # Directions button (placeholder)
                if st.button(f"Get Directions", key=f"directions_{shelter_id}"):
                    if lat and lon:
                        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
                        st.markdown(f"[Open in Google Maps]({maps_url})")
                    else:
                        st.error("Location coordinates not available")
    
    st.divider()
    
    # Emergency shelter guidelines
    st.subheader("📋 Shelter Guidelines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Before Going to a Shelter:**
        - Check availability status above
        - Call the shelter to confirm space
        - Bring essential documents (ID, medical records)
        - Pack emergency supplies (medications, clothes)
        - Inform family members of your location
        """)
    
    with col2:
        st.markdown("""
        **What to Expect:**
        - Basic sleeping arrangements
        - Food and water provisions
        - Medical assistance if needed
        - Communication facilities
        - Safety and security measures
        """)
    
    # Emergency contacts for shelters
    st.subheader("📞 Shelter Coordination Contacts")
    
    emergency_contacts = [
        ("Shelter Coordination Center", "+91-9876543200", "24/7 shelter information and booking"),
        ("Emergency Transport Service", "+91-9876543201", "Transportation to shelters"),
        ("Medical Emergency (Shelters)", "+91-9876543202", "Medical assistance at shelters"),
        ("Disaster Management Office", "+91-9876543203", "General disaster management queries")
    ]
    
    for name, phone, description in emergency_contacts:
        col1, col2, col3 = st.columns([2, 1.5, 2])
        with col1:
            st.write(f"**{name}**")
        with col2:
            st.code(phone)
        with col3:
            st.write(description)
    
    # Map integration notice
    st.info("💡 **Tip:** Visit the Emergency Map section to see shelter locations and get visual directions.")
