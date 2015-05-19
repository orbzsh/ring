%define username   zabbix
%define groupname  zabbix
#defined the path
%define srcname zabbix
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define bin_path       %{install_path}/bin
%define sbin_path       %{install_path}/sbin
%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path %{install_path}/conf
%define log_path /data/logs/zabbix
%define nginx_vhost /data/app/nginx/conf/vhosts

#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

Name		: uuzu-%{srcname}
Version		: 2.4.4
Release		: 1%{?dist}
Summary		: Enterprise-class open source distributed monitoring solution.

Group		: uuzu-sys/monitor
License		: GPLv2+
URL		: http://www.zabbix.com/
Source0		: %{srcname}-%{version}.tar.gz
Source1		: zabbix-web.conf
Source2		: zabbix-logrotate.in
Source3		: zabbix-java-gateway.init
Source4		: uuzu-zabbix-userparameter.conf
Source10         : zabbix-agent.init
Source11         : zabbix-server.init
Source12         : zabbix-proxy.init
#Patch0		: config.patch
Patch1		: fonts-config.patch
#Patch2		: zabbix-agent.patch

Buildroot	: %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)

%define build_server 0%{!?_only_agent:1}
%if 0%{?_only_agent:1}
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0
%endif

%if %{build_server}
BuildRequires	: uuzu-mysql-devel
BuildRequires	: postgresql-devel
BuildRequires	: net-snmp-devel
BuildRequires	: openldap-devel
BuildRequires	: gnutls-devel
BuildRequires	: iksemel-devel
BuildRequires	: sqlite-devel
BuildRequires	: unixODBC-devel
BuildRequires	: curl-devel >= 7.13.1
BuildRequires	: OpenIPMI-devel >= 2
BuildRequires	: libssh2-devel >= 1
BuildRequires   : java-devel >= 1.6.0
BuildRequires   : libxml2-devel
%endif

Requires	: logrotate
Requires(pre)	: /usr/sbin/useradd

%description
Zabbix is software that monitors numerous parameters of a network and
the health and integrity of servers. Zabbix uses a flexible
notification mechanism that allows users to configure e-mail based
alerts for virtually any event.  This allows a fast reaction to server
problems. Zabbix offers excellent reporting and data visualisation
features based on the stored data. This makes Zabbix ideal for
capacity planning.

Zabbix supports both polling and trapping. All Zabbix reports and
statistics, as well as configuration parameters are accessed through a
web-based front end. A web-based front end ensures that the status of
your network and the health of your servers can be assessed from any
location. Properly configured, Zabbix can play an important role in
monitoring IT infrastructure. This is equally true for small
organisations with a few servers and for large companies with a
multitude of servers.

%package agent
Summary		: Zabbix Agent
Group		: Applications/Internet
Requires	: %{name} = %{version}-%{release}
Requires(post)	: /sbin/chkconfig
Requires(preun)	: /sbin/chkconfig
Requires(preun)	: /sbin/service

%description agent
The Zabbix client agent, to be installed on monitored systems.

%package get
Summary		: Zabbix Get
Group		: Applications/Internet

%description get
Zabbix get command line utility

%package sender
Summary		: Zabbix Sender
Group		: Applications/Internet

%description sender
Zabbix sender command line utility

%if %{build_server}
%package server
Summary		: Zabbix server common files
Group		: Applications/Internet
Requires	: %{name} = %{version}-%{release}
Requires	: %{name}-server-implementation = %{version}-%{release}
Requires	: fping
Requires	: net-snmp
Requires	: iksemel
Requires	: unixODBC
Requires	: libssh2 >= 1.0.0
Requires	: curl >= 7.13.1
Requires	: OpenIPMI-libs >= 2.0.14
Conflicts	: %{name}-proxy
Requires(post)	: /sbin/chkconfig
Requires(preun)	: /sbin/chkconfig
Requires(preun)	: /sbin/service

%description server
Zabbix server common files.

%package server-mysql
Summary		: Zabbix server compiled to use MySQL database
Group		: Applications/Internet
Requires	: %{name} = %{version}-%{release}
Requires	: %{name}-server = %{version}-%{release}
Provides	: %{name}-server-implementation = %{version}-%{release}
Obsoletes	: %{name} <= 1.5.3-0.1
Conflicts	: %{name}-server-pgsql

%description server-mysql
Zabbix server compiled with MySQL database support.

%package server-pgsql
Summary		: Zabbix server compiled to use PostgresSQL database
Group		: Applications/Internet
Requires	: %{name} = %{version}-%{release}
Requires	: %{name}-server = %{version}-%{release}
Requires	: postgresql
Provides	: %{name}-server-implementation = %{version}-%{release}
Conflicts	: %{name}-server-mysql

