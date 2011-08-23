#!/bin/sh

DB_NAME=nova
DB_USER=nova
DB_PASS=nova
CC_HOST=
PWD=nova
ETH=eth1

CC_HOST=`./getmyip.sh $ETH`
HOSTS='gd-1-local gd-2-local gd-3-local gd-4-local'

for service in api compute objectstore scheduler network; do service openstack-nova-$service stop; done

for n in $(virsh list|grep instance |perl -pi -e 's/^\s*(\d+).*$/$1/'); do virsh destroy $n; done

mysqladmin -uroot -p$PWD -f drop nova
mysqladmin -uroot -p$PWD create nova
nova-manage db sync
rm -f /var/log/nova/nova*log*
rm -fr /var/lib/nova/instances/* /var/lib/nova/images/*
rm -rf /var/lib/libvirt/qemu/save/*

for h in $HOSTS localhost; do
	echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'$h' IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql
done
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO $DB_USER IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO root IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql

for service in api compute objectstore scheduler network; do service openstack-nova-$service start; done

rm -fr images
rm -fr /tmp/tmp*
