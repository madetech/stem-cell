import urllib2
import json


class AwsUserDataGateway:
    def __init__(self):
        self.user_data = json.loads(urllib2.urlopen("http://169.254.169.254/latest/user-data").read())

    def get_version_control_url(self):
        return self.user_data['version_control_url']

    def get_version_control_token(self):
        return self.user_data['version_control_token']
