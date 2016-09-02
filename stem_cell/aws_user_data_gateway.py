import urllib2
import json


class AwsUserDataGateway:
    AUTHENTICATION_TOKEN_CONFIG_KEY = 'git_repository_authentication_token'
    PRIVATE_KEY_CONFIG_KEY = 'git_repository_private_key'

    def __init__(self):
        self.user_data = json.loads(urllib2.urlopen("http://169.254.169.254/latest/user-data").read())

    @property
    def version_control_url(self):
        return self.user_data['target_ansible_package']

    @property
    def version_control_token(self):
        if self.AUTHENTICATION_TOKEN_CONFIG_KEY not in self.user_data:
            return False
        return self.user_data[self.AUTHENTICATION_TOKEN_CONFIG_KEY]

    @property
    def version_control_private_key(self):
        if self.PRIVATE_KEY_CONFIG_KEY not in self.user_data:
            return False
        return self.user_data[self.PRIVATE_KEY_CONFIG_KEY]
