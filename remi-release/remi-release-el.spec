Name:           remi-release
%if %{rhel} == 7
Version:        7.1
Release:        2%{?dist}
%endif
%if %{rhel} == 6
Version:        6.6
Release:        1%{?dist}
%endif
%if %{rhel} == 5
Version:        5.10
Release:        1%{?dist}
%endif
Summary:        YUM configuration for remi repository
Summary(fr):    Configuration de YUM pour le dépôt remi

Group:          System Environment/Base
License:        GPL
URL:            http://remirepo.net
Source0:        RPM-GPG-KEY-remi
Source1:        remi-el.repo
Source2:        remi-safe.repo
Source3:        remi-php70.repo

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArchitectures: noarch

Requires:       yum
Requires:       redhat-release >= %{rhel}
Requires:       epel-release >= %{rhel}


%description
This package contains yum configuration for the Remi's RPM Repository,
as well as the public GPG keys used to sign them.
%if %{rhel} == 7
Only the "remi-safe" repository is enabled after installation.
%else
The repository is not enabled after installation.
%endif
For PHP 5.4 you must use --enablerepo=remi yum option.
For PHP 5.5 you must use --enablerepo=remi,remi-php55 yum option.
For PHP 5.6 you must use --enablerepo=remi,remi-php56 yum option.
For PHP 7.0 you must use --enablerepo=remi,remi-php70 yum option.
%if %{rhel} >= 6
Software Collections are in the main "remi" repository.
%endif
FAQ:   http://blog.remirepo.net/pages/English-FAQ
Forum: http://forum.remirepo.net/

%description -l fr
Ce paquetage contient le fichier de configuration de YUM pour utiliser
les RPM du dépôt de Remi ainsi que la clé GPG utilisée pour les signer.
%if %{rhel} == 7
Seul le dépôt "remi-safe" est activé après l'installation.
%else
Le dépôt n'est pas activé après l'installation.
%endif
Pour PHP 5.4 vous devez utiliser l'option --enablerepo=remi
Pour PHP 5.5 vous devez utiliser l'option --enablerepo=remi,remi-php55
Pour PHP 5.6 vous devez utiliser l'option --enablerepo=remi,remi-php56
Pour PHP 7.0 vous devez utiliser l'option --enablerepo=remi,remi-php70
%if %{rhel} >= 6
Les "Software Collections" sont dans le dépôt principal "remi".
%endif
FAQ:   http://blog.remirepo.net/pages/FAQ-en-Francais
Forum: http://forum.remirepo.net/


%prep
%setup -c -T
sed -e "s/VERSION/%{rhel}/" %{SOURCE1} | tee remi.repo

%if %{rhel} >= 6
sed -e "s/VERSION/%{rhel}/" %{SOURCE2} | tee remi-safe.repo
sed -e "s/VERSION/%{rhel}/" %{SOURCE3} | tee remi-php70.repo
%endif


%build
echo empty build


%install
rm -rf %{buildroot}

# PGP
install -Dp -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi

# YUM
for repo in *repo
do
  install -Dp -m 644 $repo %{buildroot}%{_sysconfdir}/yum.repos.d/$repo
done


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/remi*repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-remi


%changelog
* Fri Jul 24 2015 Remi Collet <remmi@remirepo.net> - 6.6-1
- add remi-safe repository

* Thu Jul 23 2015 Remi Collet <remmi@remirepo.net> - 7.1-2 and 6.5-2
- add remi-php70 repository

* Tue Jun  2 2015 Remi Collet <remmi@remirepo.net> - 7.1-1
- add remi-safe repository
- translate repository name
- update repository configuration for "remirepo.net" domain

* Thu Apr 24 2014 Remi Collet <RPMS@FamilleCollet.com> - 7.0-1
- EL-7 build

* Fri Feb 28 2014 Remi Collet <RPMS@FamilleCollet.com> - 5.10-1 and 6.5-1
- add php56 repository

* Thu Oct  3 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.9-1 and 6.4-1
- add php55 repository

* Tue Feb 12 2013 Remi Collet <RPMS@FamilleCollet.com> - 5-9 and 6-2
- add debuginfo repo
- drop failovermethod option (switch to roundrobin)

* Sat Nov 13 2010 Remi Collet <RPMS@FamilleCollet.com> - 6-1.el6.remi
- EL-6 rebuild

* Sat May 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 5-8.el5.remi
- use a mirrorlist URL

* Sun May 03 2009 Remi Collet <RPMS@FamilleCollet.com> - 5-7.el5.remi
- new repo layout

* Thu Jan 22 2009 Remi Collet <RPMS@FamilleCollet.com> - 5-6.el5.remi
- fix bad $releasever in remi.repo (5Server doesn't work)

* Tue Jan 20 2009 Remi Collet <RPMS@FamilleCollet.com> - 5-5.el5.remi
- remove free.fr mirror

* Sat Feb  2 2008 Remi Collet <RPMS@FamilleCollet.com> - 5-4.el5.remi
- new mirror http://rpms.famillecollet.com/

* Sat Nov 17 2007 Remi Collet <RPMS@FamilleCollet.com> - 5-3.el5.remi
- add requires epel-release

* Sun Jun 24 2007 Remi Collet <RPMS@FamilleCollet.com> - 5-2.el5.remi
- New key (email change, same ID)

* Sat May 26 2007 Remi Collet <RPMS@FamilleCollet.com> - 5-1.el5.remi
- EL-5 rebuild

