%global with_doc 1

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             openstack-nova
Version:	2011.3
Release:	0.20110711.1265%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          http://nova.openstack.org/tarballs/nova-2011.3~d3~20110712.1266.tar.gz
Source1:          %{name}-README.rhel6
Source2:          %{name}-noVNC-snap2011.03.24.tgz
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
Source19:         %{name}-vncproxy.init

Source20:         %{name}-sudoers
Source21:         %{name}-polkit.pkla
Source22:         %{name}-rhel-ifc-template

#Patch1:           %{name}-rhel-config-paths.patch
Patch2:           %{name}-guestfs-image-injects.patch
Patch3:           %{name}-bexar-libvirt.xml.template.patch
Patch4:           %{name}-rhel-netcat.patch
Patch5:           %{name}-rhel-ajaxterm-path.patch
Patch6:           %{name}-s3server-quickfix.patch
Patch7:           %{name}-scsi-target-utils-support.patch
Patch8:           %{name}-rpc-improvements.patch

BuildRoot:        %{_tmppath}/nova-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-distutils-extra >= 2.18
BuildRequires:    python-netaddr

Requires:         python-nova = %{version}-%{release}
Requires:         %{name}-config = %{version}
Requires:         sudo
Requires:         euca2ools = 1.3.1-3gd

Requires(post):   chkconfig grep sudo libselinux-utils
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

%package          noVNC
Summary:          OpenStack Nova VNC console service
Group:            Applications/System
License:          LGPL v3 with exceptions
URL:              https://github.com/openstack/noVNC

Requires:         %{name} = %{version}-%{release}

%description      noVNC
This package contains noVNC code and daemon which is required for accessing
instances's console using VNC.

%package          node-full
Summary:          OpenStack Nova full node installation
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-cc-config = %{version}
Requires:         %{name}-api = %{version}-%{release}
Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-instancemonitor = %{version}-%{release}
Requires:         %{name}-network = %{version}-%{release}
Requires:         %{name}-noVNC = %{version}-%{release}
Requires:         %{name}-objectstore = %{version}-%{release}
Requires:         %{name}-scheduler = %{version}-%{release}
Requires:         %{name}-volume = %{version}-%{release}
Requires:         openstack-client
Requires:         openstack-glance = %{version}
Requires:         openstack-glance-doc = %{version}
%if 0%{?with_doc}
Requires:         %{name}-doc = %{version}-%{release}
%endif

%description      node-full
This package installs full set of OpenStack Nova packages and Cloud Controller
configuration.

%package          node-compute
Summary:          OpenStack Nova compute node installation
Group:            Applications/System

Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-compute-config = %{version}
Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-instancemonitor = %{version}-%{release}

%description      node-compute
This package installs compute set of OpenStack Nova packages and Compute node
configuration.

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
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python-redis
Requires:         python-routes >= 1.12.3
Requires:         python-sqlalchemy >= 0.6
Requires:         python-suds >= 0.4.0
Requires:         python-tornado
Requires:         python-twisted-core >= 10.1.0
Requires:         python-twisted-web >= 10.1.0
Requires:         python-webob
Requires:         python-netaddr
Requires:         python-glance
Requires:         python-novaclient
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
Requires:         libvirt >= 0.8.2
Requires:         libxml2-python
Requires:         rabbitmq-server
Requires:         python-cheetah
Requires:         dmidecode

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
BuildRequires:    python-routes >= 1.12.3
BuildRequires:    python-sqlalchemy
BuildRequires:    python-tornado
BuildRequires:    python-twisted-core
BuildRequires:    python-twisted-web
BuildRequires:    python-webob
BuildRequires:    python-lockfile
BuildRequires:    intltool

%description      doc
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n nova-%{version}

#patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p1
%patch7 -p1
#patch8 -p1

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
cp -rp nova/CA %{buildroot}%{_sharedstatedir}/nova

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-volume
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{name}-direct-api
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{name}-ajax-console-proxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/%{name}-vncproxy

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

# Fixing ajaxterm installation
mv %{buildroot}%{_datarootdir}/nova/euca-get-ajax-console %{buildroot}%{_bindir}
rm -fr %{buildroot}%{_datarootdir}/nova/{install_venv.py,nova-debug,pip-requires,clean-vlans,with_venv.sh,esx} %{buildroot}%{_datarootdir}/nova/ajaxterm/configure*

# Remove unneeded in production stuff
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