%description server-pgsql
Zabbix server compiled with PostgresSQL database support.

%package proxy
Summary		: Zabbix Proxy common files
Group		: Applications/Internet
Requires	: %{name} = %{version}-%{release}
Requires	: %{name}-proxy-implementation = %{version}-%{release}
Requires	: fping
Requires	: net-snmp
Requires	: unixODBC
Requires	: libssh2 >= 1.0.0
Requires	: curl >= 7.13.1
Requires	: OpenIPMI-libs >= 2.0.14
Conflicts	: %{name}-server
Conflicts	: %{name}-web
Requires(post)	: /sbin/chkconfig
Requires(preun)	: /sbin/chkconfig
Requires(preun)	: /sbin/service

%description proxy
The Zabbix proxy common files

%package proxy-mysql
Summary		: Zabbix proxy compiled to use MySQL
Group		: Applications/Internet
Requires	: %{name}-proxy = %{version}-%{release}
Requires	: mysql
Provides	: %{name}-proxy-implementation = %{version}-%{release}
Conflicts	: %{name}-proxy-pgsql
Conflicts	: %{name}-proxy-sqlite3

%description proxy-mysql
The Zabbix proxy compiled to use MySQL

%package proxy-pgsql
Summary		: Zabbix proxy compiled to use PostgreSQL
Group		: Applications/Internet
Requires	: %{name}-proxy = %{version}-%{release}
Requires	: postgresql
Provides	: %{name}-proxy-implementation = %{version}-%{release}
Conflicts	: %{name}-proxy-mysql
Conflicts	: %{name}-proxy-sqlite3

%description proxy-pgsql
The Zabbix proxy compiled to use PostgreSQL

%package proxy-sqlite3
Summary		: Zabbix proxy compiled to use SQLite3
Group		: Applications/Internet
Requires	: %{name}-proxy = %{version}-%{release}
Requires	: sqlite
Provides	: %{name}-proxy-implementation = %{version}-%{release}
Conflicts	: %{name}-proxy-mysql
Conflicts	: %{name}-proxy-pgsql

%description proxy-sqlite3
The Zabbix proxy compiled to use SQLite3

%package java-gateway
Summary		: Zabbix java gateway
Group		: Applications/Internet
Requires	: %{name} = %{version}-%{release}
Requires	: java >= 1.6.0
Requires(post)	: /sbin/chkconfig
Requires(preun)	: /sbin/chkconfig
Requires(preun)	: /sbin/service

%description java-gateway
The Zabbix java gateway

%package web
Summary		: Zabbix Web Frontend
Group		: Applications/Internet
%if 0%{?fedora} > 9 || 0%{?rhel} >= 6
BuildArch	: noarch
%endif
Requires	: uuzu-nginx
Requires	: uuzu-php >= 5.0
Requires	: uuzu-php-gd
Requires	: uuzu-php-bcmath
Requires	: uuzu-php-mbstring
Requires	: uuzu-php-xml
# DejaVu fonts doesn't exist on EL <= 5
%if 0%{?fedora} || 0%{?rhel} >= 6
Requires	: dejavu-sans-fonts
%endif
Requires	: %{name}-web-database = %{version}-%{release}
Requires(post)	: %{_sbindir}/update-alternatives
Requires(preun)	: %{_sbindir}/update-alternatives
Conflicts	: %{name}-proxy

%description web
The php frontend to display the zabbix web interface.

%package web-mysql
Summary		: Zabbix web frontend for MySQL
Group		: Applications/Internet
%if 0%{?fedora} > 9 || 0%{?rhel} >= 6
BuildArch	: noarch
%endif
Requires	: uuzu-zabbix-web = %{version}-%{release}
Requires	: uuzu-php-mysql
Provides	: %{name}-web-database = %{version}-%{release}
Conflicts	: %{name}-web-pgsql
Conflicts	: %{name}-web-sqlite3
Obsoletes	: %{name}-web <= 1.5.3-0.1

%description web-mysql
Zabbix web frontend for MySQL

%package web-pgsql
Summary		: Zabbix web frontend for PostgreSQL
Group		: Applications/Internet
%if 0%{?fedora} > 9 || 0%{?rhel} >= 6
BuildArch	: noarch
%endif
Requires	: %{name}-web = %{version}-%{release}
Requires	: php-pgsql
Provides	: %{name}-web-database = %{version}-%{release}
Conflicts	: %{name}-web-mysql
Conflicts	: %{name}-web-sqlite3

%description web-pgsql
Zabbix web frontend for PostgreSQL

