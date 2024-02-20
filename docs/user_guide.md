# User Guide

## Introduction

An introduction to how to use the chatbot, including basic setup.

## How to Use

Detailed instructions on how to interact with the chatbot, including examples.

### How to connect our model to your whatsapp

1) Start by signing up for a free Vonage API account: https://developer.vonage.com/en/home
2) Download python, flask and ngrok
3) For ngrok, you have to create an account here(check if you have mac or windows): https://dashboard.ngrok.com/get-started/setup/macos
4) First start by creating a message API Sandbox for whatsapp:
      - Once you sign up to Vonage, go to API Dashboard --> Deveolper Tools --> and Message Sandbox.
      - Then scan the QR code and send the passphrase given to that number in whatsapp.
      - Then, after you downloaded ngrok, co to your cmd and type ngrok to make sure it works.
      - After, type ngrok http 8080: This will give you a forwarding URL that ends with free.app.
      - Copy that link, and go back to your vonage account, and paste it on the message sandbox, where it says webhooks on the inbound box. On the Status box, paste the same link, and on the end put "/wastatus". 
      - Finally, save the webhooks.
5) Now for the code:
      - Go to watsapp --> generate_auth.py, and put your api_key and api_secret(you will find this in your Vonage account in API Settings) and save.
      - Next, run python generate_auth.py. This will give you the authorization_header.
      - Next, go to config.py and paste that authorization_header in the vonage_authorization_header.
      - Then, go to OpenAI(https://platform.openai.com/api-keys), and create an OpenAI API Key(make sure this key has credit, otherwise it will give you an error saying there is a problem with your OpenAI API Key).
      -  After, in the vonage_sandbox_number, input the number you sent the passphrase to in whatsapp(the vonage number). You should input this number without the + sign. E.g., 14157386102.
      -  Finally, save this.
  6) Next to run the code, you should enter these commands:
      - Remove-Item -Recurse -Force .\env\
      - python -m venv env
      - .\env\Scripts\activate
      - python -m pip install --upgrade pip setuptools wheel
      - pip install flask openai requests python-dateutil
      - pip install openai==0.28.1
7) Finally, run python app.py and send a message throught whatsapp to test our model! (Type start registration, or start report if you want to start those processes, otherwise it will connect you to ChatGPT).
