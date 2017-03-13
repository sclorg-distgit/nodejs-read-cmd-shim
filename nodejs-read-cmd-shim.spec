%{?scl:%scl_package nodejs-read-cmd-shim}
%{!?scl:%global pkg_name %{name}}

%{?nodejs_find_provides_and_requires}

%global packagename read-cmd-shim
%global enable_tests 0

Name:		%{?scl_prefix}nodejs-read-cmd-shim
Version:	1.0.1
Release:	4%{?dist}
Summary:	Figure out what a cmd-shim is pointing at

License:	ISC
URL:		https://github.com/npm/read-cmd-shim.git
Source0:	https://registry.npmjs.org/%{packagename}/-/%{packagename}-%{version}.tgz
Source1:	LICENSE-ISC.txt
# license file requested upstream at https://github.com/npm/read-cmd-shim/issues/1

Patch0:		read-cmd-shim_fix-tests.patch
# patch to fix the tests, submitted upstream at https://github.com/npm/read-cmd-shim/pull/2

BuildArch:	noarch
%if 0%{?fedora} >= 19
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:	%{?scl_prefix}nodejs-devel
%if 0%{?enable_tests}
BuildRequires:	%{?scl_prefix}npm(cmd-shim)
BuildRequires:  %{?scl_prefix}npm(graceful-fs)
BuildRequires:	%{?scl_prefix}npm(rimraf)
BuildRequires:	%{?scl_prefix}npm(tap)
%endif

%description
Figure out what a cmd-shim is pointing at. This acts as the equivalent of
fs.readlink.

%prep
%setup -q -n package
cp -p %{SOURCE1} .
%patch0 -p1

%build
# nothing to do!

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{packagename}
cp -pr package.json *.js \
	%{buildroot}%{nodejs_sitelib}/%{packagename}

%nodejs_symlink_deps

%if 0%{?enable_tests}

%check
%nodejs_symlink_deps --check
%{__nodejs} -e 'require("./")'
%{_bindir}/tap test/*.js
%endif

%files
%{!?_licensedir:%global license %doc}
%doc *.md
%license LICENSE-ISC.txt
%{nodejs_sitelib}/%{packagename}

%changelog
* Thu Sep 15 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.0.1-4
- Built for RHSCL

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 31 2015 Tom Hughes <tom@compton.nu> - 1.0.1-2
- Require npm(graceful-fs) for tests

* Thu Dec 17 2015 Jared Smith <jsmith@fedoraproject.org> - 1.0.1-1
- Initial packaging