# %package web-japanese
# Summary		: Japanese font for Zabbix web frontend
# Group		: Applications/Internet
# %if 0%{?fedora} > 9 || 0%{?rhel} >= 6
# BuildArch	: noarch
# Requires	: vlgothic-p-fonts
# %else
# Requires	: ipa-pgothic-fonts
#%endif
# Requires	: %{srcname}-web = %{version}-%{release}
# Requires(post)	: %{sbin_path}/update-alternatives
# Requires(preun)	: %{sbin_path}/update-alternatives

# %description web-japanese
# Japanese font for Zabbix web frontend
%endif

%prep
%setup -q -n %{srcname}-%{version}
#%setup -T -D -a 9 -n %{srcname}-%{version}
#%patch0 -p1
%patch1 -p1
#%patch2 -p1


# DejaVu fonts doesn't exist on EL <= 5
%if 0%{?fedora} || 0%{?rhel} >= 6
# remove included fonts
rm -rf frontends/php/fonts/DejaVuSans.ttf
%endif

# remove executable permissions
chmod a-x upgrades/dbpatches/1.8/mysql/upgrade

# fix up some lib64 issues
sed -i.orig -e 's|_LIBDIR=/usr/lib|_LIBDIR=%{lib_path}|g' \
    configure

# kill off .htaccess files, options set in SOURCE1
rm -f frontends/php/include/.htaccess
rm -f frontends/php/include/classes/.htaccess
rm -f frontends/php/api/.htaccess
rm -f frontends/php/conf/.htaccess

# set timestamp on modified config file and directories
touch -r frontends/php/styles/blocks.css frontends/php/include/setup.inc.php \
    frontends/php/include/classes/class.cconfigfile.php \
    frontends/php/include/classes/core/ZBase.php \
    frontends/php/include \
    frontends/php/include/classes \
    frontends/php/api \
    frontends/php/conf

# fix path to traceroute utility
sed -i.orig -e 's|/usr/bin/traceroute|/bin/traceroute|' database/mysql/data.sql
sed -i.orig -e 's|/usr/bin/traceroute|/bin/traceroute|' database/postgresql/data.sql
sed -i.orig -e 's|/usr/bin/traceroute|/bin/traceroute|' database/sqlite3/data.sql

# remove .orig files in frontend
find frontends/php -srcname '*.orig'|xargs rm -f

# remove prebuild Windows binaries
rm -rf bin

# change log directory of zabbix_java.log
sed -i -e 's|/tmp/zabbix_java.log|/opt/logs/zabbix/zabbix_java_gateway.log|g' src/zabbix_java/lib/logback.xml

%build

%if %{build_server}
common_flags="
    --bindir=%{bin_path}
    --sbindir=%{sbin_path}
    --sysconfdir=%{conf_path}
    --libdir=%{lib_path}
    --includedir=%{include_path}
    --enable-dependency-tracking
    --enable-server
    --enable-agent
    --enable-proxy
    --enable-ipv6
    --enable-java
    --with-net-snmp
    --with-ldap
    --with-libcurl
    --with-openipmi
    --with-jabber
    --with-unixodbc
    --with-ssh2
    --with-libxml2
"

%configure $common_flags --with-mysql=/data/app/mysql/bin/mysql_config
make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure $common_flags --with-postgresql
make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql

%configure $common_flags --with-sqlite3
make %{?_smp_mflags}
#mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_sqlite3
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3

touch src/zabbix_server/zabbix_server
touch src/zabbix_proxy/zabbix_proxy

%else
%configure --enable-dependency-tracking --enable-agent \
    --bindir=%{bin_path} \
    --sbindir=%{sbin_path} \
    --sysconfdir=%{conf_path} \
    --libdir=%{lib_path} \
    --includedir=%{include_path}
make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT

# install 
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p %{buildroot}%{install_root}
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{init_dir}
mkdir -p %{buildroot}%{include_path}
mkdir -p %{buildroot}%{lib_path}
mkdir -p %{buildroot}%{logrotate_dir}
mkdir -p %{buildroot}%{bin_path}
mkdir -p %{buildroot}%{sbin_path}
mkdir -p %{buildroot}%{log_path}
mkdir -p $RPM_BUILD_ROOT%{nginx_vhost}
mkdir -p %{buildroot}%{install_path}/alertscripts
mkdir -p %{buildroot}%{install_path}/externalscripts

# remove unnecessary files
rm -rf $RPM_BUILD_ROOT%{conf_path}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{srcname}
%if %{build_server}
rm $RPM_BUILD_ROOT%{sbin_path}/zabbix_server
rm $RPM_BUILD_ROOT%{sbin_path}/zabbix_proxy
%endif
find ./frontends/php -srcname '*.orig'|xargs rm -f
find ./database -srcname '*.orig'|xargs rm -f

