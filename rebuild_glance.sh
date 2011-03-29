#!/bin/sh

# If you need to build a specific version - specify it as bzr build # (digits only).
# If build # is not specified, latest available tarball will be built

RPMSANDBOX=`grep topdir $HOME/.rpmmacros 2>/dev/null | awk '{print ($2)}'`
[ "$RPMSANDBOX" == "" ] && RPMSANDBOX="$HOME/rpmbuild/"
GLANCESPECORIG="openstack-glance.spec"
TARBALLSHOME="http://glance.openstack.org/tarballs"

GLANCESPEC="$RPMSANDBOX/SPECS/$GLANCESPECORIG"
GLANCEVER=$(grep '^Version:' $GLANCESPECORIG | sed 's/^Version:\s\+//')

if [ $1 ]; then
	BUILD=$1
else
	BUILD=`curl -s $TARBALLSHOME'/?C=M;O=D'|grep bzr|perl -pi -e 's/^.*bzr(\d+).*$/$1/'|head -n 1`
fi

SRCFILE="glance-$GLANCEVER~bzr$BUILD.tar.gz"
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
	perl -pi -e "s,^Source0:.*$,Source0:          http://glance.openstack.org/tarballs/glance-%{version}~bzr$BUILD.tar.gz," $GLANCESPECORIG
	if [ ! -f "$RPMSRC" ]; then
		wget -O "$RPMSRC" "$TARBALLURL"
	fi
	SPECRELEASE=$(grep '^Release:' $GLANCESPECORIG | sed 's/^Release:\s\+//')
	SPECBUILD=$(echo "$SPECRELEASE" | cut -d. -f3 | sed 's/bzr//')
	if [ "$SPECBUILD" -ne "$BUILD" ]; then
		# Need to increase build in specfile and update changelog
		perl -pi -e 's,^(Release:.+bzr)\d+,${1}'$BUILD',' $GLANCESPECORIG
		rpmdev-bumpspec --comment="- Update to bzr$BUILD" $GLANCESPECORIG
	fi
else
	have_trunk=0
	perl -pi -e "s,^Source0:.*$,Source0:          glance-%{version}.tar.gz,"
fi

SPECRELEASENEW=$(grep '^Release:' $GLANCESPECORIG | sed 's/^Release:\s\+//')
rm -f "$RPMSANDBOX/RPMS/*/*-$GLANCEVER-$SPECRELEASENEW*.rpm" 2>/dev/null
rpmbuild -bb $GLANCESPECORIG
if [ "$?" != "0" ]; then
	git checkout -- "$GLANCESPECORIG"
	exit -1
else
	git add "$GLANCESPECORIG"
	git commit -m "Update to bzr$BUILD"
	git push
fi
rpmbuild -bs $GLANCESPECORIG

for fn in $RPMSANDBOX/RPMS/noarch/*$GLANCEVER-$SPECRELEASENEW*.rpm; do ./sign_rpm $fn; done

if [ ! -d "$REPOPATH" ];
then
	mkdir -p "$REPOPATH"
fi

if [ -f "$RPMSANDBOX/RPMS/noarch/openstack-glance-$GLANCEVER-$SPECRELEASENEW.noarch.rpm" ]; then
	rm -fr $REPOPATH/python-glance*.rpm  $REPOPATH/openstack-glance*.rpm
	mv $RPMSANDBOX/RPMS/noarch/*$GLANCEVER-$SPECRELEASENEW*.rpm "$REPOPATH"
fi


