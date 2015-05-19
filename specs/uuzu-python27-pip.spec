%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")} 
%define install_path   /data/app/python
%define bin_path       %{install_path}/bin
%define install_root   /data/app

%global srcname pip

Name:           uuzu-python27-pip
Version:        1.5.6
Release:        1%{?dist}
Summary:        A tool for installing and managing Python packages.
Group:          Development/Libraries
License:        Python or ZPLv2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz
Requires:       uuzu-python27-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  uuzu-python27-devel
BuildRequires:  uuzu-python27-setuptools

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

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


%files
%defattr(-,root,root,-)
#%doc *.txt docs
%{python_sitelib}/*
%{bin_path}/pip
%{bin_path}/pip2
%{bin_path}/pip2.7

%changelog
* Mon Nov 10 2014 Yule Fan <yulefan@cyou-inc.com> - 1.5.6
 - craete uuzu-python27-pip 1.5.6
