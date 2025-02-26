# remirepo/fedora spec file for php-horde-Horde-Serialize
#
# Copyright (c) 2012-2015 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Serialize
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Serialize
Version:        2.0.4
Release:        1%{?dist}
Summary:        Data Encapulation API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-bz2
Requires:       php-json
Requires:       php-wddx
Requires:       php-zlib
Requires:       php-pecl(LZF)
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional and skipped for build order: Horde_Imap_Client, Horde_Mime

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-serialize) = %{version}


%description
The Horde_Serialize library provides various methods of encapsulating data.


%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

%if 0%{?fedora} < 24
: Skip failed test with jsonc before 1.3.8
sed -e 's/function testJsonInvalidUTF8Input/function SKIP_testJsonInvalidUTF8Input/' \
    -i JsonTest.php
%endif

phpunit --verbose .


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Serialize
%{pear_phpdir}/Horde/Serialize.php
%{pear_testdir}/%{pear_name}


%changelog
* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (no change)

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3
- add provides php-composer(horde/horde-serialize)

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Feb 6 2013 Nick Bebout <nb@fedoraproject.org> - 2.0.1-3
- Update for review

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-1
- Initial package
