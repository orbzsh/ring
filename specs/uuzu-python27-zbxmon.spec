%define __python /data/app/python/bin/python%{pybasever}
%if 0%{?el5}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")}
%endif

%global short_name zbxmon

%define pyver 27
%define pybasever 2.7
%define real_name zbxmon

# Filter Python modules from Provides
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Name:           uuzu-python%{pyver}-zbxmon
Version:        0.2
Release:        1%{?dist}
Summary:	A script for zabbix agent monitor service, etc. mysql, mongodb, memcache..

Group:          Development/Languages
License:        MIT
URL:            https://github.com/damagedcode/zbxmon/
Source0:        %{short_name}-%{version}.tar.gz

Requires:       uuzu-python27-argh
Requires:       uuzu-python27-psutil
Requires:       uuzu-python27-pymongo
Requires:       uuzu-python27-memcached
Requires:       uuzu-python27-redis
Requires:       uuzu-MySQL-python

BuildRequires:  uuzu-python27-devel

%if 0%{?el5}
BuildRequires:  uuzu-python27-setuptools
BuildRequires:  gcc44
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

%description
A script for zabbix agent monitor service, etc. mysql, mongodb, memcache.

%prep
%setup -q -n %{short_name}


%build
export LIBRARY_PATH='/data/app/lib/'
CFLAGS=$RPM_OPT_FLAGS %{__python} setup.py build


%install
%if 0%{?el5}
rm -rf $RPM_BUILD_ROOT
%endif

%{__python} setup.py install \
  --skip-build \
  --root $RPM_BUILD_ROOT


%files
/data/app/bin/zbxmon
%{python_sitearch}/%{short_name}/
%{python_sitearch}/*.egg-info


%changelog
* Thu Nov 17 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 0.1-1
- create this file

