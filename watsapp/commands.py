import requests, json
from   requests.auth import HTTPBasicAuth
from   config import *
import openai
import logging
from openai.error import RateLimitError
from config import vonage_sandbox_number, vonage_authorization_header, endpoint_vonage_message_send
from datetime import datetime
from toPDF import create_pdf_from_string


# Configuration and initial setup
from config import *
logging.basicConfig(format='%(message)s', level=logging.INFO)

user_info = {}
user_states = {}

# Define the questions for the report flow
questions = [
    ('farm_name', "What's the name of your farm?"),
    ('location', "Where is your farm located? Please provide the address or GPS coordinates."),
    ('farm_area', "How large is your farm? Please specify in hectares."),
    # Add more questions as needed
]

# Define the questions dictionary for easy lookup
questions_dict = {q[0]: q[1] for q in questions}

def help(req_data):
    msg = "Ask me anything..."
    logging.info(msg)
    return msg

def is_valid_name(name):
    return name.replace(' ', '').isalpha()

def is_valid_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def is_question(text):
    return text.strip().endswith('?')


def process_message(req_data):
    destination_number = req_data['from']
    message = req_data['text'].strip()

    if message.lower() == 'start report':
        user_info[destination_number] = {}
        user_states[destination_number] = 'farm_name'
        send_whatsapp_msg(destination_number, questions_dict['farm_name'])
    elif destination_number in user_states:
        if is_question(message):
            response = chatbot(message, destination_number)
            send_whatsapp_msg(destination_number, response)
            # Re-ask the last question
            last_question_key = user_states[destination_number]
            send_whatsapp_msg(destination_number, questions_dict[last_question_key])
        else:
            handle_response(destination_number, message)
    else:
        send_whatsapp_msg(destination_number, "Please start the report by typing 'start report'.")

def handle_response(destination_number, message):
    current_question = user_states[destination_number]
    if current_question == 'farm_name' and not is_valid_name(message):
        send_whatsapp_msg(destination_number, "Please enter a valid name for your farm.")
    elif current_question == 'farm_area' and not is_valid_number(message):
        send_whatsapp_msg(destination_number, "Please enter a valid number for the farm area.")
    else:
        user_info[destination_number][current_question] = message
        next_question_index = questions.index((current_question, questions_dict[current_question])) + 1
        if next_question_index < len(questions):
            next_question_key = questions[next_question_index][0]
            user_states[destination_number] = next_question_key
            send_whatsapp_msg(destination_number, questions_dict[next_question_key])
        else:
            generate_and_send_report(destination_number)

            

def generate_and_send_report(destination_number):
    report_content = create_report_content(user_info[destination_number])
    pdf_filename = f"{destination_number}_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    create_pdf_from_string(report_content, pdf_filename)
    # Send the PDF report or provide a download link
    send_whatsapp_msg(destination_number, "Your report has been generated. Please download it from [link].")
    # Clean up after sending the report
    user_info.pop(destination_number, None)
    user_states.pop(destination_number, None)
    
def create_report_content(user_responses):
    content = "Farm Report\n\n"
    for key, answer in user_responses.items():
        content += f"{key.replace('_', ' ').capitalize()}: {answer}\n"
    return content



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

    try:
        response = requests.post(endpoint_vonage_message_send, headers=headers, data=payload)
        print("Response from send_whatsapp_msg:", response.text)  # Print the response for debugging
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {str(e)}")



def chatbot(req_data):
    question = str(req_data['text']).strip()  # Keep the original text case
    recipient = req_data['from']
    openai.api_key = openai_key
    
    try:
        send_whatsapp_msg(recipient, "Please wait, communicating to chatgpt...")
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and kind AI Assistant."},
                {"role": "user", "content": question}
            ]
        )
        reply = chat_response.choices[0].message.content
        logging.info(f"answer received: {reply}")
        send_whatsapp_msg(recipient, reply)  # Send the reply directly to the user
    except Exception as e:
        logging.error(f"ChatGPT Error: {str(e)}")
        send_whatsapp_msg(recipient, "Sorry, I'm having trouble understanding that right now.")





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
    question = str(req_data['text']).strip()
    destination_number = req_data['from']
    logging.info(f"Question received: {question}")

    # Check if the user is initiating or already in the report flow
    if question.lower() == "start report" or destination_number in user_states:
        process_message(req_data)  # This will handle both starting and continuing the report flow
    # Handle image requests
    elif question.split()[0].upper() == "IMAGE":
        imgurl = imagebot(req_data)  # Make sure this function is properly defined elsewhere in your code
        logging.info(f"Sending reply: {imgurl}")
        send_whatsapp_img(destination_number, imgurl, caption=question)  # Make sure this function is properly defined
    # Handle the joining message or any other predefined commands
    elif question.upper() == "JOIN DENIM FLAME":
        welcome_msg = (
            "Welcome to ChatGPT powered by Vonage Messaging API.\n"
            "To get more information about using this service, type *help*.\n"
            "Since it is in beta version, please expect delay in receiving messages.\n"
            "We are also working to fix an issue which is duplicate message sending.\n"
            "You can now ask any question."
        )
        logging.info(f"Sending reply: {welcome_msg}")
        send_whatsapp_msg(destination_number, welcome_msg)
    # If none of the above, assume it is a general question and proceed with ChatGPT
    else:
        chat_response = chatbot(question, destination_number)  # Make sure this function is properly defined
        logging.info(f"Sending reply: {chat_response}")
        send_whatsapp_msg(destination_number, chat_response)

# Additional functions such as send_whatsapp_img, imagebot, chatbot need to be defined accordingly.



# Make sure to update or implement the chatbot, send_whatsapp_img, and imagebot functions accordingly.
    
    


command_set = {'CHATGPT_TEXT': chatgpt_text,
               'HELP': help,
               'HELLO': hello_vonage_ai,
               'SEND': get_advice_vonage_ai}
