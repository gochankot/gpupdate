%define _unpackaged_files_terminate_build 1

Name: gpupdate
Version: 0.0.3
Release: alt1

Summary: GPT applier
License: MIT
Group: Other
Url: http://git.altlinux.org/
BuildArch: noarch

Requires: control
Requires: local-policy

BuildRequires: rpm-build-python3

Source0: %name-%version.tar

%description
GPT applier

%prep
%setup -q

%install
install -pD -m755 gpupdate \
	%buildroot%_bindir/gpupdate

mkdir -p \
	%buildroot%python3_sitelibdir/
cp -r gpoa \
	%buildroot%python3_sitelibdir/

mkdir -p \
	%buildroot%_sbindir/
ln -s %python3_sitelibdir/gpoa/main.py \
	%buildroot%_sbindir/gpoa

mkdir -p %buildroot%_datadir/%name
mv %buildroot%python3_sitelibdir/gpoa/templates \
	%buildroot%_datadir/%name/

install -Dm0644 %name.service %buildroot%_unitdir/%name.service

%preun
%preun_service gpupdate

%post
%post_service gpupdate

%files
%_sbindir/gpoa
%_bindir/gpupdate
%attr(755,root,root) %python3_sitelibdir/gpoa/main.py
%python3_sitelibdir/gpoa
%_datadir/%name
%_unitdir/%name.service

%changelog
* Sun Nov 17 2019 Evgeny Sinelnikov <sin@altlinux.org> 0.0.3-alt1
- Clean code, fix functionality (Initialize cache if missing, retrieve SIDs)
- Run GPO applier as /usr/sbin/gpoa

* Fri Nov 15 2019 Igor Chudov <nir@altlinux.org> 0.0.2-alt1
- Removed hreg dependency
- Introduced caches for SIDs and Registry.pol file paths
- gpupdate transformed into simple gpoa starter
- gpoa learned to work with username
- Introduced TDB manager in order to work with samba-regedit registry
- DC domain detection now uses native python-samba functions to query LDAP

* Thu Nov 14 2019 Igor Chudov <nir@altlinux.org> 0.0.1-alt1
- Initial release

