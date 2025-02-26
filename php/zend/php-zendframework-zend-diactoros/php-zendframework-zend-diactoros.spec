# remirepo spec file for php-zendframework-zend-diactoros, from
#
# Fedora spec file for php-zendframework-zend-diactoros
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     zendframework
%global github_name      zend-diactoros
%global github_version   1.1.3
%global github_commit    e2f5c12916c74da384058d0dfbc7fbc0b03d1181

%global composer_vendor  zendframework
%global composer_project zend-diactoros

# "php": ">=5.4"
%global php_min_ver 5.4
# "psr/http-message": "~1.0"
%global psr_http_message_min_ver 1.0
%global psr_http_message_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PSR HTTP Message implementations

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-zendframework-zend-diactoros-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                  >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/http-message) >= %{psr_http_message_min_ver}
## phpcompatinfo (computed from version 1.1.3)
### NOTE: curl, gd, gmp, and shmop are all optional for
###       ZendTest\Diactoros\StreamTest::getResourceFor67()
###       (test/StreamTest.php) but the first one found wins
###       so only curl is chosen as a requirement here.
BuildRequires: php-curl
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                  >= %{php_min_ver}
Requires:      php-composer(psr/http-message) >= %{psr_http_message_min_ver}
Requires:      php-composer(psr/http-message) <  %{psr_http_message_max_ver}
# phpcompatinfo (computed from version 1.1.3)
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
Provides:      php-composer(psr/http-message-implementation)        = 1.0.0

%description
A PHP package containing implementations of the accepted PSR-7 HTTP message
interfaces [1], as well as a "server" implementation similar to node's
http.Server [2].

[1] http://www.php-fig.org/psr/psr-7/
[2] http://nodejs.org/api/http.html


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Zend\\Diactoros\\', dirname(dirname(__DIR__)));

require_once '%{phpdir}/Psr/Http/Message/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Zend/Diactoros
cp -rp src/* %{buildroot}%{phpdir}/Zend/Diactoros/


%check
%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Zend/Diactoros/autoload.php';

$fedoraClassLoader->addPrefix('ZendTest\\Diactoros\\', __DIR__ . '/test');

require_once __DIR__ . '/test/TestAsset/Functions.php';
require_once __DIR__ . '/test/TestAsset/SapiResponse.php';
BOOTSTRAP

%{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%doc README.md
%doc composer.json
%dir %{phpdir}/Zend
     %{phpdir}/Zend/Diactoros


%changelog
* Tue Aug 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.3-1
- Updated to 1.1.3 (RHBZ #1252195)
- Updated autoloader to load dependencies after self registration

* Tue Aug 11 2015 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Mon Jul 20 2015 Remi Collet <remi@remirepo.net> - 1.1.2-1
- add EL-5 stuff, backport for #remirepo

* Wed Jul 15 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.2-1
- Update to 1.1.2
- Fix license
- Update description
- Use full path in autoloader

* Wed Jul 08 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-1
- Initial package
