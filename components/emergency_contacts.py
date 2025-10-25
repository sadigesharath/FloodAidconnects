import streamlit as st
from utils import format_phone_number

def emergency_contacts_page():
    """Emergency contacts page with Hyderabad-specific contacts"""
    st.header("📞 Emergency Contacts")
    st.write("Important emergency contact numbers for Hyderabad flood response")
    
    # Quick emergency numbers at the top
    st.subheader("🚨 Quick Emergency Numbers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a52); padding: 1.5rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.2rem;">🚨 POLICE</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">100</h2>
            <p style="margin: 0; font-size: 0.9rem;">All Emergency Services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ecdc4, #44a08d); padding: 1.5rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.2rem;">🚑 MEDICAL</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">108</h2>
            <p style="margin: 0; font-size: 0.9rem;">Ambulance Services</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #45b7d1, #2980b9); padding: 1.5rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 1.2rem;">🔥 FIRE</h3>
            <h2 style="margin: 0.5rem 0; font-size: 2rem;">101</h2>
            <p style="margin: 0; font-size: 0.9rem;">Fire & Rescue</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Detailed emergency contacts
    tabs = st.tabs(["🏥 Hospitals", "🚔 Police Stations", "🛟 Rescue Teams", "🏛️ Government", "🚁 Emergency Services"])
    
    with tabs[0]:  # Hospitals
        st.subheader("🏥 Major Hospitals in Hyderabad")
        st.write("Emergency contact numbers for major hospitals with flood response capabilities")
        
        hospitals = [
            {
                "name": "Apollo Hospitals",
                "emergency": "+91 40 2345 6789",
                "ambulance": "+91-40-2360-3470",
                "address": "Road No. 72, Jubilee Hills, Hyderabad",
                "facilities": "24/7 Emergency, ICU, Trauma Center, Helicopter Landing"
            },
            {
                "name": "Yashoda Hospitals",
                "emergency": "+91 40 2233 4455",
                "ambulance": "+91-40-4777-7777",
                "address": "Behind Hari Haran Kala Mandir, SP Road, Secunderabad",
                "facilities": "Multi-specialty Emergency, Advanced ICU, Disaster Response"
            },
            {
                "name": "Apollo Hospital Hyderguda",
                "emergency": "+91-40-2378-8888",
                "ambulance": "+91-40-2378-8889",
                "address": "Hyderguda, Near LB Stadium, Hyderabad",
                "facilities": "Emergency Medicine, Critical Care, Blood Bank"
            },
            {
                "name": "Continental Hospitals Gachibowli",
                "emergency": "+91-40-6715-4444",
                "ambulance": "+91-40-6715-4445",
                "address": "IT Park Road, Nanakramguda, Gachibowli, Hyderabad",
                "facilities": "Trauma Center, Emergency Surgery, Advanced Life Support"
            },
            {
                "name": "KIMS Hospital Kondapur",
                "emergency": "+91-40-4463-4000",
                "ambulance": "+91-40-4463-4001",
                "address": "Minister Road, Kondapur, Hyderabad",
                "facilities": "Emergency Department, Critical Care, Flood Response Unit"
            },
            {
                "name": "Global Hospitals Lakdi-ka-pul",
                "emergency": "+91-40-2330-7777",
                "ambulance": "+91-40-2330-7778",
                "address": "Lakdi-ka-pul, Hyderabad",
                "facilities": "Emergency Services, Intensive Care, Emergency Surgery"
            }
        ]
        
        for hospital in hospitals:
            with st.expander(f"🏥 {hospital['name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **📍 Address:** {hospital['address']}
                    
                    **🚑 Emergency:** {format_phone_number(hospital['emergency'])}
                    
                    **🚨 Ambulance:** {format_phone_number(hospital['ambulance'])}
                    
                    **🏥 Facilities:** {hospital['facilities']}
                    """)
                
                with col2:
                    if st.button(f"Call Emergency", key=f"call_hospital_{hospital['name']}"):
                        st.info(f"Call: {hospital['emergency']}")
                    if st.button(f"Call Ambulance", key=f"ambulance_{hospital['name']}"):
                        st.info(f"Call: {hospital['ambulance']}")
    
    with tabs[1]:  # Police Stations
        st.subheader("🚔 Police Stations & Emergency Response")
        st.write("Police stations with flood response and emergency coordination capabilities")
        
        police_stations = [
            {
                "name": "Central Police Station",
                "emergency": "+91 40 2755 1234",
                "control_room": "+91-40-2719-8445",
                "address": "Gachibowli, Hyderabad",
                "jurisdiction": "Gachibowli, Kondapur, Madhapur, Hitech City",
                "special": "Disaster Response Unit, Water Rescue Team"
            },
            {
                "name": "Traffic Police Hyderabad",
                "emergency": "+91 40 2344 7788",
                "control_room": "+91-40-2785-4445",
                "address": "Basheerbagh, Hyderabad",
                "jurisdiction": "Central Hyderabad, Old City, Secunderabad",
                "special": "Emergency Response Wing, Flood Control Unit"
            },
            {
                "name": "Rachakonda Police Commissionerate",
                "emergency": "+91-40-2717-8444",
                "control_room": "+91-40-2717-8445",
                "address": "Neredmet, Hyderabad",
                "jurisdiction": "LB Nagar, Uppal, Nagole, Hayathnagar",
                "special": "Quick Response Team, Emergency Services"
            },
            {
                "name": "Jubilee Hills Police Station",
                "emergency": "+91-40-2360-3456",
                "control_room": "+91-40-2360-3457",
                "address": "Road No. 36, Jubilee Hills, Hyderabad",
                "jurisdiction": "Jubilee Hills, Banjara Hills, Film Nagar",
                "special": "VIP Security, Emergency Response"
            },
            {
                "name": "Secunderabad Police Station",
                "emergency": "+91-40-2784-0123",
                "control_room": "+91-40-2784-0124",
                "address": "SP Road, Secunderabad",
                "jurisdiction": "Secunderabad, Trimulgherry, Alwal",
                "special": "Railway Security, Flood Response"
            }
        ]
        
        for station in police_stations:
            with st.expander(f"🚔 {station['name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **📍 Address:** {station['address']}
                    
                    **🚨 Emergency:** {format_phone_number(station['emergency'])}
                    
                    **📞 Control Room:** {format_phone_number(station['control_room'])}
                    
                    **🗺️ Jurisdiction:** {station['jurisdiction']}
                    
                    **⭐ Special Units:** {station['special']}
                    """)
                
                with col2:
                    if st.button(f"Call Emergency", key=f"call_police_{station['name']}"):
                        st.info(f"Call: {station['emergency']}")
                    if st.button(f"Control Room", key=f"control_{station['name']}"):
                        st.info(f"Call: {station['control_room']}")
    
    with tabs[2]:  # Rescue Teams
        st.subheader("🛟 Specialized Rescue Teams")
        st.write("Professional rescue teams trained for flood and disaster response")
        
        rescue_teams = [
            {
                "name": "Rescue Team",
                "emergency": "+91 40 9999 888899",
                "coordinator": "+91-40-2345-6790",
                "address": "Secretariat, Hyderabad",
                "specialization": "Water Rescue, Building Collapse, High-Angle Rescue",
                "equipment": "Boats, Helicopters, Advanced Life Support, Heavy Machinery"
            },
            {
                "name": "National Disaster Response Force (NDRF) - Hyderabad",
                "emergency": "+91-40-2987-6543",
                "coordinator": "+91-40-2987-6544",
                "address": "NDRF Campus, Chegunta, Medak District",
                "specialization": "Flood Rescue, Chemical Hazards, Urban Search & Rescue",
                "equipment": "Specialized Boats, Diving Equipment, Medical Support"
            },
            {
                "name": "Hyderabad Fire & Rescue Services",
                "emergency": "101",
                "coordinator": "+91-40-2456-7890",
                "address": "Fire Station, Koti, Hyderabad",
                "specialization": "Fire Fighting, Water Rescue, Technical Rescue",
                "equipment": "Fire Engines, Rescue Boats, Hydraulic Tools"
            },
            {
                "name": "108 Emergency Medical Services",
                "emergency": "108",
                "coordinator": "+91-40-3456-7891",
                "address": "Multiple locations across Hyderabad",
                "specialization": "Medical Emergency, Patient Transport, Advanced Life Support",
                "equipment": "Ambulances, Medical Equipment, Paramedic Teams"
            },
            {
                "name": "Volunteer Rescue Groups Hyderabad",
                "emergency": "+91-9876-543-210",
                "coordinator": "+91-9876-543-211",
                "address": "Various locations",
                "specialization": "Community Response, First Aid, Evacuation Support",
                "equipment": "Basic Rescue Equipment, First Aid Supplies, Communication"
            }
        ]
        
        for team in rescue_teams:
            with st.expander(f"🛟 {team['name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **📍 Base Location:** {team['address']}
                    
                    **🚨 Emergency:** {format_phone_number(team['emergency'])}
                    
                    **👤 Coordinator:** {format_phone_number(team['coordinator'])}
                    
                    **🎯 Specialization:** {team['specialization']}
                    
                    **🛠️ Equipment:** {team['equipment']}
                    """)
                
                with col2:
                    if st.button(f"Emergency Call", key=f"rescue_{team['name']}"):
                        st.info(f"Call: {team['emergency']}")
    
    with tabs[3]:  # Government
        st.subheader("🏛️ Government Emergency Contacts")
        st.write("Government departments and officials for disaster management coordination")
        
        govt_contacts = [
            {
                "department": "Telangana State Emergency Operations Center",
                "emergency": "+91-40-2345-1111",
                "office": "+91-40-2345-1112",
                "head": "Director, Emergency Management",
                "address": "Secretariat, Hyderabad",
                "services": "Overall disaster coordination, Resource allocation, Inter-agency coordination"
            },
            {
                "department": "Greater Hyderabad Municipal Corporation (GHMC)",
                "emergency": "+91-40-2111-2222",
                "office": "+91-40-2111-2223",
                "head": "Commissioner, GHMC",
                "address": "GHMC Head Office, Hyderabad",
                "services": "Urban flood management, Drainage, Municipal services"
            },
            {
                "department": "Hyderabad Metropolitan Water Supply (HMWS&SB)",
                "emergency": "+91-40-2322-3333",
                "office": "+91-40-2322-3334",
                "head": "Managing Director, HMWS&SB",
                "address": "Khairatabad, Hyderabad",
                "services": "Water supply, Sewerage, Pump house operations"
            },
            {
                "department": "Revenue Department - Disaster Management",
                "emergency": "+91-40-2433-4444",
                "office": "+91-40-2433-4445",
                "head": "Principal Secretary, Revenue",
                "address": "Secretariat, Hyderabad",
                "services": "Relief operations, Compensation, Damage assessment"
            },
            {
                "department": "Telangana State Road Transport Corporation (TSRTC)",
                "emergency": "+91-40-2544-5555",
                "office": "+91-40-2544-5556",
                "head": "Managing Director, TSRTC",
                "address": "RTC House, Hyderabad",
                "services": "Emergency transport, Evacuation buses, Route diversions"
            }
        ]
        
        for dept in govt_contacts:
            with st.expander(f"🏛️ {dept['department']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **📍 Address:** {dept['address']}
                    
                    **🚨 Emergency:** {format_phone_number(dept['emergency'])}
                    
                    **📞 Office:** {format_phone_number(dept['office'])}
                    
                    **👤 Head:** {dept['head']}
                    
                    **🛠️ Services:** {dept['services']}
                    """)
                
                with col2:
                    if st.button(f"Emergency", key=f"govt_emergency_{dept['department']}"):
                        st.info(f"Call: {dept['emergency']}")
                    if st.button(f"Office", key=f"govt_office_{dept['department']}"):
                        st.info(f"Call: {dept['office']}")
    
    with tabs[4]:  # Emergency Services
        st.subheader("🚁 Specialized Emergency Services")
        st.write("Additional emergency services and utilities")
        
        emergency_services = [
            {
                "service": "Helicopter Emergency Medical Service (HEMS)",
                "number": "+91-40-2655-7777",
                "available": "24/7",
                "coverage": "Hyderabad Metropolitan Area",
                "description": "Air ambulance and aerial rescue operations"
            },
            {
                "service": "Emergency Power Restoration (TSSPDCL)",
                "number": "+91-40-2766-8888",
                "available": "24/7",
                "coverage": "Telangana State",
                "description": "Power outage reporting and emergency restoration"
            },
            {
                "service": "Gas Leak Emergency (IOCL/HPCL)",
                "number": "+91-40-2877-9999",
                "available": "24/7",
                "coverage": "Hyderabad City",
                "description": "Gas leak reporting and emergency response"
            },
            {
                "service": "Telecommunications Emergency (BSNL)",
                "number": "+91-40-2988-0000",
                "available": "24/7",
                "coverage": "Hyderabad Circle",
                "description": "Communication infrastructure and emergency connectivity"
            },
            {
                "service": "Emergency Food & Water Distribution",
                "number": "+91-40-3099-1111",
                "available": "During emergencies",
                "coverage": "GHMC Area",
                "description": "Emergency relief supplies and distribution"
            },
            {
                "service": "Animal Rescue Emergency",
                "number": "+91-40-3100-2222",
                "available": "Daylight hours",
                "coverage": "Hyderabad City",
                "description": "Pet and livestock rescue during floods"
            }
        ]
        
        for service in emergency_services:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{service['service']}**")
                st.write(service['description'])
            
            with col2:
                st.code(service['number'])
                st.write(f"Available: {service['available']}")
            
            with col3:
                st.write(f"Coverage: {service['coverage']}")
                if st.button("Call", key=f"service_{service['service']}"):
                    st.info(f"Calling: {service['number']}")
    
    st.divider()
    
    # Important notes
    st.subheader("📋 Important Emergency Guidelines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **When to Call Emergency Numbers:**
        - Life-threatening situations
        - Immediate danger to multiple people
        - Natural disaster emergency
        - Major accidents or incidents
        - When you need immediate professional help
        """)
    
    with col2:
        st.markdown("""
        **What Information to Provide:**
        - Your exact location (address, landmarks)
        - Nature of emergency
        - Number of people involved
        - Your contact number
        - Any immediate dangers present
        """)
    
    # Quick reference card
    st.subheader("💳 Quick Reference Emergency Card")
    st.markdown("""
    **Keep these numbers saved in your phone:**
    - **Police Emergency:** 100
    - **Medical Emergency:** 108  
    - **Fire Emergency:** 101
    - **Women Helpline:** 1091
    - **Disaster Management:** +91-40-2345-1111
    - **GHMC Emergency:** +91-40-2111-2222
    """)
    
    st.info("💡 **Tip:** Save these numbers in your phone before an emergency occurs. During floods, network connectivity may be limited.")
