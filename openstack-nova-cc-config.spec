Name:             openstack-nova-cc-config
Version:          2011.3
Release:          3
Summary:          OpenStack Compute (nova) - Cloud Controller config

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          %{name}.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    perl

Conflicts:        openstack-nova-compute-config = %{version}
Requires:         openstack-nova = %{version}
Requires:         MySQL-python
Requires:         mysql-server
Provides:         openstack-nova-config = %{version}

%description
Configuration files for Nova as Cloud Controller.

%prep
#setup -q -n nova-%{version}

%build
#{__python} setup.py build

%install
rm -rf %{buildroot}

# Setup directories
install -d -m 755 %{buildroot}%{_sysconfdir}/nova

# Install config files
install -p -D -m 600 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova.conf

%clean
rm -rf %{buildroot}

%files
%config(noreplace) %attr(0600, nova, nobody) %{_sysconfdir}/nova/nova.conf

%changelog
* Wed Jun 29 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-3
- Release bump for Diablo-2
- Fixed ownership of /etc/nova/nova.conf

* Wed May 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-2
- Secured permissions and ownership of /etc/nova/nova.conf

* Wed Apr 27 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-1
- Finally bumped version to Diablo

* Wed Apr 13 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-4
- Added --logdir

* Tue Apr 12 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-3
- Added vncproxy options

* Sun Apr 10 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-2
- Added --lock_path

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-1
- Pre-Cactus version

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-1
- Release 2011.1.1

* Fri Feb 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-17
- Switched back to nova.image.s3.S3ImageService instead of glance
- Use of qcow2 images enabled by default

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-16
- Added --state-path

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-15
- Bexar release

* Wed Jan 26 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-14
- Changed dep to mysql-server

* Wed Jan 26 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-13
- Added dependencies on MySQL-python and mysql - default DB for running Nova on
  more than one host

* Fri Jan 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-12
- Updated configs

* Mon Jan 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-11
- Changed --logfile to --logdir
- Moved all config files to one /etc/nova/nova.conf

* Thu Dec 16 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-10
- Added Conflicts for openstack-nova-compute-config package

* Tue Dec 14 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-9
- --dhcpbridge=/usr/bin/nova-dhcpbridge

* Tue Dec 14 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-8
- --instances_path=/var/lib/nova/instances

* Mon Dec 13 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-7
- Added missing options (again)

* Mon Dec 13 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-6
- Refactored specfile to use one source file instead of many
- Added missing options

* Wed Dec 08 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-5
- Added /etc/nova/nova.conf

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-4
- Added missed --cc_host parameter

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-3
- Changed configs to multiple server setup in accordance with Wiki page:
  http://wiki.openstack.org/NovaInstall/MultipleServer

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-2
- Added version to Provides

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-1
- Initial build
