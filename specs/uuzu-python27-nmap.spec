%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")} 
%define install_path   /data/app/python
%define bin_path       %{install_path}/bin
%define install_root   /data/app

%global srcname python-nmap

Name:           uuzu-python27-nmap
Version:        0.1.4
Release:        1%{?dist}
Summary:        A tool for installing and managing Python packages.
Group:          Development/Libraries
License:        Python or ZPLv2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/p/nmap/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  uuzu-python27-devel

%description
python-nmap is a python library which helps in using nmap port scanner. 
It allows to easilly manipulate nmap scan results and will be a perfect tool for systems administrators who want to automatize scanning task and reports. 
It also supports nmap script outputs.
It can even be used asynchronously. Results are returned one host at a time to a callback function defined by the user.

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

#%check
#%{__python} setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#%doc *.txt docs
%{python_sitelib}/*

%changelog
* Mon Nov 11 2014 Yule Fan <yulefan@cyou-inc.com> - 0.1.4
 - craete uuzu-python27-nmap 0.1.4
