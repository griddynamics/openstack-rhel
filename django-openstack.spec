%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           django-openstack
Release:	0.20110715.18%{?dist}
Version:	0.3
Url:            http://www.openstack.org
Summary:        A Django interface for OpenStack
License:        Apache 2.0
Vendor:         Grid Dynamics Consulting Services, Inc.
Group:          Development/Languages/Python
Source0:          http://django-openstack.openstack.org/tarballs/%{name}-%{version}.tar.gz  
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools
BuildArch:      noarch
Requires:       openstack-keystone openstack-compute openstackx python-eventlet >= 0.9.12 python-greenlet python-sqlalchemy >= 0.6.3 python-sqlalchemy-migrate >= 0.6 python-webob >= 1 python-cloudfiles python-boto = 1.9b python-httplib2 Django = 1.3 django-mailer

%description
The Django-Openstack project is a Django module that is used to provide web based
interactions with the OpenStack Nova cloud controller.

There is a reference implementation that uses this module located at:

    http://launchpad.net/openstack-dashboard

It is highly recommended that you make use of this reference implementation
so that changes you make can be visualized effectively and are consistent.
Using this reference implementation as a development environment will greatly
simplify development of the django-openstack module.

Of course, if you are developing your own Django site using django-openstack, then
you can disregard this advice.

%prep
%setup -q -n %{name}-%{version}/django-openstack/

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record %{name}.files

%clean
rm -rf %{buildroot}

%files -f %{name}.files
%defattr(-,root,root,-)

%changelog
