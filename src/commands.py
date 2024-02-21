import requests, json
from   requests.auth import HTTPBasicAuth
import openai
import logging
from openai.error import RateLimitError
from config import *
from datetime import datetime


user_info = {}
user_sessions = {}
user_states = {}
logging.basicConfig(format='%(message)s', level=logging.INFO)

def help(req_data):
    msg = "Ask me anything..."
    logging.info(msg)
    return msg



def start_registration_flow(destination_number):
    user_states[destination_number] = 'registration'
    send_whatsapp_msg(destination_number, "What's your full name?")
    return "Asked for user's full name."


def continue_registration_flow(destination_number, message):
    if 'name' not in user_info.get(destination_number, {}):
        if message.isalpha() or ' ' in message:  # Simple check for a valid name
            user_info[destination_number] = {'name': message}
            send_whatsapp_msg(destination_number, "Where is your farm located? Please provide the address or GPS coordinates.")
            return "Asked for farm location."
        else:
            send_whatsapp_msg(destination_number, "Invalid name. Please enter a valid full name.")
            return "Invalid name provided."

    elif 'location' not in user_info[destination_number]:
        # No specific validation for location as it could be an address or GPS coordinates
        user_info[destination_number]['location'] = message
        send_whatsapp_msg(destination_number, "How large is your farm? Please specify in hectares.")
        return "Asked for farm size."

    elif 'size' not in user_info[destination_number]:
        if message.replace('.', '', 1).isdigit():  # Check if it's a positive number, possibly a float
            user_info[destination_number]['size'] = message
            send_whatsapp_msg(destination_number, f"Please review your information: Name - {user_info[destination_number]['name']}, Location - {user_info[destination_number]['location']}, Size - {message} hectares. Is this correct?")
            user_states.pop(destination_number, None)  # Clear the user state
            return "Asked for confirmation of registration info."
        else:
            send_whatsapp_msg(destination_number, "Invalid farm size. Please enter a valid number in hectares.")
            return "Invalid farm"


def is_valid_number(input_str):
    try:
        # Convert to float to accept integers and decimal numbers
        float(input_str)
        return True
    except ValueError:
        return False
    
