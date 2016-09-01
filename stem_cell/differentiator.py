class Differentiator:
    PAYLOAD_ENTRY_ANSIBLE_PLAYBOOK = '/main.yml'

    def __init__(self, user_data_gateway, version_control_system, ansible, file_gateway):
        self.ansible = ansible
        self.file_gateway = file_gateway
        self.user_data_gateway = user_data_gateway
        self.version_control_system = version_control_system

    def differentiate(self):
        payload_location = self.clone_payload()
        self.ansible.run_playbook(payload_location + self.PAYLOAD_ENTRY_ANSIBLE_PLAYBOOK)

    def clone_payload(self):
        private_key = self.user_data_gateway.version_control_private_key
        if private_key:
            return self.clone_with_private_key(private_key)

        return self.clone_with_url()

    def clone_with_url(self):
        return self.version_control_system.clone(self.version_control_url)

    def clone_with_private_key(self, key):
        self.file_gateway.write_file('/tmp/key.pem', key)
        return self.version_control_system.clone_with_private_key(self.version_control_url, '/tmp/key.pem')

    @property
    def version_control_url(self):
        version_control_url = self.user_data_gateway.version_control_url
        authentication_token = self.user_data_gateway.version_control_token
        if authentication_token:
            version_control_url = version_control_url.replace('://', "://" + authentication_token + "@")
        return version_control_url
