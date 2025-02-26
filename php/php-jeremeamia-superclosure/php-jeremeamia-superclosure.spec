# remirepo/fedora spec file for php-jeremeamia-superclosure
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github
%global gh_commit    b712f39c671e5ead60c7ebfe662545456aade833
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     jeremeamia
%global gh_project   super_closure
# Packagist
%global pk_vendor    jeremeamia
%global pk_name      superclosure
# PSR-0 namespace
%global namespace    SuperClosure

Name:           php-%{pk_vendor}-%{pk_name}
Version:        2.1.0
Release:        1%{?dist}
Summary:        Serialize Closure objects, including their context and binding

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# Create git snapshot as tests are excluded from official tarball
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(nikic/php-parser) >= 1.4
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0",
#        "codeclimate/php-test-reporter": "~0.1.2"
BuildRequires:  php-composer(phpunit/phpunit)  >= 4.0
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From composer.json, "require": {
#        "php": ">=5.4",
#        "nikic/php-parser": "~1.2"
# php-parser 1.4 for autoloader
Requires:       php(language) >= 5.4
Requires:       php-composer(nikic/php-parser) >= 1.4
Requires:       php-composer(nikic/php-parser) <  2
# From phpcompatifo report for 2.1.0
Requires:       php-hash
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(%{pk_vendor}/%{pk_name}) = %{version}


%description
Even though serializing closures is "not allowed" by PHP,
the SuperClosure library makes it possible

To use this library, you just have to add, in your project:
  require-once '%{_datadir}/php/%{namespace}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}
install -pm 644 %{SOURCE2} src/autoload.php


%build
# Nothing


%install
rm -rf     %{buildroot}
# Restore PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{namespace}


%check
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{namespace}/autoload.php';
require dirname(__DIR__) . '/tests/Integ/Fixture/Collection.php';
require dirname(__DIR__) . '/tests/Integ/Fixture/Foo.php';
EOF

%{_bindir}/phpunit -v


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md composer.json
%{_datadir}/php/%{namespace}


%changelog
* Tue Sep  1 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- initial package