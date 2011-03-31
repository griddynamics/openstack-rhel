#!/bin/sh

# If you need to build a specific version - specify it as bzr build # (digits only).
# If build # is not specified, latest available tarball will be built

RPMSANDBOX=`grep topdir $HOME/.rpmmacros 2>/dev/null | awk '{print ($2)}'`
[ "$RPMSANDBOX" == "" ] && RPMSANDBOX="$HOME/rpmbuild/"
NOVASPECORIG="openstack-nova.spec"
TARBALLSHOME="http://nova.openstack.org/tarballs"

NOVASPEC="$RPMSANDBOX/SPECS/$NOVASPECORIG"
NOVAVER=$(grep '^Version:' $NOVASPECORIG | sed 's/^Version:\s\+//')

if [ $1 ]; then
	BUILD=$1
else
	BUILD=`curl -s $TARBALLSHOME'/?C=M;O=D'|grep bzr|perl -pi -e 's/^.*bzr(\d+).*$/$1/'|head -n 1`
fi

SRCFILE="nova-$NOVAVER~bzr$BUILD.tar.gz"
RPMSRC="$RPMSANDBOX/SOURCES/$SRCFILE"
TARBALLURL="$TARBALLSHOME/$SRCFILE"

if [ ! -d ".git" ]; then
	echo "Need to run from Git repo openstack-nova-rhel6 !"
	exit -1
fi

GITDEVBRANCH="master"
GITCURBRANCH=$(git branch|grep '*'|cut -f2 -d' ')
REPOPATH="/home/build/repo/$GITCURBRANCH/nova"

abspath="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
cd `dirname $abspath`

if [ "$GITDEVBRANCH" == "$GITCURBRANCH" ]; then
	have_trunk=1
	perl -pi -e "s,^Source0:.*$,Source0:          http://nova.openstack.org/tarballs/nova-%{version}~bzr$BUILD.tar.gz," $NOVASPECORIG
	if [ ! -f "$RPMSRC" ]; then
		wget -O "$RPMSRC" "$TARBALLURL"
	fi
	SPECRELEASE=$(grep '^Release:' $NOVASPECORIG | sed 's/^Release:\s\+//')
	SPECBUILD=$(echo "$SPECRELEASE" | cut -d. -f3 | sed 's/bzr//')
	if [ "$SPECBUILD" -ne "$BUILD" ]; then
		# Need to increase build in specfile and update changelog
		perl -pi -e 's,^(Release:.+bzr)\d+,${1}'$BUILD',' $NOVASPECORIG
		rpmdev-bumpspec --comment="- Update to bzr$BUILD" $NOVASPECORIG
	fi
else
	have_trunk=0
	perl -pi -e "s,^Source0:.*$,Source0:          nova-%{version}.tar.gz,"
fi

SPECRELEASENEW=$(grep '^Release:' $NOVASPECORIG | sed 's/^Release:\s\+//')
rm -f "$RPMSANDBOX/RPMS/*/*-$NOVAVER-$SPECRELEASENEW*.rpm" 2>/dev/null
rpmbuild -bb $NOVASPECORIG
if [ "$?" != "0" ]; then
	git checkout -- "$NOVASPECORIG"
	exit -1
else
	git add "$NOVASPECORIG"
	git commit -m "Update to bzr$BUILD"
	git push
fi
rpmbuild -bs $NOVASPECORIG

for fn in $RPMSANDBOX/RPMS/noarch/*$NOVAVER-$SPECRELEASENEW*.rpm; do ./sign_rpm $fn; done

if [ ! -d "$REPOPATH" ];
then
	mkdir -p "$REPOPATH"
fi

if [ -f "$RPMSANDBOX/RPMS/noarch/openstack-nova-$NOVAVER-$SPECRELEASENEW.noarch.rpm" ]; then
	rm -fr $REPOPATH/python-nova-$NOVAVER-*.rpm $REPOPATH/openstack-nova-$NOVAVER-*.rpm $REPOPATH/openstack-nova-{api,compute,doc,instancemonitor,network,objectstore,scheduler,volume}-$NOVAVER-*.rpm $REPOPATH/openstack-nova-node-*-$NOVAVER-*.rpm
	mv $RPMSANDBOX/RPMS/noarch/*$NOVAVER-$SPECRELEASENEW*.rpm "$REPOPATH"
fi

