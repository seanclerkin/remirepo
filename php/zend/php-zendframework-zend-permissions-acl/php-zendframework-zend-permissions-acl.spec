# remirepo/Fedora spec file for zend-permissions-acl
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    7f1aac3bf99d0be8f71fe4ae79981338be8a08dc
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-permissions-acl
%global php_home     %{_datadir}/php
%global library      Acl
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.1
Release:        1%{?dist}
Summary:        Zend Framework Permissions-%{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0",
#        "zendframework/zend-di": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5"
BuildRequires:  php-composer(%{gh_owner}/zend-di)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.3.23"
Requires:       php(language) >= 5.3.23
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-servicemanager": "To support Zend\\Permissions\\Acl\\Assertion\\AssertionManager plugin manager usage"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-spl

Obsoletes:      php-ZendFramework2-Permissions-%{library} < 2.5
Provides:       php-ZendFramework2-Permissions-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Provides a lightweight and flexible access control list (ACL)
implementation for privileges management.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/Permissions/
cp -pr src %{buildroot}%{php_home}/Zend/Permissions/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\\\Permissions\\\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\\\Permissions\\\\%{library}'     => '%{buildroot}%{php_home}/Zend/Permissions/%{library}'
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
%dir %{php_home}/Zend/Permissions
     %{php_home}/Zend/Permissions/%{library}


%changelog
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package