# set up some required directories
mkdir -p $RPM_BUILD_ROOT%{conf_path}
mkdir -p $RPM_BUILD_ROOT%{conf_path}/web
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{srcname}/alertscripts
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{srcname}/externalscripts
mkdir -p $RPM_BUILD_ROOT%{_datadir}

# install the frontend
cp -a frontends/php $RPM_BUILD_ROOT%{_datadir}/%{srcname}

# prepare ghosted config file
touch $RPM_BUILD_ROOT%{conf_path}/web/zabbix.conf.php

# move maintenance.inc.php
mv $RPM_BUILD_ROOT%{_datadir}/%{srcname}/conf/maintenance.inc.php $RPM_BUILD_ROOT%{conf_path}/web/

# drop config files in place
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{nginx_vhost}/%{srcname}.conf

# install zabbix_agent.conf and userparameter files
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{srcname}-agent-%{version}
install -m 0644 conf/zabbix_agent.conf $RPM_BUILD_ROOT%{_docdir}/%{srcname}-agent-%{version}
install -dm 755 $RPM_BUILD_ROOT%{conf_path}/zabbix_agentd.d
install -m 0644 conf/zabbix_agentd/userparameter_mysql.conf $RPM_BUILD_ROOT%{conf_path}/zabbix_agentd.d
install -m 0644 conf/zabbix_agentd/userparameter_examples.conf $RPM_BUILD_ROOT%{_docdir}/%{srcname}-agent-%{version}
#install -m 755 %{SOURCE5} %{buildroot}%{install_path}/externalscripts/17173_php_monitor.pl
#install -m 755 %{SOURCE6} %{buildroot}%{install_path}/externalscripts/17173_nginx_monitor.pl
#install -m 755 %{SOURCE8} %{buildroot}%{install_path}/externalscripts/mysql_discovery.py
install -m 644 %{SOURCE4} %{buildroot}%{conf_path}/zabbix_agentd.d/uuzu-zabbix-userparameter.conf
#install -m 644 %{SOURCE7} %{buildroot}%{conf_path}/zabbix_agentd.d/container-cgroup.conf

#install 173 script
#install -dm 755 $RPM_BUILD_ROOT%{install_path}/externalscripts/lib
#install -m 755 ./173-zabbix-script/lib/*.py %{buildroot}%{install_path}/externalscripts/lib
#install -m 755 ./173-zabbix-script/*.py %{buildroot}%{install_path}/externalscripts/

# fix config file options
cat conf/zabbix_agentd.conf | sed \
    -e '/^# PidFile=/a \\nPidFile=%{log_path}/zabbix_agentd.pid' \
    -e 's|^LogFile=.*|LogFile=%{log_path}/zabbix_agentd.log|g' \
    -e '/^# LogFileSize=.*/a \\nLogFileSize=0' \
    -e '/^# Include=$/a \\nInclude=%{conf_path}/zabbix_agentd.d/' \
    -e 's/ServerActive=.*/ServerActive=zabbix.173ops.com/' \
    -e 's/Server=.*/Server=zabbix.173ops.com,ck01.ctc.proxy.zabbix.173ops.com/' \
    -e 's/^# AllowRoot=0/AllowRoot=1/' \
    -e 's/^# UnsafeUserParameters=0/UnsafeUserParameters=1/' \
    -e 's/^# ListenPort=10050/ListenPort=10050/' \
    > $RPM_BUILD_ROOT%{conf_path}/zabbix_agentd.conf

cat conf/zabbix_server.conf | sed \
    -e '/^# PidFile=/a \\nPidFile=%{log_path}/zabbix_server.pid' \
    -e 's|^LogFile=.*|LogFile=%{log_path}/zabbix_server.log|g' \
    -e '/^# LogFileSize=/a \\nLogFileSize=0' \
    -e '/^# AlertScriptsPath=/a \\nAlertScriptsPath=%{install_path}/alertscripts' \
    -e '/^# ExternalScripts=/a \\nExternalScripts=%{install_path}/externalscripts' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e '/^# DBSocket=/a \\nDBSocket=/opt/logs/mysql/mysql.sock' \
    -e '/^# SNMPTrapperFile=.*/a \\nSNMPTrapperFile=/var/log/snmptt/snmptt.log' \
    > $RPM_BUILD_ROOT%{conf_path}/zabbix_server.conf

cat conf/zabbix_proxy.conf | sed \
    -e '/^# PidFile=/a \\nPidFile=%{log_path}/zabbix_proxy.pid' \
    -e 's|^LogFile=.*|LogFile=%{log_path}/zabbix_proxy.log|g' \
    -e '/^# LogFileSize=/a \\nLogFileSize=0' \
    -e '/^# ExternalScripts=/a \\nExternalScripts=%{install_path}/externalscripts' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e '/^# DBSocket=/a \\nDBSocket=/opt/logs/mysql/mysql.sock' \
    > $RPM_BUILD_ROOT%{conf_path}/zabbix_proxy.conf

