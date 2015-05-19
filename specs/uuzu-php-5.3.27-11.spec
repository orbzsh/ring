
%{!?lsb_release: %global lsb_release %(lsb_release -r | awk {' print $2 '})}
%global rhel_point_release %(echo %{lsb_release} | awk -F . {' print $2 '})

%global contentdir /data/html
# API/ABI Check
%global apiver 20090626
%global zendver 20090626
%global pdover 20080721
# Extension version
%global fileinfover 1.0.5-dev
%global pharver     2.0.1
%global zipver      1.11.0
%global jsonver     1.2.1

%global httpd_mmn %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%define srcname php
%define mysql_config   /data/app/mysql/bin/mysql_config
%define mysql_sock   %(/data/app/mysql/bin/mysql_config --socket || echo /var/lib/mysql/mysql.sock)
%define install_root   /data/app
%define install_path   %{install_root}/%{srcname}
%define init_dir      %{install_path}/init.d
%define include_path   %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path      %{install_path}/conf
%define bin_path       %{install_path}/bin
%define sbin_path       %{install_path}/sbin
%define php_tmp      %{install_path}/tmp
%define log_path       /data/logs/php
%define session_path      %{log_path}/session
#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}
%define _unpackaged_files_terminate_build 0

# enabled optional build options
%global _with_milter        1
%global _with_embedded  	1
%global _with_zts       	1
%global _with_litespeed     1

# disabled optional build options
%define _with_oci8        0
# %%define _with_interbase   1

# fpm requires a later version of libevent
%if (0%{?rhel} >= 5 && 0%{?rhel_point_release} >= 5)
%global _with_fpm       1
%endif

# fpm should be enabled on EL6
%if (0%{?rhel} >= 6)
%global _with_fpm       1
%endif

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

%if 0%{?_with_oci8}
%global instantclient_ver 11.2
%endif

%global real_name php
%global name uuzu-php
%global base_ver 5.3

Summary: The PHP HTML-embedded scripting language. (PHP: Hypertext Preprocessor)
Name: %{name}
Version: 5.3.27
Release: 11%{?dist}
License: The PHP License v3.01
Group: Development/Languages
Vendor: zhuhuipeng@uuzu-inc.com
URL: http://www.php.net/

Source0: http://www.php.net/distributions/%{real_name}-%{version}.tar.gz
Source1: php.conf
Source2: php53-ius.ini
Source3: macros.php
Source4: php-fpm.conf
Source6: php-fpm-app.init
Source7: php-fpm.logrotate
Source8: fpm-default.conf
Source9: php-fpm-app.conf

# Ported from Fedora/Redhat
# Build fixes
Patch1: php-5.3.3-gnusrc.patch
Patch2: php-5.3.0-install.patch
Patch3: php-5.2.4-norpath.patch
Patch4: php-5.3.0-phpize64.patch
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
#Patch8: php-5.3.3-aconf26x.patch
Patch9: php-5.3.14-aconf259.patch
Patch10: php-5.3.14-autoconf-milter.patch

# Fixes for extension modules
Patch20: php-4.3.11-shutdown.patch
Patch21: php-5.3.3-macropen.patch

# Functional changes
Patch40: php-5.0.4-dlopen.patch
Patch41: php-5.3.0-easter.patch
Patch42: php-5.3.1-systzdata-v7.patch

# Security patch from upstream SVN
# http://svn.php.net/viewvc?view=revision&revision=306154
#Patch50: php-5.3.4-bug53512.patch

# Fixes for tests
Patch61: php-5.0.4-tests-wddx.patch

# IUS Patches
Patch302: php-5.3.0-oci8-lib64.patch
#Patch316: php-5.3.4-bug53632.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, expat-devel
BuildRequires: gmp-devel, aspell-devel >= 0.50.0
BuildRequires: httpd-devel >= 2.0.46-1, uuzu-libjpeg-devel, uuzu-libpng-devel, pam-devel
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.0.0
BuildRequires: zlib, zlib-devel, smtpdaemon, libedit-devel
BuildRequires: bzip2, fileutils, file >= 3.39, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: apr-devel, elfutils-libelf-devel, apr-util-devel
BuildRequires: t1lib-devel
BuildRequires: libtool-ltdl-devel, e2fsprogs-devel
BuildRequires: redhat-lsb

%if 0%{?_with_milter}
BuildRequires: sendmail-devel
%endif

