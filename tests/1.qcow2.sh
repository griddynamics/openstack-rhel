#!/bin/bash

USER=abr
PROJECT=rhelimg
#NETWORK="192.168.99.0/24"
#ADDR_PER_NETWORK=250
NETWORK="10.20.0.0/16"
ADDR_PER_NETWORK=512
NETWORKS_NUM=4
TMPDIR="rhelimg"


rm -fr "$TMPDIR" >/dev/null
mkdir "$TMPDIR"

nova-manage user admin $USER
nova-manage project create $PROJECT $USER
echo "Setting quotas"
nova-manage project quota $PROJECT instances 512
nova-manage project quota $PROJECT cores 1024
echo "Creating network..."
nova-manage network create $NETWORK $NETWORKS_NUM $ADDR_PER_NETWORK

# Turning on network injection
#echo "UPDATE networks SET injected = 1" | mysql -uroot -pnova nova

nova-manage project zip $PROJECT $USER $TMPFILE $TMPDIR/nova_creds.zip

CDIR=`pwd`
cd $TMPDIR || exit -1
unzip nova_creds.zip
source novarc

euca-add-keypair rhelkey > rhelkey.priv
chmod 600 rhelkey.priv
