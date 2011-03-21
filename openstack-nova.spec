%global with_doc 0

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-nova
Version:          2011.2
Release:          0.11.bzr837
Summary:          OpenStack Compute (nova)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://nova.openstack.org/tarballs/nova-%{version}~bzr837.tar.gz
Source1:          %{name}-README.rhel6
Source6:          %{name}.logrotate

# Initscripts
Source11:         %{name}-api.init
Source12:         %{name}-compute.init
Source13:         %{name}-network.init
Source14:         %{name}-objectstore.init
Source15:         %{name}-scheduler.init
Source16:         %{name}-volume.init
Source17:         %{name}-direct-api.init
Source18:         %{name}-ajax-console-proxy.init

Source20:         %{name}-sudoers
Source21:         %{name}-polkit.pkla
Source22:         %{name}-rhel-ifc-template

Patch0:           %{name}-openssl-relaxed-policy.patch
Patch1:           %{name}-rhel-config-paths.patch
Patch2:           %{name}-guestfs-image-injects.patch
Patch3:           %{name}-bexar-libvirt.xml.template.patch

BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-distutils-extra >= 2.18
BuildRequires:    python-netaddr

Requires:         python-nova = %{version}-%{release}
Requires:         %{name}-config = %{version}
Requires:         sudo

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils qemu-kvm

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
Requires:         python-eventlet >= 0.9.12-1.1.el6
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
Requires:         python-sqlalchemy-migrate
Requires:         radvd
Requires:         iptables iptables-ipv6
Requires:         iscsi-initiator-utils
Requires:         scsi-target-utils
Requires:         lvm2
Requires:         socat
Requires:         coreutils
Requires:         python-libguestfs

%description -n   python-nova
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Python library.

%package          api
Summary:          A nova API server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon
Requires:         python-paste
Requires:         python-paste-deploy

%description      api
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} API Server.

%package          compute
Summary:          A nova compute server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon
Requires:         libvirt-python
Requires:         libxml2-python
Requires:         rabbitmq-server
Requires:         python-cheetah

%description      compute
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Compute Worker.

%package          instancemonitor
Summary:          A nova instancemonitor server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

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
Requires:         start-stop-daemon

%description      network
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Network Controller.

%package          objectstore
Summary:          A nova objectstore server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

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
Requires:         start-stop-daemon

%description      scheduler
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Scheduler.

%package          volume
Summary:          A nova volume server
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         start-stop-daemon

%description      volume
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains the %{name} Volume service.

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
#BuildRequires:    python-daemon
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
%patch2 -p1
%patch3 -p1

install %{SOURCE1} README.rhel6

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

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-volume
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{name}-direct-api
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{name}-ajax-console-proxy

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/%{name}

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
install -p -D -m 644 nova/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/nova/interfaces.rhel.template

# Clean CA directory
find %{buildroot}%{_sharedstatedir}/nova/CA -name .gitignore -delete
find %{buildroot}%{_sharedstatedir}/nova/CA -name .placeholder -delete

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-%{name}.pkla

# Fix for api-paste.ini misplacement
install -d -m 750 %{buildroot}%{_sysconfdir}/nova
mv %{buildroot}%{_sysconfdir}/api-paste.ini %{buildroot}%{_sysconfdir}/nova/api-paste.ini

# Install ajaxterm
gzip --best -c tools/ajaxterm/ajaxterm.1 > tools/ajaxterm/ajaxterm.1.gz
install -p -m 755 tools/ajaxterm/ajaxterm.1.gz %{buildroot}%{_mandir}/man1/ajaxterm.1*
install -d -m 755 %{buildroot}%{python_sitelib}/tools
install -m 644 tools/ajaxterm/{ajaxterm.css,ajaxterm.html,ajaxterm.js,qweb.py,sarissa.js,sarissa_dhtml.js} %{buildroot}%{python_sitelib}/tools
install -m 755 tools/ajaxterm/ajaxterm.py %{buildroot}%{python_sitelib}/tools
install -m 755 tools/euca-get-ajax-console %{buildroot}%{_bindir}

