%global  nginx_user          nginx
%global  nginx_group         %{nginx_user}

%define srcname nginx
%define install_root   /data/app
%define install_path   %{install_root}/%{srcname}
%define init_dir      %{install_path}/init.d
%define include_path   %{install_root}/include
%define lib_path %{install_root}/%{_lib}
%define logrotate_dir %{install_root}/logrotate.d
%define conf_path      %{install_path}/conf
%define bin_path       %{install_path}/bin
%define sbin_path       %{install_path}/sbin
%define nginx_tmp      %{install_path}/tmp
%define log_path       /data/logs/nginx
%define  nginx_webroot       %{install_path}/html

#off debug package rpmbuild have a bug con't build the debuginfo package
%define debug_package %{nil}

Name:              uuzu-nginx
Version:           1.4.4
Release:           8%{?dist}

Summary:           A high performance web server and reverse proxy server
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://nginx.org/

Source0:           http://nginx.org/download/nginx-%{version}.tar.gz
Source1:           nginx.init
Source2:           nginx.logrotate
Source3:           nginx.conf
Source4:           default.conf
Source5:           ssl.conf
Source6:           virtual.conf
#Source7:           nginx.sysconfig
Source8:           ngx_devel_kit-0.2.19.tar.gz
Source9:           lua-nginx-module-0.9.2.tar.gz
Source10:           Nginx_upstream_hash-0.3.1.tar.gz
Source11:           set-misc-nginx-module-0.23.tar.gz
Source12:           headers-more-nginx-module-0.24.tar.gz
Source13:           echo-nginx-module-0.50.tar.gz
Source14:           memc-nginx-module-0.14.tar.gz
Source15:           redis2-nginx-module-0.10.tar.gz
Source16:           ngx_cache_purge-master.zip
Source17:           limitCompany
Source18:           limitTest
Source19:           spider
Source20:           robots
Source21:           mime.types
Source22:           nginx-push-stream-module-0.4.0.tar.gz
# Source23:           ngx_http_dyups_module-master.zip
Source24:           iconv-nginx-module.tar.gz
Source25:           nginx_upstream_check_module-0.3.0.tar.gz
Source100:         index.html
Source101:         poweredby.png
Source102:         nginx-logo.png
Source103:         404.html
Source104:         50x.html

# removes -Werror in upstream build scripts.  -Werror conflicts with
# -D_FORTIFY_SOURCE=2 causing warnings to turn into errors.
Patch0:     nginx-auto-cc-gcc.patch


BuildRequires:     uuzu-GeoIP-devel
BuildRequires:     uuzu-gd-devel
BuildRequires:     libxslt-devel
BuildRequires:     openssl-devel
BuildRequires:     pcre-devel
BuildRequires:     perl-devel
BuildRequires:     perl(ExtUtils::Embed)
BuildRequires:     zlib-devel
BuildRequires:     uuzu-luajit-devel
Requires:          uuzu-GeoIP
Requires:          uuzu-luajit
Requires:          uuzu-gd
Requires:          openssl
Requires:          pcre
Requires:          perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):     shadow-utils
Requires(post):    chkconfig
Requires(preun):   chkconfig, initscripts
Requires(postun):  initscripts
Provides:          webserver

%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.


%prep
%setup -q -n %{srcname}-%{version}
%setup -T -D -n %{srcname}-%{version} -a 8
%setup -T -D -n %{srcname}-%{version} -a 9
%setup -T -D -n %{srcname}-%{version} -a 10
%setup -T -D -n %{srcname}-%{version} -a 11
%setup -T -D -n %{srcname}-%{version} -a 12
%setup -T -D -n %{srcname}-%{version} -a 13
%setup -T -D -n %{srcname}-%{version} -a 14
%setup -T -D -n %{srcname}-%{version} -a 15
%setup -T -D -n %{srcname}-%{version} -a 16
%setup -T -D -n %{srcname}-%{version} -a 22
# %setup -T -D -n %{srcname}-%{version} -a 23
%setup -T -D -n %{srcname}-%{version} -a 24
%setup -T -D -n %{srcname}-%{version} -a 25



%build
# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export LUAJIT_LIB=%{lib_path}
export LUAJIT_INC=%{include_path}/luajit-2.0/

export DESTDIR=%{buildroot}

#patch for nginx_upstream_hash
patch -p0 < %{_builddir}/%{srcname}-%{version}/nginx_upstream_hash-0.3.1/nginx.patch

