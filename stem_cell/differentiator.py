class Differentiator:
    PAYLOAD_ENTRY_ANSIBLE_PLAYBOOK = '/main.yml'

    def __init__(self, user_data_gateway, version_control_system, ansible):
        self.ansible = ansible
        self.user_data_gateway = user_data_gateway
        self.version_control_system = version_control_system

    def differentiate(self):
        payload_location = self.clone_differentiation_payload()
        self.ansible.run_playbook(payload_location + self.PAYLOAD_ENTRY_ANSIBLE_PLAYBOOK)

    def clone_differentiation_payload(self):
        return self.version_control_system.clone(self.get_version_control_url())

    def get_version_control_url(self):
        version_control_url = self.user_data_gateway.get_version_control_url()
        authentication_token = self.user_data_gateway.get_version_control_token()
        if authentication_token:
            version_control_url = version_control_url.replace('://', "://" + authentication_token + "@")
        return version_control_url
