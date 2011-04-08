#!/bin/bash

prj="swift"
jenkins="localhost:8080"
GithubUserProject="abrindeyev/openstack-nova-rhel6"
TarballsHome="http://$prj.openstack.org/tarballs"
SpecOrig="openstack-$prj.spec"

abspath="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
dirname="$(dirname $abspath)"
cd "$dirname" || exit -1
source triggers
run_trigger