# Enforce Apache module ABI compatibility
Requires: httpd-mmn = %{httpd_mmn} 
Requires: file >= 3.39
Requires: libxslt >= 1.1.11 
Requires: %{name}-common = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{name}-cli = %{version}-%{release}
#Requires: %{name}-pear >= 1:1.8
Requires: t1lib
Requires: libtool-ltdl
Requires: libedit

Provides: mod_php = %{version}-%{release}
Provides: mod_%{name} = %{version}-%{release}
Provides: %{real_name} = %{version}-%{release}
Provides: uuzu-php = %{version}-%{release}

Conflicts: %{real_name} < %{base_ver}
Conflicts: php51, php52
Autoreq: no

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-cli = %{version}-%{release}
Provides: uuzu-php-cli = %{version}-%{release}
Provides: %{name}-cgi = %{version}-%{release}, %{real_name}-cgi = %{version}-%{release}
Provides: uuzu-php-cgi = %{version}-%{release}
Provides: %{name}-pcntl, %{name}-readline, %{name}-pcntl 
Provides: uuzu-php-pcntl, php53-readline, php53-pcntl 


%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.

%package common
Group: Development/Languages
Summary: Common files for PHP
Provides: %{real_name}-common = %{version}-%{release}
Provides: uuzu-php-common = %{version}-%{release}
Provides: %{name}-api = %{apiver}, %{name}-zend-abi = %{zendver}
Provides: %{real_name}-api = %{apiver}, %{real_name}-zend-abi = %{zendver}
Provides: uuzu-php-api = %{apiver}, php53-zend-abi = %{zendver}
Provides: %{name}(api) = %{apiver}, %{name}(zend-abi) = %{zendver}
Provides: %{real_name}(api) = %{apiver}, %{real_name}(zend-abi) = %{zendver}
Provides: uuzu-php(api) = %{apiver}, php53(zend-abi) = %{zendver}

# Provides for all builtin modules for php5x:
Provides: %{name}-bz2, %{name}-calendar, %{name}-ctype, %{name}-curl
Provides: %{name}-date, %{name}-exif, %{name}-ftp, %{name}-gettext
Provides: %{name}-gmp, %{name}-hash, %{name}-iconv, %{name}-libxml
Provides: %{name}-openssl, %{name}-pcre, %{name}-posix
Provides: %{name}-reflection, %{name}-session, %{name}-shmop 
Provides: %{name}-simplexml, %{name}-sockets, %{name}-spl, %{name}-sysvsem
Provides: %{name}-sysvshm, %{name}-sysvmsg, %{name}-tokenizer, %{name}-wddx
Provides: %{name}-zlib, %{name}-json, %{name}-zip
Provides: %{name}-sqlite3
Provides: %{name}-fileinfo

# add for php
Provides: %{real_name}-bz2, %{real_name}-calendar, %{real_name}-ctype
Provides: %{real_name}-curl, %{real_name}-date, %{real_name}-exif 
Provides: %{real_name}-ftp, %{real_name}-gettext, %{real_name}-gmp
Provides: %{real_name}-hash, %{real_name}-iconv, %{real_name}-libxml
Provides: %{real_name}-openssl, %{real_name}-pcre, 
Provides: %{real_name}-posix, %{real_name}-reflection
Provides: %{real_name}-session, %{real_name}-shmop, %{real_name}-simplexml
Provides: %{real_name}-sockets, %{real_name}-spl, %{real_name}-sysvsem
Provides: %{real_name}-sysvshm, %{real_name}-sysvmsg, %{real_name}-tokenizer
Provides: %{real_name}-wddx, %{real_name}-zlib, %{real_name}-json
Provides: %{real_name}-zip
Provides: %{real_name}-sqlite3
Provides: %{real_name}-fileinfo

# add for packages expecting php53 from RHEL
Provides: uuzu-php-bz2, php53-calendar, php53-ctype
Provides: uuzu-php-curl, php53-date, php53-exif
Provides: uuzu-php-ftp, php53-gettext, php53-gmp
Provides: uuzu-php-hash, php53-iconv, php53-libxml
Provides: uuzu-php-openssl, php53-pcre,
Provides: uuzu-php-posix, php53-reflection
Provides: uuzu-php-session, php53-shmop, php53-simplexml
Provides: uuzu-php-sockets, php53-spl, php53-sysvsem
Provides: uuzu-php-sysvshm, php53-sysvmsg, php53-tokenizer
Provides: uuzu-php-wddx, php53-zlib, php53-json
Provides: uuzu-php-zip
Provides: uuzu-php-sqlite3

