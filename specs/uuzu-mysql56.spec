%define username   mysql
%define groupname  mysql
#defined the path
%define srcname mysql
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path %{install_path}/conf

#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

%global basever 5.6

Name: uuzu-mysql
Version: 5.6.14
Release: 4%{?dist}

Summary: MySQL client programs and shared libraries
Group: Applications/Databases
URL: http://www.mysql.com
# exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
License: GPLv2 with exceptions

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%global runselftest 0}
%global runselftest 0

# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/mysql/
Source0: mysql-%{version}-nodocs.tar.gz
# The upstream tarball includes non-free documentation that we cannot ship.
# To remove the non-free documentation, run this script after downloading
# the tarball into the current directory:
# ./generate-tarball.sh $VERSION
Source1: generate-tarball.sh
Source2: mysql.init
Source3: my.cnf
Source4: scriptstub.c
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
Source9: mysql-embedded-check.c
Source10: mysql.tmpfiles.d
Source11: mysqld.service
Source12: mysqld-prepare-db-dir
Source13: mysqld-wait-ready
Source14: rh-skipped-tests-base.list
Source15: rh-skipped-tests-arm.list
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh

# Comments for these patches are in the patch files.
#Patch1: mysql-errno.patch
Patch2: mysql-strmov.patch
Patch16: mysql-logrotate.patch
Patch22: mysql-embedded-shared.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl, readline-devel, openssl-devel
BuildRequires: gcc-c++, cmake, ncurses-devel, zlib-devel, libaio-devel
BuildRequires: systemtap-sdt-devel
# make test requires time and ps
BuildRequires: time procps
# Socket and Time::HiRes are needed to run regression tests
BuildRequires: perl(Socket), perl(Time::HiRes)
%if 0%{?fedora} > 14
BuildRequires: systemd-units
%endif

Requires: grep, fileutils
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: bash

# MySQL (with caps) is upstream's spelling of their own RPMs for mysql
#Conflicts: MySQL
# mysql-cluster used to be built from this SRPM, but no more
Obsoletes: mysql-cluster < 5.1.44

# IUS-isms
#Conflicts: mysql < %{basever}
Provides: mysql = %{version}-%{release}

# When rpm 4.9 is universal, this could be cleaned up:
%global __perl_requires %{SOURCE999}
%global __perllib_requires %{SOURCE999}

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MySQL client programs and generic MySQL files.

%package libs

Summary: The shared libraries required for MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig

# IUS-isms
#Conflicts: mysql-libs < %{basever}
Provides: mysql-libs = %{version}-%{release}
Provides: config(mysql-libs) = %{version}-%{release}

%description libs
The mysql-libs package provides the essential shared libraries for any 
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.

%package server

Summary: The MySQL server and related files
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: sh-utils
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
%if 0%{?fedora} < 15
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%else
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires: systemd-units
# Make sure it's there when scriptlets run, too
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%endif
# mysqlhotcopy needs DBI/DBD support
#Requires: perl-DBI, uuzu-perl-DBD-MySQL
Requires: uuzu-perl-DBD-MySQL
#Conflicts: MySQL-server

# IUS-isms
#Conflicts: mysql-server < %{basever}
Provides: mysql-server = %{version}-%{release}
Provides: config(mysql-server) = %{version}-%{release}

%description server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.

%package devel

Summary: Files for development of MySQL applications
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: openssl-devel%{?_isa}
#Conflicts: MySQL-devel

# IUS-isms
#Conflicts: mysql-devel < %{basever}
Provides: mysql-devel = %{version}-%{release}

%description devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.

%package embedded

Summary: MySQL as an embeddable library
Group: Applications/Databases

# IUS-isms
#Conflicts: mysql-embedded < %{basever}
Provides: mysql-embedded = %{version}-%{release}

%description embedded
MySQL is a multi-user, multi-threaded SQL database server. This
package contains a version of the MySQL server that can be embedded
into a client application instead of running as a separate process.

