#defined the path
%define srcname luajit
%define install_root /data/app
%define install_path %{install_root}/%{srcname}
#%define init_dir     %{install_path}/init.d
%define include_path %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define bin_path     %{install_path}/bin                 
#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}


Name:           uuzu-luajit
Version:        2.0.2
Release:        2%{?dist}
Summary:        Just-In-Time Compiler for Lua

Group:          uuzu/Languages
License:        MIT
URL:            http://luajit.org/luajit.html
Source0:        http://luajit.org/download/LuaJIT-%{version}.tar.gz

%description
LuaJIT implements the full set of language features defined by Lua 5.1.
The virtual machine (VM) is API- and ABI-compatible to the standard
Lua interpreter and can be deployed as a drop-in replacement.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%package static
Summary:        Static library for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
This package contains the static version of libluajit for %{name}.

%prep
%setup -q -n LuaJIT-%{version}

%build
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
make amalg Q= E=@: PREFIX=%{_prefix} \
        INSTALL_LIB=%{lib_path} \
	INSTALL_BIN=%{bin_path} \
	INSTALL_INC=%{include_path}/luajit-2.0 \
	CFLAGS="%{optflags}" %{?_smp_mflags}

%install
# PREREL= - disable -betaX suffix
# INSTALL_TNAME - executable name
make install INSTALL_TNAME=%{name} PREFIX=%{_prefix} \
        INSTALL_LIB=%{buildroot}%{lib_path} \
	INSTALL_BIN=%{buildroot}%{bin_path} \
	INSTALL_INC=%{buildroot}%{include_path}/luajit-2.0 \
	DESTDIR=%{buildroot}

mkdir -p %{buildroot}/opt/uuzu/

ln -s %{install_path} %{buildroot}/opt/uuzu/LuaJIT

%post
echo "/data/app/lib" > %{_sysconfdir}/ld.so.conf.d/%{name}.conf
/sbin/ldconfig

%postun
rm -f %{_sysconfdir}/ld.so.conf.d/%{name}.conf
/sbin/ldconfig

%files
# %%defattr(-,root,root,-) # no longer needed
%doc COPYRIGHT README doc/*.html doc/*.css doc/img/*.png
/opt/uuzu/*
%{bin_path}/luajit
%{bin_path}/%{name}
%{lib_path}/libluajit*.so.*
%{_mandir}/man1/luajit*
%{_datadir}/%{srcname}-%{version}/
# directories that might contain libraries/modules
%dir %{lib_path}/lua
%dir %{lib_path}/lua/5.1
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.1

%files devel
%defattr(-,root,root,-)
%{include_path}/luajit-2.0/l*.h
%{include_path}/luajit-2.0/l*.hpp
%{lib_path}/libluajit*.so
%{lib_path}/pkgconfig/*.pc
#%dir %{install_path}/luajit-2.0

%files static
%defattr(-,root,root,-)
%{lib_path}/*.a

%changelog
* Fri Oct 25 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.0.2-1
- Change to 17173 corp dir 
