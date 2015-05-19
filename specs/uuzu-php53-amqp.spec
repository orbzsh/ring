%define pecl_name amqp
%define pecl_dir_name amqp

%define php_extdir %(/opt/uuzu/php/bin/php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define install_root   /data/app
%define include_path   %{install_root}/include
%define phpize /opt/uuzu/php/bin/phpize
%define debug_package %{nil}
Name:		uuzu-php-%{pecl_name}
Version:	1.2.0
Release:	1%{?dist}
Summary:	PHP extension for Communicate with any AMQP compliant server

Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source0:	%{pecl_name}-%{version}.tgz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXX)

Requires:	librabbitmq
BuildRequires:	uuzu-php-cli,uuzu-php-devel,librabbitmq-devel

%description
This extension can communicate with any AMQP spec 0-9-1 compatible server, such as RabbitMQ, OpenAMQP and Qpid, giving you the ability to create and delete exchanges and queues, as well as publish to any exchange and consume from any queue.


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

; ----- Options to use the amqp.
;  The host to which to connect.
;amqp.host = localhost
;  The virtual host on the broker to which to connect.
;amqp.vhost = /
;  The port on which to connect.
;amqp.port = 5672
;  The login to use while connecting to the broker.
;amqp.login = guest
;  The password to use while connecting to the broker.
;amqp.password = guest
;  Whether calls to AMQPQueue::get() and AMQPQueue::consume() should require that the client explicitly acknowledge messages. Setting this value to 1 will pass in the AMQP_AUTOACK flag to the above method calls if the flags field is omitted.
;amqp.auto_ack = 0
;  The minimum number of messages to require during a call to AMQPQueue::consume().
;amqp.min_messages = 0
;  The maximum number of messages to require during a call to AMQPQueue::consume().
;amqp.max_messages = 1
;  The number of messages to prefect from the server during a call to AMQPQueue::get() or AMQPQueue::consume() during which the AMQP_AUTOACK flag is not set.
;amqp.prefetch_count = 3
EOF


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) /opt/uuzu/php/conf/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so



%changelog
* Sun Jan 26 2014 Cheng Chen <chengchen_17173@cyou-inc.com> - 1.2.0-1
- Create this file