%package embedded-devel

Summary: Development files for MySQL as an embeddable library
Group: Applications/Databases
Requires: %{name}-embedded%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

# IUS-isms
#Conflicts: mysql-embedded-devel < %{basever}
Provides: mysql-embedded-devel = %{version}-%{release}

%description embedded-devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains files needed for developing and testing with
the embedded version of the MySQL server.

%package bench

Summary: MySQL benchmark scripts and data
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
#Conflicts: MySQL-bench

# IUS-isms
#Conflicts: mysql-bench < %{basever}
Provides: mysql-bench = %{version}-%{release}

%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.

%package test

Summary: The test suite distributed with MySQL
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-server%{?_isa} = %{version}-%{release}
#Conflicts: MySQL-test

# IUS-isms
#Conflicts: mysql-test < %{basever}
Provides: mysql-test = %{version}-%{release}

%description test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.

%prep
%setup -q -n mysql-%{version}

%patch2 -p1
%patch16 -p1
%patch22 -p1

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# upstream has fallen down badly on symbol versioning, do it ourselves
# mysql-versioning.patch handles this now
#cp %{SOURCE8} libmysql/libmysql.version

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE14} > mysql-test/rh-skipped-tests.list
# disable some tests failing on ARM architectures
%ifarch %{arm}
cat %{SOURCE15} >> mysql-test/rh-skipped-tests.list
%endif

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "mysql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"
# gcc seems to have some bugs on sparc as of 4.4.1, back off optimization
# submitted as bz #529298
%ifarch sparc sparcv9 sparc64
CFLAGS=`echo $CFLAGS| sed -e "s|-O2|-O1|g" `
%endif
# extra C++ flags as per recommendations in mysql's INSTALL-SOURCE doc
CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{install_path}/share and so forth here.

cmake . -DBUILD_CONFIG=mysql_release \
	-DFEATURE_SET="community" \
        -DSYSCONFDIR=%{conf_path} \
	-DINSTALL_LAYOUT=RPM \
	-DINSTALL_INCLUDEDIR=%{install_root}/include/mysql \
	-DINSTALL_INFODIR=%{install_path}/share/info \
	-DINSTALL_LIBDIR=%{lib_path}/mysql \
	-DINSTALL_MANDIR=%{install_path}/share/man \
	-DINSTALL_MYSQLSHAREDIR=%{install_path}/share/mysql \
	-DINSTALL_MYSQLTESTDIR=%{install_path}/share/mysql-test \
	-DINSTALL_PLUGINDIR=%{lib_path}/mysql/plugin \
	-DINSTALL_SBINDIR=%{install_path}/bin \
	-DINSTALL_BINDIR=%{install_path}/bin \
	-DINSTALL_SCRIPTDIR=%{install_path}/bin \
	-DINSTALL_SQLBENCHDIR=%{install_path}/share \
	-DINSTALL_SUPPORTFILESDIR=%{install_path}/share/mysql \
	-DMYSQL_DATADIR=/data/mysql \
	-DMYSQL_UNIX_ADDR=/data/logs/mysql/3306/mysql.sock \
	-DENABLED_LOCAL_INFILE=ON \
	-DENABLE_DTRACE=ON \
	-DWITH_EMBEDDED_SERVER=ON \
	-DWITH_READLINE=ON \
%if 0%{?rhel} == 5
	-DWITH_SSL=bundled \
%else
	-DWITH_SSL=system \
%endif
	-DWITH_ZLIB=system

gcc $CFLAGS $LDFLAGS -o scriptstub "-DLIBDIR=\"%{lib_path}/mysql\"" %{SOURCE4}

make %{?_smp_mflags} VERBOSE=1

