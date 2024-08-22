# template: default
%global gem_name parallel

Name: rubygem-%{gem_name}
Version: 1.26.3
Release: 1%{?dist}
Summary: Run any kind of code in parallel processes
License: MIT
URL: https://github.com/grosser/parallel
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: ruby >= 2.7
BuildRequires: ruby >= 2.7
BuildRequires: rubygems-devel
BuildArch: noarch
# end specfile generated dependencies

%description
Run any kind of code in parallel processes.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n  %{gem_name}-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Thu Aug 22 2024 Foreman Packaging Automation <packaging@theforeman.org> - 1.26.3-1
- Update to 1.26.3

* Sun Jul 07 2024 Foreman Packaging Automation <packaging@theforeman.org> - 1.25.1-1
- Update to 1.25.1

* Fri Jan 26 2024 Foreman Packaging Automation <packaging@theforeman.org> - 1.24.0-1
- Update to 1.24.0

* Thu May 11 2023 Foreman Packaging Automation <packaging@theforeman.org> 1.23.0-1
- Update to 1.23.0

* Wed Jul 06 2022 Foreman Packaging Automation <packaging@theforeman.org> 1.22.1-1
- Update to 1.22.1

* Thu Mar 11 2021 Eric D. Helms <ericdhelms@gmail.com> - 1.19.1-2
- Rebuild against rh-ruby27

* Mon Apr 13 2020 Eric D. Helms <ericdhelms@gmail.com> 1.19.1-1
- Add rubygem-parallel generated by gem2rpm using the scl template

