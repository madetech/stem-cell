import os


class Ansible(object):
    def run_playbook(self, playbook):
        os.system("ansible-playbook " + playbook)
