%global with_doc 1

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-swift
Version:	1.4.2
Release:	0.20110725.330%{?dist}
Summary:          OpenStack Object Storage (swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://swift.openstack.org/tarballs/swift-1.4.2~20110725.330.tar.gz  
Source1:          %{name}-functions
Source2:          %{name}-account-auditor.init
Source3:          %{name}-account-reaper.init
Source4:          %{name}-account-replicator.init
Source5:          %{name}-account-server.init
Source7:          %{name}-container-auditor.init
Source8:          %{name}-container-replicator.init
Source9:          %{name}-container-server.init
Source10:          %{name}-container-updater.init
Source11:          %{name}-object-auditor.init
Source12:          %{name}-object-replicator.init
Source13:          %{name}-object-server.init
Source14:          %{name}-object-updater.init
Source15:          %{name}-proxy.init
BuildRoot:        %{_tmppath}/swift-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-simplejson
Requires:         python-webob >= 0.9.8
Requires:         python-nose
Requires:         pyxattr
Requires:         python-netifaces
Requires:         python-paste-deploy

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

%description
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new nodes,
which are automatically configured. Should a node fail, OpenStack works to
replicate its content from other active nodes. Because OpenStack uses software
logic to ensure data replication and distribution across different devices,
inexpensive commodity hard drives and servers can be used in lieu of more
expensive equipment.

%package          account
Summary:          A swift account server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      account
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} account server.

%package          container
Summary:          A swift container server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      container
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} container server.

%package          object
Summary:          A swift object server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      object
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} object server.

%package          proxy
Summary:          A swift proxy server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      proxy
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} proxy server.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{name}
Group:            Documentation

BuildRequires:    python-sphinx
# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-simplejson
BuildRequires:    python-webob
BuildRequires:    pyxattr

%description      doc
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n swift-%{version}
# Fix wrong-file-end-of-line-encoding warning
dos2unix LICENSE

%build
%{__python} setup.py build

%if 0%{?with_doc}
mkdir doc/build
python setup.py build_sphinx
# Fix hidden-file-or-dir warning 
rm doc/build/html/.buildinfo
%endif

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Init helper functions
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_datarootdir}/%{name}/functions
# Init scripts
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-account-auditor
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-account-reaper
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-account-replicator
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-account-server
install -p -D -m 755 %{SOURCE7} %{buildroot}%{_initrddir}/%{name}-container-auditor
install -p -D -m 755 %{SOURCE8} %{buildroot}%{_initrddir}/%{name}-container-replicator
install -p -D -m 755 %{SOURCE9} %{buildroot}%{_initrddir}/%{name}-container-server
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{name}-container-updater
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-object-auditor
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-object-replicator
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-object-server
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-object-updater
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-proxy
# Install man stubs
for name in $( ls ./man ); do
    mkdir -p "%{buildroot}%{_mandir}/$name"
    cp "./man/$name/"*.gz "%{buildroot}%{_mandir}/$name"
done
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/swift
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift

%clean
rm -rf %{buildroot}

%pre
getent group swift >/dev/null || groupadd -r swift
getent passwd swift >/dev/null || \
useradd -r -g swift -d %{_sharedstatedir}/swift -s /sbin/nologin \
-c "OpenStack Swift Daemons" swift
exit 0

%post account
/sbin/chkconfig --add %{name}-account-auditor
/sbin/chkconfig --add %{name}-account-reaper
/sbin/chkconfig --add %{name}-account-replicator
/sbin/chkconfig --add %{name}-account-server

%preun account
if [ $1 = 0 ] ; then
    /sbin/service %{name}-account-auditor stop >/dev/null 2>&1
    /sbin/service %{name}-account-reaper stop >/dev/null 2>&1
    /sbin/service %{name}-account-replicator stop >/dev/null 2>&1
    /sbin/service %{name}-account-server stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-account-auditor
    /sbin/chkconfig --del %{name}-account-reaper
    /sbin/chkconfig --del %{name}-account-replicator
    /sbin/chkconfig --del %{name}-account-server
fi

%postun account
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-account-auditor condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-account-reaper condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-account-replicator condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-account-server condrestart >/dev/null 2>&1 || :
fi

%post container
/sbin/chkconfig --add %{name}-container-auditor
/sbin/chkconfig --add %{name}-container-replicator
/sbin/chkconfig --add %{name}-container-server
/sbin/chkconfig --add %{name}-container-updater

