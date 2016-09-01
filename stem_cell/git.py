import os


class Git:
    def __init__(self, ):
        self.path = '/tmp/app-seed'

    def clone(self, url):
        os.system(self.git_command(url))
        return self.path

    def clone_with_private_key(self, url, private_key_path):
        os.system('GIT_SSH=/opt/ssh-git.sh PKEY=' + private_key_path + " " + self.git_command(url))
        return self.path

    def git_command(self, url):
        return 'git clone ' + url + ' ' + self.path
