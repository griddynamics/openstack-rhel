#!/bin/sh

VM="RHEL6_node"
SNAPID="a09ecda3-9efd-4138-a97b-9bfbadb4bf8f"

ssh mac prlctl stop $VM --kill
ssh mac prlctl snapshot-switch $VM -i $SNAPID
ssh mac prlctl start $VM
sleep 20
ssh n /root/install.sh
