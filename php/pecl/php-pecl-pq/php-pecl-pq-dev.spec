# remirepo spec file for php-pecl-pq
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package        php-pecl-pq}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global gh_commit  e381164032a750583657e449875f62d52b7b6609
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   m6w6
%global gh_project ext-pq
%global gh_date    20150819
%global with_zts   0%{?__ztsphp:1}
%global pecl_name  pq
%global rcver      dev
%if %{?runselftest}%{!?runselftest:1}
# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}
%else
# Build using "--with tests" to enable tests
%global with_tests 0%{?_with_tests:1}
%endif
%if "%{php_version}" < "5.6"
# After raph, json
%global ini_name   z-%{pecl_name}.ini
%else
# After 40-json, 40-raphf
%global ini_name   50-%{pecl_name}.ini
%endif

Summary:        PostgreSQL client library (libpq) binding
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        2.0.0
%if 0%{?gh_date:1}
Release:        0.3.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  postgresql-devel > 9
BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?sub_prefix}php-pecl-raphf-devel >= 1.1.0
%if %{with_tests}
BuildRequires:  postgresql-server
BuildRequires:  postgresql-contrib
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-json%{?_isa}
Requires:       %{?sub_prefix}php-raphf%{?_isa}  >= 1.1.0
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
PostgreSQL client library (libpq) binding.

Documents: http://devel-m6w6.rhcloud.com/mdref/pq

Highlights:
* Nearly complete support for asynchronous usage
* Extended type support by pg_type
* Fetching simple multi-dimensional array maps
* Working Gateway implementation

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.


%prep
%setup -q -c
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .

# Don't install tests
sed -e '/role="test"/d' -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_PQ_VERSION/{s/.* "//;s/".*$//;p}' php_pq.h)
if test "x${extver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?rcver}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable "%{summary}" extension module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
OPT="-n"
[ -f %{php_extdir}/json.so ]  && OPT="$OPT -d extension=json.so"
[ -f %{php_extdir}/raphf.so ] && OPT="$OPT -d extension=raphf.so"

: Minimal load test for NTS extension
%{__php} $OPT \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} $OPT \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
RET=0

: Running a server
DATABASE=$PWD/data
%ifarch x86_64
PORT=5440
%else
PORT=5436
%endif
pg_ctl initdb -D $DATABASE
cat <<EOF >>$DATABASE/postgresql.conf
unix_socket_directories = '$DATABASE'
port = $PORT
EOF
pg_ctl -D $DATABASE -l $DATABASE/log -w -t 200  start
createdb -h localhost -p $PORT rpmtest

cd NTS
sed -e "/PQ_DSN/s/\"host.*\"/'host=localhost port=$PORT dbname=rpmtest'/" \
    -i tests/_setup.inc

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="$OPT -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || RET=1

%if %{with_zts}
cd ../ZTS
sed -e "/PQ_DSN/s/\"host.*\"/'host=localhost port=$PORT dbname=rpmtest'/" \
    -i tests/_setup.inc

: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/zts-php \
TEST_PHP_ARGS="$OPT -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/zts-php -n run-tests.php --show-diff || RET=1
%endif

cd ..
: Cleanup
psql -h localhost -p $PORT -c "SELECT version()" rpmtest
pg_ctl -D $DATABASE -w stop
rm -rf $DATABASE

exit $RET
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{?_licensedir:%license NTS/LICENSE}

%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.20150819gite381164
- F23 rebuild with rh_layout

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.20150819gite381164
- really drop dependency on pear

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.20150819gite381164
- update to 2.0.0dev for PHP 7
- sources from github

* Wed Jul 29 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-0.3.RC2
- allow build against rh-php56 (as more-php56)

* Tue Jul 28 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-0.2.RC2
- Update to 0.6.0RC2 (beta)
- raise dependency on raphf 1.1.0

* Wed Jun 10 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-0.1.RC1
- Update to 0.6.0RC1
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5

* Sat Oct 18 2014 Remi Collet <remi@fedoraproject.org> - 0.5.2-2
- launch a postgresql server for test
- enable upstream test suite during build

* Fri Oct 17 2014 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- initial package, version 0.5.1 (beta)