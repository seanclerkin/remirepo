# remirepo/Fedora spec file for php-zendframework-zend-mvc
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    bae0da8318323da7dd71d64aa8054f91f782951b
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-mvc
%global php_home     %{_datadir}/php
%global library      Mvc
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.3
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-reflection
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-form)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-authentication": "~2.5",
#        "zendframework/zend-cache": "~2.5",
#        "zendframework/zend-console": "~2.5",
#        "zendframework/zend-di": "~2.5",
#        "zendframework/zend-filter": "~2.5",
#        "zendframework/zend-http": "~2.5",
#        "zendframework/zend-i18n": "~2.5",
#        "zendframework/zend-inputfilter": "~2.5",
#        "zendframework/zend-json": "~2.5",
#        "zendframework/zend-log": "~2.5",
#        "zendframework/zend-modulemanager": "~2.5",
#        "zendframework/zend-session": "~2.5",
#        "zendframework/zend-serializer": "~2.5",
#        "zendframework/zend-text": "~2.5",
#        "zendframework/zend-uri": "~2.5",
#        "zendframework/zend-validator": "~2.5",
#        "zendframework/zend-version": "~2.5",
#        "zendframework/zend-view": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-authentication)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-di)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-inputfilter)      >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-log)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-modulemanager)    >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-text)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-version)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5",
#        "zendframework/zend-eventmanager": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-form": "~2.5",
#        "zendframework/zend-stdlib": ">=2.5.0,<2.7.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  3
Requires:       php-composer(%{gh_owner}/zend-form)             >= 2.5
Requires:       php-composer(%{gh_owner}/zend-form)             <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5.0
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  2.7
# From composer, "suggest": {
#        "zendframework/zend-authentication": "Zend\\Authentication component for Identity plugin",
#        "zendframework/zend-config": "Zend\\Config component",
#        "zendframework/zend-console": "Zend\\Console component",
#        "zendframework/zend-di": "Zend\\Di component",
#        "zendframework/zend-filter": "Zend\\Filter component",
#        "zendframework/zend-http": "Zend\\Http component",
#        "zendframework/zend-i18n": "Zend\\I18n component for translatable segments",
#        "zendframework/zend-inputfilter": "Zend\\Inputfilter component",
#        "zendframework/zend-json": "Zend\\Json component",
#        "zendframework/zend-log": "Zend\\Log component",
#        "zendframework/zend-modulemanager": "Zend\\ModuleManager component",
#        "zendframework/zend-serializer": "Zend\\Serializer component",
#        "zendframework/zend-session": "Zend\\Session component for FlashMessenger, PRG, and FPRG plugins",
#        "zendframework/zend-text": "Zend\\Text component",
#        "zendframework/zend-uri": "Zend\\Uri component",
#        "zendframework/zend-validator": "Zend\\Validator component",
#        "zendframework/zend-version": "Zend\\Version component",
#        "zendframework/zend-view": "Zend\\View component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-authentication)
Suggests:       php-composer(%{gh_owner}/zend-config)
Suggests:       php-composer(%{gh_owner}/zend-console)
Suggests:       php-composer(%{gh_owner}/zend-di)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-inputfilter)
Suggests:       php-composer(%{gh_owner}/zend-json)
Suggests:       php-composer(%{gh_owner}/zend-log)
Suggests:       php-composer(%{gh_owner}/zend-modulemanager)
Suggests:       php-composer(%{gh_owner}/zend-serializer)
Suggests:       php-composer(%{gh_owner}/zend-session)
Suggests:       php-composer(%{gh_owner}/zend-text)
Suggests:       php-composer(%{gh_owner}/zend-uri)
Suggests:       php-composer(%{gh_owner}/zend-validator)
Suggests:       php-composer(%{gh_owner}/zend-version)
Suggests:       php-composer(%{gh_owner}/zend-view)
%endif
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-reflection
Requires:       php-intl
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Mvc is a brand new MVC implementation designed from the ground up
for Zend Framework 2, focusing on performance and flexibility.

The MVC layer is built on top of the following components:
* Zend\ServiceManager - Zend Framework provides a set of default service
  definitions set up at Zend\Mvc\Service. The ServiceManager creates and
  configures your application instance and workflow.
* Zend\EventManager - The MVC is event driven. This component is used
  everywhere from initial bootstrapping of the application, through returning
  response and request calls, to setting and retrieving routes and matched
  routes, as well as render views.
* Zend\Http - specifically the request and response objects, used within:
  Zend\Stdlib\DispatchableInterface. All “controllers” are simply dispatchable
  objects.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
# TODO need investigation
rm test/Controller/Plugin/FilePostRedirectGetTest.php

mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Thu Sep 24 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- version 2.5.3

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- version 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package