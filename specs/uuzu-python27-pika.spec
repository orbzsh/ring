%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define short_name pika

Name:           uuzu-python27-%{short_name}
Version:        0.9.13
Release:        1%{?dist}
Summary:        AMQP 0-9-1 client library for Python

Group:          Development/Libraries
License:        MPLv1.1 or GPLv2
URL:            http://github.com/%{short_name}/%{short_name}
# The tarball comes from here:
# http://github.com/%{short_name}/%{short_name}/tarball/v%{version}
# GitHub has layers of redirection and renames that make this a troublesome
# URL to include directly.
Source0:        %{short_name}-%{version}.tar.gz
#Patch0:         blocking_connection.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  uuzu-python27-devel
Requires:       uuzu-python27

%description
Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that
tries to stay fairly independent of the underlying network support
library.


%prep
%setup -q -n %{short_name}-%{version}
#%patch0 -p0


%build
export LIBRARY_PATH='/data/app/lib/'
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/%{short_name}*
%{python_sitelib}/%{short_name}*/*

%changelog
* Tue Apr 10 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 0.9.13-1
- upgrade to 0.9.13 and build with python 2.7

* Tue Dec 13 2011 Daniel Aharon <dan@danielaharon.com> - 0.9.5-2
- Patch pika/adapters/blocking_connection.py

* Sun Apr 3 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.5-1
- Upgrade to version 0.9.5

* Sun Mar 6 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.4-1
- Upgrade to version 0.9.4

* Sat Feb 19 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.3-1
- Upgrade to version 0.9.3

* Sat Oct 2 2010 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.5.2-1
- Initial Package

