# remirepo spec file for php-phpseclib-crypt-tripledes, from:
#
# Fedora spec file for php-phpseclib-crypt-tripledes
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{!?__pear:       %global __pear %{_bindir}/pear}
%global pear_name Crypt_TripleDES

Name:           php-phpseclib-crypt-tripledes
Version:        1.0.0
Release:        1%{?dist}
Summary:        Pure-PHP implementation of Triple DES

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(phpseclib.sourceforge.net)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(phpseclib.sourceforge.net)
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_DES) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Hash)

Provides:       php-pear(phpseclib.sourceforge.net/Crypt_TripleDES) = %{version}


%description
Uses mcrypt, if available, and an internal implementation, otherwise. 
Operates in the EDE3 mode (encrypt-decrypt-encrypt).

%prep
%setup -q -c
mv package.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


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


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        phpseclib.sourceforge.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Crypt/TripleDES.php


%changelog
* Mon Aug 03 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10

* Mon Nov 10 2014 Remi Collet <remi@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9 (no change)

* Sat Sep 13 2014 Remi Collet <remi@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8 (no change)

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Wed Feb 26 2014 Remi Collet <remi@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6

* Fri Jan 24 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-3
- backport for remi repo

* Thu Jan 09 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- requires crypt-hash

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
