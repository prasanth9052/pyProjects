import boto3


def ec2_resource():
    return boto3.resource('ec2')


def list_all_instances():
    a = []
    for i in ec2_resource().instances.all():
        a.append(i.instance_id)
    return a


def list_instances_state(state):
    instances = ec2_resource().instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': state}])
    l = []
    for instance in instances:
        l.append(instance.id)
    return l

def stop_running_ec2():
    ec2_resource().instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}]).stop()

#stop_running_ec2()
print(list_all_instances())