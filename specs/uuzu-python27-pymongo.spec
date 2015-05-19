%define __python /data/app/python/bin/python%{pybasever}
%define pybasever 2.7
%define srcname pymongo
%define realname python27-pymongo
%if 0%{?fedora} > 17
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

# Fix private-shared-object-provides error
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}

Name:           uuzu-python27-pymongo
Version:        2.7
Release:        1%{?dist}
Summary:        Python driver for MongoDB

Group:          Development/Languages
License:        Apache License, Version 2.0
URL:            http://api.mongodb.org/python
Source0:        http://pypi.python.org/packages/source/p/pymongo/pymongo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       uuzu-python27
Requires:       uuzu-python27-bson = %{version}-%{release}

Provides:       pymongo27 = %{version}-%{release}
#Obsoletes:      pymongo <= 2.1.1-4

BuildRequires:  uuzu-python27-devel
#remove check
#BuildRequires:  uuzu-python27-nose
#BuildRequires:  uuzu-python27-setuptools

%if 0%{?with_python3}
BuildRequires:  python-tools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

# Mongodb must run on a little-endian CPU (see bug #630898)
ExcludeArch:    ppc ppc64 %{sparc} s390 s390x

%description
The Python driver for MongoDB.

%if 0%{?with_python3}
%package -n python3-pymongo
Summary:        Python driver for MongoDB
Group:          Development/Languages
Requires:       python3-bson = %{version}-%{release}

%description -n python3-pymongo
The Python driver for MongoDB.  This package contains the python3 version of
this module.
%endif # with_python3

%package gridfs
Summary:        Python GridFS driver for MongoDB
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       uuzu-pymongo27-gridfs = %{version}-%{release}
Obsoletes:      pymongo-gridfs <= 2.1.1-4

%description gridfs
GridFS is a storage specification for large objects in MongoDB.

%if 0%{?with_python3}
%package -n python3-pymongo-gridfs
Summary:        Python GridFS driver for MongoDB
Group:          Development/Libraries
Requires:       python3-pymongo%{?_isa} = %{version}-%{release}

%description -n python3-pymongo-gridfs
GridFS is a storage specification for large objects in MongoDB.  This package
contains the python3 version of this module.
%endif # with_python3

%package -n uuzu-python27-bson
Summary:        Python bson library
Group:          Development/Libraries

%description -n uuzu-python27-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.

%if 0%{?with_python3}
%package -n python3-bson
Summary:        Python bson library
Group:          Development/Libraries

%description -n python3-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.  This package
contains the python3 version of this module.
%endif # with_python3

%prep
%setup -q -n pymongo-%{version}
rm -r pymongo.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups --no-diffs %{py3dir}
%endif # with_python3

%build
export LIBRARY_PATH='/data/app/lib/'
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitearch}/pymongo
%{python_sitearch}/pymongo-%{version}-*.egg-info

%if 0%{?with_python3}
%files -n python3-pymongo
%defattr(-,root,root,-)
%{python3_sitearch}/pymongo
%{python3_sitearch}/pymongo-%{version}-*.egg-info
%endif # with_python3

%files gridfs
%defattr(-,root,root,-)
%{python_sitearch}/gridfs

%if 0%{?with_python3}
%files -n python3-pymongo-gridfs
%defattr(-,root,root,-)
%{python3_sitearch}/gridfs
%endif # with_python3

%files -n uuzu-python27-bson
%defattr(-,root,root,-)
%{python_sitearch}/bson

%if 0%{?with_python3}
%files -n python3-bson
%defattr(-,root,root,-)
%{python3_sitearch}/bson
%endif # with_python3

#check
## Exclude tests that require an active MongoDB connection
# exclude='(^test_auth_from_uri$'
#exclude+='|^test_auto_auth_login$'
#exclude+='|^test_auto_reconnect_exception_when_read_preference_is_secondary$'
#exclude+='|^test_auto_start_request$'
#exclude+='|^test_binary$'
#exclude+='|^test_client$'
#exclude+='|^test_collection$'
#exclude+='|^test_common$'
#exclude+='|^test_config_ssl$'
#exclude+='|^test_connect$'
#exclude+='|^test_connection$'
#exclude+='|^test_constants$'
#exclude+='|^test_contextlib$'
#exclude+='|^test_copy_db$'
#exclude+='|^test_cursor$'
#exclude+='|^test_database$'
#exclude+='|^test_database_names$'
#exclude+='|^test_delegated_auth$'
#exclude+='|^test_disconnect$'
#exclude+='|^test_document_class$'
#exclude+='|^test_drop_database$'
#exclude+='|^test_equality$'
#exclude+='|^test_fork$'
#exclude+='|^test_from_uri$'
#exclude+='|^test_fsync_lock_unlock$'
#exclude+='|^test_get_db$'
#exclude+='|^test_getters$'
#exclude+='|^test_grid_file$'
#exclude+='|^test_gridfs$'
#exclude+='|^test_host_w_port$'
#exclude+='|^test_interrupt_signal$'
#exclude+='|^test_ipv6$'
#exclude+='|^test_iteration$'
#exclude+='|^test_json_util$'
#exclude+='|^test_kill_cursor_explicit_primary$'
#exclude+='|^test_kill_cursor_explicit_secondary$'
#exclude+='|^test_master_slave_connection$'
#exclude+='|^test_nested_request$'
#exclude+='|^test_network_timeout$'
#exclude+='|^test_network_timeout_validation$'
#exclude+='|^test_operation_failure_with_request$'
#exclude+='|^test_operation_failure_without_request$'
#exclude+='|^test_operations$'
#exclude+='|^test_pinned_member$'
#exclude+='|^test_pooling$'
#exclude+='|^test_pooling_gevent$'
#exclude+='|^test_properties$'
#exclude+='|^test_pymongo$'
#exclude+='|^test_read_preferences$'
#exclude+='|^test_replica_set_client$'
#exclude+='|^test_replica_set_connection$'
#exclude+='|^test_replica_set_connection_alias$'
#exclude+='|^test_repr$'
#exclude+='|^test_request_threads$'
#exclude+='|^test_safe_insert$'
#exclude+='|^test_safe_update$'
#exclude+='|^test_schedule_refresh$'
#exclude+='|^test_server_disconnect$'
#exclude+='|^test_son_manipulator$'
#exclude+='|^test_threading$'
#exclude+='|^test_threads$'
#exclude+='|^test_threads_replica_set_connection$'
#exclude+='|^test_timeouts$'
#exclude+='|^test_tz_aware$'
#exclude+='|^test_uri_options$'
#exclude+='|^test_use_greenlets$'
#exclude+='|^test_with_start_request$'
#exclude+=')'
#pushd test
#nosetests --exclude="$exclude"
#popd

%changelog
* Thu Apr 10 2013 HarrisonZhu <zhuhuipeng@cyou-inc.com> - 2.7-1
- upgrade to 2.7 and build with python 2.7
