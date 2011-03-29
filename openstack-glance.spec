%global with_doc 1
%global prj glance

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-%{prj}
Version:          2011.2
Release:          0.14.bzr99
Summary:          OpenStack Image Registry and Delivery Service

Group:            Development/Languages
License:          ASL 2.0
URL:              http://%{prj}.openstack.org
Source0:          http://glance.openstack.org/tarballs/glance-%{version}~bzr99.tar.gz
Source2:          %{name}.init

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
install -p -D -m 644 etc/%{prj}.conf.sample %{buildroot}%{_sysconfdir}/%{prj}/%{prj}.conf
install -p -D -m 644 etc/logging.cnf.sample %{buildroot}%{_sysconfdir}/%{prj}/logging.cnf

# Initscript
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}

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
-c "OpenStack Glance Daemon" %{prj}
exit 0

%post
/sbin/chkconfig --add openstack-%{prj}

%preun
if [ $1 = 0 ] ; then
    /sbin/service openstack-%{prj} stop
    /sbin/chkconfig --del openstack-%{prj}
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
%{_initrddir}/%{name}
%defattr(-,%{prj},nobody,-)
%config(noreplace) %{_sysconfdir}/%{prj}/%{prj}.conf
%config(noreplace) %{_sysconfdir}/%{prj}/logging.cnf
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
