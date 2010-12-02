Name:             openstack-nova-cc-config
Version:          2011.1
Release:          4
Summary:          OpenStack Compute (nova) - Cloud Controller config

Group:            Development/Languages
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source1:          %{name}-api.conf
Source3:          %{name}-compute.conf
Source5:          %{name}-dhcpbridge.conf
Source7:          %{name}-manage.conf
Source8:          %{name}-network.conf
Source10:         %{name}-objectstore.conf
Source12:         %{name}-scheduler.conf
Source14:         %{name}-volume.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

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
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/nova/nova-api.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/nova/nova-compute.conf
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/nova/nova-dhcpbridge.conf
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/nova/nova-manage.conf
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/nova/nova-network.conf
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/nova/nova-objectstore.conf
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/nova/nova-scheduler.conf
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/nova/nova-volume.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova-api.conf
%config(noreplace) %{_sysconfdir}/nova/nova-compute.conf
%config(noreplace) %{_sysconfdir}/nova/nova-dhcpbridge.conf
%config(noreplace) %{_sysconfdir}/nova/nova-manage.conf
%config(noreplace) %{_sysconfdir}/nova/nova-network.conf
%config(noreplace) %{_sysconfdir}/nova/nova-objectstore.conf
%config(noreplace) %{_sysconfdir}/nova/nova-scheduler.conf
%config(noreplace) %{_sysconfdir}/nova/nova-volume.conf

%changelog
* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-4
- Added missed --cc_host parameter

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-3
- Changed configs to multiple server setup in accordance with Wiki page:
  http://wiki.openstack.org/NovaInstall/MultipleServer

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-2
- Added version to Provides

* Wed Dec 01 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-1
- Initial build
