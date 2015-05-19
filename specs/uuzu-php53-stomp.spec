%define pecl_name stomp
%define pecl_dir_name stomp

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	1.0.5
Release:	1%{?dist}
Summary:	PHP extension for Stomp client

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

BuildRequires:	uuzu-php-cli,uuzu-php-devel

%description
This extension allows php applications to communicate with any Stomp compliant Message Brokers through easy object oriented and procedural interfaces.


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

; ----- Options to use the stomp.
;  The default broker URI to use when connecting to the message broker if no other URI is specified.
;stomp.default_broker = "tcp://localhost:61613"
;  The seconds part of the default connection timeout.
;stomp.default_connection_timeout_sec = 2
;  The microseconds part of the default connection timeout.
;stomp.default_connection_timeout_usec = 0
;  The seconds part of the default reading timeout.
;stomp.default_read_timeout_sec = 2
;  The microseconds part of the default reading timeout.
;stomp.default_read_timeout_usec = 0
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so



%changelog
* Mon Jan 20 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.0.5-1
- Create this file
