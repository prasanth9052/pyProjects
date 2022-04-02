import boto3

ec2_resource = boto3.resource('ec2')
sns_client = boto3.client('sns')

backup_filter = [
    {
        'Name': 'tag:Backup',
        'Values': ['Yes']
    }
]
snapshot_ids=[]
#looping through list of ec2 instances with backup filter
for instance in ec2_resource.instances.filter(Filters= backup_filter):
    for vol in instance.volumes.all():
        snap = vol.create_snapshot(Description= 'Snapshot created by boto3')
        snapshot_ids.append(snap.snapshot_id)

sns_client.publish(
TopicArn='arn:aws:sns:us-east-1:870183841450:cpu-threshold',
Subject='Snapshot created',
Message=str(snapshot_ids)
)