# regular build will make libmysqld.a but not libmysqld.so :-(
# mysql-embedded-shared.patch now builds libmysql.so
mkdir libmysqld/work
cd libmysqld/work
#ar -x ../libmysqld.a
# these result in missing dependencies: (filed upstream as bug 59104)
#rm -f sql_binlog.cc.o rpl_utility.cc.o
#gcc $CFLAGS $LDFLAGS -shared -Wl,-soname,libmysqld.so.0 -o libmysqld.so.0.0.1 \
#	*.o ../../probes_mysql.o \
#	-lpthread -laio -lcrypt -lssl -lcrypto -lz -lrt -lstdc++ -ldl -lm -lc
# this is to check that we built a complete library
cp %{SOURCE9} .
ln -s ../libmysqld.so libmysqld.so.0
gcc -I../../include $CFLAGS mysql-embedded-check.c libmysqld.so.0
LD_LIBRARY_PATH=. ldd ./a.out
cd ../..

%if %runselftest
  # hack to let 32- and 64-bit tests run concurrently on same build machine
  case `uname -m` in
    ppc64 | s390x | x86_64 | sparc64 )
      MTR_BUILD_THREAD=7
      ;;
    *)
      MTR_BUILD_THREAD=11
      ;;
  esac
  export MTR_BUILD_THREAD

  make test

  # The cmake build scripts don't provide any simple way to control the
  # options for mysql-test-run, so ignore the make target and just call it
  # manually.  Nonstandard options chosen are:
  # --force to continue tests after a failure
  # no retries please
  # test SSL with --ssl
  # skip tests that are listed in rh-skipped-tests.list
  # avoid redundant test runs with --binlog-format=mixed
  # increase timeouts to prevent unwanted failures during mass rebuilds
  (
    cd mysql-test
    perl ./mysql-test-run.pl --force --retry=0 --ssl \
	--skip-test-list=rh-skipped-tests.list \
	--mysqld=--binlog-format=mixed \
	--suite-timeout=720 --testcase-timeout=30
    # cmake build scripts will install the var cruft if left alone :-(
    rm -rf var
  ) 
%endif

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p %{buildroot}/var/log/mysql \
#         %{buildroot}/var/lib/mysqllogs \
#         %{buildroot}/var/lib/mysqltmp

make DESTDIR=$RPM_BUILD_ROOT install

# List the installed tree for RPM package maintenance purposes.
find $RPM_BUILD_ROOT -print | sed "s|^$RPM_BUILD_ROOT||" | sort > ROOTFILES

# multilib header hacks
# we only apply this to known Red Hat multilib arches, per bug #181335
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | s390 | s390x | sparc | sparc64 )
    mv $RPM_BUILD_ROOT%{install_root}/include/mysql/my_config.h $RPM_BUILD_ROOT%{install_root}/include/mysql/my_config_`uname -i`.h
    install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{install_root}/include/mysql
    ;;
  *)
    ;;
esac

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' -e 's:/usr//opt/:/data/app/:'\
	${RPM_BUILD_ROOT}%{install_path}/bin/mysql_config >mysql_config.tmp
cp -f mysql_config.tmp ${RPM_BUILD_ROOT}%{install_path}/bin/mysql_config
chmod 755 ${RPM_BUILD_ROOT}%{install_path}/bin/mysql_config

# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also mysql-file-contents.patch)
install -m 644 Docs/INFO_SRC ${RPM_BUILD_ROOT}%{lib_path}/mysql/
install -m 644 Docs/INFO_BIN ${RPM_BUILD_ROOT}%{lib_path}/mysql/

mkdir -p $RPM_BUILD_ROOT/data/logs/mysql/3306
mkdir -p $RPM_BUILD_ROOT/data/mysql/mysql_3306
touch $RPM_BUILD_ROOT/data/logs/mysql/3306/mysqld.log
touch $RPM_BUILD_ROOT/data/logs/mysql/query.log
touch $RPM_BUILD_ROOT/data/logs/mysql/3306/slow_query.txt

