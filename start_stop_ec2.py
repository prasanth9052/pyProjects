import boto3


def start_ec2(instance_id):
    ec2_client = boto3.client('ec2')
    return ec2_client.start_instances(InstanceIds=instance_id)


def stop_ec2(instance_id):
    ec2_client = boto3.client('ec2')
    return ec2_client.stop_instances(InstanceIds=instance_id)


def terminate_ec2(instance_id):
    ec2_client = boto3.client('ec2')
    return ec2_client.terminate_instances(InstanceIds=instance_id)


def ec2_list(states):
    ec2_res = boto3.resource('ec2')
    instances = ec2_res.instances.filter(Filters=[{'Name': 'instance-state-name',
                                                   'Values': states}])
    ec2_list = []
    for instance in instances:
        ec2_list.append(instance.id)

    return ec2_list


states = ['running','stopped']
instance_ids = ec2_list(states)
print(instance_ids)
'''
start_resp = start_ec2(instance_ids)
for i in start_resp['StartingInstances']:
    print('Current state is: ', i['CurrentState']['Name'])
    print('Previous state is: ', i['PreviousState']['Name'])

stop_resp = stop_ec2(instance_ids)
for i in stop_resp['StoppingInstances']:
    print('Current state is: ', i['CurrentState']['Name'])
    print('Previous state is: ', i['PreviousState']['Name'])
'''
terminate_resp = terminate_ec2(instance_ids)
for i in terminate_resp['TerminatingInstances']:
    print('Current state is: ', i['CurrentState']['Name'])
    print('Previous state is: ', i['PreviousState']['Name'])
