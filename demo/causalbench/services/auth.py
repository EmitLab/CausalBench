import json
import requests
def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)
def authenticate(config):
    login_url = "http://127.0.0.1:8000/authenticate/login"
    email = config['email']
    password = config['password']

    # Payload for login request
    payload = {
        'email_id': email,
        'password': password
    }

    try:
        # Sending login request
        response = requests.post(login_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response = response.json()

        return response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def init_auth():
    # Load config from file
    config = load_config('config.json')
    response = authenticate(config)
    access_token = response['data']['access_token']
    print(access_token)
    return access_token
