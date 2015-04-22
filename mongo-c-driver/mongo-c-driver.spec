# spec file for mongo-c-driver
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   mongo-c-driver
#global prever       beta
%ifarch x86_64
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%else
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%endif
%global libname      libmongoc
%global libver       1.0

Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   1.1.4
Release:   1%{?dist}
License:   ASL 2.0
Group:     System Environment/Libraries
URL:       https://github.com/%{gh_owner}/%{gh_project}
Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz

BuildRequires: python
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libbson-1.0)
BuildRequires: cyrus-sasl-devel
%if %{with_tests}
BuildRequires: mongodb-server
BuildRequires: openssl
BuildRequires: perl
%endif
%if 0%{?fedora} > 21
BuildRequires: libtool autoconf
%endif


%description
%{name} is a client library written in C for MongoDB.

There are absolutely no guarantees of API/ABI stability at this point.
But generally, we won't break API/ABI unless we have good reason.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}.


%package tools
Summary:    MongoDB tools
Group:      Applications/System
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains some command line tools to manage
a MongoDB Server.


%prep
%setup -q

%if 0%{?fedora} < 22
# Ensure we are using system library
rm -r src/libbson
%endif


%build
export LIBS=-lpthread
%if 0%{?fedora} > 21
# Workaround https://jira.mongodb.org/browse/CDRIVER-624
sed -e 's/&& __GNUC_MINOR__ >= 1//' -i ./build/autotools/CheckCompiler.m4
autoreconf -fi
%endif

%configure \
  --enable-sasl \
  --enable-ssl \
  --enable-man-pages

make %{_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}

rm    %{buildroot}%{_libdir}/*la
rm -r %{buildroot}%{_datadir}/doc


%check
%if %{with_tests}
: Run a server
mkdir dbtest
mongod \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
ret=0
make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

exit $ret
%else
: check disabled, missing '--with tests' option
%endif


%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/%{libname}-%{libver}.so.*
%{_libdir}/%{libname}-priv.so.*


%files tools
%{_bindir}/mongoc-stat

%files devel
%doc NEWS README
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.so
%{_libdir}/%{libname}-priv.so
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_mandir}/man3/mongoc*


%changelog
* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Initial package
- open https://jira.mongodb.org/browse/CDRIVER-624 - gcc 5