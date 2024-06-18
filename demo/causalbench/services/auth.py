import requests
import yaml

from causalbench.commons.utils import causal_bench_path


def authenticate(config):
    login_url = "http://35.92.40.127:8000/authenticate/login"
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
    # load config from file
    config_path = causal_bench_path('config.yaml')
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # authenticate
    response = authenticate(config)
    access_token = response['data']['access_token']

    return access_token
