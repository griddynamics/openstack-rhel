#!/bin/sh

NOVAVER="2011.1"

if [ $1 ]; then
	BUILD=$1
else
	echo "Specify build to package it"
	exit -1
fi

REPOPATH="/var/www/html/openstack-nova"
RPMSANDBOX="$HOME/rpmbuild/"
SRCFILE="nova-$NOVAVER~bzr$BUILD.tar.gz"
RPMSRC="$RPMSANDBOX/SOURCES/$SRCFILE"
TARBALLURL="http://nova.openstack.org/tarballs/$SRCFILE"

NOVASPEC="$RPMSANDBOX/SPECS/openstack-nova.spec"

if [ ! -f "$RPMSRC" ]; then
	wget -O "$RPMSRC" "$TARBALLURL"
fi

perl -pi -e "s/bzr(\d+)/bzr$BUILD/" "$NOVASPEC"
rm -f "$RPMSANDBOX/RPMS/*/*bzr$BUILD*.rpm"
rpmbuild -bb $NOVASPEC

#if [ -f "$RPMSANDBOX/RPMS/noarch/python-nova*bzr$BUILD*.rpm" ]; then
	rm -fr $REPOPATH/*bzr*.rpm
	mv $RPMSANDBOX/RPMS/noarch/*bzr$BUILD*.rpm "$REPOPATH"
	createrepo "$REPOPATH"
#fi

