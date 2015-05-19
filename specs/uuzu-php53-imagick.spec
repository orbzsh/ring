%define pecl_name imagick
%define pecl_dir_name imagick

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	3.1.2
Release:	1%{?dist}
Summary:	PHP extension for ImageMagick library wrapper

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

Requires:	ImageMagick
BuildRequires:	uuzu-php-cli,uuzu-php-devel,ImageMagick-devel

%description
Imagick is a native php extension to create and modify images using the ImageMagick API.
This extension requires ImageMagick version 6.2.4+ and PHP 5.1.3+.
IMPORTANT: Version 2.x API is not compatible with earlier versions.


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

; ----- Options to use the imagick.
;  Fixes a drawing bug with locales that use ',' as float separators.
;imagick.locale_fix = FALSE
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{include_path}/php/ext/%{pecl_name}/*



%changelog
* Sun Jan 26 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 3.1.2-1
- Create this file
