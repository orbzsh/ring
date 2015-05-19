%define pecl_name oci8
%define pecl_dir_name oci8

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	2.0.8
Release:	1%{?dist}
Summary:	Extension for Oracle Database

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

Requires:	oracle-instantclient11.2-basic
BuildRequires:	uuzu-php-cli,uuzu-php-devel,oracle-instantclient11.2-devel

%description
Use the OCI8 extension to access Oracle Database. The extension can
be linked with Oracle client libraries from Oracle Database 10.2, 11,
or 12.1. These libraries are found in the database installation, or
in the free Oracle Instant Client available from Oracle. Oracle's
standard cross-version connectivity applies. For example, PHP OCI8
linked with Instant Client 11.2 can connect to Oracle Database 9.2
onward. See Oracle's note "Oracle Client / Server Interoperability
Support" (ID 207303.1) for details. PHP OCI8 2.0 can be built with
PHP 5.2 onward. Use the older PHP OCI8 1.4.10 when using PHP 4.3.9
through to PHP 5.1.x, or when only Oracle Database 9.2 client
libraries are available.


%prep
%setup -q -c -n %{pecl_dir_name}-%{version}


%build
cd %{pecl_dir_name}-%{version}
%{phpize}
./configure --with-php-config=/opt/uuzu/php/bin/php-config --with-oci8

make %{?_smp_mflags}


%install
cd %{pecl_dir_name}-%{version}
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

%{__mkdir_p} %{buildroot}/opt/uuzu/php/conf/php.d
%{__cat} > %{buildroot}/opt/uuzu/php/conf/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
;----defalut options
;oci8.connection_class = ""
;oci8.default_prefetch = "100"
;oci8.events = Off
;oci8.max_persistent = "-1"
;oci8.old_oci_close_semantics = Off
;oci8.persistent_timeout = "-1"
;oci8.ping_interval = "60"
;oci8.privileged_connect = Off
;oci8.statement_cache_size = "20"
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so



%changelog
* Fri May 16 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.0.8-1
- Create this file
- Build with oracle-instantclient11.2, not support oracle 12g
