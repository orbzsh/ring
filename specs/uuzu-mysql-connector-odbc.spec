#defined the path
%define srcname mysql-connector-odbc
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path %{install_path}/conf

#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

Name:		uuzu-%{srcname}
Version:	5.2.6
Release:	1%{?dist}
Summary:	ODBC driver for MySQL

Group:		System Environment/Libraries
License:	GPLv2 with exceptions
URL:		http://dev.mysql.com/downloads/connector/odbc/
Source0:	http://cdn.mysql.com/Downloads/Connector-ODBC/5.2/%{srcname}-5.2.6-src.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	unixODBC-devel uuzu-mysql-devel
Requires:	unixODBC uuzu-mysql-libs

%description
An ODBC (rev 3) driver for MySQL, for use with unixODBC.

%prep
%setup -q -n %{srcname}-%{version}-src


%build
export CFLAGS="%{optflags}"
cmake -G "Unix Makefiles"   \
    -DRPM_BUILD=1           \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DMYSQL_CONFIG_EXECUTABLE=/opt/uuzu/mysql/bin/mysql_config \
    -DMYSQL_LIB=/data/app/lib/mysql/libmysqlclient.so \
    -DINSTALL_LIBDIR=%{lib_path} \
    -DWITH_UNIXODBC=1
make  %{?_smp_mflags} VERBOSE=1


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install VERBOSE=1
#Change shared lib path,why the arg -DINSTALL_LIBDIR have no effect
mkdir -p %{buildroot}%{lib_path}
mv %{buildroot}/usr/lib64/*.so %{buildroot}%{lib_path}
#remove no used file include docs  
rm -rf %{buildroot}/usr
mkdir -p %{buildroot}/etc/ld.so.conf.d
#add ld.so.conf.d
echo "%{lib_path}" > %{buildroot}/etc/ld.so.conf.d/%{name}.conf

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%{lib_path}/*.so
/etc/ld.so.conf.d/%{name}.conf



%changelog
* Tue Feb 18 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com>
- create this file to build mysql-odbc driver 5.2.6 use mysql 5.6.4 for 17173 col
- remove all doc file and odbc install
