# remirepo/fedora spec file for php-sebastian-recursion-context
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    994d4a811bafe801fb06dccbee797863ba2792ba
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   recursion-context
%global php_home     %{_datadir}/php
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-sebastian-recursion-context
Version:        1.0.1
Release:        1%{?dist}
Summary:        Recursively process PHP variables

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.4"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.4
%endif

# from composer.json
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report for version 1.0.0
Requires:       php-hash
Requires:       php-spl

Provides:       php-composer(sebastian/recursion-context) = %{version}


%description
Provides functionality to recursively process PHP variables.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/SebastianBergmann
cp -pr src %{buildroot}%{php_home}/SebastianBergmann/RecursionContext


%check
%if %{with_tests}
%{_bindir}/php -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
%{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/SebastianBergmann/RecursionContext/autoload.php
%else
: bootstrap build with test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%dir %{php_home}/SebastianBergmann
     %{php_home}/SebastianBergmann/RecursionContext


%changelog
* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1 (only CS)

* Sat Jan 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package