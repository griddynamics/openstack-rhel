%global with_doc 1

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-swift
Version:          1.0.2
Release:          5%{?dist}
Summary:          OpenStack Object Storage (swift)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://launchpad.net/swift
Source0:          http://launchpad.net/swift/1.0/%{version}/+download/swift-%{version}.tar.gz
Source1:          %{name}-functions
Source2:          %{name}-account.init
Source3:          %{name}-auth.init
Source4:          %{name}-container.init
Source5:          %{name}-object.init
Source6:          %{name}-proxy.init
BuildRoot:        %{_tmppath}/swift-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-simplejson
Requires:         python-webob
Requires:         pyxattr

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

%package          auth
Summary:          A swift auth server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      auth
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} auth server.

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
pushd doc; make html; popd
# Fix hidden-file-or-dir warning 
rm doc/build/html/.buildinfo
%endif

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# Init helper functions
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_datarootdir}/%{name}/functions
# Init scripts
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-account
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-auth
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-container
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-object
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/%{name}-proxy
# Install man stubs
for name in $( ls ./man ); do
    mkdir -p "%{buildroot}%{_mandir}/$name"
    cp "./man/$name/"*.gz "%{buildroot}%{_mandir}/$name"
done
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/swift
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/account-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/auth-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/container-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/object-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/proxy-server
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/account-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/auth-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/container-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/object-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/proxy-server

%clean
rm -rf %{buildroot}

%pre
getent group swift >/dev/null || groupadd -r swift
getent passwd swift >/dev/null || \
useradd -r -g swift -d %{_sharedstatedir}/swift -s /sbin/nologin \
-c "OpenStack Swift Daemons" swift
exit 0

%post account
/sbin/chkconfig --add swift-account

%preun account
if [ $1 = 0 ] ; then
    /sbin/service swift-account stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-account
fi

%postun account
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-account condrestart >/dev/null 2>&1 || :
fi

%post auth
/sbin/chkconfig --add swift-auth

%preun auth
if [ $1 = 0 ] ; then
    /sbin/service swift-auth stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-auth
fi

%postun auth
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-auth condrestart >/dev/null 2>&1 || :
fi

%post container
/sbin/chkconfig --add swift-container

%preun container
if [ $1 = 0 ] ; then
    /sbin/service swift-container stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-container
fi

%postun container
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-container condrestart >/dev/null 2>&1 || :
fi

%post object
/sbin/chkconfig --add swift-object

%preun object
if [ $1 = 0 ] ; then
    /sbin/service swift-object stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-object
fi

%postun object
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-object condrestart >/dev/null 2>&1 || :
fi

%post proxy
/sbin/chkconfig --add swift-proxy

%preun proxy
if [ $1 = 0 ] ; then
    /sbin/service swift-proxy stop >/dev/null 2>&1
    /sbin/chkconfig --del swift-proxy
fi

%postun proxy
if [ "$1" -ge "1" ] ; then
    /sbin/service swift-proxy condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%dir %{_datarootdir}/%{name}/functions
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift
%dir %{_sysconfdir}/swift
%dir %{python_sitelib}/swift
%{_bindir}/st
%{_bindir}/swift-account-audit
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-stats-populate
%{_bindir}/swift-stats-report
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/common
%{python_sitelib}/swift-%{version}-*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%dir %{_initrddir}/%{name}-account
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/account-server
%dir %{_sysconfdir}/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{python_sitelib}/swift/account

%files auth
%defattr(-,root,root,-)
%doc etc/auth-server.conf-sample
%dir %{_initrddir}/%{name}-auth
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/auth-server
%dir %{_sysconfdir}/swift/auth-server
%{_bindir}/swift-auth-create-account
%{_bindir}/swift-auth-recreate-accounts
%{_bindir}/swift-auth-server
%{python_sitelib}/swift/auth

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%dir %{_initrddir}/%{name}-container
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/container-server
%dir %{_sysconfdir}/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{python_sitelib}/swift/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%dir %{_initrddir}/%{name}-object
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/object-server
%dir %{_sysconfdir}/swift/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{python_sitelib}/swift/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%dir %{_initrddir}/%{name}-proxy
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/proxy-server
%dir %{_sysconfdir}/swift/proxy-server
%{_bindir}/swift-proxy-server
%{python_sitelib}/swift/proxy

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif

%changelog
* ??? Nov 03 2010 Silas Sewell <silas@sewell.ch> - ???????
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
