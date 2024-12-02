import os
import sys
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

import jwt
import requests
import yaml

from causalbench.commons.utils import causal_bench_path


__access_token = None

def get_access_token() -> str | None:
    global __access_token
    if __access_token is None or is_token_expired(__access_token):
        __access_token = init_auth()
    return __access_token


def is_token_expired(token):
    exp_timestamp = jwt.decode(token, options={"verify_signature": False})["exp"]
    return datetime.now(timezone.utc).timestamp() >= exp_timestamp


def init_auth() -> str | None:
    # load config from file
    config_path = causal_bench_path('config.yaml')

    # config file does not exist
    if not os.path.isfile(config_path):
        print('Credentials required')
        create_config(config_path)

    # validate config
    while True:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # authenticate
        access_token = authenticate(config)

        # authentication successful
        if access_token is not None:
            return access_token

        # authentication failed
        print('Incorrect credentials')
        create_config(config_path)


def authenticate(config) -> str | None:
    login_url = "https://www.causalbench.org/api/authenticate/login"

    if 'email' in config:
        email = config['email']
    else:
        return

    if 'password' in config:
        password = config['password']
    else:
        return

    # Payload for login request
    payload = {
        'email_id': email,
        'password': password
    }

    try:
        # Sending login request
        response = requests.post(login_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()['data']

        if data is not None:
            return data['access_token']

    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {e}', file=sys.stderr)
        sys.exit(1)


def create_config(config_path: str):
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)

    input_pass = getpass if sys.stdin.isatty() else input

    email: str = input('Email: ')
    password: str = input_pass('Password: ')
    print()

    with open(config_path, 'w') as file:
        yaml.safe_dump({'email': email, 'password': password}, file, indent=4)
