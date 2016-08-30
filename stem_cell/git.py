import os


class Git:
    def __init__(self, ):
        self.path = '/tmp/app-seed'

    def clone(self, url):
        os.system("git clone " + url + ' ' + self.path)
        return self.path
