Name:             openstack-nova-cc-config
Version:          2011.1
Release:          8
Summary:          OpenStack Compute (nova) - Cloud Controller config

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          %{name}.conf
#Source1:          %{name}-api.conf
#Source3:          %{name}-compute.conf
#Source5:          %{name}-dhcpbridge.conf
#Source7:          %{name}-manage.conf
#Source8:          %{name}-network.conf
#Source10:         %{name}-objectstore.conf
#Source12:         %{name}-scheduler.conf
#Source14:         %{name}-volume.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    perl

Requires:         openstack-nova = %{version}
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
install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-api.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-api.log,' %{buildroot}%{_sysconfdir}/nova/nova-api.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-compute.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-compute.log,' %{buildroot}%{_sysconfdir}/nova/nova-compute.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-dhcpbridge.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-dhcpbridge.log,' %{buildroot}%{_sysconfdir}/nova/nova-dhcpbridge.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-manage.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-manage.log,' %{buildroot}%{_sysconfdir}/nova/nova-manage.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-network.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-network.log,' %{buildroot}%{_sysconfdir}/nova/nova-network.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-objectstore.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-objectstore.log,' %{buildroot}%{_sysconfdir}/nova/nova-objectstore.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-scheduler.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-scheduler.log,' %{buildroot}%{_sysconfdir}/nova/nova-scheduler.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-volume.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-volume.log,' %{buildroot}%{_sysconfdir}/nova/nova-volume.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %{_sysconfdir}/nova/nova-api.conf
%config(noreplace) %{_sysconfdir}/nova/nova-compute.conf
%config(noreplace) %{_sysconfdir}/nova/nova-dhcpbridge.conf
%config(noreplace) %{_sysconfdir}/nova/nova-manage.conf
%config(noreplace) %{_sysconfdir}/nova/nova-network.conf
%config(noreplace) %{_sysconfdir}/nova/nova-objectstore.conf
%config(noreplace) %{_sysconfdir}/nova/nova-scheduler.conf
%config(noreplace) %{_sysconfdir}/nova/nova-volume.conf

%changelog
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
