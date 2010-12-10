#!/bin/sh

VM="RHEL6_node"
SNAPID="2774479e-dcb2-4786-90c0-fc15121b235e" # run 'ssh mac prlctl snapshot-list RHEL6_node' to get it

ssh mac prlctl stop $VM --kill
ssh mac prlctl snapshot-switch $VM -i $SNAPID
ssh mac prlctl start $VM
echo "Sleeping a bit to allow VM to boot"
sleep 20
ssh n /root/install.sh
