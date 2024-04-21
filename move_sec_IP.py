import boto3
import sys

def move_secondary_ip(source_instance_id, dest_instance_id, region_name, aws_access_key_id, aws_secret_access_key, aws_session_token):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    # Describe the source and destination instances
    source_instance = ec2_client.describe_instances(InstanceIds=[source_instance_id])
    dest_instance = ec2_client.describe_instances(InstanceIds=[dest_instance_id])

    # Get the secondary private IP from the source instance
    source_secondary_ip = None
    for iface in source_instance['Reservations'][0]['Instances'][0]['NetworkInterfaces']:
        for private_ip in iface['PrivateIpAddresses']:
            if private_ip['Primary'] is False:
                source_secondary_ip = private_ip['PrivateIpAddress']
                break
        if source_secondary_ip:
            print(f"Secondary private IP found on source instance {source_instance_id}")
            break

    if not source_secondary_ip:
        print(f"No secondary private IP found on source instance {source_instance_id}")
        return

    # Unassigne the secondary private IP from the destination instance
    try:
        ec2_client.unassign_private_ip_addresses(
            NetworkInterfaceId=source_instance['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['NetworkInterfaceId'],
            PrivateIpAddresses=[source_secondary_ip]
        )
        print(f"Successfully unssigned secondary private IP {source_secondary_ip} from {source_instance_id} ")
    except Exception as e:
        print(f"Error unssigning secondary private IP: {e}")

    # Assign the secondary private IP to the destination instance
    try:
        ec2_client.assign_private_ip_addresses(
            NetworkInterfaceId=dest_instance['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['NetworkInterfaceId'],
            PrivateIpAddresses=[source_secondary_ip]
        )
        print(f"Successfully moved secondary private IP {source_secondary_ip} from {source_instance_id} to {dest_instance_id}")
    except Exception as e:
        print(f"Error moving secondary private IP: {e}")

if __name__ == '__main__':
    # AWS credentials
    aws_access_key_id = 'AS UDW'
    aws_secret_access_key = 'ie  BsZ'
    aws_session_token = "IQ8 =="


    # AWS region
    region_name = 'eu-west-1'

    # Source and destination instance IDs
    #source_instance_id = 'i-0913'
    #dest_instance_id = 'i-0cd79'

    source_instance_id = str(sys.argv[1])
    dest_instance_id = str(sys.argv[2])

    move_secondary_ip(source_instance_id, dest_instance_id, region_name, aws_access_key_id, aws_secret_access_key, aws_session_token)
