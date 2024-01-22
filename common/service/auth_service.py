import base64
import requests

class AuthService:

    def __init__(self,basic_auth_host):
        self._basic_auth_host = basic_auth_host

    def build_basic_auth_header_value(self,username,password):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def validate_basic_auth_credentials(self,username,password):
        basic_auth_header_value = self.build_basic_auth_header_value(username,password)
        response = requests.get(f'{self._basic_auth_host}/v1/auth/basic',headers={'Authorization':basic_auth_header_value})
        if response.status_code == 200:
            return True
        else:
            return False