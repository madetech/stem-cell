import urllib2
import json


class AwsUserDataGateway:
    def __init__(self):
        self.user_data = json.loads(urllib2.urlopen("http://169.254.169.254/latest/user-data").read())

    @property
    def version_control_url(self):
        return self.user_data['version_control_url']

    @property
    def version_control_token(self):
        if 'version_control_token' not in self.user_data:
            return False
        return self.user_data['version_control_token']

    @property
    def version_control_private_key(self):
        if 'version_control_private_key' not in self.user_data:
            return False
        return self.user_data['version_control_private_key']
