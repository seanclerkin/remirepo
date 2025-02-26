# remirepo spec file for php-pecl-yaf
#
# Copyright (c) 2012-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package        php-pecl-yaf}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name yaf
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif

Summary:       Yet Another Framework
Name:          %{?sub_prefix}php-pecl-yaf
Version:       2.3.5
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/yaf
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:       %{pecl_name}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel >= 5.2.0
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: pcre-devel

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The Yet Another Framework (Yaf) extension is a PHP framework that is used
to develop web applications. 

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{scl_vendor})}.


%prep
%setup -q -c 
mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' -i package.xml

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_YAF_VERSION/{s/.*\t"//;s/".*$//;p}' php_yaf.h )
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


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
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Sun Sep  6 2015 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- Update to 2.3.5

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-2
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.3.3-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 2.3.2-4
- improve SCL build

* Thu Jun 26 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-3
- upstream patch for PHP 5.6

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-2
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan 09 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2 (beta)

* Wed Jan 08 2014 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1 (beta)

* Wed Jan 08 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0 (beta)
- install doc in pecl doc_dir
- install tests in pecl test_dir
- adapt for SCL
- add missing files from upstream git repo
  https://github.com/laruence/php-yaf/issues/82

* Fri Jan  4 2013 Remi Collet <remi@fedoraproject.org> - 2.2.9-1
- version 2.2.9 (stable)

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> - 2.2.8-1
- version 2.2.8 (stable)

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- version 2.2.7 (stable)

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 2.2.6-1
- version 2.2.6 (stable)

* Mon Oct 22 2012 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- version 2.2.5 (stable)
- LICENSE now provided by upstream

* Tue Sep  4 2012 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- version 2.2.4 (beta)
- initial package