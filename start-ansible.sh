#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False
cd /opt/project/autox/ansible
ansible-playbook -i ./inventories/production/hosts --become --become-user=root ./site.yml