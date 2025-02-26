# remirepo/Fedora spec file for php-zendframework-zend-form
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    468a172b71f2b484d557cb8dc3fa33cd90d71c25
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-form
%global php_home     %{_datadir}/php
%global library      Form
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
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-date
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-inputfilter)      >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "doctrine/annotations": "~1.0",
#        "zendframework/zend-cache": "~2.5",
#        "zendframework/zend-captcha": "~2.5",
#        "zendframework/zend-code": "~2.5",
#        "zendframework/zend-di": "~2.5",
#        "zendframework/zend-eventmanager": "~2.5",
#        "zendframework/zend-filter": "~2.5",
#        "zendframework/zend-i18n": "~2.5",
#        "zendframework/zend-mvc": "~2.5",
#        "zendframework/zend-servicemanager": "~2.5",
#        "zendframework/zend-session": "~2.5",
#        "zendframework/zend-text": "~2.5",
#        "zendframework/zend-validator": "~2.5",
#        "zendframework/zend-view": "~2.5",
#        "zendframework/zendservice-recaptcha": "*",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(doctrine/annotations)              >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-captcha)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-code)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-di)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-text)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Missing
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5",
#        "zendframework/zend-inputfilter": "~2.5",
#        "zendframework/zend-stdlib": ">=2.5.0,<2.7.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-inputfilter)      >= 2.5
Requires:       php-composer(%{gh_owner}/zend-inputfilter)      <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  2.7
# From composer, "suggest": {
#        "zendframework/zend-captcha": "Zend\\Captcha component",
#        "zendframework/zend-code": "Zend\\Code component",
#        "zendframework/zend-eventmanager": "Zend\\EventManager component",
#        "zendframework/zend-filter": "Zend\\Filter component",
#        "zendframework/zend-i18n": "Zend\\I18n component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-validator": "Zend\\Validator component",
#        "zendframework/zend-view": "Zend\\View component",
#        "zendframework/zendservice-recaptcha": "ZendService\\ReCaptcha component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-captcha)
Suggests:       php-composer(%{gh_owner}/zend-code)
Suggests:       php-composer(%{gh_owner}/zend-eventmanager)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-validator)
Suggests:       php-composer(%{gh_owner}/zend-view)
#Suggests:       php-composer(%{gh_owner}/zendservice-recaptcha)
%endif
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-date
Requires:       php-intl
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Form is intended primarily as a bridge between your domain models
and the View Layer. It composes a thin layer of objects representing form
elements, an InputFilter, and a small number of methods for binding data to
and from the form and attached objects.


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
cat << 'EOF' | tee vendor/autoload.php
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
* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise minimum php version to 5.5

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package