#!/bin/bash

# If you need to build a specific version - specify it as ./build # (digits only).
# If build # is not specified, latest available tarball will be built

NOACTION=n
DEBUG=y

TARBALLSHOME="http://nova.openstack.org/tarballs"
CURVERSION=(`curl -s $TARBALLSHOME/?C=M\;O=D | grep -m 1 'nova-[0-9]' | perl -p -e 's!^.*nova-(\d+\.\d+)~(\w+)~(\d+\.\d+)\.tar\.gz.*$!\n$1 $2 $3 $4 $5\n!i'`)

if [ ! -d ".git" ]; then
        echo "Need to run from Git repo openstack-nova-rhel6 !"
        exit -1
fi

if [ $1 ]; then
        BUILD=$1
else
        BUILD=${CURVERSION[2]}
fi



GithubUserProject="griddynamics/openstack-rhel"
RPMSANDBOX=`grep topdir $HOME/.rpmmacros 2>/dev/null | awk '{print ($2)}'`
[ "$RPMSANDBOX" == "" ] && RPMSANDBOX="$HOME/rpmbuild/"

##  --- MY VARS --

RPMMOCK=$RPMSANDBOX/MOCK

OLDSPEC="openstack-nova.spec"
OLDVER=$(grep '^Version:' $OLDSPEC | sed 's/^Version:\s\+//')
OLDRELEASE=$(grep '^Release:' $OLDSPEC | sed 's/^Release:\s\+//' | sed 's/%{?dist}$//')

BUILDSPEC="$RPMSANDBOX/SPECS/$OLDSPEC"
NEWVER=${CURVERSION[0]}
BR=${CURVERSION[1]}
NEWRELEASE=${CURVERSION[2]}

NEWBUILDFILE="nova-$NEWVER~$BR~$BUILD.tar.gz"
RPMSRC="$RPMSANDBOX/SOURCES/$NEWBUILDFILE"
TARBALLURL="$TARBALLSHOME/$NEWBUILDFILE"
BUILDLOG='mktemp'

[ $DEBUG ] && echo "CURVERSION=${CURVERSION[@]}"
[ $DEBUG ] && echo "RPMSANDBOX = $RPMSANDBOX"
[ $DEBUG ] && echo "OLDVER = $OLDVER"
[ $DEBUG ] && echo "OLDRELEASE = 0.$OLDRELEASE"
[ $DEBUG ] && echo "NEWVER = $NEWVER"
[ $DEBUG ] && echo "NEWRELEASE = $NEWRELEASE"
[ $DEBUG ] && echo "TARBALLURL = $TARBALLURL"



GITDEVBRANCH="master"
GITCURBRANCH=$(git branch|grep '*'|cut -f2 -d' ')
REPOPATH="/home/build/repo/$GITCURBRANCH/openstack"

abspath="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
cd `dirname $abspath`

[ $DEBUG ] && echo "GITCURBRANCH = $GITCURBRANCH"
[ $DEBUG ] && echo "GITDEVBRANCH = $GITDEVBRANCH"


## Update SPEC file and get tarball
if [ "$GITDEVBRANCH" == "$GITCURBRANCH" ]; then
        have_trunk=1
        [ $DEBUG ] && echo "Building release - $BUILD"
        [ $NOACTION ] && perl -pi -e "s,^Source0:.*$,Source0:          $TARBALLURL," $OLDSPEC


        if [ ! -f "$RPMSRC" ]; then
                wget -O "$RPMSRC" "$TARBALLURL"
        fi
#       SPECRELEASE=$(grep '^Release:' $NOVASPECORIG | sed 's/^Release:\s\+//' | sed 's/%{?dist}$//')
#       SPECBUILD=$(echo "$SPECRELEASE" | cut -d. -f3 | sed 's/bzr//')
#       [ $DEBUG ] && echo "SPECRELEASE = $SPECRELEASE"
#       [ $DEBUG ] && echo "SPECBUILD = $SPECBUILD"
#       if [ "$SPECBUILD" -ne "$BUILD" ]; then
#               # Need to increase build in specfile and update changelog
#               [ $NOACTION ] && perl -pi -e 's,^(Release:.+bzr)\d+,${1}'$BUILD',' $NOVASPECORIG
                perl -pi -e 's,^(Version:).*$,${1}\t'$NEWVER'%{\?dist},' $OLDSPEC
                perl -pi -e 's,^(Release:).*%{\?dist}$,${1}\t0\.'$BUILD'%{\?dist},' $OLDSPEC
