#
# spec file for package python-dashboard
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
#%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
#%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define mod_name dashboard
%define py_puresitedir  /usr/lib/python2.6/site-packages

Name:           openstack-dashboard
Release:	0.20110715.18%{?dist}
Version:	1.0
Url:            http://www.openstack.org
Summary:        Django based reference implementation of a web based management interface for OpenStack.
License:        Apache 2.0
Group:          Development/Languages/Python
Source0:          http://openstack-dashboard.openstack.org/tarballs/%{name}-%{version}.tar.gz  
Source1:        %{name}.init
Source2:        %{name}-%{version}-setup.py
Source3:        %{name}-%{version}-dashboard
Patch:          %{name}-%{version}-conf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools
BuildArch:      noarch
Requires:       django-openstack django-registration django-nose sudo

%description
The OpenStack Dashboard is a reference implementation of a Django site that
uses the Django-Nova project to provide web based interactions with the
OpenStack Nova cloud controller.

%prep
%setup -q -n %{name}-%{version}/openstack-dashboard/
%patch -p1

%build
cp %{SOURCE2} setup.py
mkdir -p bin
cp %{SOURCE3} bin/dashboard
python setup.py build

%install
%__rm -rf %{buildroot}

python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record %{name}.files

mkdir -p %{buildroot}%{_sharedstatedir}/%{mod_name}
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

install -d -m 755 %{buildroot}%{_localstatedir}/log/%{mod_name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{mod_name}

%clean
%__rm -rf %{buildroot}

%pre
getent passwd osdashboard >/dev/null || \
useradd -r -g nobody -G nobody -d %{_sharedstatedir}/osdashboard -s /sbin/nologin \
-c "OpenStack Dashboard Daemon" osdashboard
exit 0

%post
if rpmquery openstack-dashboard 1>&2 >/dev/null; then
        (cd /etc/dashboard/local && cp local_settings.py.example local_settings.py)
        # Database init
        if [ $1 -le 1 ]; then
           echo "DB init code, new installation"
           sudo -u osdashboard python -m dashboard.manage syncdb
        fi
fi

%files -f %{name}.files
%defattr(-,root,root,-)
%doc README
%{_sysconfdir}
%{_sharedstatedir}/dashboard
%dir %attr(0755, osdashboard, nobody) %{_localstatedir}/lib/%{mod_name}
%dir %attr(0755, osdashboard, nobody) %{_localstatedir}/log/%{mod_name}
%dir %attr(0755, osdashboard, nobody) %{_localstatedir}/run/%{mod_name}

%changelog
