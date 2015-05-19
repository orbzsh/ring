%define __python /data/app/python/bin/python%{pybasever}
%if 0%{?el5}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")}
%endif

%global short_name argh

%define pyver 27
%define pybasever 2.7
%define real_name python-argh

# Filter Python modules from Provides
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Name:           uuzu-python%{pyver}-argh
Version:        0.25.0
Release:        1%{?dist}
Summary:        An unobtrusive argparse wrapper with natural syntax

Group:          Development/Languages
License:        BSD
URL:		http://github.com/neithere/argh/
Source0:        https://pypi.python.org/packages/source/p/%{short_name}/%{short_name}-%{version}.tar.gz

BuildRequires:  uuzu-python27-devel

%if 0%{?el5}
BuildRequires:  uuzu-python27-setuptools
BuildRequires:  gcc44
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

%description
Building a command-line interface? Found yourself uttering "argh!" while 
struggling with the API of argparse? Don't like the complexity but need the power?
Argh is a smart wrapper for argparse. Argparse is a very powerful tool; Argh just makes it easy to use.

%prep
%setup -q -n %{short_name}-%{version}


%build
export LIBRARY_PATH='/data/app/lib/'
CFLAGS=$RPM_OPT_FLAGS %{__python} setup.py build


%install
%if 0%{?el5}
rm -rf $RPM_BUILD_ROOT
%endif

%{__python} setup.py install \
  --skip-build \
  --root $RPM_BUILD_ROOT


%files
%{python_sitearch}/%{short_name}/
%{python_sitearch}/*.egg-info


%changelog
* Thu Aug 26 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 0.25.0-1
- create this file

