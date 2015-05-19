
%define srcname        GeoIP
%define install_root   /data/app
%define install_path   %{install_root}/%{srcname}
%define include_path   %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define bin_path       %{install_path}/bin
%define conf_path      %{install_path}/conf

#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

Name: uuzu-GeoIP           
Version: 1.4.8
Release: 1%{?dist}
Summary: C library for country/city/organization to IP address or hostname mapping     
Group: Development/Libraries         
License: LGPLv2+
URL: http://www.maxmind.com/app/c            
Source0: http://www.maxmind.com/download/geoip/api/c/GeoIP-%{version}.tar.gz 
Source1: LICENSE.txt
Source2: fetch-geoipdata-city.pl
Source3: fetch-geoipdata.pl
Source4: README.Fedora
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: geoip < %{version}-%{release}
Provides: uuzu-geoip = %{version}-%{release}
BuildRequires: zlib-devel

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. It uses a file based database that is
accurate as of March 2003. This database simply contains IP blocks as keys, and
countries as values. This database should be more complete and accurate than
using reverse DNS lookups.

%package devel
Summary: Development headers and libraries for GeoIP     
Group: Development/Libraries         
Requires: %{name} = %{version}-%{release}
Provides: uuzu-geoip-devel = %{version}-%{release}
Obsoletes: geoip-devel < %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP-based applications

%prep
%setup -q -n %{srcname}-%{version}
install -D -m644 %{SOURCE1} LICENSE.txt
install -D -m644 %{SOURCE2} fetch-geoipdata-city.pl
install -D -m644 %{SOURCE3} fetch-geoipdata.pl
install -D -m644 %{SOURCE4} README.fedora

%build
./configure --prefix=%{_prefix} \
 --sysconfdir=%{conf_path} \
 --libdir=%{lib_path} \
 --bindir=%{bin_path} \
 --includedir=%{include_path} \
 --disable-static \
 --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# nix the stuff we don't need like .la files.
rm -f %{buildroot}/%{lib_path}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO INSTALL LICENSE* fetch-*
%{lib_path}/libGeoIP.so.*
%{lib_path}/libGeoIPUpdate.so.*
%{bin_path}/geoiplookup6
%{bin_path}/geoiplookup
%{bin_path}/geoipupdate
%config(noreplace) %{conf_path}/GeoIP.conf.default
%config(noreplace) %{conf_path}/GeoIP.conf
%{_datadir}/GeoIP
%{_mandir}/man1/geoiplookup.1*
%{_mandir}/man1/geoiplookup6.1*
%{_mandir}/man1/geoipupdate.1*

%files devel
%defattr(-,root,root,-)
%{include_path}/GeoIP.h
%{include_path}/GeoIPCity.h
%{include_path}/GeoIPUpdate.h
%{lib_path}/libGeoIP.so
%{lib_path}/libGeoIPUpdate.so

%changelog
* Tue Sep 06 2011 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 1.4.8-1
- Update to 1.4.8