cat src/zabbix_java/settings.sh | sed \
    -e 's|^PID_FILE=.*|PID_FILE="%{log_path}/zabbix_java.pid"|g' \
    > $RPM_BUILD_ROOT%{conf_path}/zabbix_java_gateway.conf

# install log rotation
cat %{SOURCE2} | sed -e 's|COMPONENT|server|g' > \
     $RPM_BUILD_ROOT%{logrotate_dir}/zabbix-server
cat %{SOURCE2} | sed -e 's|COMPONENT|agentd|g' > \
     $RPM_BUILD_ROOT%{logrotate_dir}/zabbix-agent
cat %{SOURCE2} | sed -e 's|COMPONENT|proxy|g' > \
     $RPM_BUILD_ROOT%{logrotate_dir}/zabbix-proxy

# init scripts
install -m 0755 -p %{SOURCE11} $RPM_BUILD_ROOT%{init_dir}/zabbix-server
install -m 0755 -p %{SOURCE10} $RPM_BUILD_ROOT%{init_dir}/zabbix-agent
install -m 0755 -p %{SOURCE12} $RPM_BUILD_ROOT%{init_dir}/zabbix-proxy
install -m 0755 -p %{SOURCE3} $RPM_BUILD_ROOT%{init_dir}/zabbix-java-gateway
sed -i 's:/usr/sbin:/data/app/zabbix/sbin:' $RPM_BUILD_ROOT%{init_dir}/zabbix-server $RPM_BUILD_ROOT%{init_dir}/zabbix-agent $RPM_BUILD_ROOT%{init_dir}/zabbix-proxy $RPM_BUILD_ROOT%{init_dir}/zabbix-java-gateway
sed -i 's:exec=zabbix_agentd:exec=/data/app/zabbix/sbin/zabbix_agentd:' $RPM_BUILD_ROOT%{init_dir}/zabbix-agent
sed -i 's:exec=zabbix_proxy:exec=/data/app/zabbix/sbin/zabbix_proxy:' $RPM_BUILD_ROOT%{init_dir}/zabbix-proxy
sed -i 's:/etc/zabbix/zabbix_java_gateway.conf:/data/app/zabbix/conf/zabbix_java_gateway.conf:' $RPM_BUILD_ROOT%{init_dir}/zabbix-java-gateway
sed -i 's:/etc/zabbix/:/data/app/zabbix/conf/:' $RPM_BUILD_ROOT%{init_dir}/zabbix-server $RPM_BUILD_ROOT%{init_dir}/zabbix-agent $RPM_BUILD_ROOT%{init_dir}/zabbix-proxy $RPM_BUILD_ROOT%{init_dir}/zabbix-java-gateway

# install server and proxy binaries
%if %{build_server}
install -m 0755 -p src/zabbix_server/zabbix_server_* $RPM_BUILD_ROOT%{sbin_path}/
install -m 0755 -p src/zabbix_proxy/zabbix_proxy_* $RPM_BUILD_ROOT%{sbin_path}/

# delete unnecessary files from java gateway
rm $RPM_BUILD_ROOT%{sbin_path}/zabbix_java/settings.sh
rm $RPM_BUILD_ROOT%{sbin_path}/zabbix_java/startup.sh
rm $RPM_BUILD_ROOT%{sbin_path}/zabbix_java/shutdown.sh
%endif

# nuke static libs and empty oracle upgrade sql
rm -rf $RPM_BUILD_ROOT%{lib_path}/libzbx*.a

# copy sql files to appropriate per package locations
for pkg in proxy server ; do
    docdir=$RPM_BUILD_ROOT%{_docdir}/%{srcname}-$pkg-mysql-%{version}
    install -dm 755 $docdir
    cp -pR database/mysql $docdir/create
    cp -pR --parents upgrades/dbpatches/1.6/mysql $docdir
    cp -pR --parents upgrades/dbpatches/1.8/mysql $docdir
    cp -pR --parents upgrades/dbpatches/2.0/mysql $docdir
    docdir=$RPM_BUILD_ROOT%{_docdir}/%{srcname}-$pkg-pgsql-%{version}
    install -dm 755 $docdir
    cp -pR database/postgresql $docdir/create
    cp -pR --parents upgrades/dbpatches/1.6/postgresql $docdir
    cp -pR --parents upgrades/dbpatches/1.8/postgresql $docdir
    cp -pR --parents upgrades/dbpatches/2.0/postgresql $docdir

    if [ "$pkg" = "proxy" ]; then
        docdir=$RPM_BUILD_ROOT%{_docdir}/%{srcname}-$pkg-sqlite3-%{version}
        install -dm 755 $docdir
        cp -pR database/sqlite3 $docdir/create
    fi
