%define pecl_name mongo
%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	1.4.5
Release:	1%{?dist}
Summary:	MongoDB database driver

Group:		Development/Languages
License:	Apache License
URL:		http://pecl.php.net/get/mongo-1.4.5.tgz
Source0:	mongo-1.4.5.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

BuildRequires:	uuzu-php-cli,uuzu-php-devel

%description
This package provides an interface for communicating with the MongoDB database in PHP.


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

; ----- Options to use the mongo

;mongo.allow_empty_keys=0
;mongo.allow_persistent=1
;mongo.chunk_size=262144
;mongo.cmd="$"
;mongo.default_host="localhost"
;mongo.default_port=27017
;mongo.is_master_interval=15
;mongo.long_as_object=0
;mongo.native_long=0
;mongo.ping_interval=5
;mongo.utf8=1
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
