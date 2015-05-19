%define pecl_name redis
%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	2.2.4
Release:	1%{?dist}
Summary:	PHP extension for interfacing with Redis

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

BuildRequires:	uuzu-php-cli,uuzu-php-devel

%description
This extension provides an API for communicating with Redis servers.


%prep
%setup -q -c -n %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
%{phpize}
./configure --with-php-config=/opt/uuzu/php/bin/php-config

make %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

%{__mkdir_p} %{buildroot}/opt/uuzu/php/conf/php.d
%{__cat} > %{buildroot}/opt/uuzu/php/conf/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the redis session handler
;  Use redis as a session handler
;session.save_handler = redis
;  session.save_path can have a simple host:port format too, but you need to provide the tcp:// scheme if you want to use the parameters.
;session.save_path = "tcp://host1:6379?weight=1, tcp://host2:6379?weight=2&timeout=2.5, tcp://host3:6379?weight=2"

EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so



%changelog
* Wed Jan 15 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 1.4.5-1
- Create this file