#patch for nginx upstream check 
patch -p1 < %{_builddir}/%{srcname}-%{version}/nginx_upstream_check_module-0.3.0/check_1.2.6+.patch

./configure \
    --prefix=%{_prefix} \
    --sbin-path=%{sbin_path}/nginx \
    --conf-path=%{conf_path}/nginx.conf \
    --error-log-path=%{log_path}/error.log \
    --http-log-path=%{log_path}/access.log \
    --http-client-body-temp-path=%{nginx_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_tmp}/fastcgi \
    --http-uwsgi-temp-path=%{nginx_tmp}/uwsgi \
    --http-scgi-temp-path=%{nginx_tmp}/scgi \
    --pid-path=%{_localstatedir}/run/nginx.pid \
    --lock-path=%{_localstatedir}/lock/subsys/nginx \
    --user=%{nginx_user} \
    --group=%{nginx_group} \
    --with-file-aio \
    --with-ipv6 \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_xslt_module \
    --with-http_image_filter_module \
    --with-http_geoip_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gzip_static_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_stub_status_module \
    --with-http_perl_module \
    --with-http_gunzip_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-debug \
    --with-cc-opt="%{optflags} $(pcre-config --cflags) -I %{include_path}" \
    --with-ld-opt="-Wl,-E -L %{lib_path}" \
    --add-module=%{_builddir}/%{srcname}-%{version}/ngx_devel_kit-0.2.19 \
    --add-module=%{_builddir}/%{srcname}-%{version}/lua-nginx-module-0.9.2 \
    --add-module=%{_builddir}/%{srcname}-%{version}/set-misc-nginx-module-0.23 \
    --add-module=%{_builddir}/%{srcname}-%{version}/nginx_upstream_hash-0.3.1 \
    --add-module=%{_builddir}/%{srcname}-%{version}/headers-more-nginx-module-0.24 \
    --add-module=%{_builddir}/%{srcname}-%{version}/echo-nginx-module-0.50 \
    --add-module=%{_builddir}/%{srcname}-%{version}/memc-nginx-module-0.14 \
    --add-module=%{_builddir}/%{srcname}-%{version}/redis2-nginx-module-0.10 \
    --add-module=%{_builddir}/%{srcname}-%{version}/ngx_cache_purge-master \
    --add-module=%{_builddir}/%{srcname}-%{version}/nginx-push-stream-module-0.4.0 \
    --add-module=%{_builddir}/%{srcname}-%{version}/nginx_upstream_check_module-0.3.0 \
    --add-module=%{_builddir}/%{srcname}-%{version}/iconv-nginx-module

#    --add-module=%{_builddir}/%{srcname}-%{version}/ngx_http_dyups_module-master \

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

install -p -D -m 0755 %{SOURCE1} \
    %{buildroot}%{init_dir}/nginx
install -p -D -m 0644 %{SOURCE2} \
    %{buildroot}%{logrotate_dir}/nginx
#install -p -D -m 0644 %{SOURCE7} \
#    %{buildroot}%{_sysconfdir}/sysconfig/nginx

install -p -d -m 0755 %{buildroot}%{conf_path}/vhosts
install -p -d -m 0700 %{buildroot}%{install_path}
install -p -d -m 0700 %{buildroot}%{nginx_tmp}
install -p -d -m 0700 %{buildroot}%{log_path}
install -p -d -m 0755 %{buildroot}%{nginx_webroot}

install -p -m 0644 %{SOURCE3} \
    %{buildroot}%{conf_path}
install -p -m 0644 %{SOURCE4} %{SOURCE5} %{SOURCE6} \
    %{buildroot}%{conf_path}/vhosts
install -p -m 0644 %{SOURCE100} \
    %{buildroot}%{nginx_webroot}
install -p -m 0644 %{SOURCE101} %{SOURCE102} \
    %{buildroot}%{nginx_webroot}
install -p -m 0644 %{SOURCE103} %{SOURCE104} \
    %{buildroot}%{nginx_webroot}

install -p -D -m 0644 %{_builddir}/nginx-%{version}/man/nginx.8 \
    %{buildroot}%{_mandir}/man8/nginx.8
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d/
ln -sf %{init_dir}/%{srcname} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
ln -sf %{logrotate_dir}/%{srcname} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
rm -rf %{buildroot}/usr/html
mkdir -p %{log_path}