Obsoletes: %{name}-pecl-zip, %{name}-pecl-json, %{name}-json, %{name}-pecl-phar, %{name}-pecl-Fileinfo

# For obsoleted pecl extension - php and php5x
Provides: %{name}-pecl-json = %{jsonver}, %{name}-pecl(json) = %{jsonver}
Provides: %{name}-pecl-zip = %{zipver}, %{name}-pecl(zip) = %{zipver}
Provides: %{name}-pecl-phar = %{pharver}, %{name}-pecl(phar) = %{pharver}
Provides: %{name}-pecl-Fileinfo = %{fileinfover}, %{name}-pecl(Fileinfo) = %{fileinfover}

Provides: %{real_name}-pecl-json = %{jsonver}, %{real_name}-pecl(json) = %{jsonver}
Provides: %{real_name}-pecl-zip = %{zipver}, %{real_name}-pecl(zip) = %{zipver}
Provides: %{real_name}-pecl-phar = %{pharver}, %{real_name}-pecl(phar) = %{pharver}
Provides: %{real_name}-pecl-Fileinfo = %{fileinfover}, %{real_name}-pecl(Fileinfo) = %{fileinfover}

Provides: uuzu-php-pecl-json = %{jsonver}, php53-pecl(json) = %{jsonver}
Provides: uuzu-php-pecl-zip = %{zipver}, php53-pecl(zip) = %{zipver}
Provides: uuzu-php-pecl-phar = %{pharver}, php53-pecl(phar) = %{pharver}
Provides: uuzu-php-pecl-Fileinfo = %{fileinfover}, php53-pecl(Fileinfo) = %{fileinfover}

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions.

Requires: %{name} = %{version}-%{release}, autoconf, automake
Provides: %{real_name}-devel = %{version}-%{release}
Provides: uuzu-php-devel = %{version}-%{release}

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-imap = %{version}-%{release}
Provides: uuzu-php-imap = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel
BuildRequires: libc-client-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Summary: A module for PHP applications that use LDAP.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-ldap = %{version}-%{release}
Provides: uuzu-php-ldap = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
#Requires: oracle-instantclient11.2-basic
#Buildrequires: oracle-instantclient11.2-devel
Provides: %{real_name}-pdo = %{version}-%{release}
Provides: uuzu-php-pdo = %{version}-%{release}
Provides: %{name}-pdo-abi = %{pdover}
Provides: %{real_name}-pdo-abi = %{pdover}
Provides: %{real_name}-pdo_sqlite = %{pdover}
Provides: uuzu-php-pdo-abi = %{pdover}
Provides: uuzu-php-pdo_sqlite = %{pdover}
Provides: uuzu-php-pdo_oci = %{pdover}
Autoreq: no

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%package sqlite
Summary: A module for PHP applications that use MySQL databases.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-sqlite = %{version}-%{release}
Provides: uuzu-php-sqlite = %{version}-%{release}
Provides: uuzu-php-sqlite

%description sqlite
The php-sqlite package contains a dynamic shared object that will add
Sqlite database support to PHP.

%package mysql
Summary: A module for PHP applications that use MySQL databases.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-mysql = %{version}-%{release}
Provides: uuzu-php-mysql = %{version}-%{release}
Provides: php_database, %{name}-mysqli, %{real_name}-mysqli
Provides: uuzu-php-mysqli
BuildRequires: uuzu-mysql-devel >= 5.0.45
Conflicts: %{name}-mysqlnd


