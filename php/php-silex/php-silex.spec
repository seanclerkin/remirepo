# remirepo spec file for php-silex, from Fedora:
#
# Fedora spec file for php-silex
#
# Copyright (c) 2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner          silexphp
%global github_name           Silex
%global github_version        1.3.4
%global github_commit         d6de62716fcda76084f3015165125f30b1563517

%global composer_vendor       silex
%global composer_project      silex

# "php": ">=5.3.9"
%global php_min_ver           5.3.9
# "doctrine/dbal": "~2.2"
%global doctrine_dbal_min_ver 2.2
%global doctrine_dbal_max_ver 3.0
# "monolog/monolog": "^1.4.1"
%global monolog_min_ver       1.4.1
%global monolog_max_ver       2.0.0
# "pimple/pimple": "~1.0"
%global pimple_min_ver        1.0
%global pimple_max_ver        2.0
# "swiftmailer/swiftmailer": "~5"
%global swiftmailer_min_ver   5.0
%global swiftmailer_max_ver   6.0
# "symfony/*": "~2.3|3.0.*"
%global symfony_min_ver       2.3
%global symfony_max_ver       3.1
# "twig/twig": "~1.8|~2.0"
%global twig_min_ver          1.8
%global twig_max_ver          3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       1%{dist}
Summary:       PHP micro-framework based on the Symfony components

Group:         Development/Libraries
License:       MIT
URL:           http://silex.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
# %%{pear_phpdir} macro
BuildRequires: php-pear
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language)                          >= %{php_min_ver}
BuildRequires: php-composer(doctrine/dbal)            >= %{doctrine_dbal_min_ver}
BuildRequires: php-composer(monolog/monolog)          >= %{monolog_min_ver}
BuildRequires: php-composer(pimple/pimple)            >= %{pimple_min_ver}
BuildRequires: php-composer(pimple/pimple)            <  %{pimple_max_ver}
BuildRequires: php-composer(symfony/browser-kit)      >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/config)           >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/css-selector)     >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/debug)            >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/dom-crawler)      >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/event-dispatcher) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder)           >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/form)             >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-foundation)  >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/http-kernel)      >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/locale)           >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/monolog-bridge)   >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/options-resolver) >= %{symfony_min_ver}
#BuildRequires: php-composer(symfony/phpunit-bridge)   >= %%{symfony_min_ver}
BuildRequires: php-composer(symfony/process)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/routing)          >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/security)         >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/serializer)       >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/translation)      >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/twig-bridge)      >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/validator)        >= %{symfony_min_ver}
BuildRequires: php-composer(twig/twig)                >= %{twig_min_ver}
BuildRequires: php-swift-Swift                        >= %{swiftmailer_min_ver}
## phpcompatinfo (computed from version 1.3.4)
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-spl
BuildRequires: php-tokenizer
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language)                          >= %{php_min_ver}
Requires:      php-composer(pimple/pimple)            >= %{pimple_min_ver}
Requires:      php-composer(pimple/pimple)            <  %{pimple_max_ver}
Requires:      php-composer(symfony/event-dispatcher) >= %{symfony_min_ver}
Requires:      php-composer(symfony/event-dispatcher) <  %{symfony_max_ver}
Requires:      php-composer(symfony/http-foundation)  >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-foundation)  <  %{symfony_max_ver}
Requires:      php-composer(symfony/http-kernel)      >= %{symfony_min_ver}
Requires:      php-composer(symfony/http-kernel)      <  %{symfony_max_ver}
Requires:      php-composer(symfony/routing)          >= %{symfony_min_ver}
Requires:      php-composer(symfony/routing)          <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.3.4)
Requires:      php-date
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-session
Requires:      php-spl
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Silex is a PHP micro-framework. It is built on the shoulders of Symfony and
Pimple and also inspired by Sinatra.

A micro-framework provides the guts for building simple single-file apps. Silex
aims to be:
* Concise: Silex exposes an intuitive and concise API that is fun to use
* Extensible: Silex has an extension system based around the Pimple micro
  service-container that makes it even easier to tie in third party libraries
* Testable: Silex uses Symfony's HttpKernel which abstracts requests and
  responses. This makes it very easy to test apps and the framework itself.
  It also respects the HTTP specification and encourages its' proper use.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee src/Silex/autoload.php
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

$fedoraClassLoader->addPrefix('Silex\\', dirname(__DIR__));

require_once '%{phpdir}/Pimple1/autoload.php';

if (file_exists('%{pear_phpdir}/Swift')) {
    $fedoraClassLoader->addPrefix('Swift_', '%{pear_phpdir}/Swift');
}

// Not all dependency autoloaders exist or are in every dist yet so fallback
// to using include path for dependencies for now
$fedoraClassLoader->setUseIncludePath(true);

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create test bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php

$fedoraClassLoader =
    require_once '%{buildroot}%{phpdir}/Silex/autoload.php';

$fedoraClassLoader->addPrefix('Silex\\Tests\\', __DIR__ . '/tests');
BOOTSTRAP

: Temporarily skip tests known to fail
rm -f \
    tests/Silex/Tests/Provider/SwiftmailerServiceProviderTest.php \
    tests/Silex/Tests/Application/SwiftmailerTraitTest.php

: Run tests
%{_bindir}/phpunit --verbose --bootstrap ./bootstrap.php
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%doc composer.json
%doc doc
%{phpdir}/Silex


%changelog
* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.4-1
- Updated to 1.3.4 (RHBZ #1256774)

* Thu Aug 13 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.1-1
- Updated to 1.3.1 (RHBZ #1250055)
- Updated autoloader to load dependencies after self registration

* Mon Aug 10 2015 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1

* Fri Jul 03 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (RHBZ #1238910)

* Fri Jul 03 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.5-1
- Updated to 1.2.5 (RHBZ #1238910)
- Autoloader changed from phpab to Symfony ClassLoader

* Sun May 31 2015 Remi Collet <remi@remirepo.net> - 1.2.4-3
- backport in remi repository

* Wed May 20 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.4-3
- "%%{phpdir}/Pimple" => "%%{phpdir}/Pimple1"

* Sun May 17 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.4-2
- Fix php-composer(pimple/pimple) dependency

* Sat May 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.4-1
- Initial package
