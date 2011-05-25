%global with_doc 1
%global prj glance

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-%{prj}
Version:          2011.3
Release:          0.17.bzr133%{?dist}
Summary:          OpenStack Image Registry and Delivery Service

Group:            Development/Languages
License:          ASL 2.0
URL:              http://%{prj}.openstack.org
Source0:          http://glance.openstack.org/tarballs/glance-%{version}~bzr133.tar.gz
Source1:          %{name}-api.init
Source2:          %{name}-registry.init
Source3:          %{name}-logging-api.conf
Source4:          %{name}-logging-registry.conf

Patch1:           %{name}-configs.patch

BuildRoot:        %{_tmppath}/%{prj}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils
Requires:         python-%{prj} = %{version}-%{release}

%description
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains the API server and a reference implementation registry
server, along with a client library.

%package -n       python-%{prj}
Summary:          Glance Python libraries
Group:            Applications/System

Requires:         python-anyjson
Requires:         python-argparse
Requires:         python-daemon = 1.5.5
Requires:         python-eventlet >= 0.9.12
Requires:         python-gflags >= 1.3
Requires:         python-lockfile = 0.8
Requires:         python-mox >= 0.5.0
Requires:         python-routes
Requires:         python-sqlalchemy >= 0.6.3
Requires:         python-webob

%description -n   python-%{prj}
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains the project's Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Glance
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-nose
# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-daemon
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob

%description      doc
The Glance project provides services for discovering, registering, and
retrieving virtual machine images. Glance has a RESTful API that allows
querying of VM image metadata as well as retrieval of the actual image.

This package contains documentation files for OpenStack Glance.

%endif

%prep
%setup -q -n %{prj}-%{version}

%patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{prj}/images

# Config file
install -p -D -m 644 etc/%{prj}-api.conf %{buildroot}%{_sysconfdir}/%{prj}/%{prj}-api.conf
install -p -D -m 644 etc/%{prj}-registry.conf %{buildroot}%{_sysconfdir}/%{prj}/%{prj}-registry.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{prj}/logging-api.conf
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{prj}/logging-registry.conf

# Initscripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-registry

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{prj}

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{prj}

%clean
rm -rf %{buildroot}

%pre
getent group %{prj} >/dev/null || groupadd -r %{prj}
getent passwd %{prj} >/dev/null || \
useradd -r -g %{prj} -d %{_sharedstatedir}/%{prj} -s /sbin/nologin \
-c "OpenStack Glance Daemons" %{prj}
exit 0

%post
/sbin/chkconfig --add openstack-%{prj}-api
/sbin/chkconfig --add openstack-%{prj}-registry

%preun
if [ $1 = 0 ] ; then
    /sbin/service openstack-%{prj}-api stop
    /sbin/chkconfig --del openstack-%{prj}-api
    /sbin/service openstack-%{prj}-registry stop
    /sbin/chkconfig --del openstack-%{prj}-registry
fi

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{prj}
%{_bindir}/%{prj}-api
%{_bindir}/%{prj}-control
%{_bindir}/%{prj}-manage
%{_bindir}/%{prj}-registry
%{_bindir}/%{prj}-upload
%{_initrddir}/%{name}-api
%{_initrddir}/%{name}-registry
%defattr(-,%{prj},nobody,-)
%config(noreplace) %{_sysconfdir}/%{prj}/%{prj}-api.conf
%config(noreplace) %{_sysconfdir}/%{prj}/%{prj}-registry.conf
%config(noreplace) %{_sysconfdir}/%{prj}/logging-api.conf
%config(noreplace) %{_sysconfdir}/%{prj}/logging-registry.conf
%{_sharedstatedir}/%{prj}
%dir %attr(0755, %{prj}, nobody) %{_localstatedir}/log/%{prj}
%dir %attr(0755, %{prj}, nobody) %{_localstatedir}/run/%{prj}

%files -n python-%{prj}
%{python_sitelib}/%{prj}
%{python_sitelib}/%{prj}-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc ChangeLog
%doc doc/build/html
%endif

