%define pecl_name apc
%define pecl_dir_name APC

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	3.1.13
Release:	1%{?dist}
Summary:	PHP extension for Alternative PHP Cache

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

BuildRequires:	uuzu-php-cli,uuzu-php-devel

%description
APC is a free, open, and robust framework for caching and optimizing PHP intermediate code.


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

; ----- Options to use the apc.
;  The optimization level. Zero disables the optimizer, and higher values use more aggressive optimizations. Expect very modest speed improvements. This is experimental.
;apc.optimization = 0
;  On by default, but can be set to off and used in conjunction with positive apc.filters so that files are only cached if matched by a positive filter.
;apc.cache_by_default = 1
;  Use the SAPI request start time for TTL.
;apc.use_request_time = 1
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{include_path}/php/ext/%{pecl_name}/*



%changelog
* Fri Jan 17 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 3.1.13-1
- Create this file
