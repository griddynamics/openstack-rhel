#!/bin/sh

NOVAVER="2011.2"

abspath="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
cd `dirname $abspath`

# If you need to build a specific version - specify it as bzr build # (digits only).
# If build # is not specified, latest available tarball will be built
if [ $1 ]; then
	BUILD=$1
else
	BUILD=`curl -s 'http://nova.openstack.org/tarballs/?C=M;O=D'|grep bzr|perl -pi -e 's/^.*bzr(\d+).*$/$1/'|head -n 1`
fi

REPOPATH="/var/www/html/openstack-nova"
RPMSANDBOX="$HOME/rpmbuild/"
SRCFILE="nova-$NOVAVER~bzr$BUILD.tar.gz"
RPMSRC="$RPMSANDBOX/SOURCES/$SRCFILE"
TARBALLURL="http://nova.openstack.org/tarballs/$SRCFILE"

NOVASPECORIG="openstack-nova.spec"
NOVASPEC="$RPMSANDBOX/SPECS/openstack-nova.spec"

if [ ! -f "$RPMSRC" ]; then
	wget -O "$RPMSRC" "$TARBALLURL"
fi

#cat $NOVASPECORIG | perl -pi -e "s/bzr(\d+)/bzr$BUILD/" > $NOVASPEC
rm -f $NOVASPEC >/dev/null 2>/dev/null
cp $NOVASPECORIG $NOVASPEC
rm -f "$RPMSANDBOX/RPMS/*/*bzr$BUILD*.rpm"
rpmbuild -bb $NOVASPEC || exit -1
rpmbuild -bs $NOVASPEC || exit -1
rm -f $NOVASPEC

if [ -f "$RPMSANDBOX/RPMS/noarch/openstack-nova-$NOVAVER-bzr$BUILD.noarch.rpm" ]; then
	rm -fr $REPOPATH/*bzr*.rpm
	mv $RPMSANDBOX/RPMS/noarch/*bzr$BUILD*.rpm "$REPOPATH"
	for fn in $REPOPATH/*.rpm; do ./sign_rpm $fn; done
	createrepo "$REPOPATH"
fi

