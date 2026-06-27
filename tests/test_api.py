"""
Tests for API endpoints
"""
import pytest
import json
from datetime import datetime
from app_modern import app, db
from database import User, Appointment, Prescription, HealthGoal


class TestAPIEndpoints:
    """Test REST API endpoints"""
    
    def test_dashboard_stats(self, client, auth_headers):
        """Test dashboard statistics endpoint"""
        response = client.get('/api/dashboard/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'appointments' in data
        assert 'prescriptions' in data
        assert 'messages' in data
    
    def test_appointments_list(self, client, auth_headers):
        """Test get appointments list"""
        response = client.get('/api/appointments')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_create_appointment(self, client, auth_headers):
        """Test creating new appointment"""
        response = client.post('/api/appointments',
            data=json.dumps({
                'doctor_name': 'Dr. Johnson',
                'date': '2026-07-01',
                'time': '2:00 PM',
                'reason': 'Follow-up'
            }),
            headers=auth_headers
        )
        
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        assert data['success'] == True or 'id' in data
    
    def test_update_appointment(self, client, auth_headers):
        """Test updating appointment"""
        # Create appointment first
        create_response = client.post('/api/appointments',
            data=json.dumps({
                'doctor_name': 'Dr. Update',
                'date': '2026-07-01',
                'time': '3:00 PM',
                'reason': 'Checkup'
            }),
            headers=auth_headers
        )
        
        if create_response.status_code in [200, 201]:
            appointment_id = json.loads(create_response.data).get('id', 1)
            
            # Update appointment
            response = client.put(f'/api/appointments/{appointment_id}',
                data=json.dumps({
                    'status': 'completed'
                }),
                headers=auth_headers
            )
            
            assert response.status_code in [200, 201]
    
    def test_prescriptions_list(self, client, auth_headers):
        """Test get prescriptions list"""
        response = client.get('/api/prescriptions')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_health_goals_list(self, client, auth_headers):
        """Test get health goals list"""
        response = client.get('/api/health-goals')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_create_health_goal(self, client, auth_headers):
        """Test creating new health goal"""
        response = client.post('/api/health-goals',
            data=json.dumps({
                'title': 'Exercise More',
                'description': 'Exercise 30 minutes daily',
                'goal_type': 'exercise',
                'target_value': 30,
                'current_value': 0,
                'unit': 'minutes',
                'target_date': '2026-08-01',
                'priority': 'high'
            }),
            headers=auth_headers
        )
        
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        assert data['success'] == True or 'id' in data
    
    def test_update_health_goal(self, client, auth_headers):
        """Test updating health goal"""
        # Create goal first
        create_response = client.post('/api/health-goals',
            data=json.dumps({
                'title': 'Test Goal',
                'description': 'Test description',
                'goal_type': 'weight_loss',
                'target_value': 10,
                'current_value': 0,
                'unit': 'lbs',
                'target_date': '2026-08-01',
                'priority': 'medium'
            }),
            headers=auth_headers
        )
        
        if create_response.status_code in [200, 201]:
            goal_id = json.loads(create_response.data).get('id', 1)
            
            # Update goal
            response = client.put(f'/api/health-goals/{goal_id}',
                data=json.dumps({
                    'current_value': 5
                }),
                headers=auth_headers
            )
            
            assert response.status_code in [200, 201]
    
    def test_add_goal_progress(self, client, auth_headers):
        """Test adding progress to health goal"""
        with app.app_context():
            # Get first user
            user = User.query.first()
            if user:
                # Create a goal
                goal = HealthGoal(
                    user_id=user.id,
                    title='Progress Test',
                    description='Test',
                    goal_type='exercise',
                    target_value=100,
                    current_value=0,
                    unit='minutes',
                    target_date=datetime.now(),
                    priority='medium',
                    status='active'
                )
                db.session.add(goal)
                db.session.commit()
                goal_id = goal.id
                
                # Add progress
                response = client.post(f'/api/health-goals/{goal_id}/progress',
                    data=json.dumps({
                        'value': 30,
                        'note': 'Completed workout'
                    }),
                    headers=auth_headers
                )
                
                assert response.status_code in [200, 201]
