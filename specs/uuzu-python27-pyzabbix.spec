%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7
%define srcname pyzabbix
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           uuzu-python27-pyzabbix
Version:        0.6
Release:        2%{?dist}
Summary:        zabbix monitoring api

Group:          Development/Languages
License:        LGPL
URL:            http://github.com/lukecyca/pyzabbix
Source0:        https://pypi.python.org/packages/source/p/pyzabbix/pyzabbix-%{version}.tar.gz
Requires:       uuzu-python27
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  uuzu-python27-devel
Requires: uuzu-python27-requests


%description
zabbix monitoring api

%prep
%setup -q -n %{srcname}-%{version}

%build
export LIBRARY_PATH='/data/app/lib/'
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{python_sitelib}/pyzabbix
%{python_sitelib}/pyzabbix/*
%{python_sitelib}/pyzabbix-%{version}-py*.egg-info/

%changelog
* Mon May 26 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> 1.53-2
- add python-requests Requires

* Fri Apr 10 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> 1.53-1
- create this file