%changelog
* Wed May 25 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.17.bzr133
- Update to bzr133

* Wed May 18 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.16.bzr132
- Update to bzr132

* Tue May 17 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.15.bzr131
- Update to bzr131

* Wed May 11 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.14.bzr130
- Update to bzr130

* Thu May 05 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.13.bzr129
- Update to bzr129

* Sun May 01 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.12.bzr128
- Update to bzr128

* Wed Apr 27 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.11.bzr126
- Update to bzr126

* Tue Apr 26 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.10.bzr125
- Update to bzr125

* Fri Apr 22 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.9.bzr124
- Update to bzr124

* Thu Apr 21 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.8.bzr123
- Update to bzr123

* Thu Apr 21 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.7.bzr122
- Update to bzr122

* Thu Apr 21 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.6.bzr121
- Update to bzr121

* Wed Apr 20 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.5.bzr120
- Update to bzr120

* Wed Apr 20 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.4.bzr119
- Update to bzr119

* Tue Apr 19 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.3.bzr118
- Update to bzr118

* Tue Apr 19 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.2.bzr117
- Update to bzr117

* Fri Apr 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.1.bzr116
- Diablo versioning

* Fri Apr 15 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.30.bzr114
- Update to bzr114

* Thu Apr 14 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.29.bzr113
- Update to bzr113

* Wed Apr 13 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.28.bzr112
- Update to bzr112

* Wed Apr 13 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.27.bzr111
- Update to bzr111

* Tue Apr 12 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.26.bzr109
- Update to bzr109

* Tue Apr 12 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.25.bzr108
- Update to bzr108

* Mon Apr 11 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.24.bzr107
- Update to bzr107

* Mon Apr 11 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.23.bzr106
- Update to bzr106

* Thu Apr 07 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.22.bzr104
- Update to bzr104

* Wed Apr 06 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.21.bzr103
- Update to bzr103

* Wed Apr 06 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.20.bzr102
- Update to bzr102

* Wed Apr 06 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.19.bzr101
- Update to bzr101

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.18.bzr100
- Added missed files

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.17.bzr100
- Added new initscripts
- Changed default logging configuration

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.16.bzr100
- fixed path to SQLite db in default config

* Tue Mar 29 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.15.bzr100
- Update to bzr100

* Tue Mar 29 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.14.bzr99
- Uncommented Changelog back

* Tue Mar 29 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.2-0.13.bzr99
- Update to bzr99

* Fri Mar 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.12.bzr96
- Update to bzr96
- Temporary commented Changelog in %doc

* Thu Mar 24 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.11.bzr95
- Update to bzr95

* Mon Mar 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.10.bzr93
- Added /var/lib/glance and subdirs to include images in package

* Mon Mar 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.9.bzr93
- Update to bzr93

* Mon Mar 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.8.bzr92
- Update to bzr92

* Thu Mar 17 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.7.bzr90
- Added ChangeLog

* Thu Mar 17 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.6.bzr90
- Update to bzr90

* Wed Mar 16 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.5.bzr88
- Update to bzr88

* Wed Mar 16 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.4.bzr87
- Default configs patched

* Wed Mar 16 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.3.bzr87
- Added new config files

* Wed Mar 16 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.2.bzr87
- Config file moved from /etc/nova to /etc/glance

* Wed Mar 16 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.1.bzr87
- pre-Cactus version

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.7-1
- Release 0.1.7

* Thu Jan 27 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.5-1
- Release 0.1.5

* Wed Jan 26 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.4-1
- Release 0.1.4

* Mon Jan 24 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.3-2
- Changed description (thanks to Jay Pipes)
- Added python-argparse to deps, required by /usr/bin/glance-upload

* Mon Jan 24 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.3-1
- Release 0.1.3
- Added glance-upload to openstack-glance package

* Fri Jan 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.2-3
- Added pid directory
- Relocated log to /var/log/glance/glance.log

* Fri Jan 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.2-2
- Changed permissions on initscript

* Thu Jan 20 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.1.2-1
- Initial build
