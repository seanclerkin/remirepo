# remirepo/fedora spec file for php-tecnickcom-tc-lib-pdf-page
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    6cead617c270d4cbed79141f87e0dba5498c1e68
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global c_vendor     tecnickcom
%global gh_owner     tecnickcom
%global gh_project   tc-lib-pdf-page
%global php_project  %{_datadir}/php/Com/Tecnick/Pdf/Page
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.1.5
Release:        1%{?dist}
Summary:        PHP library containing PDF page formats and definitions

Group:          Development/Libraries
License:        LGPLv3+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php(language) >= 5.3.3
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.1.1
# Nothing

# Composer
Provides:       php-composer(%{c_vendor}/%{gh_project}) = %{version}
# Upstream package name
Provides:       php-%{gh_project} = %{version}


%description
PHP library containing PDF page formats and definitions.

The initial source code has been extracted from TCPDF (http://www.tcpdf.org).


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Sanity check
grep -q '^%{version}$' VERSION


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   $(dirname %{buildroot}%{php_project})
cp -pr src %{buildroot}%{php_project}
cp -p  resources/autoload.php \
           %{buildroot}%{php_project}/autoload.php


%check
%if %{with_tests}
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{buildroot}%{php_project}/autoload.php';
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
%license LICENSE.TXT
%doc composer.json
%doc README.md
%dir %{_datadir}/php/Com
%dir %{_datadir}/php/Com/Tecnick
%dir %{_datadir}/php/Com/Tecnick/Pdf
%{php_project}


%changelog
* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- update to 1.1.5 (no change)

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3
- provide php-composer(tecnickcom/tc-lib-pdf-page)

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2 (no change)

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- initial package, version 1.1.1