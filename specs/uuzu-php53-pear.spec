%define srcname php
%define php_version 5.3.27
%define mysql_config /data/app/lib/mysql/mysql_config
%define install_root   /data/app
%define install_path   %{install_root}/%{srcname}-%{php_version}
%define init_dir      %{install_path}/init.d
%define include_path   %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path      %{install_path}/conf
%define bin_path       /opt/uuzu/php/bin
%define sbin_path       %{install_path}/sbin
%define php_tmp      %{install_path}/tmp
%define log_path       /opt/logs/php
%define session_path      %{log_path}/session



%global peardir %{install_path}/pear

%global xmlrpcver 1.5.1
%global getoptver 1.2.3
%global arctarver 1.3.3
%global structver 1.0.2
%global xmlutil   1.2.1

%define php_base uuzu-%{srcname}
%define basever 1.9
%define real_name php-pear
%define name %{php_base}-pear
Summary: PHP Extension and Application Repository framework
Name: %{name}
Version: 1.9.4
Release: 1%{?dist}
Epoch: 1
License: PHP
Group: Development/Languages
URL: http://pear.php.net/package/PEAR
Source0: http://download.pear.php.net/package/PEAR-%{version}.tgz
# wget http://cvs.php.net/viewvc.cgi/pear-core/install-pear.php?revision=1.39 -O install-pear.php
Source1: install-pear.php
Source2: relocate.php
Source3: strip.php
Source4: LICENSE
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source13: macros.pear
Source20: http://pear.php.net/get/XML_RPC-%{xmlrpcver}.tgz
Source21: http://pear.php.net/get/Archive_Tar-%{arctarver}.tgz
Source22: http://pear.php.net/get/Console_Getopt-%{getoptver}.tgz
Source23: http://pear.php.net/get/Structures_Graph-%{structver}.tgz
Source24: http://pear.php.net/get/XML_Util-%{xmlutil}.tgz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{php_base}-cli, %{php_base}-xml, gnupg
Provides: %{php_base}-pear(Console_Getopt) = %{getoptver}
Provides: %{php_base}-pear(Archive_Tar) = %{arctarver}
Provides: %{php_base}-pear(PEAR) = %{version}
Provides: %{php_base}-pear(Structures_Graph) = %{structver}
Provides: %{php_base}-pear(XML_RPC) = %{xmlrpcver}
Provides: %{php_base}-pear(XML_Util) = %{xmlutil}
Provides: %{php_base}-pear-XML-Util = %{xmlutil}-%{release}
Requires: %{php_base}-cli

# IUS Stuff
Provides: %{real_name} = %{version}
Conflicts: %{real_name} < %{basever}

# FIX ME: Should be removed before/after RHEL 5.6 is out
# See: https://bugs.launchpad.net/ius/+bug/691755


%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cT -n %{real_name}-%{version}

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}
do
    tar xzf  $archive --strip-components 1 || tar xzf  $archive --strip-path 1
done
tar xzf %{SOURCE24} package.xml
mv package.xml XML_Util.xml

# apply patches on used PEAR during install
# -- no patch

%build
# This is an empty build section.

%install
rm -rf $RPM_BUILD_ROOT

export PHP_PEAR_SYSCONF_DIR=%{conf_path}
export PHP_PEAR_SIG_KEYDIR=%{conf_path}/pearkeys
export PHP_PEAR_SIG_BIN=%{bin_path}/gpg
export PHP_PEAR_INSTALL_DIR=%{peardir}

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d $RPM_BUILD_ROOT%{peardir} \
           $RPM_BUILD_ROOT/opt/logs/php/php-pear \
           $RPM_BUILD_ROOT%{_localstatedir}/www/html \
           $RPM_BUILD_ROOT%{peardir}/.pkgxml \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm \
           $RPM_BUILD_ROOT%{conf_path}/pear

export INSTALL_ROOT=$RPM_BUILD_ROOT

%{bin_path}/php -n -dmemory_limit=32M -dshort_open_tag=0 -dsafe_mode=0 \
         -derror_reporting=E_ALL -ddetect_unicode=0 \
      %{SOURCE1} -d %{peardir} \
                 -c %{conf_path}/pear \
                 -b %{bin_path} \
                 -w %{_localstatedir}/www/html \
                 %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE20}

# Replace /usr/bin/* with simple scripts:
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{bin_path}/pear
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{bin_path}/pecl
install -m 755 %{SOURCE12} $RPM_BUILD_ROOT%{bin_path}/peardev

# Sanitize the pear.conf
%{bin_path}/php -n %{SOURCE2} $RPM_BUILD_ROOT%{conf_path}/pear.conf $RPM_BUILD_ROOT | 
  %{bin_path}/php -n %{SOURCE2} php://stdin $PWD > new-pear.conf
%{bin_path}/php -n %{SOURCE3} new-pear.conf ext_dir |
  %{bin_path}/php -n %{SOURCE3} php://stdin http_proxy > $RPM_BUILD_ROOT%{conf_path}/pear.conf

%{bin_path}/php -r "print_r(unserialize(substr(file_get_contents('$RPM_BUILD_ROOT%{conf_path}/pear.conf'),17)));"

install -m 644 -c %{SOURCE4} LICENSE

install -m 644 -c %{SOURCE13} \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.pear     

# apply patches on installed PEAR tree
pushd $RPM_BUILD_ROOT%{peardir} 
# -- no patch
popd

# Why this file here ?
rm -rf $RPM_BUILD_ROOT/.depdb* $RPM_BUILD_ROOT/.lock $RPM_BUILD_ROOT/.channels $RPM_BUILD_ROOT/.filemap

# Need for re-registrying XML_Util
install -m 644 XML_Util.xml $RPM_BUILD_ROOT%{peardir}/.pkgxml/

#modfiy php path
sed -i 's:/usr/bin:/opt/uuzu/php/bin:' $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.pear $RPM_BUILD_ROOT%{bin_path}/pear $RPM_BUILD_ROOT%{bin_path}/pecl $RPM_BUILD_ROOT%{bin_path}/peardev
sed -i 's:/usr/share:/opt/uuzu/php:' $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.pear $RPM_BUILD_ROOT%{bin_path}/pear $RPM_BUILD_ROOT%{bin_path}/pecl $RPM_BUILD_ROOT%{bin_path}/peardev

%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{conf_path}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{conf_path}/pear.conf && exit 1
grep '"/tmp"' $RPM_BUILD_ROOT%{conf_path}/pear.conf && exit 1
grep /usr/local $RPM_BUILD_ROOT%{conf_path}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1


%clean
rm -rf $RPM_BUILD_ROOT
rm new-pear.conf


%triggerpostun -- php-pear-XML-Util
# re-register extension unregistered during postun of obsoleted php-pear-XML-Util
%{bin_path}/pear install --nodeps --soft --force --register-only %{pear_xmldir}/XML_Util.xml >/dev/null || :


%files
%defattr(-,root,root,-)
%{peardir}
%{bin_path}/*
%config(noreplace) %{conf_path}/pear.conf
%config %{_sysconfdir}/rpm/macros.pear
%dir /opt/logs/php/php-pear
%dir %{conf_path}/pear
%doc LICENSE README


%changelog