mkdir -p $RPM_BUILD_ROOT/var/run/mysqld
#install -m 0755 -d $RPM_BUILD_ROOT/var/lib/mysql
%if 0%{?fedora} < 15
mkdir -p %{install_path}/init.d
install -m 0755 -D %{SOURCE2} %{buildroot}%{install_path}/init.d/mysqld
%endif

mkdir -p $RPM_BUILD_ROOT%{conf_path}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{conf_path}/my.cnf

%if 0%{?fedora} > 14
# install systemd unit files and scripts for handling server startup
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{install_path}/libexec
install -m 644 %{SOURCE11} ${RPM_BUILD_ROOT}%{_unitdir}/
install -m 755 %{SOURCE12} ${RPM_BUILD_ROOT}%{install_path}/libexec
install -m 755 %{SOURCE13} ${RPM_BUILD_ROOT}%{install_path}/libexec

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/mysql.conf
%endif

# Fix scripts for multilib safety
mv ${RPM_BUILD_ROOT}%{install_path}/bin/mysqlbug ${RPM_BUILD_ROOT}%{lib_path}/mysql/mysqlbug
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{install_path}/bin/mysqlbug
mv ${RPM_BUILD_ROOT}%{install_path}/bin/mysql_config ${RPM_BUILD_ROOT}%{lib_path}/mysql/mysql_config
install -m 0755 scriptstub ${RPM_BUILD_ROOT}%{install_path}/bin/mysql_config

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f ${RPM_BUILD_ROOT}%{lib_path}/mysql/libmysqlclient_r.so*
ln -s libmysqlclient.so ${RPM_BUILD_ROOT}%{lib_path}/mysql/libmysqlclient_r.so

# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv ${RPM_BUILD_ROOT}%{install_path}/share/mysql-test/lib/My/SafeProcess/my_safe_process ${RPM_BUILD_ROOT}%{install_path}/bin
ln -s ../../../../../bin/my_safe_process ${RPM_BUILD_ROOT}%{install_path}/share/mysql-test/lib/My/SafeProcess/my_safe_process

# Remove files that %%doc will install in preferred location
rm -f ${RPM_BUILD_ROOT}%{install_path}/COPYING
rm -f ${RPM_BUILD_ROOT}%{install_path}/README

# Remove files we don't want installed at all
rm -f ${RPM_BUILD_ROOT}%{install_path}/INSTALL-BINARY
rm -f ${RPM_BUILD_ROOT}%{install_path}/docs/ChangeLog
rm -f ${RPM_BUILD_ROOT}%{install_path}/data/mysql/.empty
rm -f ${RPM_BUILD_ROOT}%{install_path}/data/test/.empty
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/mysql/solaris/postinstall-solaris

# should move this to /etc/ ?
rm -f ${RPM_BUILD_ROOT}%{install_path}/bin/mysqlaccess.conf
rm -f ${RPM_BUILD_ROOT}%{install_path}/bin/mysql_embedded
rm -f ${RPM_BUILD_ROOT}%{lib_path}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/mysql/magic
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/mysql/ndb-config-2-node.ini
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/mysql/mysqld_multi.server
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/man/man1/comp_err.1*
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/man/man1/mysql-stress-test.pl.1*
rm -f ${RPM_BUILD_ROOT}%{install_path}/share/man/man1/mysql-test-run.pl.1*

# put logrotate script where it needs to be
mkdir -p $RPM_BUILD_ROOT/data/app/logrotate.d
mv ${RPM_BUILD_ROOT}%{install_path}/share/mysql/mysql-log-rotate $RPM_BUILD_ROOT/data/app/logrotate.d/mysqld
chmod 644 $RPM_BUILD_ROOT/data/app/logrotate.d/mysqld

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
echo "%{lib_path}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf
echo 'export PATH="$PATH:/data/app/mysql/bin"' > $RPM_BUILD_ROOT/etc/profile.d/uuzu-mysql.sh

# copy additional docs into build tree so %%doc will find them
cp %{SOURCE6} README.mysql-docs
cp %{SOURCE7} README.mysql-license

