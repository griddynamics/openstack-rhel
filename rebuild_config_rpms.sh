#!/bin/sh

if [ ! -d ".git" ]; then
	echo "Need to run from Git repo openstack-nova-rhel6 !"
	exit -1
fi
sandbox='/home/build/rpmbuild/RPMS/noarch'
branch=$(git branch|grep '*'|cut -f2 -d' ')
repo="/home/build/repo/$branch/openstack/"
host=`hostname -s`
if [[ "$host" != "je-cssn" ]]; then
	echo "That script should be run only on Jenkins host!"
fi

rpmbuild -ba openstack-nova-cc-config.spec
if [ "$?" != "0" ]; then
	exit -1
fi

rpmbuild -ba openstack-nova-compute-config.spec
if [ "$?" != "0" ]; then
	exit -1
fi

./sign_rpm $sandbox/openstack-nova-cc-config-*.rpm
./sign_rpm $sandbox/openstack-nova-compute-config-*.rpm

rm -f $repo/openstack-nova-cc-config*.rpm
rm -f $repo/openstack-nova-compute-config*.rpm

mv $sandbox/openstack-nova-cc-config-*.rpm $sandbox/openstack-nova-compute-config-*.rpm $repo

