%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           uuzu-python27-requests
Version:        2.4.3
Release:        1%{?dist}
Summary:        Awesome Python HTTP Library That's Actually Usable

Group:          Development/Libraries
License:        Apache 2.0
URL:            https://pypi.python.org/pypi/requests
Source0:        https://pypi.python.org/packages/source/r/requests/requests-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  uuzu-python27-devel
#BuildRequires:  python-setuptools-devel

Requires:       uuzu-python27
BuildArch:      noarch

%description
Requests allow you to send HTTP/1.1 requests. You can add headers, 
form data, multipart files, and parameters with simple Python dictionaries, 
and access the response data in the same way. It's powered by httplib and urllib3, 
but it does all the hard work and crazy hacks for you.


%prep
%setup -q -n requests-%{version}


%build
export LIBRARY_PATH='/data/app/lib/'
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
chmod -x $RPM_BUILD_ROOT%{python_sitearch}/requests-*-*.egg-info/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitearch}/requests-*-*.egg-info/
%{python_sitearch}/requests/

%changelog
* Mon Nov 11 2014 Yule Fan <yulefan@cyou-inc.com> 2.4.3-1
- update to 2.4.3

* Tue Apr 10 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> 2.3.0-1
- create this file
