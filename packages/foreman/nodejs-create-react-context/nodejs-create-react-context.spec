%{?scl:%scl_package nodejs-%{npm_name}}
%{!?scl:%global pkg_name %{name}}

%global npm_name create-react-context

Name: %{?scl_prefix}nodejs-create-react-context
Version: 0.2.3
Release: 5%{?dist}
Summary: Polyfill for the proposed React context API
License: SEE LICENSE IN LICENSE
Group: Development/Libraries
URL: https://github.com/thejameskyle/create-react-context#readme
Source0: https://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
%if 0%{?scl:1}
BuildRequires: %{?scl_prefix_nodejs}npm
%else
BuildRequires: nodejs-packaging
BuildRequires: npm
%endif
Requires: %{?scl_prefix}npm(fbjs) >= 0.8.0
Requires: %{?scl_prefix}npm(fbjs) < 0.9.0
Requires: %{?scl_prefix}npm(gud) >= 1.0.0
Requires: %{?scl_prefix}npm(gud) < 2.0.0
BuildArch: noarch
ExclusiveArch: %{nodejs_arches} noarch
Provides: %{?scl_prefix}npm(%{npm_name}) = %{version}

%description
%{summary}

%prep
%setup -q -n package

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr lib %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}

%nodejs_symlink_deps

%check
%{nodejs_symlink_deps} --check

%files
%{nodejs_sitelib}/%{npm_name}
%license LICENSE
%doc README.md

%changelog
* Tue Mar 17 2020 Zach Huntington-Meath <zhunting@redhat.com> - 0.2.3-5
- Bump packages to build for el8

* Mon Oct 21 2019 Eric D. Helms <ericdhelms@gmail.com> - 0.2.3-4
- Build for SCL

* Thu Oct 10 2019 Eric D. Helms <ericdhelms@gmail.com> - 0.2.3-3
- Update requires for SCL prefix

* Fri Oct 04 2019 Eric D. Helms <ericdhelms@gmail.com> - 0.2.3-2
- Update specs to handle SCL

* Wed Oct 10 2018 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> 0.2.3-1
- Add nodejs-create-react-context generated by npm2rpm using the single strategy