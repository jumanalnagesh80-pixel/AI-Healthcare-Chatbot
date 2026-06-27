"""
Utility functions for AI Healthcare Chatbot
Real-time features, notifications, and data export
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
from typing import List, Dict
import time


def show_notification(message: str, notification_type: str = "info"):
    """Show a notification banner"""
    if notification_type == "success":
        st.success(message)
    elif notification_type == "error":
        st.error(message)
    elif notification_type == "warning":
        st.warning(message)
    else:
        st.info(message)


def calculate_time_remaining(appointment_date: str, appointment_time: str) -> str:
    """Calculate time remaining until appointment"""
    try:
        # Combine date and time
        appointment_datetime_str = f"{appointment_date} {appointment_time}"
        appointment_datetime = datetime.strptime(appointment_datetime_str, "%Y-%m-%d %I:%M %p")
        
        # Calculate difference
        now = datetime.now()
        time_diff = appointment_datetime - now
        
        if time_diff.total_seconds() < 0:
            return "⏰ Past due"
        
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        
        if days > 0:
            return f"⏳ In {days} day(s) and {hours} hour(s)"
        elif hours > 0:
            return f"⏳ In {hours} hour(s) and {minutes} minute(s)"
        else:
            return f"⏳ In {minutes} minute(s)"
    except Exception as e:
        return "⏰ Invalid time"


def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp to readable format"""
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - timestamp
        
        if diff.seconds < 60:
            return "Just now"
        elif diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f"{minutes} minute(s) ago"
        elif diff.seconds < 86400:
            hours = diff.seconds // 3600
            return f"{hours} hour(s) ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} day(s) ago"
        else:
            return timestamp.strftime("%b %d, %Y")
    except:
        return timestamp_str


def export_to_csv(data: List[Dict], filename: str) -> bytes:
    """Export data to CSV format"""
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')


def export_to_json(data: List[Dict], filename: str) -> str:
    """Export data to JSON format"""
    return json.dumps(data, indent=2, default=str)


def get_activity_icon(activity_type: str) -> str:
    """Get emoji icon for activity type"""
    icons = {
        "login": "🔐",
        "logout": "🚪",
        "user_created": "👤",
        "patient_registered": "📝",
        "appointment_booked": "📅",
        "appointment_updated": "✏️",
        "appointment_deleted": "🗑️",
        "patient_deleted": "🗑️",
        "symptom_checked": "🩺",
        "user_activated": "✅",
        "user_deactivated": "❌",
    }
    return icons.get(activity_type, "📌")


def get_status_color(status: str) -> str:
    """Get color for status"""
    colors = {
        "Scheduled": "🟢",
        "Completed": "🔵",
        "Cancelled": "🔴",
        "Pending": "🟡"
    }
    return colors.get(status, "⚪")


def auto_refresh_component(refresh_interval: int = 30):
    """Add auto-refresh functionality to page"""
    st.markdown(f"""
        <script>
            setTimeout(function(){{
                window.location.reload();
            }}, {refresh_interval * 1000});
        </script>
    """, unsafe_allow_html=True)


def display_live_counter(target_date: str, target_time: str, label: str = "Time remaining"):
    """Display a live countdown timer"""
    try:
        target_datetime_str = f"{target_date} {target_time}"
        target_datetime = datetime.strptime(target_datetime_str, "%Y-%m-%d %I:%M %p")
        now = datetime.now()
        time_diff = target_datetime - now
        
        if time_diff.total_seconds() > 0:
            days = time_diff.days
            hours = time_diff.seconds // 3600
            minutes = (time_diff.seconds % 3600) // 60
            seconds = time_diff.seconds % 60
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Days", days)
            with col2:
                st.metric("Hours", hours)
            with col3:
                st.metric("Minutes", minutes)
            with col4:
                st.metric("Seconds", seconds)
        else:
            st.warning("⏰ Time has passed!")
    except Exception as e:
        st.error(f"Error calculating time: {e}")


def check_upcoming_appointments(appointments: List[Dict]) -> List[str]:
    """Check for upcoming appointments and generate reminders"""
    reminders = []
    now = datetime.now()
    
    for apt in appointments:
        try:
            apt_datetime_str = f"{apt['date']} {apt['time']}"
            apt_datetime = datetime.strptime(apt_datetime_str, "%Y-%m-%d %I:%M %p")
            time_diff = apt_datetime - now
            
            # Reminder for appointments in next 24 hours
            if 0 < time_diff.total_seconds() < 86400:
                hours_remaining = time_diff.total_seconds() / 3600
                reminders.append(
                    f"⏰ Reminder: {apt['patient_name']} has an appointment with {apt['specialty']} "
                    f"in {int(hours_remaining)} hours at {apt['time']}"
                )
            # Urgent reminder for appointments in next hour
            elif 0 < time_diff.total_seconds() < 3600:
                minutes_remaining = time_diff.total_seconds() / 60
                reminders.append(
                    f"🚨 URGENT: {apt['patient_name']} has an appointment with {apt['specialty']} "
                    f"in {int(minutes_remaining)} minutes!"
                )
        except:
            continue
    
    return reminders


def display_notification_banner(notifications: List[str]):
    """Display notification banner at top of page"""
    if notifications:
        with st.container():
            for notification in notifications:
                if "URGENT" in notification:
                    st.error(notification)
                else:
                    st.info(notification)


def get_system_health() -> Dict:
    """Get system health metrics"""
    from database import db
    
    stats = db.get_statistics()
    
    # Calculate health score
    health_score = 100
    warnings = []
    
    # Check for issues
    if stats.get('active_users', 0) == 0:
        health_score -= 20
        warnings.append("⚠️ No active users in system")
    
    if stats.get('todays_appointments', 0) == 0:
        warnings.append("ℹ️ No appointments scheduled for today")
    
    if stats.get('total_patients', 0) < 5:
        warnings.append("ℹ️ Low patient count - system in early stage")
    
    status = "🟢 Healthy" if health_score >= 80 else "🟡 Warning" if health_score >= 60 else "🔴 Critical"
    
    return {
        "score": health_score,
        "status": status,
        "warnings": warnings,
        "stats": stats
    }


def create_live_chart_data(appointments: List[Dict]) -> pd.DataFrame:
    """Create data for real-time charts"""
    if not appointments:
        return pd.DataFrame()
    
    df = pd.DataFrame(appointments)
    
    # Count by specialty
    specialty_counts = df['specialty'].value_counts().reset_index()
    specialty_counts.columns = ['Specialty', 'Count']
    
    return specialty_counts


def validate_search_query(query: str) -> bool:
    """Validate search query"""
    if not query or len(query.strip()) < 2:
        return False
    return True


def highlight_search_results(text: str, query: str) -> str:
    """Highlight search query in text"""
    if query and query.lower() in text.lower():
        highlighted = text.replace(query, f"**{query}**")
        return highlighted
    return text


def format_file_size(bytes_size: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def get_activity_summary(activities: List[Dict]) -> Dict:
    """Get summary of activities"""
    if not activities:
        return {"total": 0, "by_type": {}, "by_user": {}}
    
    summary = {
        "total": len(activities),
        "by_type": {},
        "by_user": {}
    }
    
    for activity in activities:
        activity_type = activity['activity_type']
        username = activity['username']
        
        summary['by_type'][activity_type] = summary['by_type'].get(activity_type, 0) + 1
        summary['by_user'][username] = summary['by_user'].get(username, 0) + 1
    
    return summary
