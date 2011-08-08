#%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
#%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define mod_name dashboard
%define py_puresitedir  /usr/lib/python2.6/site-packages

Name:           openstack-dashboard
Release:	0.20110805.20%{?dist}
Version:	1.0
Url:            http://www.openstack.org
Summary:        Django based reference implementation of a web based management interface for OpenStack.
License:        Apache 2.0
Vendor:         Grid Dynamics Consulting Services, Inc.
Group:          Development/Languages/Python
Source0:          http://openstack-dashboard.openstack.org/tarballs/%{name}-%{version}.tar.gz  
Source1:        %{name}.init
Source2:        %{name}-%{version}-setup.py
Source3:        %{name}-%{version}-dashboard
#Patch:          %{name}-%{version}-conf.patch
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
#%patch -p1

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
