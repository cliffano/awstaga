# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Fixed
- Fix command not found on examples script run

## 2.0.0 - 2025-06-01
### Added
- Add deps-extra-apt to CI run due to sphinx-build bundling

### Changed
- Upgrade PieMaker to 1.10.0

### Removed
- Remove support for Python 3.8 and 3.9

## 1.3.0 - 2024-04-27
### Added
- Readd poetry.lock to repo

### Changed
- Use PieMaker for Makefile build

## 1.2.1 - 2023-12-12
### Fixed
- Fix default batch size to 5
- Fix display of failed tagging API calls to only display when there's at least 1 failure

## 1.2.0 - 2023-12-11
### Added
- Add error logging for failed tagging API calls
- Add --delay flag to CLI [#3]

## 1.1.1 - 2023-12-01
### Fixed
- Fix default basch size to 20

## 1.1.0 - 2023-11-28
### Added
- Add batch tagging support
- Add --batch-size flag to CLI

## 1.0.0 - 2023-11-27
### Added
- Add dry-run support
- Add Python 3.12 support
- Add YAML-include support [#2]

### Changed
- Allow tagsets, resource tags, and resource tagsetnames to be optional [#1]

### Removed
- Remove unused certifi dependency
- Remove dev Makefile target now that poetry.lock is ignored

## 0.12.0 - 2023-10-18
### Changed
- Use Poetry to manage project
- Switch dependency versioning to allow compatible with version

## 0.11.0 - 2023-08-10
### Changed
- Upgrade conflog to 1.5.1

### Fixed
- Fix installation error with Cython 3.0.0a10 via PyYAML 6.0.1 upgrade

## 0.10.1 - 2023-07-02
### Fixed
- Fix missing twine publish dependency

## 0.10.0 - 2023-07-02
### Added
- Initial version
