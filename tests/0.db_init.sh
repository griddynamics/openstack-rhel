#!/bin/sh

####################################################################
# BIG FAT WARNING:
# ASSUMPTION: a password for root user in MySQL server is `nova' !!!
####################################################################

DB_NAME=nova
DB_USER=nova
DB_PASS=nova
PWD=nova

CC_HOST=$(ip addr show dev eth0 |grep 'inet '|perl -pi -e 's/^.*inet ([\d.]+).*$/$1/')
#CC_HOST="10.0.0.11" # IPv4 address
HOSTS="$CC_HOST localhost" # compute nodes list

./stop.sh

killall dnsmasq
mysqladmin -uroot -p$PWD -f drop nova
for n in $(virsh list --all|grep instance |perl -pi -e 's/^\s*(\d+).*$/$1/'); do virsh destroy $n; done

rm -fr /var/lib/nova/instances/* /var/lib/nova/images/* /var/lib/nova/buckets/* /var/log/nova/*.log* /var/log/glance/*.log /var/lib/glance/images/* /var/lib/glance/glance.sqlite
rm -f /var/lib/nova/CA/serial /var/lib/nova/CA/serial.old  /var/lib/nova/CA/openssl.cnf /var/lib/nova/CA/index.txt* /var/lib/nova/CA/newcerts/* /var/lib/nova/CA/cacert.pem
rm -fr /tmp/tmp*

mysqladmin -uroot -p$PWD create nova

for h in $HOSTS; do
        echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'$h' IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql
done
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO $DB_USER IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql
echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO root IDENTIFIED BY '$DB_PASS';" | mysql -uroot -p$DB_PASS mysql

nova-manage db sync
./start.sh
