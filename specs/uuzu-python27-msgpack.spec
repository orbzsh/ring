%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global srcname msgpack

Name:           uuzu-python27-%{srcname}
Version:        0.4.2
Release:        1%{?dist}
Summary:        A Python MessagePack (de)serializer

Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/msgpack-python/
Source0:        http://pypi.python.org/packages/source/m/%{srcname}-python/%{srcname}-python-%{version}.tar.gz
#Patch0:         msgpack-python-0.1.9-endian.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  uuzu-python27-devel
#BuildRequires:  python-setuptools
#BuildRequires:  python-nose

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}


%description
MessagePack is a binary-based efficient data interchange format that is
focused on high performance. It is like JSON, but very fast and small.
This is a Python (de)serializer for MessagePack.


%prep
%setup -q -n %{srcname}-python-%{version}
#%patch0 -p1 -b .endian


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}


##%check
##PYTHONPATH="%{buildroot}%{python_sitearch}" nosetests -w test


%files
%defattr(-,root,root,-)
%{python_sitearch}/%{srcname}/
%{python_sitearch}/%{srcname}*.egg-info


%changelog
* Fri Apr 11 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 0.4.2-1
- create this file