done
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}
# remove extraneous ones
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{srcname}/create
rm -f %{buildroot}%{install_path}/externalscripts/*.py{c,o}
rm -f %{buildroot}%{install_path}/externalscripts/lib/*.py{c,o}


%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group %{groupname} > /dev/null || groupadd -r zabbix
getent passwd %{groupname} > /dev/null || \
    useradd -r -g %{groupname} -d %{lib_path} -s /sbin/nologin \
    -c "Zabbix Monitoring System" zabbix
:

%post agent
LOCALIP=`/sbin/ifconfig | sed -n '/^[^ \t]/{N;s/\(^[^ ]*\).*addr:\([^ ]*\).*/\1\t\2/p}'|grep '10.5\|10.255'|head -1|awk '{print $2}'`
sed -i "s/# ListenIP=0.0.0.0/ListenIP=$(ifconfig | egrep "10\.(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){2}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])" | cut -d":" -f2 | cut -d' ' -f1 | head -1)/" %{conf_path}/zabbix_agentd.conf 
sed -i "s/Hostname=Zabbix server/Hostname=$(ifconfig | egrep "10\.(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){2}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])" | cut -d":" -f2 | cut -d' ' -f1 | head -1)/" %{conf_path}/zabbix_agentd.conf
IPA=`echo $LOCALIP|awk -F\. '{print $1}' `;IPB=`echo $LOCALIP|awk -F\. '{print $2}' `; IPC=`echo $LOCALIP|awk -F\. '{print $3}' ` D=`echo $LOCALIP|awk -F\. '{print $4}' `
sed -i "s/^Server=.*/Server=zabbixpt.uuzu.com/" %{conf_path}/zabbix_agentd.conf
sed -i "s/^ServerActive=.*/ServerActive=zabbixpt.uuzu.com/" %{conf_path}/zabbix_agentd.conf
ln -sf %{init_dir}/zabbix-agent %{_sysconfdir}/rc.d/init.d/uuzu-zabbix-agent
/sbin/chkconfig --add uuzu-zabbix-agent || :
/sbin/chkconfig uuzu-zabbix-agent on
service uuzu-zabbix-agent start

%if %{build_server}
%post server
ln -sf %{init_dir}/zabbix-server %{_sysconfdir}/rc.d/init.d/uuzu-zabbix-server
/sbin/chkconfig --add uuzu-zabbix-server
if [ $1 -gt 1 ]
then
  # Apply permissions also in *.rpmnew upgrades from old permissive ones
  chmod 0640 %{conf_path}/zabbix_server.conf
  chown root:zabbix %{conf_path}/zabbix_server.conf
fi
:

%post server-mysql
old=`update-alternatives --display zabbix-server | head -2 | tail -1 | awk -F '/' '{print $4}'`; /usr/sbin/update-alternatives --remove zabbix-server /data/app/$old/sbin/zabbix_server_mysql 
/usr/sbin/update-alternatives --install %{sbin_path}/zabbix_server zabbix-server %{sbin_path}/zabbix_server_mysql 10
:

%post server-pgsql
old=`update-alternatives --display zabbix-server | head -2 | tail -1 | awk -F '/' '{print $4}'`; /usr/sbin/update-alternatives --remove zabbix-server /data/app/$old/sbin/zabbix_server_pgsql
/usr/sbin/update-alternatives --install %{sbin_path}/zabbix_server zabbix-server %{sbin_path}/zabbix_server_pgsql 10
:

%post proxy
ln -sf %{init_dir}/zabbix-proxy %{_sysconfdir}/rc.d/init.d/uuzu-zabbix-proxy
/sbin/chkconfig --add uuzu-zabbix-proxy
if [ $1 -gt 1 ]
then
  # Apply permissions also in *.rpmnew upgrades from old permissive ones
  chmod 0640 %{conf_path}/zabbix_proxy.conf
  chown root:zabbix %{conf_path}/zabbix_proxy.conf
fi
:

%post proxy-mysql
old=`update-alternatives --display zabbix-proxy | head -2 | tail -1 | awk -F '/' '{print $4}'`; /usr/sbin/update-alternatives --remove zabbix-proxy /data/app/$old/sbin/zabbix_proxy_mysql 
/usr/sbin/update-alternatives --install %{sbin_path}/zabbix_proxy zabbix-proxy %{sbin_path}/zabbix_proxy_mysql 10
:

%post proxy-pgsql
old=`update-alternatives --display zabbix-proxy | head -2 | tail -1 | awk -F '/' '{print $4}'`; /usr/sbin/update-alternatives --remove zabbix-proxy /data/app/$old/sbin/zabbix_proxy_pgsql
/usr/sbin/update-alternatives --install %{sbin_path}/zabbix_proxy zabbix-proxy %{sbin_path}/zabbix_proxy_pgsql 10
:

