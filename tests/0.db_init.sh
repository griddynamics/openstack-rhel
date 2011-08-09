#!/bin/sh

##########################################################################
# BIG FAT WARNING:
# ASSUMPTION: a password for root user in MySQL server is same as for nova
##########################################################################

export LC_ALL=C

source ./helpers

DB_NAME=nova
DB_USER=nova
DB_PASS=nova
PWD=nova

CC_HOST=$(ip addr show dev eth0 |grep 'inet '|perl -pi -e 's/^.*inet ([\d.]+).*$/$1/')
#CC_HOST="10.0.0.11" # IPv4 address
#HOSTS="$CC_HOST localhost" # compute nodes list

HOSTS="$CC_HOST 10.0.0.13 10.0.0.14" # compute nodes list, first MUST be a Cloud Controller address

nova_stop "$HOSTS"
nova_cleanup "$HOSTS"
nova_initial_setup "$HOSTS"
nova_start "$HOSTS"
echo "Allow services to come up online"
sleep 2
nova-manage service list
