#!/bin/sh

VM="RHEL6_node"
SNAPID="97055158-7ae3-4394-afd0-93a35789d80a" # run 'ssh mac prlctl snapshot-list RHEL6_node' to get it

ssh mac prlctl stop $VM --kill
ssh mac prlctl snapshot-switch $VM -i $SNAPID
ssh mac prlctl start $VM
echo "Sleeping a bit to allow VM to boot"
sleep 20
ssh n /root/install.sh
