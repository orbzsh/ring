%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}

%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name: uuzu-python27-markupsafe
Version: 0.21
Release: 1%{?dist}
Summary: Implements a XML/HTML/XHTML Markup safe string for Python

Group: Development/Languages
License: BSD
URL: http://pypi.python.org/pypi/MarkupSafe
Source0: http://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: uuzu-python27-devel

%if 0%{?with_python3}
BuildRequires: python3-devel python3-setuptools
# For /usr/bin/2to3
BuildRequires: python-tools
%endif # if with_python3


%description
A library for safe markup escaping.

%if 0%{?with_python3}
%package -n python3-markupsafe
Summary: Implements a XML/HTML/XHTML Markup safe string for Python
Group: Development/Languages

%description -n python3-markupsafe
A library for safe markup escaping.
%endif #if with_python3

%prep
%setup -q -n MarkupSafe-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif # with_python3

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# C code errantly gets installed
rm $RPM_BUILD_ROOT/%{python_sitearch}/markupsafe/*.c

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{python3_sitearch}/markupsafe/*.c
popd
%endif # with_python3


%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-markupsafe
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.rst
%{python3_sitearch}/*
%endif # with_python3


%changelog
* Wed Apr 23 2010 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 0.21
 - create this
