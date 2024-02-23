import pytest
import requests
import json

# The base URL of your Flask application
base_url = 'http://localhost:8080'
headers = {'Content-Type': 'application/json'}

# A list of test cases with input text and the expected substring in the response
test_cases = [
    {"input": "What is the capital of France?", "expected": "Paris"},
    {"input": "What is 2+2?", "expected": "4"},
    # Add more test cases as needed
]

@pytest.mark.parametrize("test_case", test_cases)
def test_chatbot_accuracy_and_response_time(test_case):
    # Send a request to the chatbot
    start_time = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC').json()['unixtime']
    response = requests.post(
        f"{base_url}/",
        headers=headers,
        data=json.dumps({
            "message_type": "text",
            "to": "test_number",
            "from": "test_user",
            "channel": "whatsapp",
            "text": test_case["input"]
        })
    )
    end_time = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC').json()['unixtime']
    response_time = end_time - start_time

    # The response must be converted to the expected format to extract the chatbot's answer
    response_data = response.text  # Adjust this as necessary to fit your actual response format

    # Assertions
    assert test_case["expected"] in response_data, f"Expected '{test_case['expected']}' to be in the response"
    assert response_time < 5, f"Response took {response_time}s, which is too slow"

# More tests can be added here for error handling, scalability, etc.
