%global git_tag_rev 3b7d5366c88eccf2517ebac57c59eb557c82f46c

Name:		php-wikimedia-cdb
Version:	1.0.1
Release:	1%{?dist}
Summary:	CDB functions for PHP

License:	GPLv2+
URL:		http://www.mediawiki.org/wiki/CDB
Source0:	http://git.wikimedia.org/zip/?r=cdb.git&format=xz&h=%{git_tag_rev}#/%{name}-%{version}.tar.xz

Buildarch:	noarch

BuildRequires:  php-dba
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  php-theseer-autoload

Requires:	php(language) >= 5.3.2
Requires:	php-spl

Provides:	php-composer(wikimedia/cdb) = %{version}


%description
CDB, short for "constant database", refers to a very fast and highly reliable
database system which uses a simple file with key value pairs. This library
wraps the CDB functionality exposed in PHP via the dba_* functions. In cases
where dba_* functions are not present or are not compiled with CDB support,
a pure-PHP implementation is provided for falling back.


%prep
%setup -qc %{name}-%{version}


%build
phpab --output src/autoload.php src


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/Cdb
cp -rp src/* %{buildroot}%{_datadir}/php/Cdb


%check
phpunit -v --bootstrap %{buildroot}%{_datadir}/php/Cdb/autoload.php test


%files
%license COPYING
%doc composer.json README.md
%{_datadir}/php/Cdb


%changelog
* Thu Jun 25 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.1-1
- Initial package