# install the list of skipped tests to be available for user runs
install -m 0644 mysql-test/rh-skipped-tests.list ${RPM_BUILD_ROOT}%{install_path}/share/mysql-test
#mkdir -p $RPM_BUILD_ROOT%{install_path}/libexec
#mv $RPM_BUILD_ROOT%{install_path}/bin/mysqld $RPM_BUILD_ROOT%{install_path}/libexec/mysqld
find $RPM_BUILD_ROOT -type f | xargs grep '/usr//data' | sed '/Binary/d' | awk -F : '{print $1}' | sort | uniq  | xargs -I{} sed -i 's:/usr//data:/data/:' {}
find $RPM_BUILD_ROOT -type f | xargs grep '/usr//usr' | sed '/Binary/d' | awk -F : '{print $1}' | sort | uniq  | xargs -I{} sed -i 's:/usr//usr:/usr:' {}
find $RPM_BUILD_ROOT -type f | xargs grep '/usr/usr' | sed '/Binary/d' | awk -F : '{print $1}' | sort | uniq  | xargs -I{} sed -i 's:/usr/usr:/usr:' {}

%clean
rm -rf $RPM_BUILD_ROOT

%post
mkdir -p /opt/{17173,logs}
ln -fs %{install_path} /opt/uuzu/%{srcname}
ln -fs %{install_path}/conf/my.cnf /etc/my.cnf
. /etc/profile

%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -s /sbin/nologin -M -N -g mysql -o -r -d %{install_root}/logs/mysql -s /bin/bash \
	-c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :

%post libs
/sbin/ldconfig


%post server
mkdir -p /opt/17173
ln -fs %{install_path}/init.d/mysqld /etc/rc.d/init.d/mysqld
ln -fs %{install_path}/conf/my.cnf /etc/my.cnf
ln -fs %{install_root}/logrotate.d/mysqld /etc/logrotate.d/mysqld
/sbin/chkconfig --add mysqld

%preun server
/sbin/service mysqld stop >/dev/null 2>&1
/sbin/chkconfig --del mysqld


%postun libs
/sbin/ldconfig

%postun server
/sbin/service mysqld stop
rm -f /etc/rc.d/init.d/mysqld /etc/my.cnf /etc/logrotate.d/mysqld 


%files
%defattr(-,root,root)
%doc README COPYING README.mysql-license
%doc README.mysql-docs

%{install_path}/bin/msql2mysql
%{install_path}/bin/mysql
%{install_path}/bin/mysql_config
%{install_path}/bin/mysql_find_rows
%{install_path}/bin/mysql_waitpid
%{install_path}/bin/mysqlaccess
%{install_path}/bin/mysqladmin
%{install_path}/bin/mysqlbinlog
%{install_path}/bin/mysqlcheck
%{install_path}/bin/mysqldump
%{install_path}/bin/mysqlimport
%{install_path}/bin/mysqlshow
%{install_path}/bin/mysqlslap
%{install_path}/bin/my_print_defaults
%{install_path}/bin/mysql_config_editor

%{install_path}/share/man/man1/mysql.1*
%{install_path}/share/man/man1/mysql_config.1*
%{install_path}/share/man/man1/mysql_find_rows.1*
%{install_path}/share/man/man1/mysql_waitpid.1*
%{install_path}/share/man/man1/mysqlaccess.1*
%{install_path}/share/man/man1/mysqladmin.1*
%{install_path}/share/man/man1/mysqldump.1*
%{install_path}/share/man/man1/mysqlshow.1*
%{install_path}/share/man/man1/mysqlslap.1*
%{install_path}/share/man/man1/my_print_defaults.1*
%{install_path}/share/man/man1/mysql_config_editor.1*

%{lib_path}/mysql/mysql_config
/data/logs/mysql/query.log
/etc/profile.d/uuzu-mysql.sh

