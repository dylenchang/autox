#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False
cd /opt/project/autox/ansible
ansible-playbook -i ./inventories/staging/hosts.allinone.ip.ini --become --become-user=root ./90-init-cluster.yml