mkdir -p %{buildroot}%{conf_path}/mod/{ssl,limit,spider}
install -p -D -m 0644 %{SOURCE17} \
    %{buildroot}%{conf_path}/mod/limit/
install -p -D -m 0644 %{SOURCE18} \
    %{buildroot}%{conf_path}/mod/limit/
install -p -D -m 0644 %{SOURCE19} \
    %{buildroot}%{conf_path}/mod/spider/
install -p -D -m 0644 %{SOURCE20} \
    %{buildroot}%{conf_path}/mod/spider/
install -p -D -m 0644 %{SOURCE21} \
    %{buildroot}%{conf_path}/

%pre
getent group %{nginx_group} > /dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} > /dev/null || \
    useradd -r -d %{install_path} -g %{nginx_group} \
    -s /sbin/nologin -c "Nginx web server" %{nginx_user}
exit 0

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi
if [ $1 -eq 2 ]; then
    # Make sure these directories are not world readable.
    chmod 755 %{install_path}
    chmod 755 %{nginx_tmp}
    chmod 755 %{log_path}
fi
sed -i "s/INTERNALIP/$(ifconfig | egrep "10\.(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){2}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])" | cut -d":" -f2 | cut -d' ' -f1 | head -1)/" %{conf_path}/nginx.conf

%preun
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -eq 2 ]; then
    /sbin/service %{name} upgrade || :
fi

%files
%doc LICENSE CHANGES README
#%{_prefix}/
%{nginx_webroot}/
%{sbin_path}/nginx
%{_mandir}/man3/nginx.3pm*
%{_mandir}/man8/nginx.8*
%{init_dir}/nginx
%{_sysconfdir}/rc.d/init.d/%{name}
%{_sysconfdir}/logrotate.d/%{name}
/data/app/%{srcname}
%dir %{conf_path}
%dir %{conf_path}/vhosts
%dir %{conf_path}/mod/limit
%dir %{conf_path}/mod/spider
%dir %{conf_path}/mod/ssl
%config(noreplace) %{conf_path}/fastcgi.conf
%config(noreplace) %{conf_path}/fastcgi.conf.default
%config(noreplace) %{conf_path}/fastcgi_params
%config(noreplace) %{conf_path}/fastcgi_params.default
%config(noreplace) %{conf_path}/koi-utf
%config(noreplace) %{conf_path}/koi-win
%config(noreplace) %{conf_path}/mime.types
%config(noreplace) %{conf_path}/mime.types.default
%config(noreplace) %{conf_path}/nginx.conf
%config(noreplace) %{conf_path}/nginx.conf.default
%config(noreplace) %{conf_path}/scgi_params
%config(noreplace) %{conf_path}/scgi_params.default
%config(noreplace) %{conf_path}/uwsgi_params
%config(noreplace) %{conf_path}/uwsgi_params.default
%config(noreplace) %{conf_path}/win-utf
%config(noreplace) %{conf_path}/vhosts/*.conf
%config(noreplace) %{conf_path}/mod/limit/limitCompany
%config(noreplace) %{conf_path}/mod/limit/limitTest
%config(noreplace) %{conf_path}/mod/spider/spider
%config(noreplace) %{conf_path}/mod/spider/robots
%config(noreplace) %{logrotate_dir}/nginx
#%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%dir %{perl_vendorarch}/auto/nginx
%dir %{log_path}
%{perl_vendorarch}/nginx.pm
%{perl_vendorarch}/auto/nginx/nginx.so
%attr(700,%{nginx_user},%{nginx_group}) %dir %{install_path}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_tmp}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{log_path}


%changelog
* Wed Feb 11 2015 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.4.4-7
-fix chmod 0700 to 0755.

* Fri Oct 17 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.4.4-6
-add mod iconv-nginx-module

* Mon Oct 13 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.4.4-5
-add mod ngx_http_dyups_module

* Wed May 28 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.4.4-4
-add mod push-stream

* Thu Feb 27 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.4.4-3
-add mod memc
-add mod redis2
-add mod ngx_cache_purge

* Mon Dec 23 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 1.4.4-2
-add mod upstream hash
-add mod set misc
-add mod headers more
-add mod echo

* Tue Nov 26 2013 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 1.4.4-1
-update to 1.4.4
-add lua mode
-change libgd,GeoIP path

* Fri Apr 26 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.0.15-5
- enable debugging (#956845)
- trim changelog
