"""
Pytest configuration and fixtures for AI Healthcare Chatbot tests
"""
import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_modern import app, db, socketio
from database import User, Appointment, Prescription, ChatMessage, HealthGoal


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test users
            create_test_data()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def socketio_client(client):
    """Create a test client for Socket.IO"""
    return socketio.test_client(app, flask_test_client=client)


@pytest.fixture
def auth_headers(client):
    """Get authentication headers for a logged-in user"""
    # Register and login
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'phone': '1234567890'
    })
    
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    return {'Content-Type': 'application/json'}


@pytest.fixture
def admin_headers(client):
    """Get authentication headers for an admin user"""
    with app.app_context():
        # Create admin user
        admin = User(
            name='Admin User',
            email='admin@example.com',
            phone='9999999999',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    # Login as admin
    client.post('/login', data={
        'email': 'admin@example.com',
        'password': 'admin123'
    })
    
    return {'Content-Type': 'application/json'}


def create_test_data():
    """Create test data in the database"""
    # Create regular user
    user = User(
        name='John Doe',
        email='john@example.com',
        phone='5555555555',
        role='patient'
    )
    user.set_password('password123')
    db.session.add(user)
    
    # Create doctor user
    doctor = User(
        name='Dr. Smith',
        email='doctor@example.com',
        phone='5555555556',
        role='doctor'
    )
    doctor.set_password('doctor123')
    db.session.add(doctor)
    
    db.session.commit()
    
    # Create test appointment
    appointment = Appointment(
        user_id=user.id,
        doctor_name='Dr. Smith',
        date=datetime.now(),
        time='10:00 AM',
        reason='Checkup',
        status='scheduled'
    )
    db.session.add(appointment)
    
    # Create test prescription
    prescription = Prescription(
        user_id=user.id,
        doctor_name='Dr. Smith',
        medication='Aspirin',
        dosage='100mg',
        frequency='Once daily',
        duration='7 days'
    )
    db.session.add(prescription)
    
    # Create test chat message
    message = ChatMessage(
        user_id=user.id,
        message='Hello',
        response='Hi! How can I help you?',
        timestamp=datetime.now()
    )
    db.session.add(message)
    
    # Create test health goal
    goal = HealthGoal(
        user_id=user.id,
        title='Lose Weight',
        description='Lose 10 pounds',
        goal_type='weight_loss',
        target_value=10.0,
        current_value=0.0,
        unit='lbs',
        target_date=datetime.now(),
        priority='high',
        status='active'
    )
    db.session.add(goal)
    
    db.session.commit()
