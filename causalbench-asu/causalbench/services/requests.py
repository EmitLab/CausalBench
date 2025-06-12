import os.path
import sys
import tempfile

import requests
from requests import JSONDecodeError as RequestsJSONDecodeError
from bunch_py3 import bunchify

from causalbench.services.auth import get_access_token


def save_module(module_type, module_id, version, public, input_file, api_base, default_output_file):
    visibility = "public" if public else "private"
    if module_id is None:
        url = f'https://causalbench.org/api/{api_base}/upload?visibility={visibility}'
    elif version is None:
        url = f'https://causalbench.org/api/{api_base}/upload/{module_id}?visibility={visibility}'
    else:
        url = f'https://causalbench.org/api/{api_base}/upload/{module_id}/{version}?visibility={visibility}'

    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }
    files = {
        'file': (default_output_file, open(input_file, 'rb'), 'application/zip')
    }

    response = requests.post(url, headers=headers, files=files)

    try:
        data = bunchify(response.json())

        if response.status_code == 200:
            if data.version_num == 0:
                print(f'Published {module_type} with module_id={data.id} (visibility={visibility})', file=sys.stderr)
            else:
                print(f'Published {module_type} with module_id={data.id} and version={data.version_num} (visibility={visibility})', file=sys.stderr)
            return data.id, data.version_num

        else:
            if version == 0:
                print(f'Failed to publish {module_type} with module_id={module_id}: {data.msg} ({response.status_code})', file=sys.stderr)
            else:
                print(f'Failed to publish {module_type} with module_id={module_id} and version={version}: {data.msg} ({response.status_code})', file=sys.stderr)
            sys.exit(1)

    except (RequestsJSONDecodeError, AttributeError):
        if version == 0:
            print(f'Failed to publish {module_type} with module_id={module_id}: {response.text} ({response.status_code})', file=sys.stderr)
        else:
            print(f'Failed to publish {module_type} with module_id={module_id} and version={version}: {response.text} ({response.status_code})', file=sys.stderr)
        sys.exit(1)


def fetch_module(module_type, module_id, version, base_api, default_output_file):
    url = f'https://causalbench.org/api/{base_api}/download/{module_id}/{version}'
    headers = {
        'Authorization': f'Bearer {get_access_token()}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract filename from the Content-Disposition header if available
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            file_name = content_disposition.split('filename=')[-1].strip('"')
        else:
            # Fallback to a default name if the header is not present
            file_name = default_output_file

        file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)

        if version == 0:
            print(f'Fetched {module_type} with module_id={module_id}', file=sys.stderr)
        else:
            print(f'Fetched {module_type} with module_id={module_id} and version={version}', file=sys.stderr)
        return file_path

    else:
        try:
            data = bunchify(response.json())

            if version == 0:
                print(f'Failed to fetch {module_type} with module_id={module_id}: {data.msg} ({response.status_code})', file=sys.stderr)
            else:
                print(f'Failed to fetch {module_type} with module_id={module_id} and version={version}: {data.msg} ({response.status_code})', file=sys.stderr)
            sys.exit(1)

        except (RequestsJSONDecodeError, AttributeError):
            if version == 0:
                print(f'Failed to fetch {module_type} with module_id={module_id}: {response.text} ({response.status_code})', file=sys.stderr)
            else:
                print(f'Failed to fetch {module_type} with module_id={module_id} and version={version}: {response.text} ({response.status_code})', file=sys.stderr)
            sys.exit(1)
