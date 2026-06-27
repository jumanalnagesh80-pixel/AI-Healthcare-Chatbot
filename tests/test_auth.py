"""
Tests for authentication functionality
"""
import pytest
from app_modern import app, db
from database import User


class TestAuthentication:
    """Test authentication flows"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/register', data={
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        with app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.name == 'New User'
            assert user.check_password('password123')
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # Register first user
        client.post('/register', data={
            'name': 'User One',
            'email': 'duplicate@example.com',
            'password': 'password123',
            'phone': '1111111111'
        })
        
        # Try to register with same email
        response = client.post('/register', data={
            'name': 'User Two',
            'email': 'duplicate@example.com',
            'password': 'password456',
            'phone': '2222222222'
        }, follow_redirects=True)
        
        assert b'Email already registered' in response.data or b'already exists' in response.data
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user
        client.post('/register', data={
            'name': 'Login User',
            'email': 'login@example.com',
            'password': 'password123',
            'phone': '3333333333'
        })
        
        # Login
        response = client.post('/login', data={
            'email': 'login@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'dashboard' in response.data.lower() or b'welcome' in response.data.lower()
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        # Register user
        client.post('/register', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'phone': '4444444444'
        })
        
        # Try to login with wrong password
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Invalid' in response.data or b'incorrect' in response.data.lower()
    
    def test_logout(self, client):
        """Test logout functionality"""
        # Register and login
        client.post('/register', data={
            'name': 'Logout User',
            'email': 'logout@example.com',
            'password': 'password123',
            'phone': '5555555555'
        })
        client.post('/login', data={
            'email': 'logout@example.com',
            'password': 'password123'
        })
        
        # Logout
        response = client.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'login' in response.data.lower() or b'sign in' in response.data.lower()
    
    def test_protected_route_requires_login(self, client):
        """Test that protected routes require authentication"""
        response = client.get('/dashboard', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'login' in response.data.lower() or b'sign in' in response.data.lower()