%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
Provides: %{name}-mysqlnd = %{version}-%{release}
Provides: %{real_name}-mysqlnd = %{version}-%{release}
Requires: %{name}-pdo = %{version}-%{release}
Provides: %{name}_database
Provides: %{name}-mysql = %{version}-%{release}
Provides: %{name}-mysql = %{version}-%{release}
Provides: %{name}-mysqli = %{version}-%{release}
Provides: %{name}-mysqli = %{version}-%{release}
Provides: %{name}-pdo_mysql, %{name}-pdo_mysql
Provides: %{real_name}_database
Provides: %{real_name}-mysql = %{version}-%{release}
Provides: %{real_name}-mysql = %{version}-%{release}
Provides: %{real_name}-mysqli = %{version}-%{release}
Provides: %{real_name}-mysqli = %{version}-%{release}
Provides: %{real_name}-pdo_mysql, %{real_name}-pdo_mysql

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-pgsql = %{version}-%{release}
Provides: uuzu-php-pgsql = %{version}-%{release}
Provides: php_database
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package odbc
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-odbc = %{version}-%{release}
Provides: uuzu-php-odbc = %{version}-%{release}
Summary: A module for PHP applications that use ODBC databases.
Provides: php_database
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, libxml2 >= 2.6.16
Provides: %{real_name}-soap = %{version}-%{release}
Provides: uuzu-php-soap = %{version}-%{release}
Summary: A module for PHP applications that use the SOAP protocol
BuildRequires: libxml2-devel >= 2.6.16

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, net-snmp >= 5.1
Provides: %{real_name}-snmp = %{version}-%{release}
Provides: uuzu-php-snmp = %{version}-%{release}
BuildRequires: net-snmp-devel >= 5.1

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, libxml2 >= 2.6.16, 
Requires: libxslt >= 1.1.11
Provides: %{real_name}-xml = %{version}-%{release}
Provides: uuzu-php-xml = %{version}-%{release}
Provides: %{name}-dom, %{name}-xsl, %{name}-domxml
Provides: %{real_name}-dom, %{real_name}-xsl, %{real_name}-domxml
Provides: uuzu-php-dom, php53-xsl, php53-domxml
BuildRequires: libxslt-devel >= 1.1.11, libxml2-devel >= 2.6.16

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Requires: uuzu-php-common = %{version}-%{release}
Provides: %{name}-xmlrpc = %{version}-%{release}
BuildRequires: expat-devel

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-mbstring = %{version}-%{release}
Provides: uuzu-php-mbstring = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-gd = %{version}-%{release}
Provides: uuzu-php-gd = %{version}-%{release}
BuildRequires: uuzu-gd-devel, freetype-devel

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

This package is built against t1lib adding Postscript Type 1 font support 
to PHP/GD.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-bcmath = %{version}-%{release}
Provides: uuzu-php-bcmath = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-dba = %{version}-%{release}
Provides: uuzu-php-dba = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%if 0%{?_with_litespeed:1}
%package litespeed
Summary: API for the Litespeed web server
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-litespeed = %{version}-%{release}
Provides: uuzu-php-litespeed = %{version}-%{release}

%description litespeed
The php-litespeed package contains the binary used by the Litespeed web server.
%endif

%package tidy
Summary: Utility to clean up and pretty print HTML/XHTML/XML
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-tidy = %{version}-%{release}
Provides: uuzu-php-tidy = %{version}-%{release}
Requires: libtidy
BuildRequires: libtidy, libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using libtidy to PHP.

%package mcrypt
Summary: A module for PHP applications that use Mcrypt.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, libmcrypt
Provides: %{real_name}-mcrypt = %{version}-%{release}
Provides: uuzu-php-mcrypt = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package is a dynamic shared object (DSO) for the Apache
Web server that adds Mcrypt support to PHP.

%package mssql
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, freetds >= 0.64
Requires: %{name}-pdo = %{version}-%{release}
Provides: %{real_name}-mssql = %{version}-%{release}
Provides: uuzu-php-mssql = %{version}-%{release}
Summary: A module for PHP applications that use MSSQL databases.
Provides: %{name}_database
BuildRequires: freetds-devel >= 0.64

%description mssql
The mssql package contains a dynamic shared object that will add
support for accessing MSSQL databases to PHP.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-pspell = %{version}-%{release}
Provides: uuzu-php-pspell = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-recode = %{version}-%{release}
Provides: uuzu-php-recode = %{version}-%{release}
Requires: recode
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-intl = %{version}-%{release}
Provides: uuzu-php-intl = %{version}-%{release}
BuildRequires: libicu-devel >= 3.6

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Human Language and Character Encoding Support
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-enchant = %{version}-%{release}
Provides: uuzu-php-enchant = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-intl package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-process = %{version}-%{release}
Provides: uuzu-php-process = %{version}-%{release}
Provides: %{name}-posix, %{name}-sysvsem, %{name}-sysvshm, %{name}-sysvmsg
Provides: %{real_name}-posix, %{real_name}-sysvsem, %{real_name}-sysvshm, %{real_name}-sysvmsg
Provides: uuzu-php-posix, php53-sysvsem, php53-sysvshm, php53-sysvmsg

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

# Optional module support

%if 0%{?_with_fpm}
%package fpm
Summary: Alternative PHP FastCGI implementation
Group: Development/Languages
Provides: %{real_name}-fpm = %{version}-%{release}
Provides: uuzu-php-fpm = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
BuildRequires: uuzu-libevent-devel >= 1.4.11

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI 
implementation with some additional features useful for sites 
of any size, especially busier sites.

%endif

