#!/bin/sh

##########################################################################
# BIG FAT WARNING:
# ASSUMPTION: a password for root user in MySQL server is same as for nova
##########################################################################

source ./helpers

DB_NAME=nova
DB_USER=nova
DB_PASS=nova
PWD=nova

CC_HOST=$(ip addr show dev eth0 |grep 'inet '|perl -pi -e 's/^.*inet ([\d.]+).*$/$1/')

HOSTS="$CC_HOST" # compute nodes list, first MUST be a Cloud Controller address

nova_stop "$HOSTS"
nova_cleanup "$HOSTS"
nova_initial_setup "$HOSTS"
nova_start "$HOSTS"
echo "Allow services to come up online"
sleep 2
nova-manage service list