%preun container
if [ $1 = 0 ] ; then
    /sbin/service %{name}-container-auditor stop >/dev/null 2>&1
    /sbin/service %{name}-container-replicator stop >/dev/null 2>&1
    /sbin/service %{name}-container-server stop >/dev/null 2>&1
    /sbin/service %{name}-container-updater stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-container-auditor
    /sbin/chkconfig --del %{name}-container-replicator
    /sbin/chkconfig --del %{name}-container-server
    /sbin/chkconfig --del %{name}-container-updater
fi

%postun container
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-container-auditor condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-container-replicator condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-container-server condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-container-updater condrestart >/dev/null 2>&1 || :
fi

%post object
/sbin/chkconfig --add %{name}-object-auditor
/sbin/chkconfig --add %{name}-object-replicator
/sbin/chkconfig --add %{name}-object-server
/sbin/chkconfig --add %{name}-object-updater

%preun object
if [ $1 = 0 ] ; then
    /sbin/service %{name}-object-auditor stop >/dev/null 2>&1
    /sbin/service %{name}-object-replicator stop >/dev/null 2>&1
    /sbin/service %{name}-object-server stop >/dev/null 2>&1
    /sbin/service %{name}-object-updater stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-object-auditor
    /sbin/chkconfig --del %{name}-object-replicator
    /sbin/chkconfig --del %{name}-object-server
    /sbin/chkconfig --del %{name}-object-updater
fi

%postun object
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-object-auditor condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-object-replicator condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-object-server condrestart >/dev/null 2>&1 || :
    /sbin/service %{name}-object-updater condrestart >/dev/null 2>&1 || :
fi

%post proxy
/sbin/chkconfig --add %{name}-proxy

%preun proxy
if [ $1 = 0 ] ; then
    /sbin/service %{name}-proxy stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-proxy
fi

%postun proxy
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name}-proxy condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift
%dir %{_sysconfdir}/swift
%dir %{python_sitelib}/swift
%{_datarootdir}/%{name}/functions
%{_bindir}/swift
%{_bindir}/swift-account-audit
#%{_bindir}/swift-account-stats-logger
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
#%{_bindir}/swift-log-stats-collector
#%{_bindir}/swift-log-uploader
%{_bindir}/swift-ring-builder
%{_bindir}/swift-stats-populate
%{_bindir}/swift-stats-report
%{_bindir}/swift-dispersion-populate
%{_bindir}/swift-dispersion-report
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/common
#%{python_sitelib}/swift/stats
%{python_sitelib}/swift-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%{_initrddir}/%{name}-account-*
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{python_sitelib}/swift/account

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%{_initrddir}/%{name}-container-*
%{_bindir}/swift-bench
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
#%{_bindir}/swift-container-stats-logger
%{_bindir}/swift-container-sync
%{_bindir}/swift-container-updater
%{python_sitelib}/swift/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%{_initrddir}/%{name}-object-*
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{python_sitelib}/swift/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%{_initrddir}/%{name}-proxy
%{_bindir}/swift-proxy-server
%{python_sitelib}/swift/proxy

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif

%changelog
* Tue Jul 19 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 1.4.2-0.20110713.325
- Added /usr/bin/swift-container-sync
- changelog cleanup

* Fri May 06 2011 Jasper Capel <jasper.capel@spilgames.com> - 1.4.0-6.bzr287
- Changed init-functions script to accomodate extra init scripts
- Removed auth init script (there only is swauth now, which is loaded from
  proxy)
- Fixed proxy init script so it will still start with the changes to the
  function script

* Fri May 06 2011 Jasper Capel <jasper.capel@spilgames.com> - 1.4-0.5.bzr287
- Added dependency on python-netifaces
- Added dependency on python-paste-deploy
- Added init scripts for swift-{container,object,account}-*
- Removed unnecessary direcories
- Removed %dir definition for components that are not directories 

* Fri Apr 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 1.4-0.1.bzr268
- Diablo versioning

* Fri Apr 08 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 1.3-0.3.bzr263
- Changed name of initscripts

* Tue Apr 05 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 1.3-0.1.bzr262
- Bumped version to Cactus

* Tue Apr 05 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 1.2.0-1
- Basic update to version 1.2.0

* Thu Nov 03 2010 Silas Sewell <silas@sewell.ch> - ???????
- Add doc flag
- Remove custom man pages

* Sun Aug 08 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-5
- Update for new Python macro guidelines
- Use dos2unix instead of sed
- Make gecos field more descriptive

* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-4
- Rename to openstack-swift

* Wed Jul 28 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-3
- Fix return value in swift-functions

* Tue Jul 27 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-2
- Add swift user
- Update init scripts

* Sun Jul 18 2010 Silas Sewell <silas@sewell.ch> - 1.0.2-1
- Initial build
