%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")} 
%define install_path   /data/app/python
%define bin_path       %{install_path}/bin
%define install_root   /data/app

%global srcname Django

Name:           uuzu-python27-Django
Version:        1.7.2
Release:        1%{?dist}
Summary:        A high-level Python Web framework.
Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/D/Django/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  uuzu-python27-devel


%description
Django is a high-level Python Web framework that encourages rapid
development and a clean, pragmatic design. It focuses on automating as
much as possible and adhering to the DRY (Don't Repeat Yourself)
principle.

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

#move bin dir
mkdir -p %{buildroot}%{install_path}
mv  %{buildroot}%{install_root}/bin %{buildroot}%{install_path}

%check
%{__python} setup.py test

%clean
rm -rf %{buildroot}

%post
useradd -s /sbin/nologin app >/dev/null 2>&1

%files
%defattr(-,root,root,-)
#%doc *.txt docs
%{python_sitelib}/*
%{bin_path}/django-admin
%{bin_path}/django-admin.py

%changelog
* Mon Jan 12 2015 Yule Fan <yulefan@cyou-inc.com> - 1.7.2-1
 - update to Django 1.7.2
 - change user from appid to app
 
* Mon Nov 12 2014 Yule Fan <yulefan@cyou-inc.com> - 1.7.1-2
 - add user appid
 
* Mon Nov 11 2014 Yule Fan <yulefan@cyou-inc.com> - 1.7.1-1
 - craete uuzu-python27-Django 1.7.1
