# remirepo spec file for php-twig
# With SCL stuff, from Fedora:
#
# Fedora spec file for php-twig
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     twigphp
%global github_name      Twig
%global github_version   1.22.2
%global github_commit    79249fc8c9ff62e41e217e0c630e2e00bcadda6a
%global github_short     %(c=%{github_commit}; echo ${c:0:7})


# Lib
%global composer_vendor  twig
%global composer_project twig

# Ext
%global ext_name twig
%global with_zts 0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name %{ext_name}.ini
%else
%global ini_name 40-%{ext_name}.ini
%endif

# "php": ">=5.2.7"
%global php_min_ver 5.2.7

%if 0%{?scl:1}
# PHPUnit not available in SCL
%global with_tests 0
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%else
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%endif

%{?scl:          %scl_package        php-twig}
%{!?scl:         %global pkg_name    %{name}}
%{!?phpdir:      %global phpdir      %{_datadir}/php}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__php:       %global __php       %{_bindir}/php}

Name:          %{?sub_prefix}php-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:       The flexible, fast, and secure template engine for PHP

Group:         Development/Libraries
License:       BSD
URL:           http://twig.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{pkg_name}-%{github_version}-%{github_short}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel >= %{php_min_ver}
%if %{with_tests}
# For tests
BuildRequires: %{_bindir}/phpunit
## phpcompatinfo (computed from version 1.22.2)
BuildRequires: %{?scl_prefix}php-ctype
BuildRequires: %{?scl_prefix}php-date
BuildRequires: %{?scl_prefix}php-dom
BuildRequires: %{?scl_prefix}php-hash
BuildRequires: %{?scl_prefix}php-iconv
BuildRequires: %{?scl_prefix}php-json
BuildRequires: %{?scl_prefix}php-mbstring
BuildRequires: %{?scl_prefix}php-pcre
BuildRequires: %{?scl_prefix}php-reflection
BuildRequires: %{?scl_prefix}php-spl
%endif

# Lib
## composer.json
Requires:      %{?scl_prefix}php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.22.2)
Requires:      %{?scl_prefix}php-ctype
Requires:      %{?scl_prefix}php-date
Requires:      %{?scl_prefix}php-dom
Requires:      %{?scl_prefix}php-hash
Requires:      %{?scl_prefix}php-iconv
Requires:      %{?scl_prefix}php-json
Requires:      %{?scl_prefix}php-mbstring
Requires:      %{?scl_prefix}php-pcre
Requires:      %{?scl_prefix}php-reflection
Requires:      %{?scl_prefix}php-spl
# Ext
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api)      = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Lib
## Composer
Provides:      %{?scl_prefix}php-composer(%{composer_vendor}/%{composer_project}) = %{version}
## Rename
Obsoletes:     %{?scl_prefix}php-twig-Twig < %{version}-%{release}
Provides:      %{?scl_prefix}php-twig-Twig = %{version}-%{release}
## PEAR
Provides:      %{?scl_prefix}php-pear(pear.twig-project.org/Twig) = %{version}
# Ext
## Rename
Obsoletes:     %{?scl_prefix}php-twig-ctwig         < %{version}-%{release}
Provides:      %{?scl_prefix}php-twig-ctwig         = %{version}-%{release}
Provides:      %{?scl_prefix}php-twig-ctwig%{?_isa} = %{version}-%{release}
## Compat SCL (rh-php56)
Provides:      %{?scl_prefix}php-twig         = %{version}-%{release}
Provides:      %{?scl_prefix}php-twig%{?_isa} = %{version}-%{release}
## PECL
Provides:      %{?scl_prefix}php-pecl(pear.twig-project.org/CTwig)         = %{version}
Provides:      %{?scl_prefix}php-pecl(pear.twig-project.org/CTwig)%{?_isa} = %{version}

