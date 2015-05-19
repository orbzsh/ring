%define __python /data/app/python/bin/python%{pybasever}
%if 0%{?el5}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")}
%endif

%global short_name psutil

%define pyver 27
%define pybasever 2.7
%define real_name python-psutil

# Filter Python modules from Provides
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Name:           uuzu-python%{pyver}-psutil
Version:        2.1.0
Release:        1%{?dist}
Summary:        A process and system utilities module for Python

Group:          Development/Languages
License:        BSD
URL:            http://psutil.googlecode.com/
#Source0:        http://psutil.googlecode.com/files/%{short_name}-%{version}.tar.gz
Source0:        https://pypi.python.org/packages/source/p/%{short_name}/%{short_name}-%{version}.tar.gz

BuildRequires:  uuzu-python27-devel

%if 0%{?el5}
BuildRequires:  uuzu-python27-setuptools
BuildRequires:  gcc44
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

%description
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network, users) in
a portable way by using Python, implementing many functionalities offered by
command line tools such as: ps, top, df, kill, free, lsof, free, netstat,
ifconfig, nice, ionice, iostat, iotop, uptime, pidof, tty, who, taskset, pmap.

%prep
%setup -q -n %{short_name}-%{version}

# Remove shebangs
for file in psutil/*.py; do
  sed -i.orig -e 1d $file && \
  touch -r $file.orig $file && \
  rm $file.orig
done

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

# Fix permissions
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/*.so

%files
%doc CREDITS HISTORY LICENSE README
%{python_sitearch}/%{short_name}/
%{python_sitearch}/*.egg-info
%{python_sitearch}/*.so


%changelog
* Thu Apr 24 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.1.0-1
- upgrade to 2.1.0

