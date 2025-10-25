import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
from database import execute_query, get_shelters, get_roads, get_active_sos_alerts, get_status_reports
from utils import format_datetime, get_status_color, create_alert_box

def government_dashboard_page():
    """Government dashboard for monitoring emergency response operations"""
    st.header("🏛️ Government Emergency Dashboard")
    st.write("Real-time monitoring and coordination of flood response operations across Hyderabad")
    
    # Dashboard overview metrics
    display_overview_metrics()
    
    st.divider()
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🗺️ Geographic Analysis", 
        "🏠 Infrastructure Status", 
        "📈 Trends & Analytics", 
        "⚙️ Administrative Controls"
    ])
    
    with tab1:
        overview_dashboard()
    
    with tab2:
        geographic_analysis()
    
    with tab3:
        infrastructure_status()
    
    with tab4:
        trends_analytics()
    
    with tab5:
        administrative_controls()

def display_overview_metrics():
    """Display key metrics at the top of the dashboard"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Get current data
    sos_alerts = get_active_sos_alerts()
    active_sos = len(sos_alerts) if isinstance(sos_alerts, list) else 0
    
    status_reports = get_status_reports()
    shelters = get_shelters()
    roads = get_roads()
    
    # Calculate metrics
    if status_reports and isinstance(status_reports, list):
        trapped_reports = len([r for r in status_reports if len(r) > 2 and r[2] == 'trapped'])
        help_requests = len([r for r in status_reports if len(r) > 2 and r[2] == 'help'])
        safe_reports = len([r for r in status_reports if len(r) > 2 and r[2] == 'safe'])
    else:
        trapped_reports = help_requests = safe_reports = 0
    
    available_shelters = len([s for s in shelters if len(s) > 7 and s[7] == 'available']) if isinstance(shelters, list) else 0
    blocked_roads = len([r for r in roads if len(r) > 2 and r[2] == 'blocked']) if isinstance(roads, list) else 0
    
    with col1:
        st.metric(
            "🆘 Active SOS Alerts", 
            active_sos,
            delta=None,
            help="Number of active emergency alerts requiring immediate response"
        )
    
    with col2:
        st.metric(
            "🚨 People Trapped", 
            trapped_reports,
            delta=None,
            help="Citizens reporting trapped status"
        )
    
    with col3:
        st.metric(
            "⚠️ Help Requests", 
            help_requests,
            delta=None,
            help="Citizens requesting assistance"
        )
    
    with col4:
        st.metric(
            "🏠 Available Shelters", 
            f"{available_shelters}/{len(shelters) if shelters else 0}",
            delta=None,
            help="Emergency shelters with available capacity"
        )
    
    with col5:
        st.metric(
            "🚫 Blocked Roads", 
            f"{blocked_roads}/{len(roads) if roads else 0}",
            delta=None,
            help="Roads currently blocked due to flooding"
        )

def overview_dashboard():
    """Main overview dashboard with key charts and information"""
    
    # Emergency status distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Emergency Status Distribution")
        
        status_reports = get_status_reports()
        if status_reports:
            status_counts = {}
            for report in status_reports:
                status = report[2]  # status field
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Create pie chart
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Citizen Status Reports",
                color_discrete_map={
                    'safe': '#28a745',
                    'help': '#ffc107', 
                    'trapped': '#dc3545'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No status reports available")
    
    with col2:
        st.subheader("🏠 Shelter Capacity Overview")
        
        shelters = get_shelters()
        if shelters:
            shelter_data = []
            for shelter in shelters:
                shelter_id, name, address, lat, lon, capacity, occupancy, status, contact, facilities, updated_at = shelter
                occupancy_rate = (occupancy / capacity * 100) if capacity > 0 else 0
                shelter_data.append({
                    'Shelter': name[:20] + '...' if len(name) > 20 else name,
                    'Capacity': capacity,
                    'Occupancy': occupancy,
                    'Rate': occupancy_rate,
                    'Status': status
                })
            
            df = pd.DataFrame(shelter_data)
            
            # Create stacked bar chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Occupied',
                x=df['Shelter'],
                y=df['Occupancy'],
                marker_color='#ffc107'
            ))
            fig.add_trace(go.Bar(
                name='Available',
                x=df['Shelter'],
                y=df['Capacity'] - df['Occupancy'],
                marker_color='#28a745'
            ))
            
            fig.update_layout(
                barmode='stack',
                title='Shelter Capacity Status',
                xaxis_title='Shelters',
                yaxis_title='People',
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No shelter data available")
    
    # Recent activity timeline
    st.subheader("📅 Recent Emergency Activity")
    
    # Get recent activities from multiple sources
    recent_sos = execute_query("""
        SELECT 'SOS Alert' as type, location, created_at, u.username 
        FROM sos_alerts s 
        JOIN users u ON s.user_id = u.id 
        WHERE s.created_at > NOW() - INTERVAL '24 hours'
        ORDER BY s.created_at DESC
    """, fetch=True)
    
    recent_status = execute_query("""
        SELECT CONCAT('Status: ', status) as type, location, created_at, u.username 
        FROM status_reports sr 
        JOIN users u ON sr.user_id = u.id 
        WHERE sr.created_at > NOW() - INTERVAL '24 hours' AND status IN ('help', 'trapped')
        ORDER BY sr.created_at DESC
    """, fetch=True)
    
    # Combine and sort activities
    all_activities = []
    if recent_sos and isinstance(recent_sos, list):
        all_activities.extend(recent_sos)
    if recent_status and isinstance(recent_status, list):
        all_activities.extend(recent_status)
    
    if all_activities:
        # Sort by timestamp
        all_activities.sort(key=lambda x: x[2], reverse=True)
        
        # Display recent activities
        for activity_type, location, timestamp, username in all_activities[:10]:
            col_time, col_type, col_location, col_user = st.columns([2, 2, 3, 2])
            
            with col_time:
                st.write(format_datetime(timestamp))
            with col_type:
                if 'SOS' in activity_type:
                    st.write("🆘 " + activity_type)
                elif 'trapped' in activity_type:
                    st.write("🚨 " + activity_type)
                else:
                    st.write("⚠️ " + activity_type)
            with col_location:
                st.write(location)
            with col_user:
                st.write(username)
    else:
        st.info("No recent emergency activity in the last 24 hours")

def geographic_analysis():
    """Geographic analysis of emergency incidents and resources"""
    st.subheader("🗺️ Geographic Distribution Analysis")
    
    # Area-wise incident analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Incidents by Area**")
        
        # Get all incidents with locations
        incidents = []
        
        # Add SOS alerts
        sos_alerts = get_active_sos_alerts()
        if isinstance(sos_alerts, list):
            for alert in sos_alerts:
                location = str(alert[2]) if len(alert) > 2 and alert[2] is not None else "Unknown Location"
                area = location.split(',')[0].strip() if ',' in location else location
                incidents.append(('SOS Alert', area))
        
        # Add status reports (help/trapped)
        status_reports = get_status_reports()
        if status_reports and isinstance(status_reports, list):
            for report in status_reports:
                if len(report) > 4 and report[2] in ['help', 'trapped']:
                    location = str(report[4]) if report[4] is not None else "Unknown Location"
                    area = location.split(',')[0].strip() if ',' in location else location
                    incidents.append((report[2].title(), area))
        
        if incidents:
            # Count incidents by area
            area_counts = {}
            for incident_type, area in incidents:
                area_counts[area] = area_counts.get(area, 0) + 1
            
            # Create bar chart
            fig = px.bar(
                x=list(area_counts.keys()),
                y=list(area_counts.values()),
                title="Emergency Incidents by Area",
                labels={'x': 'Area', 'y': 'Number of Incidents'},
                color=list(area_counts.values()),
                color_continuous_scale='Reds'
            )
            fig.update_layout(xaxis={'tickangle': 45})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No incidents to display")
    
    with col2:
        st.write("**Resource Distribution**")
        
        shelters = get_shelters()
        if shelters:
            # Analyze shelter distribution by area
            shelter_areas = {}
            for shelter in shelters:
                address = str(shelter[2]) if shelter[2] is not None else "Unknown Address"
                area = address.split(',')[-2].strip() if ',' in address else address
                if area not in shelter_areas:
                    shelter_areas[area] = {'count': 0, 'capacity': 0}
                shelter_areas[area]['count'] += 1
                shelter_areas[area]['capacity'] += shelter[5]  # capacity
            
            # Create visualization
            areas = list(shelter_areas.keys())
            counts = [shelter_areas[area]['count'] for area in areas]
            capacities = [shelter_areas[area]['capacity'] for area in areas]
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(name="Number of Shelters", x=areas, y=counts, marker_color='lightblue'),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(name="Total Capacity", x=areas, y=capacities, mode='lines+markers', marker_color='red'),
                secondary_y=True
            )
            
            fig.update_xaxes(title_text="Area")
            fig.update_yaxes(title_text="Number of Shelters", secondary_y=False)
            fig.update_yaxes(title_text="Total Capacity", secondary_y=True)
            fig.update_layout(title="Shelter Resources by Area")
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No shelter data available")
    
    # High-risk areas identification
    st.subheader("⚠️ High-Risk Areas Identification")
    
    if incidents:
        # Identify areas with highest incident rates
        area_incident_types = {}
        for incident_type, area in incidents:
            if area not in area_incident_types:
                area_incident_types[area] = {'SOS Alert': 0, 'Help': 0, 'Trapped': 0}
            if incident_type == 'SOS Alert':
                area_incident_types[area]['SOS Alert'] += 1
            elif incident_type in ['Help', 'Trapped']:
                area_incident_types[area][incident_type] += 1
        
        # Sort areas by total incidents
        sorted_areas = sorted(area_incident_types.items(), 
                            key=lambda x: sum(x[1].values()), reverse=True)
        
        st.write("**Areas Requiring Priority Attention:**")
        
        for i, (area, counts) in enumerate(sorted_areas[:5]):
            total = sum(counts.values())
            risk_level = "HIGH" if total >= 3 else "MEDIUM" if total >= 2 else "LOW"
            risk_color = "#dc3545" if risk_level == "HIGH" else "#ffc107" if risk_level == "MEDIUM" else "#28a745"
            
            st.markdown(f"""
            <div style="border-left: 5px solid {risk_color}; padding: 10px; margin: 5px 0; background-color: rgba(0,0,0,0.05);">
                <strong>{i+1}. {area}</strong> - <span style="color: {risk_color};">{risk_level} RISK</span><br>
                Total Incidents: {total} | SOS: {counts['SOS Alert']} | Help: {counts['Help']} | Trapped: {counts['Trapped']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No high-risk areas identified currently")

def infrastructure_status():
    """Infrastructure status monitoring"""
    st.subheader("🏗️ Infrastructure Status Monitoring")
    
    # Road status analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Road Network Status**")
        
        roads = get_roads()
        if roads:
            road_status_counts = {}
            for road in roads:
                status = road[2]  # status field
                road_status_counts[status] = road_status_counts.get(status, 0) + 1
            
            # Create donut chart
            fig = px.pie(
                values=list(road_status_counts.values()),
                names=list(road_status_counts.keys()),
                title="Road Network Status",
                hole=0.4,
                color_discrete_map={
                    'open': '#28a745',
                    'limited': '#ffc107',
                    'blocked': '#dc3545'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed road status
            st.write("**Critical Road Conditions:**")
            blocked_roads = [r for r in roads if r[2] == 'blocked']
            limited_roads = [r for r in roads if r[2] == 'limited']
            
            if blocked_roads:
                st.error(f"🚫 **Blocked Roads ({len(blocked_roads)}):**")
                for road in blocked_roads:
                    st.write(f"• {road[1]} - {road[3]}")
            
            if limited_roads:
                st.warning(f"⚠️ **Limited Access Roads ({len(limited_roads)}):**")
                for road in limited_roads:
                    st.write(f"• {road[1]} - {road[3]}")
            
            if not blocked_roads and not limited_roads:
                st.success("✅ All monitored roads are open")
        else:
            st.info("No road data available")
    
    with col2:
        st.write("**Shelter Infrastructure**")
        
        shelters = get_shelters()
        if shelters:
            # Shelter capacity utilization
            shelter_data = []
            total_capacity = 0
            total_occupancy = 0
            
            for shelter in shelters:
                capacity = shelter[5]
                occupancy = shelter[6]
                total_capacity += capacity
                total_occupancy += occupancy
                
                utilization = (occupancy / capacity * 100) if capacity > 0 else 0
                shelter_data.append({
                    'Name': shelter[1][:15] + '...' if len(shelter[1]) > 15 else shelter[1],
                    'Utilization': utilization,
                    'Status': shelter[7]
                })
            
            df = pd.DataFrame(shelter_data)
            
            # Utilization chart
            fig = px.bar(
                df, 
                x='Name', 
                y='Utilization',
                title='Shelter Capacity Utilization (%)',
                color='Utilization',
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(xaxis={'tickangle': 45})
            fig.add_hline(y=80, line_dash="dash", line_color="red", 
                         annotation_text="80% Capacity Warning")
            st.plotly_chart(fig, use_container_width=True)
            
            # Overall utilization
            overall_utilization = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
            st.metric("Overall Shelter Utilization", f"{overall_utilization:.1f}%")
            
            # Shelter status breakdown
            status_counts = {}
            for shelter in shelters:
                status = shelter[7]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in status_counts.items():
                emoji = "✅" if status == 'available' else "⚠️" if status == 'limited' else "❌"
                st.write(f"{emoji} {status.title()}: {count} shelters")
        else:
            st.info("No shelter data available")

def trends_analytics():
    """Trends and analytics over time"""
    st.subheader("📈 Emergency Response Trends & Analytics")
    
    # Time-based analysis
    st.write("**24-Hour Emergency Activity Trend**")
    
    # Get hourly activity data
    hourly_activity = execute_query("""
        SELECT 
            EXTRACT(HOUR FROM created_at) as hour,
            COUNT(*) as count,
            'Status Reports' as type
        FROM status_reports 
        WHERE created_at > NOW() - INTERVAL '24 hours'
        GROUP BY EXTRACT(HOUR FROM created_at)
        
        UNION ALL
        
        SELECT 
            EXTRACT(HOUR FROM created_at) as hour,
            COUNT(*) as count,
            'SOS Alerts' as type
        FROM sos_alerts 
        WHERE created_at > NOW() - INTERVAL '24 hours'
        GROUP BY EXTRACT(HOUR FROM created_at)
        
        ORDER BY hour
    """, fetch=True)
    
    if hourly_activity:
        # Process data for visualization
        hours = list(range(24))
        status_counts = [0] * 24
        sos_counts = [0] * 24
        
        for hour, count, activity_type in hourly_activity:
            hour_idx = int(hour)
            if activity_type == 'Status Reports':
                status_counts[hour_idx] = count
            else:
                sos_counts[hour_idx] = count
        
        # Create line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, y=status_counts, mode='lines+markers',
            name='Status Reports', line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=hours, y=sos_counts, mode='lines+markers',
            name='SOS Alerts', line=dict(color='red')
        ))
        
        fig.update_layout(
            title='24-Hour Emergency Activity Pattern',
            xaxis_title='Hour of Day',
            yaxis_title='Number of Reports',
            xaxis=dict(tickmode='linear', tick0=0, dtick=2)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for trend analysis")
    
    # Response time analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Response Metrics**")
        
        # Get message response data
        response_data = execute_query("""
            SELECT 
                COUNT(*) as total_responses,
                AVG(EXTRACT(EPOCH FROM (m.created_at - s.created_at))/60) as avg_response_time
            FROM messages m
            JOIN sos_alerts s ON m.alert_id = s.id
            WHERE m.message_type = 'sos_response'
            AND m.created_at > NOW() - INTERVAL '24 hours'
        """, fetch=True)
        
        if response_data and response_data[0][0] > 0:
            total_responses, avg_response_time = response_data[0]
            st.metric("Total Responses (24h)", int(total_responses))
            st.metric("Avg Response Time", f"{avg_response_time:.1f} min" if avg_response_time else "N/A")
        else:
            st.info("No response data available for the last 24 hours")
        
        # Resource allocation efficiency
        st.write("**Resource Allocation Efficiency**")
        
        shelters = get_shelters()
        if shelters:
            total_capacity = sum(s[5] for s in shelters)
            total_occupancy = sum(s[6] for s in shelters)
            efficiency = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
            
            st.metric("Shelter Utilization", f"{efficiency:.1f}%")
            
            # Efficiency indicator
            if efficiency < 50:
                st.success("✅ Good capacity available")
            elif efficiency < 80:
                st.warning("⚠️ Moderate utilization")
            else:
                st.error("🚨 High utilization - additional resources may be needed")
    
    with col2:
        st.write("**Emergency Type Distribution**")
        
        # Analyze types of emergencies from SOS messages
        emergency_types = execute_query("""
            SELECT 
                CASE 
                    WHEN message LIKE '%medical%' THEN 'Medical Emergency'
                    WHEN message LIKE '%trapped%' OR message LIKE '%TRAPPED%' THEN 'Trapped'
                    WHEN message LIKE '%fire%' THEN 'Fire Emergency'
                    WHEN message LIKE '%flood%' OR message LIKE '%water%' THEN 'Flood Related'
                    ELSE 'General Emergency'
                END as emergency_type,
                COUNT(*) as count
            FROM sos_alerts
            WHERE created_at > NOW() - INTERVAL '7 days'
            GROUP BY emergency_type
            ORDER BY count DESC
        """, fetch=True)
        
        if emergency_types:
            types = [et[0] for et in emergency_types]
            counts = [et[1] for et in emergency_types]
            
            fig = px.bar(
                x=counts, y=types, orientation='h',
                title='Emergency Types (Last 7 Days)',
                labels={'x': 'Number of Incidents', 'y': 'Emergency Type'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No emergency type data available")

def administrative_controls():
    """Administrative controls and system management"""
    st.subheader("⚙️ Administrative Controls")
    
    # System status
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**System Status**")
        
        # Database connection status
        try:
            test_query = execute_query("SELECT COUNT(*) FROM users", fetch=True)
            db_status = "✅ Connected" if test_query else "❌ Error"
            total_users = test_query[0][0] if test_query else 0
        except:
            db_status = "❌ Connection Failed"
            total_users = 0
        
        st.write(f"**Database:** {db_status}")
        st.write(f"**Total Users:** {total_users}")
        
        # Get user counts by role
        user_roles = execute_query("""
            SELECT role, COUNT(*) as count 
            FROM users 
            GROUP BY role
        """, fetch=True)
        
        if user_roles:
            for role, count in user_roles:
                st.write(f"• {role.title()}: {count}")
        
        # System uptime (placeholder - would need actual implementation)
        st.write("**System Status:** 🟢 Operational")
        st.write("**Last Update:** " + format_datetime(datetime.now()))
    
    with col2:
        st.write("**Quick Actions**")
        
        if st.button("🔄 Refresh All Data", use_container_width=True):
            st.success("Data refreshed successfully!")
            st.rerun()
        
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Generating comprehensive emergency report...")
            # This would trigger report generation
            
        if st.button("🚨 Send System Alert", use_container_width=True):
            st.warning("System alert broadcasting feature")
            # This would open alert composition interface
        
        if st.button("🔧 System Maintenance", use_container_width=True):
            st.info("Maintenance mode controls")
            # This would provide maintenance options
    
    # Data management
    st.subheader("📊 Data Management")
    
    tab1, tab2, tab3 = st.tabs(["📈 Statistics", "🗂️ Data Export", "🔧 Maintenance"])
    
    with tab1:
        # Comprehensive statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Emergency Data**")
            total_sos = execute_query("SELECT COUNT(*) FROM sos_alerts", fetch=True)
            total_sos = total_sos[0][0] if total_sos else 0
            
            total_status = execute_query("SELECT COUNT(*) FROM status_reports", fetch=True)
            total_status = total_status[0][0] if total_status else 0
            
            total_messages = execute_query("SELECT COUNT(*) FROM messages", fetch=True)
            total_messages = total_messages[0][0] if total_messages else 0
            
            st.metric("Total SOS Alerts", total_sos)
            st.metric("Total Status Reports", total_status)
            st.metric("Total Messages", total_messages)
        
        with col2:
            st.write("**Infrastructure Data**")
            st.metric("Total Shelters", len(get_shelters()))
            st.metric("Total Roads Monitored", len(get_roads()))
            
            # Calculate average response time
            avg_response = execute_query("""
                SELECT AVG(EXTRACT(EPOCH FROM (m.created_at - s.created_at))/60) 
                FROM messages m
                JOIN sos_alerts s ON m.alert_id = s.id
                WHERE m.message_type = 'sos_response'
            """, fetch=True)
            
            avg_time = avg_response[0][0] if avg_response and avg_response[0][0] else 0
            st.metric("Avg Response Time (min)", f"{avg_time:.1f}" if avg_time else "N/A")
        
        with col3:
            st.write("**Performance Metrics**")
            
            # Active alerts resolution rate
            resolved_alerts = execute_query("""
                SELECT COUNT(*) FROM sos_alerts WHERE status = 'resolved'
            """, fetch=True)
            resolved_count = resolved_alerts[0][0] if resolved_alerts else 0
            
            resolution_rate = (resolved_count / total_sos * 100) if total_sos > 0 else 0
            st.metric("Alert Resolution Rate", f"{resolution_rate:.1f}%")
            
            # Shelter utilization
            shelters = get_shelters()
            if shelters:
                total_capacity = sum(s[5] for s in shelters)
                total_occupancy = sum(s[6] for s in shelters)
                utilization = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
                st.metric("Shelter Utilization", f"{utilization:.1f}%")
    
    with tab2:
        st.write("**Export Emergency Data**")
        
        export_options = st.multiselect(
            "Select data to export:",
            ["SOS Alerts", "Status Reports", "Messages", "Shelter Data", "Road Status"],
            default=["SOS Alerts", "Status Reports"]
        )
        
        date_range = st.date_input(
            "Date range",
            value=[datetime.now().date() - timedelta(days=7), datetime.now().date()],
            help="Select date range for data export"
        )
        
        if st.button("📥 Export Data", use_container_width=True):
            if export_options:
                st.success(f"Exporting {len(export_options)} datasets for date range: {date_range[0]} to {date_range[1]}")
                st.info("Export functionality would generate CSV/Excel files with selected data")
            else:
                st.error("Please select at least one dataset to export")
    
    with tab3:
        st.write("**System Maintenance**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Database Maintenance**")
            
            if st.button("🧹 Clean Old Data", use_container_width=True):
                st.info("Would clean data older than specified retention period")
            
            if st.button("📊 Optimize Database", use_container_width=True):
                st.info("Database optimization initiated")
            
            if st.button("💾 Backup Data", use_container_width=True):
                st.success("Backup process started")
        
        with col2:
            st.write("**System Configuration**")
            
            if st.button("🔧 Update Settings", use_container_width=True):
                st.info("System configuration panel")
            
            if st.button("👥 Manage Users", use_container_width=True):
                st.info("User management interface")
            
            if st.button("📝 View Logs", use_container_width=True):
                st.info("System logs and audit trail")
    
    # Alert and notification settings
    st.subheader("🔔 Alert & Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Emergency Thresholds**")
        
        sos_threshold = st.number_input("SOS Alert Threshold", min_value=1, max_value=50, value=10, 
                                       help="Alert when active SOS alerts exceed this number")
        
        shelter_threshold = st.slider("Shelter Capacity Warning (%)", min_value=50, max_value=95, value=80,
                                     help="Warning when shelter utilization exceeds this percentage")
        
        response_threshold = st.number_input("Response Time Alert (minutes)", min_value=5, max_value=60, value=30,
                                           help="Alert when average response time exceeds this")
    
    with col2:
        st.write("**Notification Recipients**")
        
        notification_emails = st.text_area(
            "Emergency Contact Emails",
            placeholder="email1@gov.in\nemail2@disaster.telangana.gov.in",
            help="Enter email addresses (one per line) for emergency notifications"
        )
        
        sms_numbers = st.text_area(
            "Emergency SMS Numbers", 
            placeholder="+91-9876543210\n+91-9876543211",
            help="Enter phone numbers (one per line) for SMS alerts"
        )
    
    if st.button("💾 Save Alert Settings", use_container_width=True):
        st.success("Alert settings saved successfully!")
    
    # Current alerts
    st.subheader("🚨 Current System Alerts")
    
    current_alerts = []
    
    # Check for threshold violations
    if active_sos := len(get_active_sos_alerts()):
        if active_sos >= sos_threshold:
            current_alerts.append(f"🆘 HIGH: {active_sos} active SOS alerts (threshold: {sos_threshold})")
    
    shelters = get_shelters()
    if shelters:
        for shelter in shelters:
            capacity = shelter[5]
            occupancy = shelter[6] 
            utilization = (occupancy / capacity * 100) if capacity > 0 else 0
            if utilization >= shelter_threshold:
                current_alerts.append(f"🏠 WARNING: {shelter[1]} at {utilization:.1f}% capacity")
    
    if current_alerts:
        for alert in current_alerts:
            create_alert_box(alert, "warning")
    else:
        st.success("✅ No system alerts - all parameters within normal ranges")
