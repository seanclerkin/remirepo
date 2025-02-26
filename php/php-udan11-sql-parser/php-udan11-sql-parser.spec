# remirepo/fedora spec file for php-udan11-sql-parser
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    1b2988f296611f7294593fd1fff07c70ac514e2a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     udan11
#global gh_date      20150820
%global gh_project   sql-parser
%global with_tests   0%{!?_without_tests:1}
%global psr0         SqlParser

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.0
Release:        2%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        A validating SQL lexer and parser with a focus on MySQL dialect

# https://github.com/udan11/sql-parser/commit/1415469b34b1fc33189e2c801302597b5b50f704
Patch0:         %{gh_project}-upstream.patch

Group:          Development/Libraries
License:        GPLv2+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
# For tests, from composer.json "require-dev": {
#        "phpunit/php-code-coverage": "~2.0",
#        "phpunit/phpunit": "4.*"
BuildRequires:  php-composer(phpunit/phpunit) >= 4
%endif
# For autoloader
BuildRequires:  php-composer(theseer/autoload)

# From composer.json, "require": {
#        "php": ">=5.3.0"
Requires:       php(language) >= 5.3.0
# From phpcompatinfo report for 20150629
Requires:       php-ctype
Requires:       php-mbstring
Requires:       php-pcre
# For generated autoloader
Requires:       php-spl

# Rename
Obsoletes:      php-dmitry-php-sql-parser < 0-0.2
Provides:       php-dmitry-php-sql-parser = %{version}-%{release}

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
A validating SQL lexer and parser with a focus on MySQL dialect.

This library was originally developed for phpMyAdmin during
the Google Summer of Code 2015.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/%{psr0}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1


%build
: generate an simple autoloader
%{_bindir}/phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{psr0}


%check
%if %{with_tests}
sed -e s/logging/nologging/ -i phpunit.xml

mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
EOF

%{_bindir}/phpunit --verbose
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc composer.json
%doc README.md
%{_datadir}/php/%{psr0}


%changelog
* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- upstream patch for phpMyAdmin 4.5.0.2

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- tagged as 1.0.0 (no change)

* Sun Sep 20 2015 Remi Collet <remi@fedoraproject.org> - 0-0.3.20150820git1b2988f
- fix provides and self-obsoletion (review #1262807)

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 0-0.2.20150820git1b2988f
- rename to php-udan11-sql-parser

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 0-0.1.20150629git4aaed44
- initial package