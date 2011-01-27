Name:		start-stop-daemon
Version:	1.9.18
Release:	1%{?dist}
Summary:	A rewrite of the original Debian's start-stop-daemon Perl script in C

Group:		System Environment/Base
License:	Public Domain
URL:		http://developer.axis.com/download/distribution
Source0:	http://developer.axis.com/download/distribution/apps-sys-utils-start-stop-daemon-IR1_9_18-2.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc

%description
A rewrite of the original Debian's start-stop-daemon Perl script
in C (faster - it is executed many times during system startup).

Can create a pidfiles for dumb programs

%prep
%setup -q -n apps

%build
cd sys-utils/start-stop-daemon-IR1_9_18-2
gcc -o %{name} %{name}.c
strip %{name}

%install
rm -rf %{buildroot}
cd sys-utils/start-stop-daemon-IR1_9_18-2
install -p -D -m 755 %{name} %{buildroot}/sbin/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/sbin/%{name}

%changelog
* Thu Jan 27 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 1.9.18-1
- Initial build for RHEL 6

