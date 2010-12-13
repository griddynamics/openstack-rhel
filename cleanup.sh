#!/bin/sh

DB_NAME=nova
DB_USER=nova
DB_PASS=nova
CC_HOST=
PWD=nova
ETH=eth0

CC_HOST=`./getmyip.sh $ETH`
HOSTS='gd-1 gd-2 gd-3 gd-4'

for service in api compute objectstore scheduler network; do service openstack-nova-$service stop; done

mysqladmin -uroot -p$PWD -f drop nova
mysqladmin -uroot -p$PWD create nova
rm -f /var/log/nova/nova*log

for h in $HOSTS localhost; do
	echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'$h' IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql
done
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO $DB_USER IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO root IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql

for service in api compute objectstore scheduler network; do service openstack-nova-$service start; done

rm -fr images
