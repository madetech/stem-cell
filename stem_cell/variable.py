import sys

from aws_user_data_gateway import AwsUserDataGateway

print AwsUserDataGateway().user_data[sys.argv[1]]
