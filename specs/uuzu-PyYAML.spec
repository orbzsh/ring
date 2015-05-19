%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}

%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif
%define srcname PyYAML
Name:           uuzu-PyYAML
Version:        3.11
Release:        1%{?dist}
Summary:        YAML parser and emitter for Python

Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{srcname}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  uuzu-python27-devel, uuzu-python27-setuptools, uuzu-libyaml-devel
Provides:       uuzu-python27-yaml = %{version}-%{release}
Provides:       uuzu-python27-yaml%{?_isa} = %{version}-%{release}
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%if 0%{?with_python3}
%package -n python3-PyYAML
Summary: YAML parser and emitter for Python
Group: Development/Libraries

%description -n python3-PyYAML
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.
%endif


%prep
%setup -q -n %{srcname}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
export LIBRARY_PATH="%{lib_path}"
CFLAGS="${RPM_OPT_FLAGS} -I%{include_path}" %{__python} setup.py --with-libyaml build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="${RPM_OPT_FLAGS} -I%{include_path}" %{__python3} setup.py --with-libyaml build
popd
%endif


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-PyYAML
%defattr(644,root,root,755)
%{python3_sitearch}/*
%endif


%changelog
* Fri Apr 11 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 3.11-1
- Upgrade to 3.11
