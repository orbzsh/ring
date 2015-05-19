
#defined the path
%define srcname redis
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define init_dir     %{install_path}/init.d
%define bin_path     %{install_path}/bin
%define sbin_path     %{install_path}/sbin
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path      %{install_path}/conf
%define log_path       /opt/logs/redis
#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

Name:             uuzu-%{srcname}
Version:          2.6.16
Release:          1%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://code.google.com/p/redis/
Source0:          http://redis.googlecode.com/files/%{srcname}-%{version}.tar.gz
Source1:          %{srcname}.logrotate
Source2:          %{srcname}.init
Patch0:           redis-2.6.13-conf.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    tcl

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

%build
%ifarch i386 i686
CFLAGS="-march=i686"
export CFLAGS
make    INSTALL_LIB=%{lib_path} \
        INSTALL_BIN=%{bin_path}
%else
make	E=@: PREFIX=%{_prefix} \
        INSTALL_LIB=%{lib_path} \
	INSTALL_BIN=%{bin_path} \
	%{?_smp_mflags}
%endif

%install
rm -fr %{buildroot}
make install PREFIX=%{buildroot}%{_prefix} \
	     INSTALL_LIB=%{buildroot}%{lib_path} \
	     INSTALL_BIN=%{buildroot}%{bin_path} 

mkdir -p %{buildroot}%{install_root}
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{init_dir}
mkdir -p %{buildroot}%{bin_path}
mkdir -p %{buildroot}%{sbin_path}
mkdir -p %{buildroot}%{include_path}
mkdir -p %{buildroot}%{lib_path}
mkdir -p %{buildroot}%{logrotate_dir}
mkdir -p %{buildroot}%{conf_path}
mkdir -p %{buildroot}%{log_path}
mkdir -p %{buildroot}/opt/17173 
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d/

# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{logrotate_dir}/%{srcname}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{init_dir}/%{srcname}
install -p -D -m 644 %{srcname}.conf %{buildroot}%{conf_path}/%{srcname}.conf
install -p -D -m 644 sentinel.conf %{buildroot}%{conf_path}/sentinel.conf
install -d -m 755 %{buildroot}%{lib_path}/%{srcname}
install -d -m 755 %{buildroot}%{log_path}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{srcname}

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{bin_path}/%{srcname}-*

# Ensure redis-server location doesn't change
mkdir -p %{buildroot}%{sbin_path}
mv %{buildroot}%{bin_path}/%{srcname}-server %{buildroot}%{sbin_path}/%{srcname}-server
ln -s %{install_path} %{buildroot}/opt/uuzu/%{srcname}
ln -sf %{init_dir}/%{srcname} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add uuzu-redis

%pre
getent group redis &> /dev/null || groupadd -r redis &> /dev/null
getent passwd redis &> /dev/null || \
useradd -r -g redis -d %{log_path} -s /sbin/nologin \
-c 'Redis Server' redis &> /dev/null
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis &> /dev/null
fi

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README
%config(noreplace) %{logrotate_dir}/%{srcname}
%config(noreplace) %{conf_path}/%{srcname}.conf
%config(noreplace) %{conf_path}/sentinel.conf
%dir %attr(0755, redis, root) %{lib_path}/%{srcname}
%dir %attr(0755, redis, root) %{log_path}
%dir %attr(0755, redis, root) %{_localstatedir}/run/%{srcname}
%{bin_path}/%{srcname}-*
%{sbin_path}/%{srcname}-*
%{init_dir}/%{srcname}
/opt/uuzu/%{srcname}
%{_sysconfdir}/rc.d/init.d/%{name}

%changelog
* Mon Sep 02 2013 Denis Frolov <d.frolov81@mail.ru> - 2.6.16-1
- Update to 2.6.16
