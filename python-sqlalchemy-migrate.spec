%global with_doc 1
%global pkg sqlalchemy-migrate

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		python-%{pkg}
Version:	0.6
Release:	1%{?dist}
Summary:	Schema migration tools for SQLAlchemy

Group:		Development/Python
License:	MIT
URL:		http://code.google.com/p/sqlalchemy-migrate/
Source0:	http://sqlalchemy-migrate.googlecode.com/files/sqlalchemy-migrate-0.6.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python-devel python-sphinx
Requires:	python-sqlalchemy >= 0.5
Requires:	python-decorator
Requires:	python-tempita

%description
Inspired by Ruby on Rails’ migrations, SQLAlchemy Migrate provides a way to
deal with database schema changes in SQLAlchemy projects.

Migrate was started as part of Google’s Summer of Code by Evan Rosson, mentored
by Jonathan LaCour.

The project was taken over by a small group of volunteers when Evan had no free
time for the project. It is now hosted as a Google Code project. During the
hosting change the project was renamed to SQLAlchemy Migrate.

Currently, sqlalchemy-migrate supports Python versions from 2.4 to 2.6.
SQLAlchemy Migrate 0.6.0 supports SQLAlchemy both 0.5.x and 0.6.x branches.

%prep
%setup -q -n %{pkg}-%{version}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/migrate
%{_bindir}/migrate-repository
%{python_sitelib}/migrate
%{python_sitelib}/sqlalchemy_migrate-%{version}-*.egg-info

%changelog
* Mon Jan 24 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> 0.6-1
- Initial build