# Remove unneeded in production stuff
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

%clean
rm -rf %{buildroot}

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%post
if ! fgrep '#includedir /etc/sudoers.d' /etc/sudoers 2>&1 >/dev/null; then
        echo '#includedir /etc/sudoers.d' >> /etc/sudoers
fi

if rpmquery openstack-nova-cc-config 1>&2 >/dev/null; then
	# Cloud controller node detected, assuming that is contains database
	
	# Database init/migration
	if [ $1 -gt 1 ]; then
		current_version=$(nova-manage db version 2>/dev/null)
		updated_version=$(cd %{python_sitelib}/nova/db/sqlalchemy/migrate_repo; %{__python} manage.py version)
		if [ "$current_version" -ne "$updated_version" ]; then
			echo "Performing Nova database upgrade"
			/usr/bin/nova-manage db sync
		fi
	else
		echo "DB init code, new installation"
		#/usr/bin/nova-manage db sync
	fi
fi

# api

%post api
/sbin/chkconfig --add %{name}-api
/sbin/chkconfig --add %{name}-direct-api

%preun api
if [ $1 = 0 ] ; then
    /sbin/service %{name}-api stop >/dev/null 2>&1
    /sbin/service %{name}-direct-api stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-api
    /sbin/chkconfig --del %{name}-direct-api
fi

%postun api
if [ $1 = 1 ] ; then
    /sbin/service %{name}-api condrestart
    /sbin/service %{name}-direct-api condrestart
fi

# compute

%post compute
/sbin/chkconfig --add %{name}-ajax-console-proxy
/sbin/chkconfig --add %{name}-compute

%preun compute
if [ $1 = 0 ] ; then
    /sbin/service %{name}-ajax-console-proxy stop >/dev/null 2>&1
    /sbin/service %{name}-compute stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-ajax-console-proxy
    /sbin/chkconfig --del %{name}-compute
fi

%postun compute
if [ $1 = 1 ] ; then
    /sbin/service %{name}-ajax-console-proxy condrestart
    /sbin/service %{name}-compute condrestart
fi

# network

%post network
/sbin/chkconfig --add %{name}-network

%preun network
if [ $1 = 0 ] ; then
    /sbin/service %{name}-network stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-network
fi

%postun network
if [ $1 = 1 ] ; then
    /sbin/service %{name}-network condrestart
fi

# objectstore

%post objectstore
/sbin/chkconfig --add %{name}-objectstore

%preun objectstore
if [ $1 = 0 ] ; then
    /sbin/service %{name}-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-objectstore
fi

%postun objectstore
if [ $1 = 1 ] ; then
    /sbin/service %{name}-objectstore condrestart
fi

# scheduler

%post scheduler
/sbin/chkconfig --add %{name}-scheduler

%preun scheduler
if [ $1 = 0 ] ; then
    /sbin/service %{name}-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-scheduler
fi

%postun scheduler
if [ $1 = 1 ] ; then
    /sbin/service %{name}-scheduler condrestart
fi

# volume

%post volume
/sbin/chkconfig --add %{name}-volume

%preun volume
if [ $1 = 0 ] ; then
    /sbin/service %{name}-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-volume
fi

%postun volume
if [ $1 = 1 ] ; then
    /sbin/service %{name}-volume condrestart
fi

%files
%defattr(-,root,root,-)
%doc README README.rhel6
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{name}
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova
%{_bindir}/nova-console
%{_bindir}/nova-debug
%{_bindir}/nova-logspool
%{_bindir}/nova-manage
%{_bindir}/nova-spoolsentry
%{_bindir}/stack
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
%{_initrddir}/%{name}-direct-api
%{_bindir}/nova-api
%{_bindir}/nova-direct-api
%defattr(-,nova,nobody,-)
%config(noreplace) %{_sysconfdir}/nova/api-paste.ini

