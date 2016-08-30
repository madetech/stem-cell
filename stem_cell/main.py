from differentiator import Differentiator
from git import Git
from aws_user_data_gateway import AwsUserDataGateway
from ansible import Ansible

Differentiator(AwsUserDataGateway(), Git(), Ansible()).differentiate()