#               [ $NOACTION ] && rpmdev-bumpspec --comment="- Update to bzr$BUILD" $NOVASPECORIG
#               [ $DEBUG ] && echo "Comment to spec =  Update to bzr$BUILD"
#       fi
else
        [ $DEBUG ] && echo "There is NO new build - $BUILD"
        have_trunk=0
        #perl -pi -e "s,^Source0:.*$,Source0:          nova-%{version}.tar.gz,"
fi

# Remove RPM of this build  if exist
#SPECRELEASENEW=$(grep '^Release:' $NOVASPECORIG | sed 's/^Release:\s\+//' | sed 's/%{?dist}$//')
[ $NOACTION ] && rm -f "$RPMSANDBOX/RPMS/*/*$NEWRELEASE*.rpm" 2>/dev/null

# Build new RPM
[ $DEBUG ] &&  echo "Building RPM.."
[ $NOACTION ] && rpmbuild -bb $OLDSPEC > $BUILDLOG 2>&1
DONERPM=`cat $BUILDLOG |grep 'Wrote:' | sed 's/Wrote://'`
[ $DEBUG ] &&  echo "RPM Done: $DONERPM"



# Build fail
if [ "$?" != "0" ]; then
    [ $DEBUG ] &&  echo "Build fail. Return to privious state."
    [ $NOACTION ] && git checkout -- "$OLDSPEC"
    exit -1
else
    # Build success
    [ $DEBUG ] &&  echo "Build success. Commiting new SPEC."
#    [ $NOACTION ] && git add "$OLDSPEC"
#    [ $NOACTION ] && git commit -m "Update to $BUILD"
        if [ "$?" != "1" ]; then
#       [ $NOACTION ] && git push
                if [ "$?" != "0" ]; then
                        # Somebody pushed a commit to origin since we last time pulled.
                        # Need to check - if that commit was to our file or to some other file?
                        GitHubUrl="http://github.com/api/v2/json/commits/list/$GithubUserProject/$GITCURBRANCH"
                        LastRepoCommit="$(curl -s $GitHubUrl | perl -MJSON::XS -e "\$a='';while(<>){\$a.=\$_} \$d=decode_json(\$a);print \$d->{'commits'}[0]->{'id'}")"
                        LastSpecCommit="$(curl -s $GitHubUrl/$OLDSPEC | perl -MJSON::XS -e "\$a='';while(<>){\$a.=\$_} \$d=decode_json(\$a);print \$d->{'commits'}[0]->{'id'}")"
                        if [[ "$LastRepoCommit" != "$LastSpecCommit" ]]; then
                                # Last Git repo commit was not to our specfile
                                # Probably we can safely do git pull to merge following by git push
#                               [ $NOACTION ] && git pull
                                if [ "$?" != "0" ]; then
                                        echo "Sorry, automatic merge failed"
                                        echo "Human intervention required, giving up here"
                                        exit -1
                                fi
#                               [ $NOACTION ] && git push
                        else
                                # Last commit was to our specfile
#                               [ $NOACTION ] && git pull
                                echo "There should be a conflict above, please fix by hands and commit"
                                exit -1
                        fi
                fi
        fi
fi

[ $DEBUG ] &&  echo "Building SRPM.."
[ $NOACTION ] && rpmbuild --quiet -bs $OLDSPEC

[ $DEBUG ] &&  echo "Signing RPM.."
# fix it. Neet rpmbuild output
[ $NOACTION ] && for fn in $RPMSANDBOX/RPMS/noarch/*$NEWRELEASE*.rpm; do ./sign_rpm $fn; done

if [ ! -d "$REPOPATH" ];
then
        mkdir -p "$REPOPATH"
fi

[ $DEBUG ] &&  echo "Moving RPM to repo.."
[ $NOACTION ] && rm -fr $REPOPATH/python-nova-$OLDVER-*.rpm $REPOPATH/openstack-nova-$OLDVER-*.rpm $REPOPATH/openstack-nova-{api,compute,doc,instancemonitor,network,noVNC,objectstore,scheduler,volume}-$OLDVER-*.rpm $REPOPATH/openstack-nova-node-*-$OLDVER-*.rpm

[ $NOACTION ] && for FILE in $DONERPM; do  mv $FILE "$REPOPATH";  done;

[ $DEBUG ] &&  echo "Generating RPM for RHEL 6.1.."

cp $RPMSANDBOX/SRPMS/openstack-nova-*-$NEWRELEASE.*.src.rpm /tmp/
[ $NOACTION ] && sudo  mock /tmp/openstack-nova-*-$NEWRELEASE.*.src.rpm
