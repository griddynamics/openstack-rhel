%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           openstackx
Release:	0.20110907.1602%{?dist}
Version:	0.01
Url:            http://github.com/cloudbuilders/openstackx/
Summary:        Python bindings to the OS API
License:        Apache 2.0
Vendor:         Grid Dynamics Consulting Services, Inc.
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Patch1:         %{name}-%{version}-project-zipfile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools
BuildArch:      noarch
Requires:       python-prettytable python-httplib2 python-argparse


%description
Python bindings to the OS API

%package django-extension
Summary:	extension for openstack nova
Group:		Application/System

%description django-extension
package dependancy for openstack-dashboard

%package openstackx
Summary:	extension for openstack nova
Group:		Application/System

%description openstackx
package dependancy for openstack-dashboard

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record %{name}.files

%post
if ! grep -q -e '--osapi_extensions_path' /etc/nova/nova.conf; then
    echo '--osapi_extensions_path=/usr/lib/python2.6/site-packages/extensions' >> /etc/nova/nova.conf
fi

%clean
rm -rf %{buildroot}

%files -f %{name}.files
%defattr(-,root,root,-)

%changelog
* Wed Sep 07 2011 Alessio Ababilov <aababilov@griddynamics.com> - 0.01-0.20110907.1602
- Added project.zipfile operation
- Add openstackx as nova extension after installation
