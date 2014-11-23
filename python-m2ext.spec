%define	module m2ext
Summary:	M2Crypto Extensions
Name:		python-m2ext
Version:	0.1
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/m/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	5b8e448a74a84f8047b8d0713b05bf85
URL:		http://pypi.python.org/pypi/m2ext
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-M2Crypto
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig
BuildRequires:	swig-python
Requires:	python-M2Crypto
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains some extended functions which are not (yet)
available in M2Crypto
<http://chandlerproject.org/Projects/MeTooCrypto> trunk.

%prep
%setup -q -n %{module}-%{version}

%build
# The pkgconfig bit was taken from m2crypto.spec
# https://apps.fedoraproject.org/packages/m2crypto/sources/spec/
CFLAGS="%{rpmcflags}"
if pkg-config openssl; then
	CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
	LDFLAGS="$LDFLAGS $(pkg-config --libs-only-L openssl)"
fi
export CFLAGS LDFLAGS

CC="%{__cc}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py \
	build install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

chmod a+x $RPM_BUILD_ROOT/%{py_sitedir}/%{module}/_m2ext.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%dir %{py_sitedir}/m2ext
%{py_sitedir}/m2ext/*.py[co]
%attr(755,root,root) %{py_sitedir}/m2ext/_m2ext.so
%{py_sitedir}/m2ext-%{version}-py*.egg-info
