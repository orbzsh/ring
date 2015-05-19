%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           uuzu-python27-pytz
Version:        2014.2
Release:        1%{?dist}
Summary:        World Timezone Definitions for Python

Group:          Development/Languages
License:        MIT
URL:            http://pytz.sourceforge.net/
Source0:        http://pypi.python.org/packages/source/p/pytz/pytz-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  uuzu-python27-devel

Requires: tzdata

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations using Python 2.3 or higher. It
also solves the issue of ambiguous times at the end of daylight savings,
which you can read more about in the Python Library Reference
(datetime.tzinfo).

Amost all (over 540) of the Olson timezones are supported.

%prep
%setup -q -n pytz-%{version}

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitelib}/pytz/*.py
rm -rf  $RPM_BUILD_ROOT%{python_sitelib}/pytz/zoneinfo

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt
%{python_sitelib}/pytz/
%{python_sitelib}/*.egg-info

%changelog
* Wed Apr 23 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2014.2
- create this file

