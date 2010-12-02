#!/bin/sh

VM="RHEL6_node"
SNAPID="8960c53b-216f-4a3b-8d45-59dc5af5f131"

ssh mac prlctl stop $VM --kill
ssh mac prlctl snapshot-switch $VM -i $SNAPID
ssh mac prlctl start $VM