%if 0%{?_with_milter}
%package milter
Group: Development/Languages
Summary: Milter SAPI interface for PHP
Requires: %{name}-common = %{version}-%{release}
Provides: uuzu-php-miter = %{version}-%{release}
Provides: %{real_name}-milter = %{version}-%{release}
BuildRequires: sendmail-devel

%description milter
The php-milter package contains the milter SAPI interface,
which can be used to write milter plugins using PHP.
%endif

%if 0%{?_with_embedded}
%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: %{name}-embedded-devel = %{version}-%{release}
Provides: %{real_name}-embedded = %{version}-%{release}
Provides: uuzu-php-embedded = %{version}-%{release}
Provides: %{real_name}-embedded-devel = %{version}-%{release}
Provides: uuzu-php-embedded-devel = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.
%endif

%if 0%{?_with_interbase}
%package interbase
Summary:        A module for PHP applications that use Interbase/Firebird databases
Group:          Development/Languages
BuildRequires:  firebird-devel
Requires:       %{name}-common = %{version}-%{release}, %{name}-pdo
Provides:       %{name}_database, %{name}-firebird, %{name}-pdo_firebird
Provides:       %{real_name}_database, %{real_name}-firebird, %{real_name}-pdo_firebird
Provides:       php53_database, php53-firebird, php53-pdo_firebird

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%if 0%{?_with_oci8}
%package oci8
Summary: A module for PHP applications that connect to Oracle.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-oci8 = %{version}-%{release}
Provides: uuzu-php-oci8 = %{version}-%{release}
Requires: oracle-instantclient-basic >= %{instantclient_ver}
BuildRequires: oracle-instantclient-basic >= %{instantclient_ver}
BuildRequires: oracle-instantclient-devel >= %{instantclient_ver}

%description oci8 
The php-oci8 package is a dynamic shared object (DSO) for the Apache
Web server that adds Oracle support to PHP.
%endif

%if 0%{?_with_zts:1}
%package zts
Group: Development/Languages
Summary: Thread-safe PHP interpreter for use with the Apache HTTP Server
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-zts = %{version}-%{release}
Provides: uuzu-php-zts = %{version}-%{release}
Requires: httpd-mmn = %{httpd_mmn}
BuildRequires: libtool-ltdl-devel

%description zts
The php-zts package contains a module for use with the Apache HTTP
Server which can operate under a threaded server processing model.
%endif


%prep
%setup -q -n %{real_name}-%{version} 


%patch1 -p1 -F-1 -b .gnusrc
%patch2 -p1 -F-1 -b .install
%patch3 -p1 -F-1 -b .norpath
%patch4 -p1 -F-1 -b .phpize64
%patch5 -p1 -F-1 -b .includedir
%patch6 -p1 -F-1 -b .embed
%patch7 -p1 -F-1 -b .recode
%patch9 -p1 -F-1 -b .aconf259
%patch10 -p1 -F-1 -b .milter

%patch20 -p1 -F-1 -b .shutdown
%patch21 -p1 -F-1 -b .macropen

%patch40 -p1 -F-1 -b .dlopen
%patch41 -p1 -F-1 -b .easter
%patch42 -p1 -F-1 -b .systzdata

#%patch50 -p4 -b .bug53512
%patch61 -p1 -F-1 -b .tests-wddx

%patch302 -p1 -F-1 -b .oci8-lib64
#%patch316 -p1 -b .bug53632

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/gd/libgd/README gd_README
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT

# Multiple builds for multiple SAPIs 
mkdir build-cgi build-apache build-milter build-embedded build-zts build-litespeed 
%if 0%{?_with_fpm}
mkdir build-fpm
%endif

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt

# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/iconv/tests/bug16069.phpt

# Safety check for API version change.
vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi

%build
%if 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:                                                         
libtoolize --force --copy                                                              
%if 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4                             
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{lib_path}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.

