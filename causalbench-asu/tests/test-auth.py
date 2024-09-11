import pytest
from causalbench.services.auth import init_auth
import jwt

def is_jwt(token):

    # Split the token into parts
    parts = token.split('.')
    
    # A valid JWT should have exactly 3 parts
    if len(parts) != 3:
        return False
    
    try:
        header = jwt.get_unverified_header(token)

        return True
    except Exception as e:
        print(f"Invalid JWT token: {e}")
        return False




# Take some config yaml file, and copy to its location.
## can be ignored for now as ertugrul's creds are already there.
response = init_auth()

assert is_jwt(response), "Response is not in JWT format. Access token could not received"
print("Response is in JWT format and it is an access token.")