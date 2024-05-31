from causalbench.services.auth import init_auth
import requests

def save_module(input_file_path, access_token, api_base, output_file_name):
    url = f'http://18.116.44.47:8000/{api_base}/upload/'
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    files = {
        'file': (output_file_name, open(input_file_path, 'rb'), 'application/zip')
    }

    response = requests.post(url, headers=headers, files=files)
    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        return True

    return False

def fetch_module(module_id, base_api, output_file_name):
    access_token = init_auth()
    filename = None
    print(f"MODULE: {module_id}")
    url = f'http://18.116.44.47:8000/{base_api}/download/{module_id}/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract filename from the Content-Disposition header if available
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[-1].strip('"')
        else:
            # Fallback to a default name if the header is not present
            filename = output_file_name

        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'Download successful, saved as {filename}')
    else:
        print(f'Failed to download file: {response.status_code}')
        print(response.text)
    return filename