import boto3

def lambda_handler(event, context):
    client = boto3.client('ec2')
    #get all snapshots
    response_snap = client.describe_snapshots(OwnerIds=['self'])
    #get all running ec2 instances volume ids
    response_ec2 = client.describe_instances(Filters=[{'Name': 'instance-state-name','Values': ['running']}])
    active_instance_volume_id=set()
    for reservation in response_ec2['Reservations']:
        for instance in reservation['Instances']:
            for volume in instance['BlockDeviceMappings']:
                active_instance_volume_id.add(volume['Ebs']['VolumeId'])
    
    for snapshot in response_snap['Snapshots']:
        snap_id=snapshot['SnapshotId']
        volume_id=snapshot['VolumeId']
        
        if not volume_id or volume_id not in active_instance_volume_id:
            client.delete_snapshot(SnapshotId=snap_id)
            print("EBS snapshot is deleted")
