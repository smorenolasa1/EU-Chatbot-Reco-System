import json, os, logging
from dateutil import tz
from config import *
from commands import *
from argparse import ArgumentParser
from flask import Flask, request, Response, send_file

app = Flask(__name__)
logging.basicConfig(format='%(message)s', level=logging.INFO)

@app.route('/wastatus', methods=['GET', 'POST'])

def whatsapp_status():
   if request.is_json:
       logging.info(request.get_json())
   else:
       data = dict(request.form) or dict(request.args)
       logging.info(data)
   return ('', 204)

@app.route('/', methods=['POST'])

def receive_message():
   message_type = ""
   to_addr = ""
   from_addr = ""
   channel = ""
   func = ""

   req_data = json.loads(request.data)
   message_type = req_data["message_type"]
   to_addr = req_data["to"]
   from_addr = req_data["from"]
   channel = req_data["channel"]
   text = req_data["text"] if req_data["text"] != None else None

   logging.info(f"sender: {from_addr}, channel: {channel}, message: {text}")

# facebook messenger
   if channel == "messenger":
       pass
  
   # viber message
   if channel == "viber_service":
       pass

   # WhatsApp
   elif channel == "whatsapp":
       func = "CHATGPT_TEXT" if message_type == "text" else func
       msg = command_set[func](req_data)
   status_code = Response(status=200)
   return status_code

@app.route('/get_image')
def get_image():
   filename = 'images/' + request.args.get('name')
   return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', default=8080)  # Set a default port here
    args = parser.parse_args()
    p = args.p
    # Ensure p is not None and convert it to int
    port = int(os.environ.get('PORT', p) if p is not None else 8080)
    app.run(host='0.0.0.0', port=port)


