#! /usr/bin/env python 

import argparse
import boto3
import json
import sys

parser = argparse.ArgumentParser(description='Dynamic inventory for autoscaling groups')
parser.add_argument('--list', help="list hosts", action="store_true")
parser.add_argument('--host', help="list host vars")
args = parser.parse_args()

if args.host:
  print "{}"

if not args.list:
   sys.exit(1)

inventory = {"_meta": {"hostvars": {}}}

ec2 = boto3.client('ec2', region_name='us-east-1')
autoscale = boto3.client('autoscaling', region_name='us-east-1')

groups = autoscale.describe_auto_scaling_groups()
for asg in groups['AutoScalingGroups']:
	asgname = asg['AutoScalingGroupName']
	ip_addresses = []
	if asgname not in inventory:
		inventory[asgname] = { "hosts": [] }
	asg_instances = [i for i in asg['Instances']]
	asg_instance_ids = [ i['InstanceId'] for i in asg_instances]
	reservations = ec2.describe_instances(Filters=[{'Name': 'instance-id', 'Values': asg_instance_ids }])
	for resdata in reservations['Reservations']:
		for instance in resdata['Instances']:
			ip_addresses.append(instance['PrivateIpAddress'])
	inventory[asgname]['hosts'] += ip_addresses 

print json.dumps(inventory)
