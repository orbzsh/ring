%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")} 
%define install_path   /data/app/python
%define bin_path       %{install_path}/bin
%define install_root   /data/app

%global srcname setuptools

Name:           uuzu-python27-setuptools
Version:        3.4.4
Release:        1%{?dist}
Summary:        Easily build and distribute Python packages

Group:          Applications/System
License:        Python or ZPLv2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/d/%{srcname}/%{srcname}-%{version}.tar.gz
#Source1:        psfl.txt
#Source2:        zpl.txt
#Patch0:         http://bitbucket.org/tarek/distribute/changeset/b045d0750c13/raw/distribute-b045d0750c13.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  uuzu-python27-devel

# Legacy: We removed this subpackage once easy_install no longer depended on
# python-devel
Provides: uuzu-python27-setuptools-devel = %{version}-%{release}
#Obsoletes: python-setuptools-devel < 0.6.7-1

# Provide this since some people will request distribute by name
Provides: uuzu-python27-distribute = %{version}-%{release}

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%prep
%setup -q -n %{srcname}-%{version}
#%patch0 -p1
#find -name '*.txt' | xargs chmod -x
#find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

rm -rf %{buildroot}%{python_sitelib}/setuptools/tests
rm -rf %{buildroot}%{python_sitelib}/*egg-info/*.orig

#install -p -m 0644 %{SOURCE1} %{SOURCE2} .

find %{buildroot}%{python_sitelib} -name '*.exe' | xargs rm -f
chmod +x %{buildroot}%{python_sitelib}/setuptools/command/easy_install.py

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
%{bin_path}/easy_install
%{bin_path}/easy_install-2.7


%changelog
* Tue Apr 22 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 3.4.4-1
 - craete uuzu-python27-setuptools 3.4.4  