# Add noVNC console
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/noVNC
tar zxf %{SOURCE2} -C %{buildroot}%{_sharedstatedir}/nova/noVNC

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
if %{_sbindir}/selinuxenabled; then
	echo -e "\033[47m\033[1;31m***************************************************\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m >> \033[5mYou have SELinux enabled on your host !\033[25m <<  \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31mPlease disable it by setting \`SELINUX=disabled' \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31min /etc/sysconfig/selinux and don't forget      \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31mto reboot your host to apply that change!       \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
	echo -e "\033[47m\033[1;31m***************************************************\033[0m"
fi

if rpmquery openstack-nova-cc-config 1>&2 >/dev/null; then
	# Cloud controller node detected, assuming that is contains database
	
	# Database init/migration
	if [ $1 -gt 1 ]; then
		db_sync
	else
		echo "New installation"
		db_sync
		echo "Please refer http://wiki.openstack.org/NovaInstall/RHEL6Notes for instructions"
	fi
fi

db_sync() {
	upgrade_db = 0
	if   nova_option 'sql_connection' 'mysql://'; then
		# Assuming that we have MySQL server on the same node with Cloud Controller
		echo "Nova database: MySQL"
		service mysqld status 2>&1 >/dev/null
		if [ "$?" = 0 ]; then
			upgrade_db = 1
		else
			echo "mysqld is not running, skipping Nova db sync"
		fi
	elif nova_option 'sql_connection' 'sqlite://'; then
		echo "Nova database: SQLite"
		upgrage_db = 1
	else
		echo "Nova database: UNSUPPORTED by this RPM postscript"
		echo "Please ensure that it's running and migrate db"	
	fi

	if [ "$upgrade_db" -eq "1" ]; then
		echo "Performing Nova database upgrade:"
		%{_bindir}/nova-manage db sync
	fi
}

nova_option () {
	grep "$1" %{_sysconfdir}/nova/nova.conf | cut -d= -f2 | grep "$2" >/dev/null
	return $?
}

# api

%post api
/sbin/chkconfig --add %{name}-api
/sbin/chkconfig --add %{name}-direct-api

%preun api
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-api stop >/dev/null 2>&1
    /sbin/service %{name}-direct-api stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-api
    /sbin/chkconfig --del %{name}-direct-api
fi

%postun api
if [ $1 -eq 1 ] ; then
    /sbin/service %{name}-api condrestart
    /sbin/service %{name}-direct-api condrestart
fi

# compute

%post compute
/sbin/chkconfig --add %{name}-ajax-console-proxy
/sbin/chkconfig --add %{name}-compute

%preun compute
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-ajax-console-proxy stop >/dev/null 2>&1
    /sbin/service %{name}-compute stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-ajax-console-proxy
    /sbin/chkconfig --del %{name}-compute
fi

%postun compute
if [ $1 -eq 1 ] ; then
    /sbin/service %{name}-ajax-console-proxy condrestart
    /sbin/service %{name}-compute condrestart
fi

# network

%post network
/sbin/chkconfig --add %{name}-network

%preun network
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-network stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-network
fi

%postun network
if [ $1 -eq 1 ] ; then
    /sbin/service %{name}-network condrestart
fi

# objectstore

%post objectstore
/sbin/chkconfig --add %{name}-objectstore

%preun objectstore
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-objectstore stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-objectstore
fi

%postun objectstore
if [ $1 -eq 1 ] ; then
    /sbin/service %{name}-objectstore condrestart
fi

# scheduler

%post scheduler
/sbin/chkconfig --add %{name}-scheduler

%preun scheduler
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-scheduler stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-scheduler
fi

%postun scheduler
if [ $1 -eq 1 ] ; then
    /sbin/service %{name}-scheduler condrestart
fi

# volume

%post volume
/sbin/chkconfig --add %{name}-volume

%preun volume
if [ $1 -eq 0 ] ; then
    /sbin/service %{name}-volume stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}-volume
fi

%postun volume
if [ $1 -eq 1 ] ; then
    /sbin/service %{name}-volume condrestart
fi

%files
%defattr(-,root,root,-)
%doc README README.rhel6
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sudoers.d/%{name}
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova
%{_bindir}/instance-usage-audit
%{_bindir}/nova-console
%{_bindir}/nova-debug
%{_bindir}/nova-logspool
%{_bindir}/nova-manage
%{_bindir}/nova-spoolsentry
%{_bindir}/instance-usage-audit
%{_bindir}/stack
%{_datarootdir}/nova
%defattr(-,nova,nobody,-)
%dir %{_sharedstatedir}/nova
%{_sharedstatedir}/nova/CA
%{_sharedstatedir}/nova/images
%{_sharedstatedir}/nova/instances
%{_sharedstatedir}/nova/keys
%{_sharedstatedir}/nova/networks
%{_sharedstatedir}/nova/tmp

