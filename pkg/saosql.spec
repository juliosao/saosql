Summary: Tiny sql query manager
Name: saosql
Version: 1.1
Release: 1%{?dist}
License: Privative
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source0: %{name}-%{version}.tar.bz2
Requires: MySQL-python
BuildArch: noarch

%description
saosql provides an ease to use graficale enviroment for running querys on mysql servers

%prep
%setup -q

%build
make

%install
make PREFIX=$RPM_BUILD_ROOT install



%clean
make clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/opt/saosql
/usr/bin/saosql
/usr/share/applications/sao-saosql.desktop

%changelog
* Thu Mar 22 2012 Julio A. Garcia Lopez <juliosao@gmail.com> 0.1.0
- Initial package.

