%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7

%if 0%{?fedora} > 12
%global with_python3 1
%endif


%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch}/.*\.so$
%endif
%filter_setup
}


%global srcname pyzmq

%global run_tests 0

Name:           uuzu-python27-zmq
Version:        14.2.0
Release:        1%{?dist}
Summary:        Software library for fast, message-based applications

Group:          Development/Libraries
License:        LGPLv3+ and ASL 2.0
URL:            http://www.zeromq.org/bindings:python
# VCS:          git:http://github.com/zeromq/pyzmq.git
# git checkout with the commands:
# git clone http://github.com/zeromq/pyzmq.git pyzmq.git
# cd pyzmq.git
# git archive --format=tar --prefix=pyzmq-%%{version}/ %%{checkout} | xz -z --force - > pyzmq-%%{version}.tar.xz
Source0:        https://pypi.python.org/packages/source/p/pyzmq/pyzmq-%{version}.tar.gz

BuildRequires:  uuzu-python27-devel
BuildRequires:  uuzu-python27-setuptools
BuildRequires:  zeromq3-devel
BuildRequires:  uuzu-python27-nose

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools
BuildRequires:  python3-nose
%endif
Requires: zeromq3

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%package tests
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
Requires:       uuzu-python-zmq = %{version}-%{release}
%description tests
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the testsuite for the python bindings.


%if 0%{?with_python3}
%package -n python3-zmq
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
%description -n python3-zmq
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%package -n python3-zmq-tests
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
Requires:       python3-zmq = %{version}-%{release}
%description -n python3-zmq-tests
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the testsuite for the python bindings.

%endif


%prep
%setup -q -n %{srcname}-%{version}
# remove shebangs
for lib in zmq/eventloop/*.py; do
    sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
    touch -r $lib $lib.new &&
    mv $lib.new $lib
done

# remove excecutable bits
chmod -x examples/pubsub/topics_pub.py
chmod -x examples/pubsub/topics_sub.py

# delete hidden files
#find examples -name '.*' | xargs rm -v


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
rm -r %{py3dir}/examples

%endif


%build
export LIBRARY_PATH='/data/app/lib/'
CFLAGS="%{optflags}" %{__python} setupegg.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3



%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# remove tests doesn't work here, do that after running the tests

popd
%endif # with_python3


%{__python} setupegg.py install -O1 --skip-build --root %{buildroot}

# remove tests doesn't work here, do that after running the tests



%check
%if 0%{?run_tests}
    rm zmq/__*
    PYTHONPATH=%{buildroot}%{python_sitearch} \
        %{__python} setup.py test

    %if 0%{?with_python3}
    # there is no python3-nose yet
    pushd %{py3dir}
    rm zmq/__*
    PYTHONPATH=%{buildroot}%{python3_sitearch} \
        %{__python3} setup.py test
    popd
    %endif
%endif


%files
%defattr(-,root,root,-)
%{python_sitearch}/%{srcname}-*.egg-info
%{python_sitearch}/zmq
%exclude %{python_sitearch}/zmq/tests

%files tests
%defattr(-,root,root,-)
%{python_sitearch}/zmq/tests

%if 0%{?with_python3}
%files -n python3-zmq
%defattr(-,root,root,-)
# examples/
%{python3_sitearch}/%{srcname}-*.egg-info
%{python3_sitearch}/zmq
%exclude %{python3_sitearch}/zmq/tests

%files -n python3-zmq-tests
%defattr(-,root,root,-)
%{python3_sitearch}/zmq/tests
%endif


%changelog
* Thu Apr 24 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 14.2.0-1
- update to 14.2.0
