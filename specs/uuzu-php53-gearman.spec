%define pecl_name gearman
%define pecl_dir_name gearman

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	1.1.2
Release:	1%{?dist}
Summary:	PHP extension for libgearman wrapper

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

Requires:	libgearman
BuildRequires:	uuzu-php-cli,uuzu-php-devel,libgearman-devel

%description
This extension uses libgearman library to provide API for communicating with gearmand, and writing clients and workers.


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
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so



%changelog
* Sun Jan 26 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.1.2-1
- Create this file
