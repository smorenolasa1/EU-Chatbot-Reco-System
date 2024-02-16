import base64

api_key = 'df2451e4'  # Your API key from Vonage
api_secret = 'uaCX3sVJheFiKIck'  # Your API secret from Vonage

encoded_credentials = base64.b64encode(f"{api_key}:{api_secret}".encode('utf-8')).decode('utf-8')
authorization_header = f"Basic {encoded_credentials}"

print(authorization_header)