build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
./configure \
	--prefix=%{install_root} \
	--bindir=%{bin_path} \
	--sbindir=%{sbin_path} \
	--libdir=%{lib_path} \
	--includedir=%{include_path} \
        --cache-file=../config.cache \
        --with-libdir=%{_lib} \
        --with-config-file-path=%{conf_path} \
        --with-config-file-scan-dir=%{conf_path}/php.d \
        --disable-debug \
        --with-pic \
        --disable-rpath \
        --without-pear \
        --with-bz2 \
        --with-exec-dir=%{bin_path} \
        --with-freetype-dir=%{_libdir} \
        --with-png-dir=%{install_root} \
        --with-xpm-dir=%{_prefix} \
        --enable-gd-native-ttf \
        --with-t1lib=%{_prefix} \
        --without-gdbm \
        --with-gettext \
        --with-gmp \
        --with-iconv \
        --with-jpeg-dir=%{install_root} \
        --with-openssl \
        --with-pcre-regex \
        --with-zlib \
        --with-layout=GNU \
        --enable-exif \
        --enable-ftp \
        --enable-magic-quotes \
        --enable-sockets \
        --enable-sysvsem --enable-sysvshm --enable-sysvmsg \
        --with-kerberos \
        --enable-ucd-snmp-hack \
        --enable-shmop \
        --enable-calendar \
        --without-mime-magic \
        --without-sqlite \
        --with-libxml-dir=%{_prefix} \
        --with-xml \
        --with-system-tzdata \
        --with-mhash \
        $* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi
build --enable-force-cgi-redirect \
      --enable-pcntl \
      --enable-shared=yes \
      --enable-mysqlnd=shared \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-sqlite=shared \
      --with-ldap=shared --with-ldap-sasl \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-fastcgi \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --enable-json=shared \
      --enable-zip=shared \
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
      %{?_with_interbase:--with-interbase=shared,%{_libdir}/firebird} \
      %{?_with_interbase:--with-pdo-firebird=shared,%{_libdir}/firebird} \
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-xmlreader --disable-xmlwriter \
      --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_sbindir}/apxs \
      --libdir=%{lib_path} \
      --with-sqlite=shared \
      --with-mysql=shared,%{install_root} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --with-pdo-sqlite=shared,%{_prefix} \
      ${without_shared}
popd

%if 0%{?_with_fpm}
#build fpm
pushd build-fpm
build --enable-fpm \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

%if 0%{?_with_milter:1}
# Build milter SAPI
# /usr/lib[64]/libphp5.so
pushd build-milter
build --with-milter \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

%if 0%{?_with_embedded:1}
# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

%if 0%{?_with_litespeed:1}
# Build litespeed module
pushd build-litespeed
build --with-litespeed \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd
%endif

%if 0%{?_with_zts:1}
# Build a special thread-safe Apache SAPI
pushd build-zts
EXTENSION_DIR=%{_libdir}/php/modules-zts
build --with-apxs2=%{_sbindir}/apxs ${without_shared} \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --disable-pdo \
      --without-mysql
popd
%endif

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.

%check
%if %runselftest
cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in `find .. -name \*.diff -type f -print`; do
    echo "TEST FAILURE: $f --"
    cat "$f"
    echo "-- $f result ends."
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#create dirs
mkdir -p %{buildroot}%{install_root}
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{init_dir}
mkdir -p %{buildroot}%{include_path}
mkdir -p %{buildroot}%{lib_path}
mkdir -p %{buildroot}%{logrotate_dir}
mkdir -p %{buildroot}%{conf_path}/php.d
mkdir -p %{buildroot}%{bin_path}
mkdir -p %{buildroot}%{sbin_path}
mkdir -p %{buildroot}%{php_tmp}
mkdir -p %{buildroot}%{log_path}
mkdir -p %{buildroot}%{session_path}
mkdir -p %{buildroot}%{conf_path}/fpm-mod

