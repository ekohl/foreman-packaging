# template: foreman_plugin
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_spacewalk
%global plugin_name spacewalk
%global foreman_min_version 1.18

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.0.0
Release: 5%{?foremandist}%{?dist}
Summary: Spacewalk integration for Foreman
Group: Applications/Systems
License: GPLv3+
URL: https://github.com/dm-drogeriemarkt/foreman_spacewalk
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: foreman >= %{foreman_min_version}
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: foreman-plugin >= %{foreman_min_version}
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-%{plugin_name}
# end specfile generated dependencies

%description
Spacewalk integration for Foreman.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%foreman_bundlerd_file

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_instdir}/db
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_plugin}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Tue Apr 06 2021 Eric D. Helms <ericdhelms@gmail.com> - 2.0.0-5
- Rebuild plugins for Ruby 2.7

* Tue Jan 07 2020 Eric D. Helms <ericdhelms@gmail.com> - 2.0.0-4
- Drop migrate, seed and restart posttans

* Wed Sep 12 2018 Bryan Kearney <bryan.kearney@gmail.com> - 2.0.0-3
- Move licenes which are GPL-* to GPLv3

* Fri Sep 07 2018 Eric D. Helms <ericdhelms@gmail.com> - 2.0.0-2
- Rebuild for Rails 5.2 and Ruby 2.5

* Fri Jun 29 2018 Timo Goebel <mail@timogoebel.name> - 2.0.0-1
- Update foreman_spacewalk to 2.0.0

* Tue Jun 05 2018 Dirk Goetz <dirk.goetz@netways.de> 1.0.0-1
- Add rubygem-foreman_spacewalk generated by gem2rpm using the foreman_plugin template
