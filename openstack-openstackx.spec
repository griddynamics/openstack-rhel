#
# spec file for package python-nova-adminclient
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

#%define mod_name openstack-openstackx

Name:           openstack-openstackx
Release:        2011.07.13
Version:        0.01
Url:            http://github.com/cloudbuilders/openstackx/
Summary:        Python bindings to the OS API
License:        Apache 2.0
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
#Patch:          %{mod_name}-%{version}-nova-api-diablo.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools
BuildArch:      noarch
Requires:       python-prettytable python-httplib2 python-argparse

%description
Python bindings to the OS API


%prep
%setup -q -n %{name}-%{version}
#%patch -p1

%build
export CFLAGS="%{optflags}"
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record %{name}.files


%clean
rm -rf %{buildroot}

%files -f %{name}.files
%defattr(-,root,root,-)

%changelog


