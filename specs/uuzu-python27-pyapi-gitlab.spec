%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")} 
%define install_path   /data/app/python
%define bin_path       %{install_path}/bin
%define install_root   /data/app

%global srcname pyapi-gitlab

Name:           uuzu-python27-pyapi-gitlab
Version:        7.0.0
Release:        2%{?dist}
Summary:        pyapi-gitlab is a python wrapper for the Gitlab API.
Group:          Development/Libraries
License:        GPL3
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/p/pyapi-gitlab/%{srcname}-%{version}.tar.gz
Requires:       uuzu-python27-Markdown
Requires:       uuzu-python27-requests
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  uuzu-python27-devel


%description
pyapi-gitlab is a wrapper to access all the functions of Gitlab from our python scripts.

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
* Mon Nov 11 2014 Yule Fan <yulefan@cyou-inc.com> - 7.0.0
 - craete uuzu-python27-pyapi-gitlab 7.0.0
