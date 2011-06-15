#!/bin/sh

# If you need to build a specific version - specify it as bzr build # (digits only).
# If build # is not specified, latest available tarball will be built

GithubUserProject="griddynamics/openstack-rhel"
RPMSANDBOX=`grep topdir $HOME/.rpmmacros 2>/dev/null | awk '{print ($2)}'`
[ "$RPMSANDBOX" == "" ] && RPMSANDBOX="$HOME/rpmbuild/"
SpecOrig="openstack-swift.spec"
TarballsHome="http://swift.openstack.org/tarballs"

Spec="$RPMSANDBOX/SPECS/$SpecOrig"
Version=$(grep '^Version:' $SpecOrig | sed 's/^Version:\s\+//')

if [ $1 ]; then
	BUILD=$1
else
	BUILD=`curl -s $TarballsHome'/?C=M;O=D'|grep bzr|perl -pi -e 's/^.*bzr(\d+).*$/$1/'|head -n 1`
fi

SrcFile="swift-$Version-dev+bzr$BUILD.tar.gz"
RPMSrc="$RPMSANDBOX/SOURCES/$SrcFile"
TarballURL="$TarballsHome/$SrcFile"

if [ ! -d ".git" ]; then
	echo "Need to run from Git repo openstack-nova-rhel6 !"
	exit -1
fi

GitDevBranch="master"
GitCurBranch=$(git branch|grep '*'|cut -f2 -d' ')
REPOPATH="/home/build/repo/$GitCurBranch/openstack"

abspath="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
cd `dirname $abspath`

if [ "$GitDevBranch" == "$GitCurBranch" ]; then
	have_trunk=1
	perl -pi -e "s,^Source0:.*$,Source0:          http://swift.openstack.org/tarballs/swift-%{version}-dev+bzr$BUILD.tar.gz," $SpecOrig
	if [ ! -f "$RPMSrc" ]; then
		wget -O "$RPMSrc" "$TarballURL"
	fi
	SpecRelease=$(grep '^Release:' $SpecOrig | sed 's/^Release:\s\+//' | sed 's/%{?dist}$//')
	SPECBUILD=$(echo "$SpecRelease" | cut -d. -f3 | sed 's/bzr//')
	if [ "$SPECBUILD" -ne "$BUILD" ]; then
		# Need to increase build in specfile and update changelog
		perl -pi -e 's,^(Release:.+bzr)\d+,${1}'$BUILD',' $SpecOrig
		rpmdev-bumpspec --comment="- Update to bzr$BUILD" $SpecOrig
	fi
else
	have_trunk=0
	#perl -pi -e "s,^Source0:.*$,Source0:          swift-%{version}.tar.gz,"
fi

SpecReleaseNew=$(grep '^Release:' $SpecOrig | sed 's/^Release:\s\+//' | sed 's/%{?dist}$//')
rm -f "$RPMSANDBOX/RPMS/*/*-$Version-$SpecReleaseNew*.rpm" 2>/dev/null
rpmbuild -bb $SpecOrig
if [ "$?" != "0" ]; then
	git checkout -- "$SpecOrig"
	exit -1
else
	git add "$SpecOrig"
	git commit -m "Update to bzr$BUILD"
	if [ "$?" != "1" ]; then
		git push
		if [ "$?" != "0" ]; then
			# Somebody pushed a commit to origin since we last time pulled.
			# Need to check - if that commit was to our file or to some other file?
			GitHubUrl="http://github.com/api/v2/json/commits/list/$GithubUserProject/$GitCurBranch"
			LastRepoCommit="$(curl -s $GitHubUrl | perl -MJSON::XS -e "\$a='';while(<>){\$a.=\$_} \$d=decode_json(\$a);print \$d->{'commits'}[0]->{'id'}")"
			LastSpecCommit="$(curl -s $GitHubUrl/$SpecOrig | perl -MJSON::XS -e "\$a='';while(<>){\$a.=\$_} \$d=decode_json(\$a);print \$d->{'commits'}[0]->{'id'}")"
			if [[ "$LastRepoCommit" != "$LastSpecCommit" ]]; then
				# Last Git repo commit was not to our specfile
				# Probably we can safely do git pull to merge following by git push
				git pull
				if [ "$?" != "0" ]; then
					echo "Sorry, automatic merge failed"
					echo "Human intervention required, giving up here"
					exit -1
				fi
				git push
			else
				# Last commit was to our specfile
				git pull
				echo "There should be a conflict above, please fix by hands and commit"
				exit -1
			fi
		fi
	fi
fi
rpmbuild -bs $SpecOrig

for fn in $RPMSANDBOX/RPMS/noarch/openstack-swift-*$Version-*.rpm; do ./sign_rpm $fn; done

if [ ! -d "$REPOPATH" ];
then
	mkdir -p "$REPOPATH"
fi

rm -fr $REPOPATH/openstack-swift-$Version-*.rpm $REPOPATH/openstack-swift-{account,auth,container,object,proxy,doc}-$Version-*.rpm
mv $RPMSANDBOX/RPMS/noarch/*$Version-$SpecReleaseNew*.rpm "$REPOPATH"
