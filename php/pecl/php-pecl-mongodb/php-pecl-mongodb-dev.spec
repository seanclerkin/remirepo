# remirepo spec file for php-pecl-mongodb
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-mongodb}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  mongodb
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
%global prever     beta2

Summary:        MongoDB driver for PHP
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        1.0.0
Release:        0.3.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libbson-1.0)    >= 1.2.0
BuildRequires:  pkgconfig(libmongoc-1.0)  >= 1.2.0
BuildRequires:  pkgconfig(libmongoc-priv) >= 1.2.0

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The purpose of this driver is to provide exceptionally thin glue between
MongoDB and PHP, implementing only fundemental and performance-critical
components necessary to build a fully-functional MongoDB driver.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define MONGODB_VERSION_S/{s/.* "//;s/".*$//;p}' php_phongo.h)
if test "x${extver}" != "x%{version}%{?prever:%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:%{prever}}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so

; Configuration
;mongodb.debug=''
EOF


%build
peclbuild() {
  %{_bindir}/${1}ize

  # Ensure we use system library
  # Need to be removed only after phpize because of m4_include
  rm -r src/libbson
  rm -r src/libmongoc

  %configure \
    --with-php-config=%{_bindir}/${1}-config \
    --with-libbson \
    --with-libmongoc \
    --enable-mongodb

  make %{?_smp_mflags}
}

cd NTS
peclbuild php

%if %{with_zts}
cd ../ZTS
peclbuild zts-php
%endif


%install
rm -rf %{buildroot}

make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3-beta2
- Update to 1.0.0beta2 (beta)

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2-beta1
- Update to 1.0.0beta1 (beta)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha2
- Update to 1.0.0alpha2 (alpha)
- buid with system libmongoc

* Thu May 07 2015 Remi Collet <remi@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0 (alpha)

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1 (alpha)

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-2
- build with system libbson
- open https://jira.mongodb.org/browse/PHPC-259

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- initial package, version 0.5.0 (alpha)