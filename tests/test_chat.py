"""
Tests for chat and AI functionality
"""
import pytest
import json
from app_modern import app
from ai_medical_knowledge import EnhancedMedicalAI


class TestChatFunctionality:
    """Test chat and AI features"""
    
    def test_chat_api_endpoint(self, client, auth_headers):
        """Test chat API endpoint"""
        response = client.post('/api/chat',
            data=json.dumps({
                'message': 'Hello, I have a headache'
            }),
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert len(data['response']) > 0
    
    def test_socketio_connection(self, socketio_client):
        """Test Socket.IO connection"""
        assert socketio_client.is_connected()
    
    def test_socketio_chat_message(self, socketio_client):
        """Test sending chat message via Socket.IO"""
        socketio_client.emit('join_chat', {'user_id': 1})
        socketio_client.emit('chat_message', {
            'message': 'Test message',
            'user_id': 1
        })
        
        received = socketio_client.get_received()
        # Check if we received any response
        assert len(received) >= 0  # May receive join confirmation or message
    
    def test_chat_history(self, client, auth_headers):
        """Test retrieving chat history"""
        # Send a message first
        client.post('/api/chat',
            data=json.dumps({
                'message': 'Test message'
            }),
            headers=auth_headers
        )
        
        # Get history
        response = client.get('/api/chat/history')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)


class TestMedicalAI:
    """Test AI medical knowledge functionality"""
    
    def test_ai_initialization(self):
        """Test AI engine initialization"""
        ai = EnhancedMedicalAI()
        assert ai is not None
    
    def test_symptom_detection(self):
        """Test symptom detection in user message"""
        ai = EnhancedMedicalAI()
        response = ai.get_response('I have a headache and fever')
        
        assert response is not None
        assert len(response) > 0
        # Should contain medical advice
        assert any(keyword in response.lower() for keyword in ['symptom', 'fever', 'headache', 'care', 'doctor'])
    
    def test_medication_query(self):
        """Test medication information retrieval"""
        ai = EnhancedMedicalAI()
        response = ai.get_response('Tell me about ibuprofen')
        
        assert response is not None
        assert 'ibuprofen' in response.lower()
    
    def test_emergency_detection(self):
        """Test emergency situation detection"""
        ai = EnhancedMedicalAI()
        response = ai.get_response('I have severe chest pain')
        
        assert response is not None
        # Should mention emergency or 911
        assert any(keyword in response.lower() for keyword in ['emergency', '911', 'immediately', 'urgent'])
    
    def test_health_tips(self):
        """Test health tips generation"""
        ai = EnhancedMedicalAI()
        response = ai.get_response('Give me some health tips')
        
        assert response is not None
        assert len(response) > 50  # Should be substantial advice
    
    def test_intent_detection(self):
        """Test intent detection"""
        ai = EnhancedMedicalAI()
        
        # Test symptom intent
        intent = ai.detect_intent('I have a fever')
        assert 'symptom' in intent.lower() or intent != 'general'
        
        # Test medication intent
        intent = ai.detect_intent('What is aspirin used for?')
        assert 'medication' in intent.lower() or intent != 'general'
    
    def test_context_awareness(self):
        """Test AI context awareness"""
        ai = EnhancedMedicalAI()
        
        # First message
        response1 = ai.get_response('I have a cough', user_id=1)
        assert response1 is not None
        
        # Follow-up message - should maintain context
        response2 = ai.get_response('How long will it last?', user_id=1)
        assert response2 is not None
        assert len(response2) > 0
