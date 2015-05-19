%define srcname salt
%define install_path   /data/app/%{srcname}-%{version}
%define bin_path       %{install_path}/bin
%define init_path      %{install_root}/init.d
%define conf_path      %{install_path}/conf
%define install_root   /data/app
%define python_bin     %{install_root}/python-2.7.6/bin
%define pybasever 2.7
%define __python_ver 27
%define __python %{python_bin}/python%{?pybasever}


%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}


Name:		uuzu-%{srcname}
Version:	2014.1.3
Release:	1%{?dist}
Summary:	A parallel remote execution system

Group:		17173 SYSTEM ALL
License:	ASL 2.0
URL:		http://saltstack.org/
Source0:	http://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz

Source1: %{srcname}-master
Source2: %{srcname}-syndic
Source3: %{srcname}-minion

BuildRoot: %{_tmppath}/%{srcname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: uuzu-python27-m2crypto
BuildRequires: uuzu-python27-crypto
BuildRequires: uuzu-python27-devel
BuildRequires: uuzu-python27-jinja2
BuildRequires: uuzu-python27-msgpack 
#BuildRequires: python-pip
BuildRequires: uuzu-python27-zmq
BuildRequires: uuzu-PyYAML

Requires: uuzu-python27-crypto
Requires: uuzu-python27-zmq
Requires: uuzu-python27-jinja2
Requires: uuzu-PyYAML
Requires: uuzu-python27-m2crypto
Requires: uuzu-python27-msgpack

Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts

%ifarch %{ix86} x86_64
Requires: dmidecode
%endif

Requires: pciutils
Requires: yum-utils
Requires: sshpass

%description
Salt is a distributed remote execution system used to execute commands and
query data. It was developed in order to bring the best solutions found in
the world of remote execution together and make them better, faster and more
malleable. Salt accomplishes this via its ability to handle larger loads of
information, and not just dozens, but hundreds or even thousands of individual
servers, handle them quickly and through a simple and manageable interface.

%package -n uuzu-salt-master
Summary: Management component for salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: salt = %{version}-%{release}

%description -n uuzu-salt-master
The Salt master is the central server to which all minions connect.

%package -n uuzu-salt-minion
Summary: Client component for salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: salt = %{version}-%{release}

%description -n uuzu-salt-minion
Salt minion is queried and controlled from the master.

%prep
%setup -q -n %{srcname}-%{version}


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{install_path}
mkdir -p %{buildroot}%{init_path}
mkdir -p %{buildroot}%{conf_path}

%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

#change bin path
mv %{buildroot}/data/app/bin %{buildroot}%{install_path}

#install initrd script
install -p %{SOURCE1} $RPM_BUILD_ROOT%{init_path}
install -p %{SOURCE2} $RPM_BUILD_ROOT%{init_path}
install -p %{SOURCE3} $RPM_BUILD_ROOT%{init_path}

#overridden default values
sed -i "s#processname:[ ]*/usr/bin/\(salt-[a-z]*\)#processname: %{bin_path}/\1#" $RPM_BUILD_ROOT%{init_path}/*
sed -i "s#^SALT\(MASTER\|SYNDIC\|MINION\)=/usr/bin/\(salt-[a-z]*\)#SALT\1=%{bin_path}/\2#" $RPM_BUILD_ROOT%{init_path}/*
sed -i "s#^PYTHON=.*#PYTHON=%{python_bin}/python%{?pybasever}#" $RPM_BUILD_ROOT%{init_path}/*
sed -i "s#^\(MASTER\|SYNDIC\|MINION\)_ARGS=.*#\1_ARGS=\"-c %{conf_path}\"#" $RPM_BUILD_ROOT%{init_path}/*

#remove docs

rm -rf %{buildroot}/data/app/share

%clean
rm -rf %{buildroot}

%preun -n uuzu-salt-master
  if [ $1 -eq 0 ]; then
      /bin/service salt-master stop >/dev/null 2>&1
      /sbin/service salt-syndic stop >/dev/null 2>&1
      /sbin/chkconfig --del salt-master
      /sbin/chkconfig --del salt-syndic
      rm -f %{_initrddir}/salt-master
  fi

%preun
  if [ $1 -eq 0 ] ; then
      /sbin/service salt-minion stop >/dev/null 2>&1
      /sbin/chkconfig --del salt-minion
      rm -f %{_initrddir}/salt-minion
  fi

%post -n uuzu-salt-master
  ln -s %{init_path}/salt-master %{_initrddir}/salt-master
  ln -s %{init_path}/salt-syndic %{_initrddir}/salt-syndic
  /sbin/chkconfig --add salt-master
  /sbin/chkconfig --add salt-syndic 

%post -n uuzu-salt-minion
  ln -s %{init_path}/salt-minion %{_initrddir}/salt-minion
  /sbin/chkconfig --add salt-minion

%postun -n uuzu-salt-master
  if [ "$1" -ge "1" ] ; then
      /sbin/service salt-master condrestart >/dev/null 2>&1 || :
      /sbin/service salt-syndic condrestart >/dev/null 2>&1 || :
  fi

%postun -n uuzu-salt-minion
  if [ "$1" -ge "1" ] ; then
      /sbin/service salt-minion condrestart >/dev/null 2>&1 || :
  fi


%files
%defattr(-,root,root,-)
%{python_sitelib}/%{srcname}/*
%{python_sitelib}/%{srcname}-%{version}-py?.?.egg-info

%files -n uuzu-salt-minion
%defattr(-,root,root)
%{bin_path}/salt-minion
%{bin_path}/salt-call
%attr(0755, root, root) %{init_path}/salt-minion

%files -n uuzu-salt-master
%defattr(-,root,root)
%{bin_path}/salt
%{bin_path}/salt-cloud
%{bin_path}/salt-cp
%{bin_path}/salt-key
%{bin_path}/salt-master
%{bin_path}/salt-run
%{bin_path}/salt-ssh
%{bin_path}/salt-syndic
%attr(0755, root, root) %{init_path}/salt-master
%attr(0755, root, root) %{init_path}/salt-syndic



%changelog
* Fri May 09 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2014.1.3-1
- create this file but have no default configure file
