# API Reference

## Overview

A brief introduction to your API and its purpose.

## Authentication

Instructions for authenticating with your API (if applicable).

## Endpoints

### Endpoint 1: Start Registration Flow
Method: POST
URL: /start-registration
Description: Initiates the user registration process by asking for the user's full name via WhatsApp.
Parameters:
destination_number: The WhatsApp number to which the registration prompt will be sent.

### Endpoint 2: Continue Registration Flow
Method: POST
URL: /continue-registration
Description: Continues the registration process based on user input, collecting additional details like farm location and size.
Parameters:
destination_number: The user's WhatsApp number.
message: The message received from the user as part of the registration flow.

### Endpoint 3: Start Report Flow
Method: POST
URL: /start-report
Description: Initiates the reporting process for users to report their farm's carbon emissions via WhatsApp.
Parameters:
destination_number: The WhatsApp number to which the reporting prompt will be sent.

### Endpoint 4: Continue Report Flow
Method: POST
URL: /continue-report
Description: Processes the user's responses for the emission reporting, including handling questions and collecting emission data.
Parameters:
destination_number: The user's WhatsApp number.
message: The user's response or query related to the emission reporting.

## Additional Functionalities
The script also includes functionalities to interact with OpenAI's GPT-3 for text-based queries (chatbot function) and image generation (imagebot function), as well as utilities for sending messages and images via WhatsApp (send_whatsapp_msg and send_whatsapp_img).
