#Create AMI from the ec2 which tags are (Name: prod) in us-east-1 region
#Wait for the AMI to be available
#Copy the AMI to ap-south-1 region
import boto3
import datetime

# ec2 client
def ec2(source_region):
    return boto3.client('ec2',region_name= source_region)

# get today's date
def time_stamp():
    x = datetime.datetime.now()
    return x.strftime("%d-%b-%Y")

#Get list of ec2 instance ids
def ec2_instances_list(ec2_filter, source_region):
    response = ec2(source_region).describe_instances(Filters=ec2_filter)
    instance_list = []
    for reservation in response['Reservations']:
        instance_list.append(reservation['Instances'][0]['InstanceId'])
    return instance_list

#Create AMIs and get image ids
def ami_backup(instance_list, source_region):
    image_ids = []
    for instance in instance_list:
        ami_response = ec2(source_region).create_image(InstanceId=instance, Name='AMI' + instance + time_stamp(), NoReboot=True)
        image_ids.append(ami_response['ImageId'])
    return image_ids

#Wait for images to be available
def wait_for_image_available(image_ids, source_region):
    waiter = ec2(source_region).get_waiter('image_available') # Get waiter image
    #Wait for images to be avaialable
    waiter.wait(ImageIds=image_ids)

def copy_images(image_ids, source_region, destination_region):

    for image_id in image_ids:
        response = ec2(destination_region).copy_image(Name='Boto3-copy'+image_id,
                                           SourceImageId= image_id,
                                           SourceRegion= source_region)
        print('Image id {} after copied in {} region'.format(response['ImageId'], destination_region))


if __name__ == '__main__':

    #Declare variables
    source_region = 'us-east-1'
    destination_region = 'ap-south-1'
    ec2_filter = [
        {
            'Name': 'tag:Name', # Filter with Tags
            'Values': [
                'Prod'
            ]
        },
        {
            'Name': 'availability-zone', # Filter with Availability zones
            'Values': [
                'us-east-1d'
            ]
        }
    ]
    instance_list = ec2_instances_list(ec2_filter, source_region) # Get the list of instances
    print('Instances list: ',instance_list)

    backup_image_ids = ami_backup(instance_list, source_region) # Create AMI's of the instances
    print("Images to be copied:", backup_image_ids)
    print("Waiting for images to be available")
    wait_for_image_available(backup_image_ids, source_region) # Wait for images to be available
    copy_images(backup_image_ids, source_region, destination_region) # Copy images to destination region
    print("All Images copied to {}".format(destination_region))

