
%global repo_orgname RedHatInsights
%global repo_name insights-client-role
%global repo_version 1.5

%global role_orgname %{repo_orgname}
%global role_name insights-client
%global role_version %{repo_version}

Name: ansiblerole-insights-client
Summary: Packaging of the insights-client Ansible role
Version: %{role_version}
Release: 1%{?dist}

License: ASL 2.0

Source: https://github.com/%{repo_orgname}/%{repo_name}/archive/v%{repo_version}.tar.gz#/%{role_name}-%{role_version}.tar.gz

Url: https://github.com/%{repo_orgname}/%{repo_name}/
BuildArch: noarch

Requires: ansible

%description
This package installs the insights-client Ansibile role.

Make sure that "/usr/share/ansible/roles" is on your Ansible role_path.

%prep

%setup -qc

%build

%install
mkdir -p %{buildroot}%{_datadir}/ansible/roles
cp -pR %{repo_name}-%{role_version} %{buildroot}%{_datadir}/ansible/roles/%{role_orgname}.%{role_name}

%files
%{_datadir}/ansible/roles/%{role_orgname}.%{role_name}
%doc %{repo_name}-%{role_version}/examples/*.yml
%doc %{repo_name}-%{role_version}/README.md
%license %{repo_name}-%{role_version}/LICENSE

%changelog
* Thu Mar 15 2018 Gavin Romig-Koch <gavin@redhat.com> - 1.5-1
- Initial release.  Based largely on the pattern of rhel-system-roles.spec
