%define pecl_name memcache
%define pecl_dir_name memcache

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	2.2.7
Release:	1%{?dist}
Summary:	PHP extension for memcached

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

BuildRequires:	uuzu-php-cli,uuzu-php-devel

%description
Memcached is a caching daemon designed especially for 
dynamic web applications to decrease database load by 
storing objects in memory.
This extension allows you to work with memcached through
handy OO and procedural interfaces.


%prep
%setup -q -c -n %{pecl_dir_name}-%{version}


%build
cd %{pecl_dir_name}-%{version}
%{phpize}
./configure --with-php-config=/opt/uuzu/php/bin/php-config

make %{?_smp_mflags}


%install
cd %{pecl_dir_name}-%{version}
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

%{__mkdir_p} %{buildroot}/opt/uuzu/php/conf/php.d
%{__cat} > %{buildroot}/opt/uuzu/php/conf/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcache.
;  Whether to transparently failover to other servers on errors.
;memcache.allow_failover = 1
;  Defines how many servers to try when setting and getting data. Used only in conjunction with memcache.allow_failover.
;memcache.max_failover_attempts = 20
;  Data will be transferred in chunks of this size, setting the value lower requires more network writes. Try increasing this value to 32768 if noticing otherwise inexplicable slowdowns.
;memcache.chunk_size = 8192
;  The default TCP port number to use when connecting to the memcached server if no other port is specified.
;memcache.default_port = 11211
;  Controls which strategy to use when mapping keys to servers. Set this value to consistent to enable consistent hashing which allows servers to be added or removed from the pool without causing keys to be remapped. Setting this value to standard results in the old strategy being used.
;memcache.hash_strategy = "standard"
;  Controls which hash function to apply when mapping keys to servers, crc32 uses the standard CRC32 hash while fnv uses FNV-1a.
;memcache.hash_function = "crc32"
;  Use memcache as a session handler by setting this value to memcache.
;session.save_handler = "files"
;  Defines a comma separated of server urls to use for session storage, for example "tcp://host1:11211, tcp://host2:11211".
;  Each url may contain parameters which are applied to that server, they are the same as for the Memcache::addServer() method. For example "tcp://host1:11211?persistent=1&weight=1&timeout=1&retry_interval=15"
;session.save_path = ""
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so



%changelog
* Sun Jan 26 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 2.2.7-1
- Create this file
