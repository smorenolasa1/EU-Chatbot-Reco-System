import requests, json
from   requests.auth import HTTPBasicAuth
from   config import *
import openai
import logging
from openai.error import RateLimitError
from config import vonage_sandbox_number, vonage_authorization_header, endpoint_vonage_message_send
from datetime import datetime
user_states = {}
user_info = {}


user_sessions = {}
logging.basicConfig(format='%(message)s', level=logging.INFO)


def help(req_data):
    msg = "Ask me anything..."
    logging.info(msg)
    return msg



def start_registration_flow(destination_number):
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


def continue_report_flow(destination_number, message):
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


# Helper function to validate emission quantity
def is_valid_emission_quantity(quantity):
    try:
        quantity = float(quantity)
        return quantity >= 0
    except ValueError:
        return False
    

def start_report_flow(destination_number):
    send_whatsapp_msg(destination_number, "It is time to report your farm's carbon emissions for the year.")
    return "Asked to start yearly report."


def no_text_field(req_data):
    logging.info("Invalid command.")
    pass




def hello_vonage_ai(req_data):
    recipient = req_data['from']['number']
    url = f"{endpoint_vonage_ai}/init"
    headers = {'X-Vgai-Key': vonage_ai_key}
    payload = '{"agent_id" : "' + vonage_ai_agent_id + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    session_data = {recipient: resp_data['session_id']}
    user_sessions.update(session_data)
    url = f"{endpoint_vonage_ai}/step"
    headers = {'X-Vgai-Key': vonage_ai_key}
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
    url = f"{endpoint_vonage_ai}/step"
    headers = {'X-Vgai-Key': vonage_ai_key}
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
        "from": vonage_sandbox_number,
        "channel": "whatsapp",
        "image": {
            "url": imgurl,
            "caption": caption
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': vonage_authorization_header
    }
    response = requests.post(endpoint_vonage_message_send, headers=headers, data=json.dumps(payload))
    print(response.text)  # Adding print to debug API response
    return response.text




def send_whatsapp_msg(destination_number, msg):
    payload = json.dumps({
    "from": vonage_sandbox_number,
    "to": destination_number,
    "message_type": "text",
    "text": msg,
    "channel": "whatsapp"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': vonage_authorization_header
    }


    response = requests.request("POST", endpoint_vonage_message_send, headers=headers, data=payload)
    return response.text


def chatbot(req_data):
    question = str(req_data['text']).upper().strip()
    recipient = req_data['from']
    openai.api_key = openai_key
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
    openai.api_key = openai_key
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
    question = str(req_data['text']).strip()  # Removed upper() for case sensitivity
    destination_number = req_data['from']
    logging.info(f"question received: {question}")


    # Check if the user is starting the registration or report flow
    if question.lower() == "start registration":
        user_states[destination_number] = 'registration'
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
   
    elif question.split()[0] == "IMAGE":
        imgurl = imagebot(req_data)
        logging.info(f"sending reply: {imgurl}")
        send_whatsapp_img(destination_number, imgurl, caption=question)
    elif question != "JOIN LINT MUSIC":
        msg = chatbot(req_data)
        logging.info(f"sending reply: {msg}")
        send_whatsapp_msg(destination_number, msg)
    else:
        msg = "Welcome to ChatGPT powered by Vonage Messaging API.\n"
        msg = msg + "To get more information about using this service, type *help*.\n"
        msg = msg + "Since it is in beta version, please expect delay in recieving messages.\n"
        msg = msg + "We are also working to fix an issue which is duplicate message sending.\n"
        msg = msg + "You can now ask any question."
        logging.info(f"sending reply: {msg}")
        send_whatsapp_msg(destination_number, msg)


command_set = {'CHATGPT_TEXT': chatgpt_text,
               'no_text_field': no_text_field,
               'HELP': help,
               'HELLO': hello_vonage_ai,
               'SEND': get_advice_vonage_ai}