%post proxy-sqlite3
old=`update-alternatives --display zabbix-proxy | head -2 | tail -1 | awk -F '/' '{print $4}'`; /usr/sbin/update-alternatives --remove zabbix-proxy /data/app/$old/sbin/zabbix_proxy_sqlite3
/usr/sbin/update-alternatives --install %{sbin_path}/zabbix_proxy zabbix-proxy %{sbin_path}/zabbix_proxy_sqlite3 10
:

%post java-gateway
ln -sf %{init_dir}/zabbix-java-gateway %{_sysconfdir}/rc.d/init.d/uuzu-zabbix-java-gateway
/sbin/chkconfig --add uuzu-zabbix-java-gateway || :

%post web
%if 0%{?fedora} || 0%{?rhel} >= 6
/usr/sbin/update-alternatives --install %{_datadir}/%{srcname}/fonts/graphfont.ttf zabbix-web-font %{_datadir}/fonts/dejavu/DejaVuSans.ttf 10
%else
/usr/sbin/update-alternatives --install %{_datadir}/%{srcname}/fonts/graphfont.ttf zabbix-web-font %{_datadir}/%{srcname}/fonts/DejaVuSans.ttf 10
%endif
# move existing config file on update
if [ "$1" -ge "1" ]
then
    if [ -f %{conf_path}/zabbix.conf.php ]
    then
        mv %{conf_path}/zabbix.conf.php %{conf_path}/web
        chown apache:apache %{conf_path}/web/zabbix.conf.php
    fi
fi
:

#%post web-japanese
#%if 0%{?fedora} || 0%{?rhel} >= 6
#  /usr/sbin/update-alternatives --install %{_datadir}/%{srcname}/fonts/graphfont.ttf zabbix-web-font %{_datadir}/fonts/vlgothic/VL-PGothic-Regular.ttf 20
#%else
#  /usr/sbin/update-alternatives --install %{_datadir}/%{srcname}/fonts/graphfont.ttf zabbix-web-font %{_datadir}/fonts/ipa-pgothic/ipagp.ttf 20
#%endif
#:
%endif

%preun agent
if [ "$1" = 0 ]
then
  /sbin/service zabbix-agent stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-agent
fi
:

%if %{build_server}
%preun server
if [ "$1" = 0 ]
then
  /sbin/service zabbix-server stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-server
fi
:

%preun server-mysql
if [ "$1" = 0 ]
then
  /usr/sbin/update-alternatives --remove zabbix-server %{sbin_path}/zabbix_server_mysql
fi
:

%preun server-pgsql
if [ "$1" = 0 ]
then
  /usr/sbin/update-alternatives --remove zabbix-server %{sbin_path}/zabbix_server_pgsql
fi
:

%preun proxy
if [ "$1" = 0 ]
then
  /sbin/service zabbix-proxy stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-proxy
fi
:

%preun proxy-mysql
if [ "$1" = 0 ]
then
  /usr/sbin/update-alternatives --remove zabbix-proxy %{sbin_path}/zabbix_proxy_mysql
fi
:

%preun proxy-pgsql
if [ "$1" = 0 ]
then
  /usr/sbin/update-alternatives --remove zabbix-proxy %{sbin_path}/zabbix_proxy_pgsql
fi
:

%preun proxy-sqlite3
if [ "$1" = 0 ]
then
  /usr/sbin/update-alternatives --remove zabbix-proxy %{sbin_path}/zabbix_proxy_sqlite3
fi
:

%preun java-gateway
if [ $1 -eq 0 ]
then
  /sbin/service zabbix-java-gateway stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-java-gateway
fi
:

%preun web
if [ "$1" = 0 ]
then
  %if 0%{?fedora} || 0%{?rhel} >= 6
    /usr/sbin/update-alternatives --remove zabbix-web-font %{_datadir}/fonts/dejavu/DejaVuSans.ttf
  %else
    /usr/sbin/update-alternatives --remove zabbix-web-font %{_datadir}/%{srcname}/fonts/DejaVuSans.ttf
  %endif
fi
:

#%preun web-japanese
#if [ "$1" = 0 ]
#then
#  %if 0%{?fedora} || 0%{?rhel} >= 6
#    /usr/sbin/update-alternatives --remove zabbix-web-font %{_datadir}/fonts/vlgothic/VL-PGothic-Regular.ttf 
#  %else
#    /usr/sbin/update-alternatives --remove zabbix-web-font %{_datadir}/fonts/ipa-pgothic/ipagp.ttf
#  %endif
#fi
#:
%endif

