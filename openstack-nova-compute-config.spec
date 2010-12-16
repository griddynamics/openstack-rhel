Name:             openstack-nova-compute-config
Version:          2011.1
Release:          1
Summary:          OpenStack Compute (nova) - Compute node configuration

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
install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-compute.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-compute.log,' %{buildroot}%{_sysconfdir}/nova/nova-compute.conf

install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/nova/nova-volume.conf
perl -pi -e 's,/var/log/nova/nova.log,/var/log/nova/nova-volume.log,' %{buildroot}%{_sysconfdir}/nova/nova-volume.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %{_sysconfdir}/nova/nova-compute.conf
%config(noreplace) %{_sysconfdir}/nova/nova-volume.conf

%changelog
* Thu Dec 16 2010 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-1
- Initial build

