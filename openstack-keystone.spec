#
# spec file for package python-keystone
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
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define mod_name keystone
%define py_puresitedir  /usr/lib/python2.6/site-packages

Name:           openstack-keystone
Release:	0.20110715.17%{?dist}
Version:	1.0
# Upstream repo: https://github.com/openstack/keystone
Url:            http://keystone.openstack.org
Summary:        Python bindings to the OS API
License:        Apache 2.0
Group:          Development/Languages/Python
Source0:        %{name}-%{version}.tar.gz  
Source1:        %{name}.init
Patch:          %{name}-%{version}-conf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools python-sphinx >= 0.6.0
BuildArch:      noarch
Requires:       python-eventlet python-lxml python-paste python-sqlalchemy python-routes python-httplib2

%description
Authentication service - proposed for OpenStack

%prep
%setup -q -n %{name}-%{version}
%patch -p1

%build
python setup.py build

%install
%__rm -rf %{buildroot}

%__make -C doc/ html PYTHONPATH=%{_builddir}/%{name}-%{version}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{mod_name}
cp -a etc/* %{buildroot}%{_sysconfdir}/%{mod_name}
%__rm -rf %{buildroot}%{py_puresitedir}/{doc,examples}
%__rm %{buildroot}%{py_puresitedir}/tools/pip-requires*

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{mod_name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{mod_name}

%clean
%__rm -rf %{buildroot}

%pre
getent passwd keystone >/dev/null || \
useradd -r -g nobody -G nobody -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemon" keystone
exit 0

%files
%defattr(-,root,root,-)
%{_sysconfdir}
%doc README.md HACKING LICENSE examples doc
%{py_puresitedir}/%{mod_name}*
%{py_puresitedir}/tools
%{_usr}/bin
%dir %attr(0755, keystone, nobody) %{_sharedstatedir}/%{mod_name}
%dir %attr(0755, keystone, nobody) %{_localstatedir}/log/%{mod_name}
%dir %attr(0755, keystone, nobody) %{_localstatedir}/run/%{mod_name}

%changelog