%if 0%{?_with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm INSTALL_ROOT=%{buildroot}
%endif

# Install the version for milter SAPI
%if 0%{?_with_milter}
make -C build-milter install-sapi install-headers INSTALL_ROOT=%{buildroot}
%endif

# Install the version for embedded script language in applications + php_embed.h
%if 0%{?_with_embedded}
make -C build-embedded install-sapi install-headers INSTALL_ROOT=%{buildroot}
%endif

# Install everything from the CGI SAPI build
pushd build-cgi
make install INSTALL_ROOT=%{buildroot} 
popd
mv $RPM_BUILD_ROOT%{lib_path}/php/modules/mysql.so $RPM_BUILD_ROOT%{lib_path}/php/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{lib_path}/php/modules/mysqli.so $RPM_BUILD_ROOT%{lib_path}/php/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{lib_path}/php/modules/pdo_mysql.so $RPM_BUILD_ROOT%{lib_path}/php/modules/pdo_mysqlnd.so



# Install the Apache module
#pushd build-apache
#make install-sapi INSTALL_ROOT=%{buildroot}
#popd
make -C build-apache install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d %{buildroot}%{_sysconfdir}/
install -m 644 %{SOURCE2} %{buildroot}%{conf_path}/php.ini
install -m 755 -d %{buildroot}%{contentdir}/icons
install -m 644 *.gif %{buildroot}%{contentdir}/icons/


# Use correct libdir
sed -i -e 's|%{_prefix}/lib|%{lib_path}|' %{buildroot}%{conf_path}/php.ini

# install the DSO to system apache
install -m 755 -d %{buildroot}%{_libdir}/httpd/modules
install -m 755 build-apache/libs/libphp5.so %{buildroot}%{_libdir}/httpd/modules

%if 0%{?_with_zts:1}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp5.so %{buildroot}%{_libdir}/httpd/modules/libphp5-zts.so
%endif

%if 0%{?_with_litespeed:1}
# install the php litespeed binary
install -m 755 build-litespeed/sapi/litespeed/php %{buildroot}%{bin_path}/php-ls
%endif

# Apache config fragment
mkdir -p %{buildroot}/etc/httpd/conf.d 
install -m 755 -d %{buildroot}/etc/httpd/conf.d
install -m 644 %{SOURCE1} %{buildroot}/etc/httpd/conf.d

#install -m 755 -d %{buildroot}%{_sysconfdir}/php.d
#install -m 755 -d %{buildroot}%{_localstatedir}/lib/php
#install -m 700 -d %{buildroot}%{_localstatedir}/lib/php/session

%if 0%{?_with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d %{buildroot}%{log_path}
install -m 755 -d %{buildroot}%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d %{buildroot}%{conf_path}/php-fpm.d
install -m 644 %{SOURCE4} %{buildroot}%{conf_path}/php-fpm.conf
install -m 644 %{SOURCE9} %{buildroot}%{conf_path}/php-fpm.d/app.conf
#mv %{buildroot}%{conf_path}/php-fpm.conf.default .
# Service
install -m 755 -d %{buildroot}%{init_dir}
install -m 755 %{SOURCE6} %{buildroot}%{init_dir}/
# LogRotate
install -m 755 -d %{buildroot}%{logrotate_dir}
install -m 644 %{SOURCE7} %{buildroot}%{logrotate_dir}/php-fpm
# fpm-mod
install -m 755 -d %{buildroot}%{conf_path}/fpm-mod
install -m 644 %{SOURCE8} %{buildroot}%{conf_path}/fpm-mod/default.conf
%endif

# Generate files lists and stub .ini files for each subpackage
for mod in sqlite pgsql mysql mysqli odbc ldap snmp xmlrpc imap \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    pdo pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite json zip \
    enchant phar mcrypt mssql tidy fileinfo intl \
    pdo_dblib pspell curl wddx posix sysvshm sysvsem sysvmsg \
    recode mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd\
    %{?_with_interbase:interbase pdo_firebird} %{?_with_oci8:oci8} tidy ; do
    cat > %{buildroot}%{conf_path}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{lib_path}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{conf_path}/php.d/${mod}.ini
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
cat files.mysqli >> files.mysql

#mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_mysql >> files.mysql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if 0%{?_with_interbase}
cat files.pdo_firebird >> files.interbase
%endif

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
#cat files.pdo_oci >> files.pdo

# Package json and zip in -common.
cat files.json files.zip files.curl files.phar files.fileinfo > files.common

# Install the macros file:
install -d %{buildroot}%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}/;s/@PHP_ZENDVER@/%{zendver}/;s/@PHP_PDOVER@/%{pdover}/" \
    < %{SOURCE3} > macros.php
install -m 644 -c macros.php \
           %{buildroot}%{_sysconfdir}/rpm/macros.php


# Remove unpackaged files
rm -rf %{buildroot}%{lib_path}/php/modules/*.a \
       %{buildroot}%{bin_path}/{phptar} \
       %{buildroot}%{_datadir}/pear \
       %{buildroot}%{lib_path}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}
rm -rf %{buildroot}%{_sysconfdir}/php*
rm -rf %{buildroot}%{_prefix}/etc

# Fix the link
(cd %{buildroot}%{bin_path}; ln -sfn phar.phar phar)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
rm files.* macros.php

%if 0%{?_with_milter}

%pre

%post
if [ -h "/data/app/%{srcname}" ]; then
    rm -f /data/app/%{srcname}
fi
if [ ! -e "/data/app/bin/%{srcname}" ]; then
    ln -sf /data/app/%{srcname} /data/app/bin/%{srcname}
fi

%post milter -p /sbin/ldconfig
%postun milter -p /sbin/ldconfig
%endif

%if 0%{?_with_embedded}
%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig
%endif

%if 0%{?_with_fpm}
%pre fpm
useradd -M -d /home/httpd/html -s /sbin/nologin app > /dev/null 2>&1
useradd -M -d /home/httpd -s /sbin/nologin test > /dev/null 2>&1

%post fpm
ln -sf %{logrotate_dir}/php-fpm %{_sysconfdir}/logrotate.d/php-fpm
ln -sf %{init_dir}/php-fpm-app.init %{_sysconfdir}/init.d/php-fpm-app
/sbin/chkconfig --add php-fpm-app

%preun fpm
if [ "$1" = 0 ] ; then
#    /sbin/service php-fpm stop >/dev/null 2>&1
#    /sbin/chkconfig --del php-fpm
    :
fi
rm -f %{_sysconfdir}/logrotate.d/php-fpm
rm -f %{_sysconfdir}/php-fpm-app
%endif


%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5.so
%attr(0755,root,app) %dir %{session_path}
%config %{_sysconfdir}/httpd/conf.d/php.conf
%{contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE 
%config(noreplace) %{conf_path}/php.ini
%dir %{conf_path}/php.d
%dir %{lib_path}/php
%dir %{lib_path}/php/modules
%dir %{log_path}
%dir %{session_path}

%files cli
%defattr(-,root,root)
%doc sapi/cgi/README* sapi/cli/README
%{bin_path}/php
%{bin_path}/phar*
%{bin_path}/php-cgi
#%{_mandir}/man1/php.1*
# provides phpize here (not in -devel) for pecl command
%{bin_path}/phpize
#%{_mandir}/man1/phpize.1*

%files devel
%defattr(-,root,root)
%{bin_path}/php-config
%{include_path}/php
%{lib_path}/php/build
#%{_mandir}/man1/php-config.1*
%config %{_sysconfdir}/rpm/macros.php

%if 0%{?_with_fpm}
%files fpm
%defattr(-,root,root)
%config(noreplace) %{conf_path}/php-fpm.conf
%config(noreplace) %{conf_path}/php-fpm.d/app.conf
%config(noreplace) %{logrotate_dir}/php-fpm
%config(noreplace) %{conf_path}/fpm-mod/default.conf
%{sbin_path}/php-fpm
%{init_dir}/php-fpm-app.init
%dir %{conf_path}/php-fpm.d
# log owned by apache for log
%attr(755,app,app) %dir %{log_path}
%dir %{_localstatedir}/run/php-fpm
#%{_mandir}/man8/php-fpm.8.gz
#%{_datadir}/fpm/status.html
%endif

%files pgsql -f files.pgsql
%files mysql -f files.mysql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%files gd -f files.gd
%doc gd_README
%files soap -f files.soap
%files bcmath -f files.bcmath
%files dba -f files.dba
%files pdo -f files.pdo
%files tidy -f files.tidy
%files mcrypt -f files.mcrypt
%files mssql -f files.mssql
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files sqlite -f files.sqlite

# Files for conditional Module Support
%if 0%{?_with_oci8}
%files oci8 -f files.oci8
%endif

%if 0%{?_with_zts}
%files zts
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5-zts.so
%endif

%if 0%{?_with_litespeed}
%files litespeed
%defattr(-,root,root)
%{bin_path}/php-ls
%endif

%if 0%{?_with_milter}
%files milter
%defattr(-,root,root)
%{bin_path}/php-milter
%endif

%if 0%{?_with_embedded}
%files embedded
%defattr(-,root,root,-)
%{lib_path}/libphp5.so
%{lib_path}/libphp5-%{version}.so
%endif

%if 0%{?_with_interbase}
%defattr(-,root,root,-)
%files interbase -f files.interbase
%endif

%changelog
* Thu Dec 11 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-11
- Fix bug: pid file to app-php-fpm.pid
* Thu Dec 11 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-10
- Fix logs dir owner to app.
* Thu Dec 11 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-9
- Change appid to app.
- Add backup before post.
* Wed Jul 23 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-8
- Fix bug: uuzu-php-fpm can't rpm -e.
* Fri May 16 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 5.3.27-7
- Enable pdo_oci
- off autorq
* Thu May 15 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-6
- Add relog option in php-fpm-appid.init.
- Change logrotate function from reload to relog.
* Tue Mar 25 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-5
- change directory structure.
- change php-fpm init to php-fpm-appid.
* Mon Mar 17 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 5.3.27-4
- enable mhash
* Wed Feb 02 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 5.3.27-3 
- enable mysqlnd
* Fri Jul 12 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.27-1.ius
- Latest sources from upstream
