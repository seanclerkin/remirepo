# remirepo/fedora spec file for php-phpunit-DbUnit
#
# Copyright (c) 2010-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9aaee6447663ff1b0cd50c23637e04af74c5e2ae
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   dbunit
%global php_home     %{_datadir}/php
%global pear_name    DbUnit
%global pear_channel pear.phpunit.de
%if 0%{?rhel} == 5
# libxml is too old for LIBXML_PARSEHUGE used in tests
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-DbUnit
Version:        1.4.1
Release:        1%{?dist}
Summary:        DbUnit port for PHP/PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoloader full path
Patch0:         %{gh_project}-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
%if %{with_tests}
BuildRequires:  php-pdo
BuildRequires:  php-pear-PHPUnit >= 4.0
%endif

# From composer.json
#        "php": ">=5.3.3",
#        "phpunit/phpunit": "~4|~5",
#        "symfony/yaml": "~2.1|~3.0",
#        "ext-pdo": "*",
#        "ext-simplexml": "*"
Requires:       php(language) >= 5.3.3
Requires:       php-pdo
Requires:       php-simplexml
Requires:       php-composer(phpunit/phpunit) >= 4
Requires:       php-composer(phpunit/phpunit) <  6
Requires:       php-composer(symfony/yaml)    >= 2.1
Requires:       php-composer(symfony/yaml)    <  4
# From phpcompatinfo report for version 1.3.0
Requires:       php-libxml
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(phpunit/dbunit) = %{version}


%description
DbUnit port for PHP/PHPUnit.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm PHPUnit/Extensions/Database/Autoload.php.in

%patch0 -p0 -b .rpm


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it.
# Also remember to fix the command to use it.

#phpab \
#  --output   PHPUnit/Extensions/Database/Autoload.php \
#  --template PHPUnit/Extensions/Database/Autoload.php.in \
#  PHPUnit


%install
rm -rf         %{buildroot}
mkdir -p       %{buildroot}%{php_home}
cp -pr PHPUnit %{buildroot}%{php_home}/PHPUnit

install -D -p -m 755 dbunit.php %{buildroot}%{_bindir}/dbunit


%if %{with_tests}
%check
: Run tests - set include_path to ensure PHPUnit autoloader use it
%{_bindir}/php -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
%{_bindir}/phpunit --verbose
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc ChangeLog.markdown
%doc Samples
%doc composer.json
%{_bindir}/dbunit
%{php_home}/PHPUnit/Extensions/Database


%changelog
* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Fri Jun  5 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- raise dependency on PHPUnit 4.0
- disable test suite on EL-5

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2
- switch all dependencies to composer

* Sun Jun 08 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-4
- fix FTBFS, add BR php-pdo
- add composer provides
- add composer.json as doc

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-3
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-2
- sources from github
- run tests during build

* Tue Apr 01 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Fri Nov 01 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- add requires: symfony2/Yaml

* Tue Mar 05 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.0 (stable)

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.0 (stable)

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependencies: php 5.3.3, PHPUnit 3.7.0,
  Yaml 2.1.0 (instead of YAML from symfony 1)

* Fri Jan 27 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Fri Aug 19 2011 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.0 (stable)

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-2
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-2
- lower PEAR dependency to allow el6 build
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean


