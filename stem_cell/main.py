from differentiator import Differentiator
from git import Git
from aws_user_data_gateway import AwsUserDataGateway
from ansible import Ansible
from file_system import FileSystem

Differentiator(AwsUserDataGateway(), Git(), Ansible(), FileSystem()).differentiate()
