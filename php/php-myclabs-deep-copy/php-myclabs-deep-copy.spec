# remirepo spec/Fedora file for php-myclabs-deep-copy
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d8093b631a31628342d0703764935f8bac2c56b1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     myclabs
%global gh_project   DeepCopy
%global c_project    deep-copy
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-myclabs-deep-copy
Version:        1.4.0
Release:        1%{?dist}
Summary:        Create deep copies (clones) of your objects

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snashop to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "doctrine/collections": "1.*",
#        "phpunit/phpunit": "~4.1"
BuildRequires:  php-composer(doctrine/collections) >= 1
BuildRequires:  php-composer(phpunit/phpunit) >= 4.1
%endif

# From composer.json, "require": {
#        "php": ">=5.4.0"
Requires:       php(language) >= 5.4
# From phpcompatinfo report for version 1.3.0
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{c_project}) = %{version}


%description
DeepCopy helps you create deep copies (clones) of your objects.
It is designed to handle cycles in the association graph.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE2} src/%{gh_project}/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p %{buildroot}%{php_home}
cp -pr src/%{gh_project} %{buildroot}%{php_home}/%{gh_project}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{php_home}/%{gh_project}/autoload.php';
$fedoraClassLoader->addPrefix('DeepCopyTest\\', __DIR__ . '/../tests');
$fedoraClassLoader->addPrefix('Doctrine\\', '%{php_home}');
EOF

%{_bindir}/php -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
%{_bindir}/phpunit --verbose
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc README.md
%{php_home}/%{gh_project}


%changelog
* Mon Oct  5 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Mon Jul 20 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1 (no change, pr #14 merged)

* Sat Jul  4 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- initial package, version 1.3.0
- open https://github.com/myclabs/DeepCopy/pull/14 - fix perms