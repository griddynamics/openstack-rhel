%global with_doc 0

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-nova
Version:          2011.1
Release:          bzr598
Summary:          OpenStack Compute (nova)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://nova.openstack.org/tarballs/nova-%{version}~%{release}.tar.gz
Source1:          %{name}-upstart.conf
Source2:          %{name}.init
Source3:          %{name}-api.conf
#Source6:          %{name}.logrotate
Source20:         %{name}-sudoers
Source21:         %{name}-polkit.pkla

Patch0:           openstack-nova-openssl-relaxed-policy.patch
Patch1:           openstack-nova-rhel-config-paths.patch

BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr

Requires:         python-nova = %{version}-%{release}
Requires:         openstack-nova-config = %{version}
Requires:         sudo
Requires:         upstart

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils

%description
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

Nova is intended to be easy to extend, and adapt. For example, it currently
uses an LDAP server for users and groups, but also includes a fake LDAP server,
that stores data in Redis. It has extensive test coverage, and uses the Sphinx
toolkit (the same as Python itself) for code and user documentation.

%package -n       python-nova
Summary:          Nova Python libraries
Group:            Applications/System

Requires:         vconfig
Requires:         PyXML
Requires:         curl
Requires:         m2crypto
Requires:         libvirt-python
Requires:         python-anyjson >= 0.2.4
Requires:         python-IPy >= 0.70
Requires:         python-boto >= 1.9b
Requires:         python-carrot >= 0.10.5
Requires:         python-daemon = 1.5.5
Requires:         python-eventlet >= 0.9.12
Requires:         python-gflags >= 1.3
Requires:         python-lockfile = 0.8
Requires:         python-mox >= 0.5.0
Requires:         python-redis
Requires:         python-routes
Requires:         python-sqlalchemy >= 0.6
Requires:         python-tornado
Requires:         python-twisted-core >= 10.1.0
Requires:         python-twisted-web >= 10.1.0
Requires:         python-webob = 0.9.8
Requires:         python-netaddr
Requires:         python-glance

%description -n   python-nova
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Python library.

%package          api
Summary:          A nova api server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         python-paste
Requires:         python-paste-deploy

%description      api
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} api server.

%package          compute
Summary:          A nova compute server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         libvirt-python
Requires:         libxml2-python
Requires:         rabbitmq-server
Requires:         python-cheetah

%description      compute
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} compute server.

%package          instancemonitor
Summary:          A nova instancemonitor server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      instancemonitor
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} instance monitor.

%package          network
Summary:          A nova network server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      network
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} network server.

%package          objectstore
Summary:          A nova objectstore server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      objectstore
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} object store server.

%package          scheduler
Summary:          A nova scheduler server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      scheduler
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} scheduler server.

%package          volume
Summary:          A nova volume server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}

%description      volume
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} volume server.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{name}
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-nose
# Required to build module documents
BuildRequires:    python-IPy
BuildRequires:    python-boto
#BuildRequires:    python-carrot
BuildRequires:    python-daemon
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
#BuildRequires:    python-mox
#BuildRequires:    python-redis
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-tornado
BuildRequires:    python-twisted-core
BuildRequires:    python-twisted-web
BuildRequires:    python-webob

%description      doc
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n nova-%{version}

%patch0 -p1
%patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova
cp -rp CA %{buildroot}%{_sharedstatedir}/nova

# Install upstart configs & initscripts wrappers
for service in api compute instancemonitor network objectstore scheduler volume; do
	install -p -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init/%{name}-$service.conf
	perl -pi -e "s/SUB/$service/g" %{buildroot}%{_sysconfdir}/init/%{name}-$service.conf

	install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-$service
	perl -pi -e "s/SUB/$service/g" %{buildroot}%{_initrddir}/%{name}-$service	
done

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/%{name}

# Install logrotate
#install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 nova/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template

# Clean CA directory
find %{buildroot}%{_sharedstatedir}/nova/CA -name .gitignore -delete
find %{buildroot}%{_sharedstatedir}/nova/CA -name .placeholder -delete

# Ugly hack for nova-manage - not needed anymore since we have correct paths?
#cd %{buildroot}%{python_sitelib} && ln -s ../../../../../var/lib/nova/CA CA

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-openstack-nova.pkla

# Install configuration file for nova-api service
install -p -D -m 440 %{SOURCE3} %{buildroot}%{_sysconfdir}/nova/nova-api.conf

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post
if ! fgrep '#includedir /etc/sudoers.d' /etc/sudoers 2>&1 >/dev/null; then
        echo '#includedir /etc/sudoers.d' >> /etc/sudoers
fi

