import os


class Git:
    def __init__(self, ):
        self.path = '/tmp'

    def clone(self, url):
        os.system("cd " + self.path + " ; git clone " + url)
        return self.path
