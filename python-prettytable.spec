%global with_doc 1
%global pkg prettytable

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		python-%{pkg}
Version:	0.5
Release:	1%{?dist}
Summary:	A simple library for displaying tabular data in a visually appealing ASCII table format

Group:		Development/Python
License:	BSD
URL:		http://code.google.com/p/prettytable/
Source0:	http://pypi.python.org/packages/source/P/PrettyTable/prettytable-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	python-devel python-sphinx

%description
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by specifying
a row range.

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
%{python_sitelib}/prettytable.*
%{python_sitelib}/*.egg-info

%changelog
* Fri Mar 25 2011 Andrey Brindeyev <abrindeyev@griddynamics.com> - 0.5-1
- Initial build
