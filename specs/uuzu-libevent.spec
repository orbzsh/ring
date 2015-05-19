%define srcname libevent
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}

Name:           uuzu-%{srcname}
Version:        2.0.21
Release:        1%{?dist}
Summary:        Abstract asynchronous event notification library

Group:          uuzu-sys/Libraries
License:        BSD
URL:            http://monkey.org/~provos/libevent/
Source0:        http://monkey.org/~provos/libevent-%{version}-stable.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: doxygen

#Patch00: libevent-1.4.13-stable-configure.patch

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}

%description devel
This package contains the static libraries documentation for %{name}. 
If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%package doc
Summary: Development documentation for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}. 
If you like to develop programs using %{name}-devel, you will 
need to install %{name}-doc.

%package headers
Summary: Header file for development  for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description headers
This package contains the header files for %{name}. If you like to 
develop programs using %{name}, you will need to install %{name}-devel.

%prep
%setup -q -n libevent-%{version}-stable

# 477685 -  libevent-devel multilib conflict
#%patch00 -p1

%build
./configure --build=%{_build} \
            --prefix=%{_prefix} \
            --bindir=%{install_path}/bin \
            --sbindir=%{install_path}/sbin \
            --libexecdir=%{install_path}/libexec \
            --sysconfdir=%{install_path}/conf \
            --libdir=%{install_root}/lib \
            --includedir=%{install_root}/include

make %{?_smp_mflags}

# Create the docs
make doxygen

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{install_root}/lib/*.la

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/html
(cd doxygen/html; \
	install *.* $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/html)

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/latex
(cd doxygen/latex; \
	install *.* $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/latex)

#mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/man/man3
#(cd doxygen/man/man3; \
#	install *.3 $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/man/man3)

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/sample
(cd sample; \
	install *.c Makefile* $RPM_BUILD_ROOT/%{_docdir}/%{srcname}-devel-%{version}/sample)

#%check
#make verify

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "/data/app/lib" >/etc/ld.so.conf.d/uuzu-libevent.conf
/sbin/ldconfig

%postun
rm -f /etc/ld.so.conf.d/uuzu-libevent.conf
/sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc README
%{install_root}/lib/libevent-*.so.*
%{install_root}/lib/libevent_core-*.so.*
%{install_root}/lib/libevent_extra-*.so.*
%{install_root}/lib/libevent_openssl*
%{install_root}/lib/libevent_pthreads*
%{install_root}/lib/pkgconfig/*

%files devel
%defattr(-,root,root,0755)
%{install_root}/lib/libevent.so
%{install_root}/lib/libevent.a
%{install_root}/lib/libevent_core.so
%{install_root}/lib/libevent_core.a
%{install_root}/lib/libevent_extra.so
%{install_root}/lib/libevent_extra.a

%{install_path}/bin/event_rpcgen.*

#%{_mandir}/man3/*

%files doc
%defattr(-,root,root,0644)
%{_docdir}/%{srcname}-devel-%{version}/html/*
%{_docdir}/%{srcname}-devel-%{version}/latex/*
#%{_docdir}/%{name}-devel-%{version}/man/man3/*
%{_docdir}/%{srcname}-devel-%{version}/sample/*

%files headers
%{install_root}/include/event.h
%{install_root}/include/evdns.h
%{install_root}/include/evhttp.h
%{install_root}/include/evrpc.h
#%{install_root}/include/event-config.h
%{install_root}/include/event2/*
%{install_root}/include/evutil.h
%defattr(-,root,root,0644)

%changelog
* Wed Oct 16 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> 2.0.21-1
- Create this file
- Have no man dir
