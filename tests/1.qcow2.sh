#!/bin/bash

USER=abr
PROJECT=rhelimg
NETWORK="192.168.99.0/24"
NETWORKS_NUM=1
ADDR_PER_NETWORK=128
TMPDIR="rhelimg"


rm -fr "$TMPDIR" >/dev/null
mkdir "$TMPDIR"

nova-manage user admin $USER
nova-manage project create $PROJECT $USER
nova-manage network create $NETWORK $NETWORKS_NUM $ADDR_PER_NETWORK
nova-manage project zip $PROJECT $USER $TMPFILE $TMPDIR/nova_creds.zip

CDIR=`pwd`
cd $TMPDIR || exit -1
unzip nova_creds.zip
source novarc

euca-add-keypair rhelkey > rhelkey.priv
chmod 600 rhelkey.priv
