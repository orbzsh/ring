%define pybasever 2.7
%define __python /data/app/python/bin/python%{pybasever}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%global with_docs 0

Name:		uuzu-python27-jinja2
Version:	2.7.2
Release:	1%{?dist}
Summary:	General purpose template engine
Group:		Development/Languages
License:	BSD
URL:		http://jinja.pocoo.org/
Source0:	http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	uuzu-python27-devel
BuildRequires:	uuzu-python27-setuptools
BuildRequires:	uuzu-python27-markupsafe
%if 0%{?with_docs}
BuildRequires:	python-sphinx10
%endif # with_docs
Requires:	uuzu-python27-babel >= 0.8
Requires:	uuzu-python27-markupsafe


%description
Jinja2 is a template engine written in pure Python.  It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.


%prep
%setup -q -n Jinja2-%{version}
#cp -p %{SOURCE1} .

# cleanup
find . -name '*.pyo' -o -name '*.pyc' -delete

# fix EOL
sed -i 's|\r$||g' LICENSE


%build
%{__python} setup.py bdist_egg

%if 0%{?with_docs}
make -C docs html SPHINXBUILD=sphinx-1.0-build
%endif # with_docs


%install
rm -rf %{buildroot}

# older versions of easy_install can't recreate path
mkdir -p %{buildroot}%{python_sitelib}

/data/app/python/bin/easy_install -m -O1 --prefix %{buildroot}/data/app dist/*.egg

# fix permissions
find %{buildroot}%{python_sitelib}/Jinja2-%{version}-py*.egg -type f \
     -exec chmod a-x {} \;

# remove hidden file
rm -rf docs/_build/html/.buildinfo


%clean
rm -rf %{buildroot}


%check
sed -i 's:python:%{__python}:' Makefile
make test


%files
%defattr(-,root,root,-)
#%doc AUTHORS CHANGES LICENSE README.Fedora
%if 0%{?with_docs}
%doc docs/_build/html
%endif # with_docs
#%doc ext
#%doc examples
%{python_sitelib}/*
#%exclude %{python_sitelib}/*/jinja2/_debugsupport.c


%changelog
*  Wed Apr 23 2014 Harrison Zhu <zhuhuipeng@cyou-inc.com> - 2.7.2-1
- create this file.
