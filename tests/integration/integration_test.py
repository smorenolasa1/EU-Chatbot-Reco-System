import json
from src.app import app

# test_app_integration.py

def test_receive_message():
    with app.test_client() as client:
        # Mock POST request to '/' endpoint
        response = client.post('/', data=json.dumps({
            "message_type": "text",
            "to": "12345",
            "from": "67890",
            "channel": "whatsapp",
            "text": "Hello"
        }), content_type='application/json')
        
        # Assert that the response status code is 200
        assert response.status_code == 200

def test_get_image():
    with app.test_client() as client:
        # Mock GET request to '/get_image' with query parameter
        response = client.get('/get_image?name=test.png')
        
        # Assert that the response is successful and content type is image/png
        assert response.status_code == 200
        assert response.content_type == 'image/png'