%files libs
%defattr(-,root,root)
%doc README COPYING README.mysql-license
# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) %{install_path}/conf/my.cnf
%dir %{lib_path}/mysql
%{lib_path}/mysql/libmysqlclient.so.*
/etc/ld.so.conf.d/*

%dir %{install_path}/share/mysql
%{install_path}/share/mysql/english
%lang(cs) %{install_path}/share/mysql/czech
%lang(da) %{install_path}/share/mysql/danish
%lang(nl) %{install_path}/share/mysql/dutch
%lang(et) %{install_path}/share/mysql/estonian
%lang(fr) %{install_path}/share/mysql/french
%lang(de) %{install_path}/share/mysql/german
%lang(el) %{install_path}/share/mysql/greek
%lang(hu) %{install_path}/share/mysql/hungarian
%lang(it) %{install_path}/share/mysql/italian
%lang(ja) %{install_path}/share/mysql/japanese
%lang(ko) %{install_path}/share/mysql/korean
%lang(no) %{install_path}/share/mysql/norwegian
%lang(no) %{install_path}/share/mysql/norwegian-ny
%lang(pl) %{install_path}/share/mysql/polish
%lang(pt) %{install_path}/share/mysql/portuguese
%lang(ro) %{install_path}/share/mysql/romanian
%lang(ru) %{install_path}/share/mysql/russian
%lang(sr) %{install_path}/share/mysql/serbian
%lang(sk) %{install_path}/share/mysql/slovak
%lang(es) %{install_path}/share/mysql/spanish
%lang(sv) %{install_path}/share/mysql/swedish
%lang(uk) %{install_path}/share/mysql/ukrainian
%lang(bg) %{install_path}/share/mysql/bulgarian
%{install_path}/share/mysql/charsets

%files server
%defattr(-,root,root)
%doc support-files/*.cnf

%{install_path}/bin/myisamchk
%{install_path}/bin/myisam_ftdump
%{install_path}/bin/myisamlog
%{install_path}/bin/myisampack
%{install_path}/bin/mysql_convert_table_format
%{install_path}/bin/mysql_fix_extensions
%{install_path}/bin/mysql_install_db
%{install_path}/bin/mysql_plugin
%{install_path}/bin/mysql_secure_installation
%{install_path}/bin/mysql_setpermission
%{install_path}/bin/mysql_tzinfo_to_sql
%{install_path}/bin/mysql_upgrade
%{install_path}/bin/mysql_zap
%{install_path}/bin/mysqlbug
%{install_path}/bin/mysqldumpslow
%{install_path}/bin/mysqld_multi
%{install_path}/bin/mysqld_safe
%{install_path}/bin/mysqlhotcopy
%{install_path}/bin/mysqltest
%{install_path}/bin/innochecksum
%{install_path}/bin/perror
%{install_path}/bin/replace
%{install_path}/bin/resolve_stack_dump
%{install_path}/bin/resolveip
%{install_path}/bin/mysqld


%{lib_path}/mysql/INFO_SRC
%{lib_path}/mysql/INFO_BIN

%{lib_path}/mysql/mysqlbug

%{lib_path}/mysql/plugin

%{install_path}/share/man/man1/msql2mysql.1*
%{install_path}/share/man/man1/myisamchk.1*
%{install_path}/share/man/man1/myisamlog.1*
%{install_path}/share/man/man1/myisampack.1*
%{install_path}/share/man/man1/mysql_convert_table_format.1*
%{install_path}/share/man/man1/myisam_ftdump.1*
%{install_path}/share/man/man1/mysql.server.1*
%{install_path}/share/man/man1/mysql_fix_extensions.1*
%{install_path}/share/man/man1/mysql_install_db.1*
%{install_path}/share/man/man1/mysql_plugin.1*
%{install_path}/share/man/man1/mysql_secure_installation.1*
%{install_path}/share/man/man1/mysql_upgrade.1*
%{install_path}/share/man/man1/mysql_zap.1*
%{install_path}/share/man/man1/mysqlbug.1*
%{install_path}/share/man/man1/mysqldumpslow.1*
%{install_path}/share/man/man1/mysqlbinlog.1*
%{install_path}/share/man/man1/mysqlcheck.1*
%{install_path}/share/man/man1/mysqld_multi.1*
%{install_path}/share/man/man1/mysqld_safe.1*
%{install_path}/share/man/man1/mysqlhotcopy.1*
%{install_path}/share/man/man1/mysqlimport.1*
%{install_path}/share/man/man1/mysqlman.1*
%{install_path}/share/man/man1/mysql_setpermission.1*
%{install_path}/share/man/man1/mysqltest.1*
%{install_path}/share/man/man1/innochecksum.1*
%{install_path}/share/man/man1/perror.1*
%{install_path}/share/man/man1/replace.1*
%{install_path}/share/man/man1/resolve_stack_dump.1*
%{install_path}/share/man/man1/resolveip.1*
%{install_path}/share/man/man1/mysql_tzinfo_to_sql.1*
%{install_path}/share/man/man8/mysqld.8*

%{install_path}/share/mysql/errmsg-utf8.txt
%{install_path}/share/mysql/fill_help_tables.sql
%{install_path}/share/mysql/mysql_system_tables.sql
%{install_path}/share/mysql/mysql_system_tables_data.sql
%{install_path}/share/mysql/mysql_test_data_timezone.sql
%{install_path}/share/mysql/innodb_memcached_config.sql
%{install_path}/share/mysql/mysql_security_commands.sql
%{install_path}/share/mysql/dictionary.txt

%{install_path}/share/mysql/my-*.cnf

%{install_path}/init.d/mysqld

%attr(0755,mysql,mysql) %dir /var/run/mysqld
#%attr(0755,mysql,mysql) %dir /var/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /data/logs/mysql/3306/mysqld.log
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /data/logs/mysql/3306/slow_query.txt
%config(noreplace) /data/app/logrotate.d/mysqld
#%attr(0755,mysql,mysql) %dir /var/lib/mysqltmp/
#%attr(0755,mysql,mysql) %dir /var/lib/mysqllogs
%attr(0755,mysql,mysql) %dir /data/logs/mysql/
%attr(0755,mysql,mysql) %dir /data/logs/mysql/3306/
%attr(0755,mysql,mysql) %dir /data/mysql/mysql_3306/


%files devel
%defattr(-,root,root)
%{install_root}/include/mysql
/usr/share/aclocal/mysql.m4
%{lib_path}/mysql/libmysqlclient.so
%{lib_path}/mysql/libmysqlclient_r.so

%files embedded
%defattr(-,root,root)
#%doc README COPYING README.mysql-license
%{lib_path}/mysql/libmysqld.so.*

%files embedded-devel
%defattr(-,root,root)
%{lib_path}/mysql/libmysqld.so
%{install_path}/bin/mysql_client_test_embedded
%{install_path}/bin/mysqltest_embedded
%{install_path}/share/man/man1/mysql_client_test_embedded.1*
%{install_path}/share/man/man1/mysqltest_embedded.1*

%files bench
%defattr(-,root,root)
%{install_path}/share/sql-bench

%files test
%defattr(-,root,root)
%{install_path}/bin/mysql_client_test
%{install_path}/bin/my_safe_process
%attr(-,mysql,mysql) %{install_path}/share/mysql-test

%{install_path}/share/man/man1/mysql_client_test.1*

%changelog
* Thu Jun 12 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 5.6.14-4
- mv share from /usr to install_path
* Wed Dec 25 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 5.6.14-3
- add file /data/logs/mysql/query.log
- make default data dir /data/mysql/mysql_3306
- change default config file my.cnf
* Tue Dec 19 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> -  5.6.14-2
- mysql user use nologin shell

* Tue Feb 12 2013 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.6.10-2
- Forked from lp:~muzazzi/ius/mysql56 
- Disabled test suite for time being

