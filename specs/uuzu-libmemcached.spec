%define srcname libmemcached
%define install_root   /data/app
%define install_path   %{install_root}/%{srcname}
#%define init_dir      %{install_path}/init.d
%define include_path   %{install_root}/include
%define lib_path %{install_root}/%{_lib}
#%define logrotate_dir %{install_root}/logrotate.d
#%define conf_path      %{install_path}/conf
%define bin_path       %{install_path}/bin

#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

Name:      uuzu-%{srcname}
Summary:   Client library and command line tools for memcached server
Version:   1.0.16
Release:   1%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       http://tangent.org/552/libmemcached.html

# Original source: http://download.tangent.org/libmemcached-%{version}.tar.gz
# Repackaged without Hsieh-licensed code using strip-hsieh.sh
Source0: libmemcached-%{version}.tar.gz
Source1: strip-hsieh.sh

# checked during configure (for test suite)
BuildRequires: uuzu-memcached

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
libmemcached is a C client library to the memcached server
(http://danga.com/memcached). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memcat - Copy the value of a key to standard output.
memflush - Flush the contents of your servers.
memrm - Remove a key(s) from the server.
memstat - Dump the stats of your servers to standard output.
memslap - Generate testing loads on a memcached cluster.
memcp - Copy files to memcached servers.
memerror - Creates human readable messages from libmemcached error codes.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q -n %{srcname}-%{version}



%build
./configure --prefix=%{_prefix} \
	    --bindir=%{bin_path} \
	    --libdir=%{lib_path} \
	    --includedir=%{include_path} \
	    --with-memcached=/data/app/memcached-1.4.15/bin/ \
	    --with-mysql=/opt/uuzu/mysql/bin/mysql_config
%{__make} %{_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%check
# For documentation only:
# test suite cannot run in mock (same port use for memcache servers on all arch)
# All tests completed successfully
# diff output.res output.cmp fails but result depend on server version
#%{__make} test


%clean
%{__rm} -rf %{buildroot}


%post
echo "%{bin_path}" > %{_sysconfdir}/ld.so.conf.d/%{name}.conf
/sbin/ldconfig


%postun
rm -f %{_sysconfdir}/ld.so.conf.d/%{name}.conf
/sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{bin_path}/mem*
%exclude %{lib_path}/libmemcached.a
%exclude %{lib_path}/libmemcached.la
%exclude %{lib_path}/libmemcachedutil.a
%exclude %{lib_path}/libhashkit.a
%exclude %{lib_path}/libmemcachedutil.la
%exclude %{lib_path}/libhashkit.la
%{lib_path}/libmemcached.so.*
%{lib_path}/libmemcachedutil.so.*
%{lib_path}/libhashkit.so.*


%files devel
%defattr (-,root,root,-) 
/usr/share/aclocal/ax_libmemcached.m4
%{include_path}/libmemcached*
%{include_path}/libhashkit*
%{lib_path}/libmemcached.so
%{lib_path}/libhashkit.so
%{lib_path}/libmemcachedutil.so
%{lib_path}/pkgconfig/libmemcached.pc


%changelog
