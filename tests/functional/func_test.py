import pytest
from src.app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_welcome_message(client):
    response = client.post('/', json={"channel": "whatsapp", "text": "JOIN LINT MUSIC", "from": "user1"})
    assert "Welcome to ChatGPT" in response.data.decode()

def test_help_command(client):
    response = client.post('/', json={"channel": "whatsapp", "text": "help", "from": "user2"})
    assert "Ask me anything" in response.data.decode()

def test_chatgpt_text_response(client):
    # This test might need to mock OpenAI's API response
    response = client.post('/', json={"channel": "whatsapp", "text": "What is the weather like today?", "from": "user3"})
    assert response.status_code == 200
    # Assert based on mocked response content

def test_image_request_handling(client):
    # Assuming your bot sends back a URL or a success status for image requests
    response = client.post('/', json={"channel": "whatsapp", "text": "IMAGE dogs", "from": "user4"})
    assert response.status_code == 200
    # Additional assertions based on your logic

def test_unrecognized_command_handling(client):
    response = client.post('/', json={"channel": "whatsapp", "text": "unrecognized command", "from": "user5"})
    assert "did not understand" in response.data.decode() or "try again" in response.data.decode()

# Add more tests for registration flow, reporting flow, and invalid input handling according to your application logic

if __name__ == '__main__':
    pytest.main()
