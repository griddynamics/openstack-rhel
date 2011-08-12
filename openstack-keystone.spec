%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define mod_name keystone
%define py_puresitedir  /usr/lib/python2.6/site-packages

Name:           openstack-keystone
Release:	0.20110813.0346%{?dist}
Version:	1.0
Url:            http://www.openstack.org
Summary:        Python bindings to the OS API
License:        Apache 2.0
Vendor:         Grid Dynamics Consulting Services, Inc.
Group:          Development/Languages/Python
Source0:          http://openstack-keystone.openstack.org/tarballs/%{name}-%{version}.tar.gz  
Source1:        %{name}.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel python-setuptools python-sphinx >= 0.6.0
BuildArch:      noarch
Requires:       python-eventlet python-lxml python-paste python-sqlalchemy python-routes python-httplib2

%description
Authentication service - proposed for OpenStack

%prep
%setup -q -n %{name}-%{version}
sed -i 's|sqlite:///keystone|sqlite:////var/lib/keystone/keystone|' etc/keystone.conf
sed -i 's|log_file = keystone.log|log_file = /var/log/keystone/keystone.log|' etc/keystone.conf

%build
python setup.py build

%install
%__rm -rf %{buildroot}

%__make -C doc/ html PYTHONPATH=%{_builddir}/%{name}-%{version}
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{mod_name}
install -m 644 etc/* %{buildroot}%{_sysconfdir}/%{mod_name}
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -m 644 examples/paste/auth_*ini %{buildroot}%{_sysconfdir}/nova
install -m 644 examples/paste/nova-api-paste.ini %{buildroot}%{_sysconfdir}/nova/api-paste.ini.keystone.example

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{mod_name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{mod_name}

install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%__rm -rf %{buildroot}%{py_puresitedir}/{doc,examples}
%__rm %{buildroot}%{py_puresitedir}/tools/pip-requires*

%clean
%__rm -rf %{buildroot}

%pre
getent passwd keystone >/dev/null || \
useradd -r -g nobody -G nobody -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemon" keystone
exit 0

%preun
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop
    /sbin/chkconfig --del %{name}
fi

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
