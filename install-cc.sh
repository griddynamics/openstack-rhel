#!/bin/sh

NETDEV=eth0
CC_ADDR=`ip addr show dev $NETDEV|grep 'inet '|perl -pi -e 's/^.*inet ([0-9\.]+).*$/$1/'`
DB_NAME="nova"
DB_USER="nova"
DB_PASS="nova"
CC_HOST=`hostname`

# Cleanup
yum clean all

# Services for Nova cloud controller - AMQP & DB
yum install -y rabbitmq-server
service rabbitmq-server start
yum install -y mysql-server MySQL-python
service mysqld start

# Creation of Nova database
mysqladmin -u root password "$DB_PASS"

mysqladmin -uroot -p$DB_PASS create $DB_NAME

# Allow incoming MySQL connections over network
iptables -A INPUT -p tcp -m tcp --dport 3306 -j ACCEPT

echo "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'$CC_HOST' IDENTIFIED BY '$DB_PASS';" > grant.sql
mysql -uroot -p$DB_PASS mysql < grant.sql
rm -f grant.sql

# Nova installation
yum install -y euca2ools openstack-nova-api openstack-nova-compute openstack-nova-instancemonitor openstack-nova-network openstack-nova-objectstore openstack-nova-scheduler openstack-nova-volume unzip libvirt qemu-kvm qemu-kvm-tools

modprobe kvm
modprobe kvm-intel
sleep 2
service libvirtd start


# Switching Nova to MySQL db rather than default SQLite
perl -pi -e "s,sql_connection=.*$,sql_connection=mysql://$DB_USER:$DB_PASS\@$CC_ADDR/$DB_NAME," /etc/nova/nova*.conf
perl -pi -e "s,s3_host=.*$,s3_host=$CC_ADDR," /etc/nova/nova*.conf
perl -pi -e "s,cc_host=.*$,cc_host=$CC_ADDR," /etc/nova/nova*.conf
perl -pi -e "s,rabbit_host=.*$,rabbit_host=$CC_ADDR," /etc/nova/nova*.conf
perl -pi -e "s,ec2_url=.*$,ec2_url=http://$CC_ADDR:8773/services/Cloud," /etc/nova/nova*.conf

perl -pi -e "s,fixed_range=.*$,fixed_range=192.168.2.64/26," /etc/nova/nova-{manage,network}.conf
perl -pi -e "s,network_size=.*$,network_size=8," /etc/nova/nova-{manage,network}.conf

# Start Nova services
service openstack-nova-api start
service openstack-nova-compute start
service openstack-nova-network start
service openstack-nova-objectstore start
service openstack-nova-scheduler start

echo "Nova-compute:"
tail -n 5 /var/log/nova/nova-compute.log

echo "Nova-api:"
tail -n 5 /var/log/nova/nova-api.log

echo "Nova-network:"
tail -n 5 /var/log/nova/nova-network.log

echo "Nova-objectstore:"
tail -n 5 /var/log/nova/nova-objectstore.log

echo "Nova-scheduler:"
tail -n 5 /var/log/nova/nova-scheduler.log

