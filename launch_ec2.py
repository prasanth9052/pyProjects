import boto3

ec2= boto3.client('ec2')

responce = ec2.run_instances(
    ImageId = 'ami-0ed9277fb7eb570c9',
    InstanceType = 't2.micro',
    KeyName = 'awskey',
    MaxCount = 1,
    MinCount = 1,
    SecurityGroupIds = ['sg-07f22bff42520e845']
)

print(responce['Instances'][0]['InstanceId'])