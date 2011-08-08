Name:             openstack-nova-compute-config
Version:          2011.3
Release:          2
Summary:          OpenStack Compute (nova) - Compute node configuration

Group:            Development/Languages
License:          ASL 2.0
Vendor:           Grid Dynamics Consulting Services, Inc.
URL:              http://openstack.org/projects/compute/
Source0:          %{name}.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    perl

Conflicts:        openstack-nova-cc-config = %{version}
Requires:         openstack-nova = %{version}
Provides:         openstack-nova-config = %{version}

%description
Configuration files for Nova as compute node.

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

%pre
getent group nova >/dev/null || groupadd -r nova
getent passwd nova >/dev/null || \
useradd -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin \
-c "OpenStack Nova Daemons" nova
exit 0

%files
%config(noreplace) %attr(0600, nova, nobody) %{_sysconfdir}/nova/nova.conf

%changelog
* Wed Jun 29 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-2
- Version bump for diablo-2

* Wed Apr 27 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.3-1
- Finally bumped version to Diablo

* Wed Apr 13 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-4
- Added --logdir

* Wed Apr 13 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-3
- Fixed --dhcpbridge_flagfile

* Sun Apr 10 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-2
- Added --lock_path

* Tue Mar 15 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-1
- Pre-Cactus version

* Wed Mar 02 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1.1-1
- Release 2011.1.1

* Fri Feb 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-6
- Switched back to nova.image.s3.S3ImageService instead of glance
- Use of qcow2 images enabled by default

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-5
- Added --state-path

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-4
- Bexar release

* Fri Jan 21 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 2011.1-3
- Updated config

* Mon Jan 11 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-2
- Changed --logfile to --logdir, unified config file /etc/nova/nova.conf

* Thu Dec 16 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-1
- Initial build