%postun agent
if [ $1 -ge 1 ]
then
  /sbin/service zabbix-agent try-restart >/dev/null 2>&1 || :
fi

%if %{build_server}
%postun server
if [ $1 -ge 1 ]
then
  /sbin/service zabbix-server try-restart >/dev/null 2>&1 || :
fi

%postun proxy
if [ $1 -ge 1 ]
then
  /sbin/service zabbix-proxy try-restart >/dev/null 2>&1 || :
fi

%postun java-gateway
if [ $1 -gt 1 ]; then
  /sbin/service zabbix-java-gateway condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%dir %{conf_path}
%attr(0755,zabbix,zabbix) %dir %{log_path}

%files agent
%defattr(-,root,root,-)
%{_docdir}/%{srcname}-agent-%{version}/
%config(noreplace) %{conf_path}/zabbix_agentd.conf
%config(noreplace) %{logrotate_dir}/zabbix-agent
%dir %{conf_path}/zabbix_agentd.d
#%config(noreplace) %{conf_path}/zabbix_agentd.d/userparameter_mysql.conf
%exclude %{conf_path}/zabbix_agentd.d/userparameter_mysql.conf
%{conf_path}/zabbix_agentd.d/uuzu-zabbix-userparameter.conf
%{init_dir}/zabbix-agent
%{sbin_path}/zabbix_agent
%{sbin_path}/zabbix_agentd
%exclude %{_mandir}/man8/zabbix_agentd.8*

%files get
%defattr(-,root,root,-)
%{bin_path}/zabbix_get
%{_mandir}/man1/zabbix_get.1*

%files sender
%defattr(-,root,root,-)
%{bin_path}/zabbix_sender
%{_mandir}/man1/zabbix_sender.1*

%if %{build_server}
%files server
%defattr(-,root,root,-)
%attr(0640,root,zabbix) %config(noreplace) %{conf_path}/zabbix_server.conf
%dir %{install_path}/alertscripts
%dir %{install_path}/externalscripts
%config(noreplace) %{logrotate_dir}/zabbix-server
%{init_dir}/zabbix-server
%{_mandir}/man8/zabbix_server.8*

%files server-mysql
%defattr(-,root,root,-)
%{_docdir}/%{srcname}-server-mysql-%{version}/
%{sbin_path}/zabbix_server_mysql

%files server-pgsql
%defattr(-,root,root,-)
%{_docdir}/%{srcname}-server-pgsql-%{version}/
%{sbin_path}/zabbix_server_pgsql

%files proxy
%defattr(-,root,root,-)
%attr(0640,root,zabbix) %config(noreplace) %{conf_path}/zabbix_proxy.conf
%attr(0755,zabbix,zabbix) %dir /usr/lib/zabbix/externalscripts
%config(noreplace) %{logrotate_dir}/zabbix-proxy
%{init_dir}/zabbix-proxy
%{_mandir}/man8/zabbix_proxy.8*

%files proxy-mysql
%defattr(-,root,root,-)
%{_docdir}/%{srcname}-proxy-mysql-%{version}/
%{sbin_path}/zabbix_proxy_mysql

%files proxy-pgsql
%defattr(-,root,root,-)
%{_docdir}/%{srcname}-proxy-pgsql-%{version}/
%{sbin_path}/zabbix_proxy_pgsql

%files proxy-sqlite3
%defattr(-,root,root,-)
%{_docdir}/%{srcname}-proxy-sqlite3-%{version}/
%{sbin_path}/zabbix_proxy_sqlite3

%files java-gateway
%defattr(-,root,root,-)
%config(noreplace) %{conf_path}/zabbix_java_gateway.conf
%{init_dir}/zabbix-java-gateway
%{sbin_path}/zabbix_java

%files web
%defattr(-,root,root,-)
%dir %attr(0750,apache,apache) %{conf_path}/web
%ghost %attr(0644,apache,apache) %config(noreplace) %{conf_path}/web/zabbix.conf.php
%config(noreplace) %{conf_path}/web/maintenance.inc.php

%config(noreplace) %{nginx_vhost}/zabbix.conf
%{_datadir}/zabbix

%files web-mysql
%defattr(-,root,root,-)

%files web-pgsql
%defattr(-,root,root,-)

# %files web-japanese
# %defattr(-,root,root,-)
%endif


%changelog
* Thu Mar 26 2015 Harrison Zhu <wcg6121@gmail.com> - 2.4.1-3
- remove 17173 monitor scripts

* Tue Nov 4 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.4.1-2
- add 17173 monitor scripts

* Fri Oct 31 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.4.1-1
- update to 2.4.1

* Mon Sep 1 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.2.6-6
- add set Activeserver config post
- add server,agent,proxy init script

* Mon Sep 1 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.2.6-1
- update to 2.2.6-1
