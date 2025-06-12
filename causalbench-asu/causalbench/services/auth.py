import os
import sys
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path

import jwt
import requests
import yaml

from causalbench.commons.utils import causal_bench_path, causalbench_version

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
    login_url = "https://causalbench.org/api/authenticate/login"

    if 'email' in config:
        email = config['email']
    else:
        return None

    if 'password' in config:
        password = config['password']
    else:
        return None

    cb_ver = causalbench_version()

    # Payload for login request
    payload = {
        'email_id': email,
        'password': password,
        'python_package_version': f'{cb_ver.major}.{cb_ver.minor}'
    }

    try:
        # Sending login request
        response = requests.post(login_url, json=payload)

        # Successful login
        if response.status_code == 200:
            data = response.json()['data']
            if data is not None:
                return data['access_token']
            return None

        # Potential version mismatch
        if response.status_code == 403:
            message = response.json()['message']
            if message is not None:
                print(message, file=sys.stderr)
                sys.exit(1)

        # Raise an exception for HTTP errors
        response.raise_for_status()

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
