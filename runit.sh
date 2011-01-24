#!/bin/bash

USER=admin
PROJECT=admin
NETWORK="192.168.0.0/16"
NETWORKS_NUM=1
ADDR_PER_NETWORK=16

TMPDIR=`mktemp -d`

nova-manage db sync
nova-manage user admin $USER
nova-manage project create $PROJECT $USER
nova-manage network create $NETWORK $NETWORKS_NUM $ADDR_PER_NETWORK
nova-manage project zip $PROJECT $USER $TMPFILE $TMPDIR/nova_creds.zip

CDIR=`pwd`
cd $TMPDIR || exit -1
unzip nova_creds.zip
source novarc

cd $CDIR
tar zxf images.tgz

euca-bundle-image -i images/aki-lucid/image -p kernel --kernel true
euca-bundle-image -i images/ari-lucid/image -p ramdisk --ramdisk true
euca-upload-bundle -m /tmp/kernel.manifest.xml -b mybucket
euca-upload-bundle -m /tmp/ramdisk.manifest.xml -b mybucket
AMI_KERNEL=`euca-register mybucket/kernel.manifest.xml | perl -pi -e 's/^IMAGE\s+//'`
AMI_RAMDISK=`euca-register mybucket/ramdisk.manifest.xml | perl -pi -e 's/^IMAGE\s+//'`
euca-bundle-image -i images/ami-tiny/image -p machine  --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK
euca-upload-bundle -m /tmp/machine.manifest.xml -b mybucket
AMI_MACHINE=`euca-register mybucket/machine.manifest.xml | perl -pi -e 's/^IMAGE\s+//'`

cd $TMPDIR || exit -1
euca-add-keypair mykey > mykey.priv
chmod 600 mykey.priv

euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k mykey -t m1.tiny
euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k mykey -t m1.tiny
euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k mykey -t m1.tiny
euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k mykey -t m1.tiny
#euca-describe-instances
sleep 2
euca-describe-instances
sleep 5
euca-describe-instances

#cat /var/log/nova/nova-compute.log

echo "MACHINE: $AMI_MACHINE"
echo "KERNEL : $AMI_KERNEL"
echo "RAMDISK: $AMI_RAMDISK"
echo "source $TMPDIR/novarc"
