# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-netifaces
Version:        0.5
Release:        1%{?dist}
Summary:        Python library which provides a list of network interfaces and its addresses on the local machine

Group:          Development/Languages
License:        MIT
URL:            http://alastairs-place.net/netifaces/
Source0:        http://alastairs-place.net/2007/03/netifaces/netifaces-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel python-setuptools

%description
netifaces provides a (hopefully portable-ish) way for Python programmers to get
access to a list of the network interfaces on the local machine, and to obtain
the addresses of those network interfaces.

%prep
%setup -q -n netifaces-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{python_sitearch}/*


%changelog
* Tue May 10 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.5-1
- Initial build
