import boto3

ec2_client = boto3.client('ec2')
response = ec2_client.describe_instances() #If you don't give any arguments then it will return all the instances.

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print('Instance ID: {}, Status: {}'.format(instance['InstanceId'], instance['State']['Name']))

