"""
Tests for admin panel functionality
"""
import pytest
import json
from app_modern import app, db
from database import User


class TestAdminPanel:
    """Test admin panel features"""
    
    def test_admin_access_denied_for_regular_user(self, client, auth_headers):
        """Test that regular users cannot access admin panel"""
        response = client.get('/admin')
        
        # Should redirect to login or show unauthorized
        assert response.status_code in [302, 401, 403] or b'Unauthorized' in response.data
    
    def test_admin_access_granted_for_admin(self, client, admin_headers):
        """Test that admin users can access admin panel"""
        response = client.get('/admin')
        
        # Should allow access
        assert response.status_code == 200
        assert b'admin' in response.data.lower() or b'dashboard' in response.data.lower()
    
    def test_admin_get_all_users(self, client, admin_headers):
        """Test getting all users as admin"""
        response = client.get('/api/admin/users')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0  # Should have at least the admin user
    
    def test_admin_get_stats(self, client, admin_headers):
        """Test getting system statistics"""
        response = client.get('/api/admin/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_users' in data
        assert 'total_appointments' in data
        assert 'total_messages' in data
    
    def test_admin_cannot_be_accessed_without_login(self, client):
        """Test that admin routes require authentication"""
        response = client.get('/api/admin/users', follow_redirects=True)
        
        # Should redirect to login or return unauthorized
        assert response.status_code in [302, 401] or b'login' in response.data.lower()
    
    def test_admin_user_has_admin_role(self, client, admin_headers):
        """Test that admin user has correct role"""
        with app.app_context():
            admin = User.query.filter_by(email='admin@example.com').first()
            assert admin is not None
            assert admin.role == 'admin'
    
    def test_regular_user_has_patient_role(self, client, auth_headers):
        """Test that regular user has patient role"""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user is not None
            assert user.role in ['patient', 'user']
