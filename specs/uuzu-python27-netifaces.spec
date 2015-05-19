%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from %distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from %distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           uuzu-python27-netifaces
Version:        0.8
Release:        1%{?dist}
Summary:        Python library to retrieve information about network interfaces

Group:          Development/Libraries
License:        MIT
URL:            http://alastairs-place.net/netifaces/
Source0:        https://pypi.python.org/packages/source/n/netifaces/netifaces-0.8.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  uuzu-python27-devel
#BuildRequires:  python-setuptools-devel

Requires:       uuzu-python27

%description
This package provides a cross platform API for getting address information
from network interfaces.


%prep
%setup -q -n netifaces-%{version}


%build
export LIBRARY_PATH='/data/app/lib/'
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
chmod -x $RPM_BUILD_ROOT%{python_sitearch}/netifaces-*-*.egg-info/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{python_sitearch}/netifaces-*-*.egg-info/
%{python_sitearch}/netifaces.so

%changelog
* Tue Apr 10 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> 0.8-1
- upgrade to 0.8 and build with python 2.7
* Wed Jun 1 2011 Ryan Rix <ry@n.rix.si> 0.5-1
- Initial packaging effort
