%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")} 
%define install_path   /data/app/python
%define bin_path       %{install_path}/bin
%define install_root   /data/app

%global srcname Markdown

Name:           uuzu-python27-Markdown
Version:        2.5.1
Release:        1%{?dist}
Summary:        Python implementation of Markdown.
Group:          Development/Libraries
License:        GPL3
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/M/Markdown/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  uuzu-python27-devel


%description
This is a Python implementation of John Gruber's Markdown. 
It is almost completely compliant with the reference implementation, though there are a few known issues. 
See Features for information on what exactly is supported and what is not. 
Additional features are supported by the Available Extensions.

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

#%check
#%{__python} setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#%doc *.txt docs
%{python_sitelib}/*
%{bin_path}/markdown_py

%changelog
* Mon Nov 11 2014 Yule Fan <yulefan@cyou-inc.com> - 2.5.1
 - craete uuzu-python27-Markdown 2.5.1
