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

%define mod_name openstack_dashboard
%define script_name /dashboard
%define py_puresitedir  /usr/lib/python2.6/site-packages
%define httpd_conf /etc/httpd/conf/httpd.conf

Name:           openstack-dashboard
Version:	1.0
Release:	0.20110928.1814%{?dist}
Url:            http://www.openstack.org
License:        Apache 2.0
Group:          Development/Languages/Python
Source0:          http://openstack-dashboard.openstack.org/tarballs/%{name}-%{version}.tar.gz  
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools
BuildArch:      noarch
Summary:        A Django interface for OpenStack

Requires:       httpd mod_wsgi 
Requires:       openstack-keystone openstack-compute openstackx 
Requires:       python-dateutil python-eventlet >= 0.9.12 python-greenlet python-sqlalchemy >= 0.6.3 
Requires:       python-sqlalchemy-migrate >= 0.6 python-webob >= 1 python-cloudfiles python-boto = 1.9b python-httplib2 
Requires:       Django = 1.3 django-mailer django-nose
Summary:        Django based reference implementation of a web based management interface for OpenStack.

%description
The OpenStack Dashboard is a reference implementation of a Django site that
uses the Django-Nova project to provide web based interactions with the
OpenStack Nova cloud controller.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build

%install
%__rm -rf %{buildroot}
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --record %{mod_name}.files

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{mod_name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{mod_name}

%clean
%__rm -rf %{buildroot}

%post
(cd /etc/%{mod_name}/local && cp local_settings.py.example local_settings.py)
# Database init
if test $1 -le 1; then
    echo "DB init code, new installation"
    python -m %{mod_name}.manage syncdb
    chown -R apache:apache %{_localstatedir}/lib/%{mod_name}
    chown -R apache:apache %{_localstatedir}/log/%{mod_name}
fi

echo 'SCRIPT_NAME = "%{script_name}"' >> /etc/%{mod_name}/local/local_settings.py

if ! grep -q '%{mod_name}/wsgi/django.wsgi' %{httpd_conf}; then
    echo "Adding entry to %{httpd_conf}"
    echo '' >> %{httpd_conf}
    echo 'WSGIScriptAlias %{script_name} /usr/lib/python2.6/site-packages/%{mod_name}/wsgi/django.wsgi' >> %{httpd_conf}
    echo 'Alias /static/%{mod_name} /usr/lib/python2.6/site-packages/%{mod_name}/static/%{mod_name}' >> %{httpd_conf}
fi

%files -f %{mod_name}.files
%defattr(-,root,root,-)
%doc README
%{_sysconfdir}
%dir %attr(0755, apache, apache) %{_localstatedir}/lib/%{mod_name}
%dir %attr(0755, apache, apache) %{_localstatedir}/log/%{mod_name}

%changelog
