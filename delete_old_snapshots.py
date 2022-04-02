from datetime import datetime, timedelta, timezone
import boto3

ec2_resource = boto3.resource('ec2')

#List ec2 snapshots

snapshots = ec2_resource.snapshots.filter(OwnerIds=['self'])

for snapshot in snapshots:
    print(snapshot)
    start_time = snapshot.start_time
    print('Start time: ', start_time)
    delete_time = datetime.now(tz=timezone.utc) - timedelta(days=1)
    print('Delete time: ', delete_time)
    if delete_time > start_time:
        print('fmt_start_time = {} and delete_time = {}'.format(start_time, delete_time))
        snapshot.delete()
