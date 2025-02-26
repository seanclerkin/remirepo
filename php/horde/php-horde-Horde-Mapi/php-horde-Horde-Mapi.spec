# remirepo/fedora spec file for php-horde-Horde-Mapi
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Mapi
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Mapi
Version:        1.0.5
Release:        1%{?dist}
Summary:        MAPI utility library

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-bcmath
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
BuildRequires:  php-pear(phpseclib.sourceforge.net/Math_BigInteger)

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
# Use phpseclib version instead of the one from pear
Requires:       php-pear(phpseclib.sourceforge.net/Math_BigInteger)
# From phpcompatinfo report for version 1.0.0
Requires:       php-date

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-mapi) = %{version}


%description
Provides various utility classes for dealing with Microsoft MAPI structured
data.


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit .


%clean
rm -rf %{buildroot}


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
%{pear_phpdir}/Horde/Mapi
%{pear_phpdir}/Horde/Mapi.php
%{pear_testdir}/%{pear_name}


%changelog
* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5
- drop dependency on bcmath
- add dependency on Math_BigInteger

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- add provides php-composer(horde/horde-mapi)

* Fri Jun 27 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Sun Jan 19 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- License is LGPLv2, upstream clarification

* Sat Jan 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package