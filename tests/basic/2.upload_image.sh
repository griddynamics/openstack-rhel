#!/bin/sh

KERNEL="vmlinuz-2.6.18-238.el5"
INITRD="initrd-2.6.18-238.el5-virtio.img"
ROOTFS="rootfs.qcow2"
BUCKET="rhel56"
CONFDIR="../rhelimg"
DIR=`mktemp -d`
CONFIG=".cnf"

source "$CONFDIR/novarc"

#for ami in $(cat $CONFIG); do
#        n=$(euca-describe-images $ami | wc -l)
#        if [ "$n" -gt 0 ]; then
#                echo "deregistering $ami"
#                euca-deregister $ami
#        fi
#done

euca-bundle-image -i $KERNEL -d $DIR -p kernel  --kernel  true
if [ "$?" != "0" ]; then
    echo "FAILED: euca-bundle-image -i $KERNEL -d $DIR -p kernel  --kernel  true"
    exit -1
fi

euca-bundle-image -i $INITRD -d $DIR -p ramdisk --ramdisk true
if [ "$?" != "0" ]; then
    echo "FAILED: euca-bundle-image -i $INITRD -d $DIR -p ramdisk --ramdisk true"
    exit -1
fi

euca-upload-bundle -m $DIR/kernel.manifest.xml  -b $BUCKET
if [ "$?" != "0" ]; then
    echo "FAILED: euca-upload-bundle -m $DIR/kernel.manifest.xml  -b $BUCKET"
    exit -1
fi

euca-upload-bundle -m $DIR/ramdisk.manifest.xml -b $BUCKET
if [ "$?" != "0" ]; then
    echo "FAILED: euca-upload-bundle -m $DIR/ramdisk.manifest.xml -b $BUCKET"
    exit -1
fi

AMI_KERNEL=`euca-register $BUCKET/kernel.manifest.xml   | tr -d "IMAGE[:blank:]"`
echo "AMI_KERNEL: $AMI_KERNEL"
AMI_RAMDISK=`euca-register $BUCKET/ramdisk.manifest.xml | tr -d "IMAGE[:blank:]"`
echo "AMI_RAMDISK: $AMI_RAMDISK"

euca-bundle-image -i $ROOTFS -p machine  --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -d $DIR

euca-upload-bundle -m $DIR/machine.manifest.xml -b $BUCKET
if [ "$?" != "0" ]; then
    echo "FAILED: euca-upload-bundle -m $DIR/machine.manifest.xml -b $BUCKET"
    exit -1
fi

AMI_MACHINE=`euca-register $BUCKET/machine.manifest.xml | tr -d "IMAGE[:blank:]"`
echo "AMI_MACHINE: $AMI_MACHINE"

rm -fr "$DIR"

echo $AMI_MACHINE >  $CONFIG
echo $AMI_KERNEL  >> $CONFIG
echo $AMI_RAMDISK >> $CONFIG

STATUS='z'
OLDSTATUS=''
for n in `seq 1 200`; do
	STATUS=$(euca-describe-images $AMI_MACHINE|cut -f5)
	if [ "$STATUS" == "$OLDSTATUS" ]; then
		echo -n "."
	else 
		if [ "$STATUS" == "available" ]; then
			ESC="\033[1;34m"
		else
			ESC="\033[1;33m"
		fi
		echo -en "\033[100D\033[K\033[0mImage's status:$ESC $STATUS"
		OLDSTATUS="$STATUS"
	fi

	if [ "$STATUS" == "available" ]; then
		break
	fi
done

echo -e "\033[0m"
if [ "$STATUS" != "available" ]; then
	echo "Can't get machine image status to available, it's still $STATUS"
	exit -1
fi

euca-authorize -P icmp -t -1:-1 default
euca-authorize -P tcp -p 22 default

echo "euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k rhelkey -t m1.tiny"
echo "euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k rhelkey -t m1.tiny" > cmd.txt
euca-run-instances $AMI_MACHINE --kernel $AMI_KERNEL --ramdisk $AMI_RAMDISK -k rhelkey -t m1.tiny
stack --user abr --project rhelimg compute get_vnc_console instance_id=1
