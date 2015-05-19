%define debug_package %{nil}
%global php_zendabiver %((echo 0; /opt/uuzu/php/bin/php -i 2>/dev/null | sed -n 's/^PHP Extension => //p') | tail -1)
%global php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)                     
%global pecl_name memcached

Summary:      Extension to work with the Memcached caching daemon
Name:         uuzu-php-pecl-memcached
Version:      2.1.0
Release:      1%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: uuzu-php-devel, uuzu-php-pear
BuildRequires: uuzu-libmemcached-devel, zlib-devel

# This is EPEL-5 specific
Requires:     uuzu-php-zend-abi = %{php_zendabiver}

Provides:     uuzu-php-pecl(%{pecl_name}) = %{version}-%{release}


%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 


%prep 
%setup -c -q
cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
/opt/uuzu/php/bin/phpize
./configure --with-php-config=/opt/uuzu/php/bin/php-config \
	    --with-libmemcached-dir=/data/app
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}/opt/uuzu/php/conf/php.d
%{__cat} > %{buildroot}/opt/uuzu/php/conf/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so


; ----- Options to use the memcached session handler

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"
EOF

# Install XML package description
%{__mkdir_p} %{buildroot}/opt/uuzu/php/pear/.pkgxml
%{__install} -m 644 ../package.xml %{buildroot}/opt/uuzu/php/pear/.pkgxml/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
/opt/uuzu/php/pear/.pkgxml/%{name}.xml


%changelog