# This pkg was the only one in this channel so the channel is no longer needed
Obsoletes:     %{?scl_prefix}php-channel-twig

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:      php53-%{ext_name} <= %{version}
Obsoletes:     php53u-%{ext_name} <= %{version}
Obsoletes:      php54-%{ext_name} <= %{version}
Obsoletes:     php54w-%{ext_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{ext_name} <= %{version}
Obsoletes:     php55w-%{ext_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{ext_name} <= %{version}
Obsoletes:     php56w-%{ext_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-%{ext_name} <= %{version}
Obsoletes:     php70w-%{ext_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{summary}.

* Fast: Twig compiles templates down to plain optimized PHP code. The
  overhead compared to regular PHP code was reduced to the very minimum.

* Secure: Twig has a sandbox mode to evaluate untrusted template code. This
  allows Twig to be used as a template language for applications where users
  may modify the template design.

* Flexible: Twig is powered by a flexible lexer and parser. This allows the
  developer to define its own custom tags and filters, and create its own
  DSL.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qn %{github_name}-%{github_commit}

: Ext -- NTS
mv ext/%{ext_name} ext/NTS
%if %{with_zts}
: Ext -- ZTS
cp -pr ext/NTS ext/ZTS
%endif

: Ext -- Create configuration file
cat > %{ini_name} << 'INI'
; Enable %{ext_name} extension module
extension=%{ext_name}.so
INI

: Create lib autoloader
cat <<'AUTOLOAD' | tee lib/Twig/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 */

require_once __DIR__ . '/Autoloader.php';
Twig_Autoloader::register();
AUTOLOAD


%build
: Ext -- NTS
pushd ext/NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

: Ext -- ZTS
%if %{with_zts}
pushd ext/ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif


%install
rm -rf %{buildroot}

: Lib
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/

: Ext -- NTS
make -C ext/NTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}
: Ext -- ZTS
%if %{with_zts}
make -C ext/ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Library version check
%{_bindir}/php -r 'require_once "%{buildroot}%{phpdir}/Twig/autoload.php";
    exit(version_compare("%{version}", Twig_Environment::VERSION, "=") ? 0 : 1);'

: Extension version check
EXT_VERSION=`grep PHP_TWIG_VERSION ext/NTS/php_twig.h | awk '{print $3}' | sed 's/"//g'` \
    %{_bindir}/php -r 'exit(version_compare("%{version}", getenv("EXT_VERSION"), "=") ? 0 : 1);'

: Extension NTS minimal load test
%{__php} --no-php-ini \
    --define extension=ext/NTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
: Extension ZTS minimal load test
%{__ztsphp} --no-php-ini \
    --define extension=ext/ZTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif

%if %{with_tests}
: Skip tests known to fail
sed -e 's#function testGetAttributeExceptions#function SKIP_testGetAttributeExceptions#' \
    -e 's/function testGetAttributeWithTemplateAsObject/function skip_testGetAttributeWithTemplateAsObject/' \
    -i test/Twig/Tests/TemplateTest.php

: Test suite without extension
%{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Twig/autoload.php --verbose

: Test suite with extension
%{_bindir}/php --define extension=ext/NTS/modules/%{ext_name}.so \
    %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Twig/autoload.php --verbose
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG README.rst composer.json
# Lib
%{phpdir}/Twig
# Ext
## NTS
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so
## ZTS
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.22.2-1
- Updated to 1.22.2 (RHBZ #1262655)
- Added lib and ext version checks

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.22.2-1
- Update to 1.22.2

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 1.22.1-1
- Update to 1.22.1

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 1.22.0-1
- Update to 1.22.0

* Sat Sep 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.21.2-1
- Updated to 1.21.2 (BZ #1256767)

* Wed Sep  9 2015 Remi Collet <remi@fedoraproject.org> - 1.21.2-1
- Update to 1.21.2

* Wed Aug 26 2015 Remi Collet <remi@fedoraproject.org> - 1.21.1-1
- Update to 1.21.1

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 1.21.0-1
- Update to 1.21.0

* Wed Aug 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.20.0-1
- Updated to 1.20.0 (BZ #1249259)

* Wed Aug 12 2015 Remi Collet <remi@fedoraproject.org> - 1.20.0-1
- Update to 1.20.0

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 1.19.0-1
- Update to 1.19.0

* Mon Jun 22 2015 Remi Collet <rcollet@redhat.com> - 1.18.2-4
- add virtual "rh-php56" provides

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 1.18.2-3
- allow build against rh-php56 (as more-php56)

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.18.2-2
- rebuild for remirepo with rawhide changes (autoloader)

* Thu Jun 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.18.2-1
- Updated to 1.18.2 (BZ #1183601)
- Added autoloader

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 1.18.2-1
- Update to 1.18.2

* Sun Apr 19 2015 Remi Collet <remi@fedoraproject.org> - 1.18.1-1
- Update to 1.18.1

* Mon Jan 26 2015 Remi Collet <remi@fedoraproject.org> - 1.18.0-1
- Update to 1.18.0

* Wed Jan 14 2015 Remi Collet <remi@fedoraproject.org> - 1.17.0-1
- Update to 1.17.0

* Fri Dec 26 2014 Remi Collet <remi@fedoraproject.org> - 1.16.3-1
- Update to 1.16.3

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.16.2-1.1
- Fedora 21 SCL mass rebuild

* Fri Oct 17 2014 Remi Collet <remi@fedoraproject.org> - 1.16.2-1
- Update to 1.16.2

* Sat Oct 11 2014 Remi Collet <remi@fedoraproject.org> - 1.16.1-1
- Update to 1.16.1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-2
- allow SCL build
- add backport stuff for EL-5

* Mon Aug 25 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-2
- Removed obsolete and provide of php-twig-CTwig (never imported into Fedora/EPEL)
- Obsolete php-channel-twig
- Removed comment about optional Xdebug in description (does not provide any new feature)
- Always run extension minimal load test

* Tue Jul 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-1
- Initial package
