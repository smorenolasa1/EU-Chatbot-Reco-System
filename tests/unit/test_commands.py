import pytest
from src import *

# test_commands.py

def test_chatgpt_text():
    # Mock request data
    req_data = {'text': 'Hello', 'from': '12345'}
    # Call the function
    response = commands.chatgpt_text(req_data)
    # Assert the response is not empty
    assert response is not None
    assert len(response) > 0

def test_help_command():
    # Mock request data
    req_data = {}
    # Call the help function
    response = commands.help(req_data)
    # Assert the response matches expected help message
    expected_message = "Ask me anything..."
    assert response == expected_message


# test_utils.py

def test_is_valid_number():
    assert commands.is_valid_number("100") is True
    assert commands.is_valid_number("notanumber") is False
    assert commands.is_valid_number("123.45") is True