%post api
/sbin/chkconfig --add openstack-nova-api

%preun api
if [ $1 = 0 ] ; then
    /sbin/service openstack-nova-api stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-nova-api
fi

%post compute
/sbin/chkconfig --add openstack-nova-compute

%preun compute
if [ $1 = 0 ] ; then
    /sbin/service openstack-nova-compute stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-nova-compute
fi

%post network
/sbin/chkconfig --add openstack-nova-network

%preun network
if [ $1 = 0 ] ; then
    /sbin/service openstack-nova-network stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-nova-network
fi

%post objectstore
/sbin/chkconfig --add openstack-nova-objectstore

%preun objectstore
if [ $1 = 0 ] ; then
    /sbin/service openstack-nova-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-nova-objectstore
fi

%post scheduler
/sbin/chkconfig --add openstack-nova-scheduler

%preun scheduler
if [ $1 = 0 ] ; then
    /sbin/service openstack-nova-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-nova-scheduler
fi

%post volume
/sbin/chkconfig --add openstack-nova-volume

%preun volume
if [ $1 = 0 ] ; then
    /sbin/service openstack-nova-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-nova-volume
fi

%files
%defattr(-,root,root,-)
%doc README
#%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{name}
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova
%{_bindir}/nova-manage
%{_datarootdir}/nova
%defattr(-,nova,nobody,-)
%{_sharedstatedir}/nova

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%files api
%defattr(-,root,root,-)
%{_initrddir}/%{name}-api
%{_bindir}/nova-api
%{_sysconfdir}/init/%{name}-api.conf
%defattr(-,nova,nobody,-)
%config(noreplace) %{_sysconfdir}/nova/nova-api.conf

%files compute
%defattr(-,root,root,-)
%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-openstack-nova.pkla
%{_bindir}/nova-compute
%{_bindir}/nova-debug
%{_bindir}/nova-logspool
%{_bindir}/nova-spoolsentry
%{_initrddir}/%{name}-compute
%{_sysconfdir}/init/%{name}-compute.conf

%files instancemonitor
%defattr(-,root,root,-)
%{_bindir}/nova-instancemonitor
%{_initrddir}/%{name}-instancemonitor
%{_sysconfdir}/init/%{name}-instancemonitor.conf

%files network
%defattr(-,root,root,-)
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/%{name}-network
%{_sysconfdir}/init/%{name}-network.conf

%files objectstore
%defattr(-,root,root,-)
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
%{_initrddir}/%{name}-objectstore
%{_sysconfdir}/init/%{name}-objectstore.conf

%files scheduler
%defattr(-,root,root,-)
%{_bindir}/nova-scheduler
%{_initrddir}/%{name}-scheduler
%{_sysconfdir}/init/%{name}-scheduler.conf

%files volume
%defattr(-,root,root,-)
%{_bindir}/nova-volume
%{_initrddir}/%{name}-volume
%{_sysconfdir}/init/%{name}-volume.conf

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif

%changelog
* Fri Jan 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr598
- Updated to bzr598
- Updated patch for rhel paths

* Fri Jan 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr597
- Added dependency for python-glance

* Tue Jan 18 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr572
- Added /etc/nova/nova-api.conf
- Reworked openstack-nova-rhel-paths.patch
- Added dependencies for openstack-nova-api for paste & paste-deploy modules

* Mon Jan 17 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr569
- Temporary commented logrotate script

* Fri Jan 14 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr565
- Added build and runtime dep on python-netaddr

* Wed Jan 12 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr553
- Added dep on python-cheetah from standard RHEL distro
- Temporary disabled build of -doc package to speed up testing env

* Wed Jan 12 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr552
- Fixed bug with upstart configs

* Wed Jan 12 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr551
- Moved initscripts to upstart

* Sat Jan 01 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr509
- Updated config patch
- Removed templates

* Tue Dec 14 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr464
- Changed dependency for python-daemon to = 1.5.5

* Tue Dec 14 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr460
- Added vconfig as a dep for python-nova

* Thu Dec 09 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr454
- Added postscript to openstac-nova package to add inclution of files to
  /etc/sudoers

* Thu Dec 09 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr453
- Added dependency >= 10.1.0 for twisted-core and twisted-web - 8.2.0 from RHEL6
  is not ok for use with nova-objectstore

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-bzr435
- Moved config files to separate package openstack-nova-cc-config for easy
  package-based deployment

* Thu Nov 04 2010 Silas Sewell <silas@sewell.ch> - 2010.1-2
- Fix various issues (init, permissions, config, etc..)

* Thu Oct 21 2010 Silas Sewell <silas@sewell.ch> - 2010.1-1
- Initial build