%files noVNC
%{_bindir}/nova-vncproxy
%{_initrddir}/%{name}-vncproxy
%{_sharedstatedir}/nova/noVNC
#%doc %{_sharedstatedir}/nova/noVNC/LICENSE.txt
#%doc %{_sharedstatedir}/nova/noVNC/README.md

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
%{_datarootdir}/nova/ajaxterm

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

%files node-full

%files node-compute

%changelog
* Tue Jul 12 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.20110711.1265
- Removed lots of meaningless changelog entries from Jenkins
- Added dependency on dmidecode to openstack-nova-compute because it's missing
  in libvirt package
- Changed versioning for better upgrade experience

* Tue May 03 2011 Mr. Jenkins GD <openstack@griddynamics.net> - 2011.3-0.36.bzr1052
- Added support for scsi-target-utils

* Wed Apr 27 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.23.bzr1032
- created separate package for noVNC due licensing issue

* Tue Apr 26 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.21.bzr1031
- Updated patch6

* Mon Apr 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.19.bzr1030
- Floating IPs merged to trunk

* Tue Apr 19 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.11.bzr1000
- Updated dependency on python-routes with version 1.12.3

* Tue Apr 19 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.10.bzr1000
- Updated floating IP patch, kudos to Ilya Alekseyev

* Fri Apr 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-0.1.bzr990
- Diablo versioning

* Thu Apr 14 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.111.bzr988
- Uncommented initial db sync on fresh install
- Added banner with link to instructions

* Thu Apr 14 2011 Ilya Alekseyev <ialekseev@griddynamics.com> - 2011.2-0.110.bzr988
- Patch for auto assigning floating ips (AWS EC2 behaviour emulation) added

* Thu Apr 14 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.108.bzr987
- Fixed an odd typo

* Tue Apr 12 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.101.bzr980
- Added initscript for vncproxy

* Mon Apr 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.97.bzr975
- Removed openssl.cnf patch (included in upstream)

* Mon Apr 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.94.bzr973
- Removed temp patch

* Mon Apr 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.93.bzr973
- Added dependency libvirt >= 0.8.2 for openstack-nova-compute package, see
  https://bugs.launchpad.net/nova/+bug/757283

* Mon Apr 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.91.bzr972
- Added temp patch for bug LP755666

* Sun Apr 10 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.89.bzr971
- Added quick fix for s3server.py which restoring euca-upload-bundle

* Fri Apr 08 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.84.bzr967
- Fixed initscript for objectstore

* Fri Apr 08 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.82.bzr965
- Added noVNC tarball

* Wed Apr 06 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.65.bzr946
- Update to bzr946
- Migrated openssl.cnf patch
- Relocated CA directory
- Disabled manual api-paste.ini installation
- Moved ajaxterm to /usr/share/nova

* Wed Apr 06 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.65.bzr942
- Updated network injection patch wich bugfix

* Tue Apr 05 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.64.bzr942
- Updated network injection patch (Ilya Alekseyev)

* Mon Apr 04 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.55.bzr932
- Removed patch for euca-get-ajax-console due it's inclution in upstream

* Fri Apr 01 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.52.bzr930
- Changed location of ajaxterm.py
- Patched netcat binary name s/netcat/nc/

* Fri Apr 01 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.51.bzr930
- Added dependency on our version of euca2ools

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.47.bzr926
- s/config-cc/cc-config/

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.46.bzr926
- Added empty files sections for meta packages to enable RPM generation

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.45.bzr926
- Added SELinux banner

* Thu Mar 31 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.43.bzr925
- Added openstack-nova-node-full, openstack-nova-node-compute meta packages

* Wed Mar 30 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.33.bzr913
- Added nova-vncproxy

* Wed Mar 30 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.28.bzr908
- Migrated guestfs patch

* Tue Mar 29 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.23.bzr905
- Enabled doc build 

* Fri Mar 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.20.bzr890
- Migrated guestfs patch

* Fri Mar 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.17.bzr886
- Added dependency on python-suds

* Fri Mar 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.15.bzr885
- Added dependency on python-novaclient

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
