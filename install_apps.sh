#!/bin/bash

if [ $# -lt 2 ]; then
  echo "Usage: $0 AutoscalingGroupName App1 (App2 ... ...)"
  exit 1
fi

asgname=$1; shift

apps=$*

echo "Installing apps into AutoscalingGroup $asgname"
for app in $apps
do
	ansible_command="ansible-pull --full -U https://github.com/concat/ansible-playbooks ${app}_app.yml"
	echo "Installing $app" 
	echo ansible $asgname -i ./inventory -m command -a "$ansible_command"
	ansible $asgname -i ./inventory -m command -a "$ansible_command"
	echo "..done"
done