%files compute
%defattr(-,root,root,-)
%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-openstack-nova.pkla
%{_bindir}/euca-get-ajax-console
%{_bindir}/nova-ajax-console-proxy
%{_bindir}/nova-compute
%{_initrddir}/%{name}-compute
%{_initrddir}/%{name}-ajax-console-proxy
%{_mandir}/man1/ajaxterm.1*
%{python_sitelib}/tools

%files instancemonitor
%defattr(-,root,root,-)
%{_bindir}/nova-instancemonitor
#{_initrddir}/%{name}-instancemonitor

%files network
%defattr(-,root,root,-)
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_initrddir}/%{name}-network

%files objectstore
%defattr(-,root,root,-)
%{_bindir}/nova-import-canonical-imagestore
%{_bindir}/nova-objectstore
%{_initrddir}/%{name}-objectstore

%files scheduler
%defattr(-,root,root,-)
%{_bindir}/nova-scheduler
%{_initrddir}/%{name}-scheduler

%files volume
%defattr(-,root,root,-)
%{_bindir}/nova-volume
%{_initrddir}/%{name}-volume

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif

%changelog
* Mon Mar 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.11.bzr837
- Update to bzr837

* Fri Mar 18 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.10.bzr828
- Update to bzr828

* Thu Mar 17 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.9.bzr815
- Update to bzr815
- Removed libvirt-xml-cpus.patch

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.8.bzr807
- Update to bzr807

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.7.bzr806
- Update to bzr806

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.6.bzr805
- Added database migration
- Temporary disabled documentation build until release

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.5.bzr805
- Update to bzr805

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.4.bzr802
- Added openstack-nova-libvirt-xml-cpus.patch to prevent error with nova-compute startup

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.3.bzr802
- sudo configuration updated

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.2.bzr802
- Update to bzr802

* Mon Mar 14 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.2-0.1.bzr795
- Cactus pre-release build
- Changed release to better comply packaging policy
  https://fedoraproject.org/wiki/Packaging:NamingGuidelines
- /etc/nova/nova-api.conf -> /etc/nova/api-paste.ini
- guestfs patch migrated
- rhel config paths patch - added handling of api-paste.ini

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-5
- Changed logrotate script - it should not rotate empty logs

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-4
- Updated logrotate script with nova-ajax-console-proxy and nova-direct-api
  logfiles

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-3
- Added initscript for nova-ajax-console-proxy

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-2
- Added initscript for nova-direct-api

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-1
- Bugfix release 2011.1.1
- Added python-distutils-extra to BuildReqs

* Fri Feb 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-5
- Merged updated guestfs patch from Ilya Alekseyev
- Refactored guestfs patch - now it creates directory only if it does not exist

* Fri Feb 18 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-4
- Added patch with network interface template for RHEL guest OS
  (kudos to Ilya Alekseyev)

* Fri Feb 18 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-3
- Disabled SELinux for KVM images in libvirt.xml.template
- Added patch for image injection (kudos to Ilya Alekseyev).
- Updated dependencies

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-1
- Bexar release

* Wed Feb 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr642
- Deleted patch from bzr638 rev because it was merged to trunk
- Updated dependencies
- Updated sudo configuration for nova user

* Mon Jan 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr640
- Updated to bzr640

* Mon Jan 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr639
- Added condrestart target to initscripts
- Added condrestart on package upgrade

* Mon Jan 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr638
- Added patch openstack-nova-logging.py - re-routing unhandled exceptions to logs

* Thu Jan 27 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr629
- Update to bzr629
- Refactored initscripts with start-stop-daemon since standard RHEL initscripts
  does not support creation of pidfiles
- Removed dependency on upstart
- All daemons are once again running under user nova instead of root

* Wed Jan 26 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr621
- Updated to bzr621

* Mon Jan 24 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-bzr604
- Update to bzr604
- Added dependency on python-sqlalchemy-migrate

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
