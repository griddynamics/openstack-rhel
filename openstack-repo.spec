Name:		openstack-repo
Version:	2011.2
Release:	0.2
Summary:	OpenStack repository configuration from Grid Dynamics

Group:		System Environment/Base
License:	GPL
Source0:	%{name}.repo
Source1:        %{name}.key
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:        noarch

%description
OpenStack repository for RHEL v.6

%prep

%build

%install
rm -rf %{buildroot}
install -p -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/openstack.repo
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OPENSTACK


%files
%defattr(-,root,root,-)
%{_sysconfdir}/yum.repos.d/openstack.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OPENSTACK

%changelog
* Tue Mar 29 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.2
- Added Jenkins key which is used for autobuilds
- Spec small fixes

* Fri Mar 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.2-0.1
- Version bumped to 2011.2

* Thu Feb 10 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-2
- Added failover repo

* Mon Feb 07 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 2011.1-1
- First release