def write_to_json_file(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
def start_report_flow(destination_number):
    user_states[destination_number] = 'report'
    send_whatsapp_msg(destination_number, "It is time to report your farm's carbon emissions for the year.")
    return "Asked to start yearly report."


def continue_report_flow(destination_number, message):
    # Check if the user is asking a question
    if '?' in message:
        # Redirect to chatbot for questions and send the response back to the user
        response = chatbot({'text': message, 'from': destination_number})
        send_whatsapp_msg(destination_number, response)
        # Now, check if there is a pending question in the user's state and re-ask it
        if user_states.get(destination_number) == 'asking_emission_source':
            send_whatsapp_msg(destination_number, "Which emission source are you reporting? Poll: - Livestock - Machinery")
        elif user_states.get(destination_number) == 'asking_emission_quantity':
            send_whatsapp_msg(destination_number, "Enter the quantity of emission source (in kg of CO2 equivalent).")
        elif user_states.get(destination_number) == 'confirming_submission':
            last_quantity = user_info[destination_number].get('emission_quantity', 'UNKNOWN')
            send_whatsapp_msg(destination_number, f"Confirm submission: {user_info[destination_number]['emission_source'].capitalize()} - {last_quantity} kg CO2 eq. Correct?")
        return "Question answered and follow-up question asked."
    
    # If the message isn't a question, proceed with the flow
    # Check if the user has provided their name
    if 'name' not in user_info.get(destination_number, {}):
        if message.isalpha() or ' ' in message:
            user_info[destination_number] = {'name': message}
            send_whatsapp_msg(destination_number, "Which emission source are you reporting? Poll: - Livestock - Machinery")
            user_states[destination_number] = 'asking_emission_source'
            return "Asked for emission source."
        else:
            send_whatsapp_msg(destination_number, "Invalid name. Please enter a valid full name.")
            return "Invalid name provided."

    # Check if the user has provided the emission source
    elif 'emission_source' not in user_info[destination_number]:
        if message.lower() in ['livestock', 'machinery']:
            user_info[destination_number]['emission_source'] = message.lower()
            send_whatsapp_msg(destination_number, "Enter the quantity of emission source (in kg of CO2 equivalent).")
            user_states[destination_number] = 'asking_emission_quantity'
            return "Asked for emission quantity."
        else:
            send_whatsapp_msg(destination_number, "Invalid emission source. Please choose between Livestock and Machinery.")
            return "Invalid emission source provided."

    # Check if the user has provided the emission quantity
    elif 'emission_quantity' not in user_info[destination_number]:
        if is_valid_number(message):
            user_info[destination_number]['emission_quantity'] = message
            send_whatsapp_msg(destination_number, f"Confirm submission: {user_info[destination_number]['emission_source'].capitalize()} - {message} kg CO2 eq. Correct?")
            user_states[destination_number] = 'confirming_submission'
            return "Asked for confirmation of emission quantity."
        else:
            send_whatsapp_msg(destination_number, "Invalid quantity. Please enter the quantity of emission source in kg of CO2 equivalent.")
            return "Invalid emission quantity provided."

    # Check if the user has confirmed the submission
    elif 'confirmation' not in user_info[destination_number]:
        if message.lower() in ['yes', 'correct']:
            user_info[destination_number]['confirmation'] = True
            send_whatsapp_msg(destination_number, "Thanks! Any other sources to report today?")
            # Here you can decide what should be the next state
            return "Asked if there are more sources to report."
        else:
            send_whatsapp_msg(destination_number, "Information not confirmed. Please start over.")
            user_info.pop(destination_number, None)  # Clear the user info to restart the process
            user_states.pop(destination_number, None)  # Clear the user state
            return "Restarting the process."

    # After the flow is finished, write the updated user_info and user_states to a JSON file
    complete_data = {
        'user_info': user_info,
        'user_states': user_states
    }
    file_name = f'{destination_number}_data_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    write_to_json_file(complete_data, file_name)
    # Implement the logic to send the JSON file to the user here
    # For example, you could upload the file to a server and send the download link to the user
    send_whatsapp_msg(destination_number, f"Your registration data has been saved. You can download it from [download link].")
    return "Data written to JSON file and download link sent."

# Helper function to validate emission quantity
def is_valid_emission_quantity(quantity):
    try:
        quantity = float(quantity)
        return quantity >= 0
    except ValueError:
        return False


def no_text_field(req_data):
    logging.info("Invalid command.")
    pass




def hello_vonage_ai(req_data):
    recipient = req_data['from']['number']
    url = f"{config.endpoint_vonage_ai}/init"
    headers = {'X-Vgai-Key': config.vonage_ai_key}
    payload = '{"agent_id" : "' + config.vonage_ai_agent_id + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    session_data = {recipient: resp_data['session_id']}
    user_sessions.update(session_data)
    url = f"{config.endpoint_vonage_ai}/step"
    headers = {'X-Vgai-Key': config.vonage_ai_key}
    payload = '{"session_id" : "' + user_sessions[recipient] + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    msg = resp_data['flow_path'][1]['message']['text'] + "\n"
    msg = msg + resp_data['flow_path'][2]['message']['text']
    logging.info(f"recipient: {recipient} triggered Vonage AI Stock advisor")
    logging.info(f"{msg}")
    return msg




def get_advice_vonage_ai(req_data):
    recipient = req_data['from']['number']
    symbol = str(req_data['message']['content']['text']).upper().strip().split()[-1]
    url = f"{config.endpoint_vonage_ai}/step"
    headers = {'X-Vgai-Key': config.vonage_ai_key}
    payload = '{"session_id" : "' + user_sessions[recipient] + '",' \
                                                               '"user_input":"' + symbol + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    msg = resp_data['flow_path'][1]['message']['text'] + "\n"
    msg = msg + json.loads(resp_data['flow_path'][2]['message']['text'])['advice']
    logging.info(f"{msg}")
    return msg


def send_msg(channel, recipient, msg):
    if channel == "whatsapp":
        send_whatsapp_msg(recipient, msg)




def send_whatsapp_img(destination_number, imgurl, caption="image"):
    payload = {
        "message_type": "image",
        "to": destination_number,
        "from": config.vonage_sandbox_number,
        "channel": "whatsapp",
        "image": {
            "url": imgurl,
            "caption": caption
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': config.vonage_authorization_header
    }
    response = requests.post(config.endpoint_vonage_message_send, headers=headers, data=json.dumps(payload))
    print(response.text)  # Adding print to debug API response
    return response.text




def send_whatsapp_msg(destination_number, msg):
    payload = json.dumps({
        "from": config.vonage_sandbox_number,
        "to": destination_number,
        "message_type": "text",
        "text": msg,
        "channel": "whatsapp"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': config.vonage_authorization_header
    }

    response = requests.request("POST", config.endpoint_vonage_message_send, headers=headers, data=payload)
    print("Response from send_whatsapp_msg:", response.text)  # Print the response for debugging
    return response.text


def chatbot(req_data):
    question = str(req_data['text']).upper().strip()
    recipient = req_data['from']
    openai.api_key = config.openai_key
    messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},]
    if question:
        send_whatsapp_msg(recipient, "Please wait, communicating to chatgpt...")
        messages.append({"role": "user", "content": question})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        logging.info(f"answer recieved: {reply}")
        return reply




def imagebot(req_data):
    question = str(req_data['text']).upper().strip()
    recipient = req_data['from']
    openai.api_key = config.openai_key
    response = ""
    image_url = ""
    send_whatsapp_msg(recipient, "Please wait, communicating to chatgpt...")
    try:
        response = openai.Image.create(
            prompt=question,
            n=1,
            size="1024x1024"
            )
        logging.info(f"answer recieved: {response}")
        image_url = response['data'][0]['url']
    except:
        image_url = "http://khan2a.com:8080/get_image?name=meme.jpg"
    return image_url


def chatgpt_text(req_data):
    question = str(req_data['text']).strip()
    destination_number = req_data['from']
    logging.info(f"question received: {question}")

    # Check if the user is starting the registration or report flow
    if question.lower() == "start registration":
        return start_registration_flow(destination_number)
    elif question.lower() == "start report":
        user_states[destination_number] = 'report'
        return start_report_flow(destination_number)

    # If user is in a specific state, continue that flow
    if destination_number in user_states:
        if user_states[destination_number] == 'registration':
            return continue_registration_flow(destination_number, question)
        elif user_states[destination_number] == 'report':
            return continue_report_flow(destination_number, question)

    # Handle image requests
    elif question.split()[0].upper() == "IMAGE":
        imgurl = imagebot(req_data)
        logging.info(f"sending reply: {imgurl}")
        send_whatsapp_img(destination_number, imgurl, caption=question)
        return "Image sent."

    # Handle the joining message
    elif question.upper() == "JOIN LINT MUSIC":
        welcome_msg = (
            "Welcome to ChatGPT powered by Vonage Messaging API.\n"
            "To get more information about using this service, type *help*.\n"
            "Since it is in beta version, please expect delay in receiving messages.\n"
            "We are also working to fix an issue which is duplicate message sending.\n"
            "You can now ask any question."
        )
        logging.info(f"sending reply: {welcome_msg}")
        send_whatsapp_msg(destination_number, welcome_msg)
        return "Welcome message sent."

    # If none of the above, assume it is a general question and proceed with ChatGPT
    else:
        msg = chatbot(req_data)  # Assuming chatbot function handles the communication with ChatGPT
        logging.info(f"sending reply: {msg}")
        send_whatsapp_msg(destination_number, msg)
        return "ChatGPT response sent."

    
    


command_set = {'CHATGPT_TEXT': chatgpt_text,
               'no_text_field': no_text_field,
               'HELP': help,
               'HELLO': hello_vonage_ai,
               'SEND': get_advice_vonage_ai}