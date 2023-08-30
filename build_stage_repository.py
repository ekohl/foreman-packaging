#!/usr/bin/env python3

import hashlib
import os
import shutil
import sys
import time
from pathlib import Path
from subprocess import STDOUT, CalledProcessError, check_output

import yaml


def execute(command: str | list[str]) -> str | bool:
    try:
        return check_output(command, universal_newlines=True, stderr=STDOUT)
    except CalledProcessError as error:
        print(error.output)
        return False


def move_rpms_from_copr_to_stage(collection: str, version: str, src_folder: Path, dest_folder:
                                 Path, source: bool=False) -> None:
    if source:
        print(f"Moving {collection} Source RPMs from Copr directory to stage repository")
    else:
        print(f"Moving {collection} RPMs from Copr directory to stage repository")

    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    repo_folder = src_folder / f"el8-{collection}-{version}"

    if source:
        files = repo_folder.glob("/**/*.src.rpm")
    else:
        files = repo_folder.glob("/**/*.rpm")

    for file in files:
        file.rename(dest_folder / file.name)

    shutil.rmtree(src_folder)

def modulemd_yaml(collection: str) -> str:
    return f"modulemd/modulemd-{collection}-el8.yaml"


def generate_modulemd_version(version: str) -> int:
    if version == 'nightly':
        modulemd_version_prefix = 9999
    else:
        major, minor = version.split('.')
        modulemd_version_prefix = int(major)*100 + int(minor)

    modulemd_version_string = time.strftime(f"{modulemd_version_prefix}%Y%m%d%H%M%S", time.gmtime())

    return int(modulemd_version_string)


def generate_modulemd_context(collection: str, version: str) -> str:
    context_string = f"{collection}-{version}"
    digest = hashlib.sha256(context_string.encode()).hexdigest()
    return digest[:8]


def create_modulemd(collection: str, version: str, stage_dir: Path) -> None:
    print("Adding modulemd to stage repository")
    cmd = [
        'rpm',
        '--nosignature',
        '--query',
        '--package',
        f"{stage_dir}/*.rpm",
        "--queryformat=%{name}-%{epochnum}:%{version}-%{release}.%{arch}\n"
    ]
    output = check_output(cmd)

    with open(modulemd_yaml(collection), 'r') as file:
        modules = yaml.safe_load(file)

    modules['data']['artifacts'] = {'rpms': output.splitlines()}
    modules['data']['version'] = generate_modulemd_version(version)
    modules['data']['context'] = generate_modulemd_context(collection, version)
    modules_yaml = os.path.join(stage_dir, 'repodata', 'modules.yaml')

    with open(modules_yaml, 'w') as modules_file:
        yaml.dump(modules, modules_file, default_flow_style=False, explicit_start=True, explicit_end=True)

    check_output(['modifyrepo_c', '--mdtype=modules', modules_yaml, f"{stage_dir}/repodata"])


def create_repository(repo_dir: Path) -> None:
    check_output(['createrepo', repo_dir])


def sync_copr_repository(collection: str, version: str, target_dir: Path, source: bool=False):
    if source:
        print(f"Syncing {collection} {version} Source RPM repository from Copr")
    else:
        print(f"Syncing {collection} {version} RPM repository from Copr")

    cmd = [
        'reposync',
        '--newest-only',
        '--repo',
        f"el8-{collection}-{version}",
        '--config',
        'reposync_config.conf'
    ]

    if execute(['reposync', '--version']):
        cmd.extend([
            '--download-path',
            target_dir.as_posix()
        ])

        if source:
            cmd.extend([
                '--source',
            ])
        else:
            cmd.extend([
                '--exclude',
                '*.src',
            ])

    else:
        cmd.extend([
            '--download_path',
            target_dir.as_posix()
        ])

        if source:
            cmd.extend([
                '--source',
            ])

    check_output(cmd)


def main():
    try:
        collection = sys.argv[1]
        version = sys.argv[2]
        operating_system = sys.argv[3]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} collection version os")

    base_dir = Path('tmp')
    rpm_sync_dir = base_dir / "rpms"
    rpm_sync_dir.mkdir(exist_ok=True)

    srpm_sync_dir = base_dir / "srpms"
    srpm_sync_dir.mkdir(exist_ok=True)

    stage_dir = base_dir / collection / version / operating_system

    rpm_dir = stage_dir / "x86_64"
    rpm_dir.mkdir(exist_ok=True)

    srpm_dir = stage_dir / "source"
    srpm_dir.mkdir(exist_ok=True)

    sync_copr_repository(collection, version, rpm_sync_dir)
    sync_copr_repository(collection, version, srpm_sync_dir, source=True)

    move_rpms_from_copr_to_stage(collection, version, srpm_sync_dir, srpm_dir, source=True)
    move_rpms_from_copr_to_stage(collection, version, rpm_sync_dir, rpm_dir)

    create_repository(rpm_dir)
    create_repository(srpm_dir)

    if collection in ['foreman', 'katello'] and operating_system == 'el8':
        create_modulemd(collection, version, rpm_dir)


if __name__ == '__main__':
    main()
