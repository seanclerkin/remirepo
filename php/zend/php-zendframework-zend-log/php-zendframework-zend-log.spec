# remirepo/Fedora spec file for php-zendframework-zend-log
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    6b0c8437c67153c5e81cdf1aaa147e5a126ed013
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-log
%global php_home     %{_datadir}/php
%global library      Log
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.2
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
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-console": "~2.5",
#        "zendframework/zend-db": "~2.5",
#        "zendframework/zend-escaper": "~2.5",
#        "zendframework/zend-filter": "~2.5",
#        "zendframework/zend-mail": "~2.5",
#        "zendframework/zend-mvc": "~2.5",
#        "zendframework/zend-validator": "~2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mail)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Optional dep
BuildRequires:  php-composer(%{gh_owner}/zend-mime)             >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-stdlib": "~2.5"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  3
# From composer, "suggest": {
#        "ext-mongo": "mongodb extetension to use MongoDB writer",
#        "zendframework/zend-console": "Zend\\Console component to use the RequestID log processor",
#        "zendframework/zend-db": "Zend\\Db component to use the database log writer",
#        "zendframework/zend-escaper": "Zend\\Escaper component, for use in the XML log formatter",
#        "zendframework/zend-mail": "Zend\\Mail component to use the email log writer",
#        "zendframework/zend-validator": "Zend\\Validator component to block invalid log messages"
%if 0%{?fedora} >= 21
Suggests:       php-pecl(mongo)
Suggests:       php-composer(%{gh_owner}/zend-console)
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-escaper)
Suggests:       php-composer(%{gh_owner}/zend-mail)
Suggests:       php-composer(%{gh_owner}/zend-validator)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-ctype
Requires:       php-date
Requires:       php-dom
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# mongo is optional

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Log is a component for general purpose logging. It supports multiple
log backends, formatting messages sent to the log, and filtering messages
from being logged.


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
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
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
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package