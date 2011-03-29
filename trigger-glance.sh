#!/bin/bash

prj="glance"
jenkins="localhost:8080"
GithubUserProject="abrindeyev/openstack-nova-rhel6"
TarballsHome="http://$prj.openstack.org/tarballs"
SpecOrig="openstack-$prj.spec"

abspath="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
dirname="$(dirname $abspath)"
cd "$dirname" || exit -1
if [[ "$dirname" =~ /jobs/.*/workspace$ ]]
then
	jobname="$(echo $dirname | sed 's/^.*\/jobs\/\([^/]\+\)\/workspace$/\1/')"
	# Query job status
	jobinqueue="$(curl -s http://$jenkins/job/$jobname/api/json | perl -MJSON::XS -e "\$a='';while(<>){\$a.=\$_} \$d=decode_json(\$a);print \$d->{'inQueue'}")"
	if [[ "$jobinqueue" == 1 ]];
	then
		# Job sits in queue, exiting
		exit 0
	fi
else
	echo "This script is designed to run from within Jenkins workspace"
	exit -1
fi

SpecVer=$(grep '^Version:' $SpecOrig | sed 's/^Version:\s\+//')
SpecRelease=$(grep '^Release:' $SpecOrig | sed 's/^Release:\s\+//')

# Gathering actual revisions
Build="$(curl -s $TarballsHome'/?C=M;O=D' | grep $SpecVer | grep bzr | perl -pi -e 's/^.*bzr(\d+).*$/$1/' | head -n 1)"
GitCurBranch="$(git branch|grep '*'|cut -f2 -d' ')"
GitRev="$(curl -s http://github.com/api/v2/json/commits/list/$GithubUserProject/$GitCurBranch/$SpecOrig | perl -MJSON::XS -e "\$a='';while(<>){\$a.=\$_} \$d=decode_json(\$a);print \$d->{'commits'}[0]->{'id'}")"

# Gathering our revisions
OurBuild=$(echo "$SpecRelease" | cut -d. -f3 | sed 's/bzr//')
OurRev=$(git log --pretty=format:"%H" -1 $SpecOrig)

FireNewBuild=0
if [[ "$Build" -ne "$OurBuild" ]]; then
	FireNewBuild=1
fi
if [[ "$GitRev" != "$OurRev" ]]; then
	FireNewBuild=1
fi

if [[ "$FireNewBuild" == 1 ]];
then
	curl -s "http://$jenkins/job/$jobname/build"
fi
