%define username   memcached
%define groupname  memcached
#defined the path
%define srcname memcached
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}
#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}


Name:           uuzu-%{srcname}
Version:        1.4.15
#%{?dist} is a user custom macros, see details in /etc/rpm/macros.dist
#this macros not in the RHEL5.X
Release:        1%{?dist}
#Don't use the epoch tags
#Epoch:		0
Summary:        High Performance, Distributed Memory Object Cache
Group:          uuzu-sys/Database
License:        BSD
URL:            http://www.memcached.org/
Source0:        http://memcached.googlecode.com/files/%{srcname}-%{version}.tar.gz
# custom init script
Source1:        memcached.sysv
BuildRoot:      %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
Autoreq: 0
BuildRequires:  uuzu-libevent-devel
BuildRequires:  perl(Test::More)
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

#sub rpm package uuzu-memcached-devel-
%package devel
Summary:	Files needed for development using memcached protocol
Group:		Development/Libraries 
#Requires:	%{srcname} = %{epoch}:%{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require access to the
memcached binary include files.

%prep
%setup -q -n %{srcname}-%{version}

%build
./configure --build=%{_build} \
            --prefix=/usr \
	    --bindir=%{install_path}/bin \
	    --sbindir=%{install_path}/sbin \
	    --libexecdir=%{install_path}/libexec \
	    --sysconfdir=%{install_path}/conf \
	    --libdir=%{install_path}/lib \
	    --includedir=%{include_path} \
	    --with-libevent=%{install_root}/
#this is a build-require, in this example we use the system path

#%{?_smp_mflags}, see details in /usr/lib/rpm/platform/x86_64-linux/macros
make %{?_smp_mflags}

%check
#start test as root
sed -i '66 i$params .= " -u root";' t/issue_67.t
# Parts of the test suite only succeed as non-root.
#just in example comment the if
#if [ `id -u` -ne 0 ]; then
  # remove failing test that doesn't work in
  # build systems
  rm -f t/daemonize.t 
  make test
#fi

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"                                         
# remove memcached-debug
rm -f %{buildroot}/%{install_path}/bin/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{install_path}/bin/memcached-tool

# Init script
mkdir -p %{init_dir}
install -Dp -m0755 %{SOURCE1} %{buildroot}%{init_dir}/%{srcname}

# Default configs
mkdir -p %{buildroot}/%{install_path}/conf/sysconfig
cat <<EOF >%{buildroot}/%{install_path}/conf/sysconfig/%{srcname}
PORT="11211"
USER="%{username}"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

# Constant timestamp on the config file.
touch -r %{SOURCE1} %{buildroot}/%{install_path}/conf/sysconfig/%{srcname}

# pid directory
mkdir -p %{buildroot}/%{_localstatedir}/run/memcached

%clean
rm -rf %{buildroot}

%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || \
useradd -r -g %{groupname} -d %{_localstatedir}/run/memcached \
    -s /sbin/nologin -c "Memcached daemon" %{username}
exit 0

%post
#create the links
mkdir -p /data/app
ln -sf %{install_path}/init.d/%{srcname} %{_initrddir}/%{name}
ln -sf %{install_path}/conf/sysconfig/%{srcname} %{_sysconfdir}/sysconfig/%{srcname}

/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1
fi
#remove links
rm -rf %{install_root}/%{srcname}
rm -f %{_initrddir}/%{name}
rm -f %{_sysconfdir}/sysconfig/%{name}
exit 0

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{install_path}/conf/sysconfig/%{srcname}

%dir %attr(755,%{username},%{groupname}) %{_localstatedir}/run/memcached
%{install_path}/bin/memcached-tool
%{install_path}/bin/memcached
%{_mandir}/man1/memcached.1*
%{init_dir}/memcached

%files devel
%defattr(-,root,root,0755)
%{include_path}/memcached/*

%changelog
* Wed Oct 16 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 1.4.15-1
- update to 1.4.15
- off debuginfo package
* Thu Oct 10 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 1.4.4-3
- create this file
- rpmbuild can used by root
