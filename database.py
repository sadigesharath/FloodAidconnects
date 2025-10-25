import sqlite3
import os
from datetime import datetime
import streamlit as st

def get_connection():
    """Get database connection using environment variables"""
    try:
        
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def init_database():
    """Initialize database tables"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'citizen',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Status reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS status_reports (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                status VARCHAR(20) NOT NULL,
                location VARCHAR(255),
                latitude FLOAT,
                longitude FLOAT,
                description TEXT,
                photo_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # SOS alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sos_alerts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                location VARCHAR(255),
                latitude FLOAT,
                longitude FLOAT,
                message TEXT,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender_id INTEGER REFERENCES users(id),
                recipient_id INTEGER,
                alert_id INTEGER,
                message TEXT NOT NULL,
                message_type VARCHAR(20) DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Shelters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shelters (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                latitude FLOAT,
                longitude FLOAT,
                capacity INTEGER,
                current_occupancy INTEGER DEFAULT 0,
                status VARCHAR(20) DEFAULT 'available',
                contact_number VARCHAR(20),
                facilities TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Roads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roads (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                status VARCHAR(20) DEFAULT 'open',
                description TEXT,
                latitude FLOAT,
                longitude FLOAT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        
        # Insert default users if not exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            insert_default_data(cursor)
            conn.commit()
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        if conn:
            conn.close()
        return False

def insert_default_data(cursor):
    """Insert default users and sample data"""
    import hashlib
    
    # Default users
    users = [
        ('citizen1', 'password123', 'citizen'),
        ('gov_official', 'admin123', 'government'),
        ('rescue1', 'rescue123', 'rescue_team'),
        ('rescue2', 'rescue123', 'rescue_team')
    ]
    
    for username, password, role in users:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, password_hash, role)
        )
    
    # Default shelters in Hyderabad
    shelters = [
        ('Gachibowli Community Center', 'Gachibowli, Hyderabad', 17.4435, 78.3772, 500, 0, 'available', '+91-9876543210', 'Medical aid, Food, Water, Blankets'),
        ('Hitech City Relief Center', 'Hitech City, Hyderabad', 17.4475, 78.3667, 300, 0, 'available', '+91-9876543211', 'Food, Water, Basic amenities'),
        ('Kukatpally Shelter', 'Kukatpally, Hyderabad', 17.4851, 78.4056, 800, 0, 'available', '+91-9876543212', 'Medical aid, Food, Water, Children care'),
        ('Secunderabad Emergency Center', 'Secunderabad, Hyderabad', 17.5040, 78.4993, 600, 0, 'available', '+91-9876543213', 'Medical aid, Food, Water'),
        ('Old City Relief Point', 'Old City, Hyderabad', 17.3753, 78.4744, 400, 0, 'limited', '+91-9876543214', 'Food, Water')
    ]
    
    for shelter in shelters:
        cursor.execute(
            "INSERT INTO shelters (name, address, latitude, longitude, capacity, current_occupancy, status, contact_number, facilities) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            shelter
        )
    
    # Default roads
    roads = [
        ('Outer Ring Road', 'open', 'Normal traffic conditions', 17.4435, 78.3772),
        ('Jubilee Hills Road', 'blocked', 'Waterlogged - avoid this route', 17.4326, 78.4071),
        ('Banjara Hills Main Road', 'limited', 'Slow moving traffic due to water accumulation', 17.4142, 78.4082),
        ('Madhapur Road', 'open', 'Clear for traffic', 17.4485, 78.3908),
        ('Kondapur Main Road', 'blocked', 'Completely flooded - road closed', 17.4648, 78.3574)
    ]
    
    for road in roads:
        cursor.execute(
            "INSERT INTO roads (name, status, description, latitude, longitude) VALUES (%s, %s, %s, %s, %s)",
            road
        )

# Database operation functions
def execute_query(query, params=None, fetch=False):
    """Execute a database query"""
    conn = get_connection()
    if not conn:
        return [] if fetch else 0
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result or []
        else:
            result = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            return result
        
    except Exception as e:
        st.error(f"Database query failed: {e}")
        if conn:
            conn.close()
        return [] if fetch else 0

def get_user_by_username(username):
    """Get user by username"""
    return execute_query(
        "SELECT id, username, password_hash, role FROM users WHERE username = %s",
        (username,),
        fetch=True
    )

def create_user(username, password_hash, role):
    """Create a new user"""
    return execute_query(
        "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
        (username, password_hash, role)
    )

def create_status_report(user_id, status, location, latitude, longitude, description, photo_path=None):
    """Create a status report"""
    return execute_query(
        "INSERT INTO status_reports (user_id, status, location, latitude, longitude, description, photo_path) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user_id, status, location, latitude, longitude, description, photo_path)
    )

def create_sos_alert(user_id, location, latitude, longitude, message):
    """Create an SOS alert"""
    return execute_query(
        "INSERT INTO sos_alerts (user_id, location, latitude, longitude, message) VALUES (%s, %s, %s, %s, %s)",
        (user_id, location, latitude, longitude, message)
    )

def get_active_sos_alerts():
    """Get all active SOS alerts"""
    return execute_query(
        "SELECT s.id, u.username, s.location, s.latitude, s.longitude, s.message, s.created_at FROM sos_alerts s JOIN users u ON s.user_id = u.id WHERE s.status = 'active' ORDER BY s.created_at DESC",
        fetch=True
    )

def get_shelters():
    """Get all shelters"""
    return execute_query(
        "SELECT * FROM shelters ORDER BY name",
        fetch=True
    )

def get_roads():
    """Get all roads"""
    return execute_query(
        "SELECT * FROM roads ORDER BY name",
        fetch=True
    )

def send_message(sender_id, recipient_id, message, message_type='general', alert_id=None):
    """Send a message"""
    return execute_query(
        "INSERT INTO messages (sender_id, recipient_id, message, message_type, alert_id) VALUES (%s, %s, %s, %s, %s)",
        (sender_id, recipient_id, message, message_type, alert_id)
    )

def get_messages_for_user(user_id):
    """Get messages for a user"""
    return execute_query(
        "SELECT m.*, u.username as sender_name FROM messages m JOIN users u ON m.sender_id = u.id WHERE m.recipient_id = %s OR m.recipient_id IS NULL ORDER BY m.created_at DESC",
        (user_id,),
        fetch=True
    )

def get_status_reports():
    """Get all status reports for dashboard"""
    return execute_query(
        "SELECT s.*, u.username FROM status_reports s JOIN users u ON s.user_id = u.id ORDER BY s.created_at DESC",
        fetch=True
    )
